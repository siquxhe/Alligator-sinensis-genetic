#!/bin/bash
# 守候 iPHoP 全库下载：每小时巡检一次，直到完成
# 完成后自动：md5 校验 → 解压 → 对 202 条基因组跑完整宿主预测
# 下载中断（进程消失）会自动幂等续传，最多 6 次
set -uo pipefail

BASE=/mnt/work/iphop_db
TAR=$BASE/iPHoP.latest.tar.gz
PARTS=$TAR.parts
DLLOG=$BASE/dl.log
LOG=$BASE/watch.log
STATUS=$BASE/status.txt
DONE=$BASE/.watch_done
URL="https://portal.nersc.gov/cfs/m342/iphop/db/iPHoP.latest.tar.gz"
MD5_EXPECT=3ce666cf17fc1151f56b150084af4ba8
TOTAL=116930251283
CHUNK_BYTES=67108864                       # 下载脚本用的 64 MiB 块
BLOCKS=$(( (TOTAL + CHUNK_BYTES - 1) / CHUNK_BYTES ))
DL=$HOME/biotools/server_dl_bigfile.sh
IPHOP=$HOME/biotools/envs/iphop/bin/iphop
INPUT=$HOME/virome/host_pred/input/hq_genomes.fna
OUT=$HOME/virome/host_pred/results_full
MAXRESTART=6

mkdir -p "$BASE"
log() { echo "[$(date '+%F %T')] $*" >> "$LOG"; }

# 单实例锁：手动启动与 systemd 托管同时存在时，只有一个生效
exec 9> "$BASE/.watch.lock"
if ! flock -n 9; then
  log "已有守候实例在运行，本实例退出"
  exit 0
fi

if [ -f "$DONE" ]; then
  log "已完成标记存在，本次不重复执行"
  exit 0
fi

log "===================== 守候启动 (pid $$) ====================="

# ---------------- 阶段一：等下载完成 ----------------
restarts=0
while :; do
  if [ -f "$TAR" ] && [ "$(stat -c %s "$TAR")" -eq "$TOTAL" ]; then
    log "下载完成：$TAR（$TOTAL 字节）"
    break
  fi

  alive=0
  pgrep -f "server_dl_bigfile\.sh" > /dev/null && alive=1

  n=$(find "$PARTS" -maxdepth 1 -type f -name '[0-9]*' 2>/dev/null | wc -l)
  b=$(find "$PARTS" -maxdepth 1 -type f -name '[0-9]*' -printf '%s\n' 2>/dev/null | awk '{s+=$1} END{print s+0}')
  pct=$(awk -v x="$b" -v t="$TOTAL" 'BEGIN{printf "%.2f", x*100/t}')
  spd=$(grep -E '^\[20' "$DLLOG" 2>/dev/null | tail -1 | grep -oE '平均 [0-9.]+ MB/s')
  line="进度 ${pct}% ｜ $(awk -v x="$b" 'BEGIN{printf "%.1f", x/1073741824}') GB / 108.9 GB ｜ 块 $n/$BLOCKS ｜ $([ $alive -eq 1 ] && { [ "$n" -ge "$BLOCKS" ] && echo 拼接中 || echo 下载中; } || echo 进程已退出) ｜ ${spd:-速度未知}"
  log "$line"
  echo "$line" > "$STATUS"

  if [ "$alive" -eq 0 ]; then
    restarts=$((restarts + 1))
    if [ "$restarts" -gt "$MAXRESTART" ]; then
      log "ERROR 已重启 $MAXRESTART 次仍未完成，放弃"
      exit 1
    fi
    log "进程不在且文件未完成 → 第 $restarts 次续传"
    cd "$BASE" && setsid nohup bash "$DL" "$URL" "$TAR" 256 64 >> "$DLLOG" 2>&1 < /dev/null &
    sleep 90
  else
    # 分块都下齐了但整包还没拼完 → 正在拼接，每 2 分钟看一次，避免空等一小时
    if [ "$n" -ge "$BLOCKS" ]; then
      sleep 120
    else
      sleep 3600
    fi
  fi
done

# ---------------- 阶段二：校验 ----------------
log "----- 校验 -----"
MD5=$(md5sum "$TAR" | awk '{print $1}')
if [ "$MD5" = "$MD5_EXPECT" ]; then
  log "md5 校验通过：$MD5"
else
  log "WARN md5 不符：得到 $MD5，期望 $MD5_EXPECT（官方清单给的是 Sept21 的名字，继续尝试解压）"
fi

# ---------------- 阶段三：解压 ----------------
XD=$BASE/extract
mkdir -p "$XD"
log "----- 解压开始 → $XD -----"
T0=$(date +%s)
if command -v "$HOME/biotools/envs/virome/bin/pigz" > /dev/null 2>&1; then
  log "使用 pigz 并行解压"
  "$HOME/biotools/envs/virome/bin/pigz" -dc "$TAR" | tar -xf - -C "$XD"
else
  log "使用 tar -xzf 单线程解压"
  tar -xzf "$TAR" -C "$XD"
fi
RC=$?
if [ "$RC" -ne 0 ]; then
  log "ERROR 解压失败 rc=$RC"
  exit 1
fi
log "解压完成，用时 $(( ($(date +%s) - T0) / 60 )) 分钟"
df -h /mnt/work | tail -1 | sed 's/^/  磁盘: /' >> "$LOG"

# ---------------- 阶段四：定位数据库 ----------------
DBROOT=$(find "$XD" -maxdepth 4 -type d -name 'iPHoP_db' 2>/dev/null | head -1)
if [ -z "$DBROOT" ]; then
  log "ERROR 解压后未找到 iPHoP_db 目录，目录树如下："
  find "$XD" -maxdepth 2 -type d 2>/dev/null | head -20 >> "$LOG"
  exit 1
fi
DBDIR=$(dirname "$DBROOT")
log "数据库目录：$DBDIR"
du -sh "$DBROOT" 2>/dev/null | sed 's/^/  库大小: /' >> "$LOG"

# ---------------- 阶段五：宿主预测 ----------------
mkdir -p "$OUT"
log "----- iPHoP 宿主预测启动（202 条基因组，8 线程）-----"
T0=$(date +%s)
"$IPHOP" predict --fa_file "$INPUT" --db_dir "$DBDIR" --out_dir "$OUT" \
  --num_threads 8 --add_tsv_output >> "$BASE/iphop.log" 2>&1
RC=$?
DUR=$(( ($(date +%s) - T0) / 60 ))

if [ "$RC" -eq 0 ]; then
  log "iPHoP 完成，用时 ${DUR} 分钟，结果在 $OUT"
  N=$(ls "$OUT"/*.tsv 2>/dev/null | wc -l)
  log "输出 tsv 文件数：$N"
  touch "$DONE"
  echo "DONE $(date '+%F %T')，用时 ${DUR} 分钟" > "$STATUS"
  log "===================== 全部完成 ====================="
else
  log "ERROR iPHoP 失败 rc=$RC，详见 $BASE/iphop.log"
  exit 1
fi

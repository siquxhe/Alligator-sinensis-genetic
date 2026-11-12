#!/bin/bash
# iPHoP 后处理：定位库目录 → 预检关键文件 → 跑宿主预测
# 与 server_watch_iphop.sh 的区别：库目录按 db/ + db_infos/ 定位（Sept_2021 结构），
# 且用 iphop12 环境（iPHoP 1.2.0，匹配非 rw 库；1.4.x 会因缺 rewish_models 直接退出）
set -uo pipefail

BASE=/mnt/work/iphop_db
XD=$BASE/extract
LOG=$BASE/watch.log
IPHOP=$HOME/biotools/envs/iphop12/bin/iphop
# iPHoP 内部用 shell 调 blastn / hmmscan / wish，必须把这些程序放进 PATH，否则静默失败
export PATH="$HOME/biotools/envs/iphop12/bin:$PATH"
# RaFAH 是 Perl 脚本，依赖 Bioperl；本环境的 perl-bioperl 装在 5.22.0 目录而 perl 是 5.22.2，
# 需要显式指定 PERL5LIB，否则报 "Can't locate Bio/SeqIO.pm"
export PERL5LIB="$HOME/biotools/envs/iphop12/lib/perl5/site_perl/5.22.0:$HOME/biotools/envs/iphop12/lib/perl5/site_perl/5.22.2${PERL5LIB:+:$PERL5LIB}"
INPUT=$HOME/virome/host_pred/input/hq_genomes.fna
OUT=$HOME/virome/host_pred/results_full
DONE=$BASE/.iphop_done

log() { echo "[$(date '+%F %T')] $*" >> "$LOG"; }

if [ ! -x "$IPHOP" ]; then
  log "ERROR 找不到 iPHoP 1.2.0（$IPHOP），请先完成 iphop12 环境安装"
  exit 1
fi
if [ ! -s "$INPUT" ]; then
  log "ERROR 输入文件不存在：$INPUT"
  exit 1
fi

# ---------- 定位库目录 ----------
DBDIR=""
while read -r d; do
  P=$(dirname "$d")
  if [ -d "$P/db" ] && [ -d "$P/db_infos" ]; then DBDIR="$P"; break; fi
done < <(find "$XD" -maxdepth 4 -type d -name 'db_infos' 2>/dev/null)

if [ -z "$DBDIR" ]; then
  log "ERROR 未找到同时含 db/ 与 db_infos/ 的库目录，当前结构："
  find "$XD" -maxdepth 3 -type d 2>/dev/null | head -20 >> "$LOG"
  exit 1
fi
log "库目录确定为：$DBDIR"

# ---------- 预检关键文件 ----------
MISS=0
for f in db/Host_Genomes/Host_Genomes db/All_CRISPR_spacers_nr_clean db_infos/Host_Genomes.tsv; do
  if [ ! -e "$DBDIR/$f" ] && [ ! -e "${DBDIR}/${f}.nal" ] && [ ! -e "${DBDIR}/${f}.fna" ]; then
    log "  WARN 缺少 $f"
    MISS=$((MISS + 1))
  else
    log "  OK   $f"
  fi
done
[ "$MISS" -gt 0 ] && log "预检有 $MISS 项缺失，仍尝试运行（iPHoP 会自行报错）"

# ---------- 运行 ----------
mkdir -p "$OUT"
log "----- iPHoP 宿主预测开始（$(grep -c '^>' "$INPUT") 条基因组，8 线程）-----"
T0=$(date +%s)
"$IPHOP" predict --fa_file "$INPUT" --db_dir "$DBDIR" --out_dir "$OUT" \
  --num_threads 8 >> "$BASE/iphop.log" 2>&1
RC=$?
DUR=$(( ($(date +%s) - T0) / 60 ))

if [ "$RC" -eq 0 ]; then
  log "iPHoP 完成，用时 ${DUR} 分钟"
  ls "$OUT" >> "$LOG" 2>/dev/null
  touch "$DONE"
  echo "DONE $(date '+%F %T')，用时 ${DUR} 分钟" > "$BASE/status.txt"
  log "===================== 全部完成 ====================="
else
  log "ERROR iPHoP 失败 rc=$RC，详见 $BASE/iphop.log"
  tail -20 "$BASE/iphop.log" >> "$LOG" 2>/dev/null
  exit 1
fi

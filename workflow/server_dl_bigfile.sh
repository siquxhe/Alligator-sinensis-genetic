#!/bin/bash
# 大文件分段并发下载（应对 NERSC 单连接限速）
# 用法: bash server_dl_bigfile.sh <url> <输出文件> [并发数] [块大小MB]
# 特性: 断点续传、单块重试、幂等（可重复运行补齐缺失块）、实时进度
set -uo pipefail

URL="${1:?url}"
OUT="${2:?output}"
PAR="${3:-256}"
CHUNK_MB="${4:-64}"

TOTAL=$(curl -sI "$URL" | awk 'tolower($1)=="content-length:"{print $2}' | tr -d '\r' | tail -1)
if [ -z "${TOTAL:-}" ]; then echo "拿不到 content-length，退出"; exit 1; fi

CHUNK=$(( CHUNK_MB * 1024 * 1024 ))
N=$(( (TOTAL + CHUNK - 1) / CHUNK ))
TMPD="${OUT}.parts"
mkdir -p "$TMPD"
rm -f "$TMPD/.failed"

echo "=================================================="
echo "URL      : $URL"
echo "总大小   : $TOTAL 字节（$(( TOTAL / 1073741824 )) GB）"
echo "分块     : $N 块 × ${CHUNK_MB} MB，并发 $PAR"
echo "临时目录 : $TMPD"
echo "开始时间 : $(date '+%F %T')"
echo "=================================================="

fetch() {
  local i=$1 s e want f got rs try
  s=$(( i * CHUNK ))
  e=$(( s + CHUNK - 1 ))
  [ "$e" -ge "$TOTAL" ] && e=$(( TOTAL - 1 ))
  want=$(( e - s + 1 ))
  f="$TMPD/$(printf %06d "$i")"

  if [ -f "$f" ] && [ "$(stat -c %s "$f")" -eq "$want" ]; then return 0; fi

  for try in $(seq 1 30); do
    got=0
    [ -f "$f" ] && got=$(stat -c %s "$f")
    [ "$got" -ge "$want" ] && { rm -f "$f"; got=0; }
    rs=$(( s + got ))
    curl -s --max-time 5400 --connect-timeout 40 \
         --speed-time 180 --speed-limit 800 \
         -r "${rs}-${e}" "$URL" >> "$f" 2>/dev/null
    if [ -f "$f" ] && [ "$(stat -c %s "$f")" -eq "$want" ]; then return 0; fi
    [ $(( try % 5 )) -eq 0 ] && echo "  重试块 $i（第 $try 次，已 $([ -f "$f" ] && stat -c %s "$f" || echo 0)/$want）"
    sleep $(( try < 10 ? try * 3 : 30 ))
  done
  echo "$i" >> "$TMPD/.failed"
  return 1
}
export -f fetch
export URL TMPD CHUNK TOTAL

# ---- 进度监控
monitor() {
  local t0=$(date +%s) done_n bytes pct spd eta
  while :; do
    sleep 60
    done_n=$(find "$TMPD" -maxdepth 1 -type f -name '[0-9]*' -size +0 2>/dev/null | wc -l)
    bytes=$(find "$TMPD" -maxdepth 1 -type f -name '[0-9]*' -printf '%s\n' 2>/dev/null | awk '{s+=$1} END{print s+0}')
    pct=$(awk -v b="$bytes" -v t="$TOTAL" 'BEGIN{printf "%.2f", b*100/t}')
    spd=$(( $(date +%s) - t0 ))
    [ "$spd" -lt 1 ] && spd=1
    spd=$(awk -v b="$bytes" -v s="$spd" 'BEGIN{printf "%.2f", b/s/1048576}')
    eta=$(awk -v b="$bytes" -v t="$TOTAL" -v s="$spd" 'BEGIN{if(s>0) printf "%.1f", (t-b)/1048576/s/3600; else print "?"}')
    echo "[$(date '+%F %T')] $done_n/$N 块，$(( bytes / 1073741824 )) GB / $(( TOTAL / 1073741824 )) GB，${pct}%，平均 ${spd} MB/s，剩余约 ${eta} 小时"
  done
}
monitor &
MON_PID=$!
trap 'kill $MON_PID 2>/dev/null' EXIT

# ---- 并发下载
seq 0 $(( N - 1 )) | xargs -P "$PAR" -I{} bash -c 'fetch {}'

kill $MON_PID 2>/dev/null
trap - EXIT

echo "=================================================="
MISS=$( [ -f "$TMPD/.failed" ] && wc -l < "$TMPD/.failed" || echo 0 )
echo "缺失块: $MISS / $N   （$([ "$MISS" -eq 0 ] && echo '全部到位' || echo '可重跑本脚本补齐')）"
[ "$MISS" -eq 0 ] || { echo "先补齐再拼接，避免拼出不完整的文件"; exit 1; }

echo "拼接中（$N 个块 → $OUT）..."
: > "$OUT"
for i in $(seq 0 $(( N - 1 ))); do
  cat "$TMPD/$(printf %06d "$i")" >> "$OUT" || { echo "拼接失败于块 $i"; exit 1; }
done

SZ=$(stat -c %s "$OUT")
echo "--------------------------------------------------"
if [ "$SZ" -eq "$TOTAL" ]; then
  echo "完成：$SZ 字节，大小校验通过"
  echo "结束时间：$(date '+%F %T')"
  rm -rf "$TMPD"
else
  echo "大小不符：得到 $SZ，应为 $TOTAL"
  exit 1
fi

#!/bin/bash
# 多连接分段下载（应对 NERSC 单连接限速）
# 用法: bash dl_parallel.sh <url> <输出文件> [并发数]
set -uo pipefail

URL="$1"
OUT="$2"
PAR="${3:-16}"

TOTAL=$(curl -sI "$URL" | awk 'tolower($1)=="content-length:"{print $2}' | tr -d '\r' | tail -1)
if [ -z "$TOTAL" ]; then echo "拿不到 content-length"; exit 1; fi
echo "总大小: $TOTAL 字节"

TMPD="${OUT}.parts"
mkdir -p "$TMPD"

# 分块大小：200KB 一块，够细以便并发填满带宽
CHUNK=204800
N=$(( (TOTAL + CHUNK - 1) / CHUNK ))
echo "分 $N 块，并发 $PAR"

fetch() {
  local i=$1 s e f want got
  s=$(( i * CHUNK )); e=$(( s + CHUNK - 1 ))
  [ $e -ge $TOTAL ] && e=$(( TOTAL - 1 ))
  want=$(( e - s + 1 ))
  f="$TMPD/$(printf %06d $i)"
  got=0
  [ -f "$f" ] && got=$(stat -c %s "$f")
  if [ "$got" -eq "$want" ]; then return 0; fi
  for try in 1 2 3 4 5; do
    rm -f "$f"
    curl -s --max-time 180 --retry 2 -r "${s}-${e}" -o "$f" "$URL"
    if [ -f "$f" ] && [ "$(stat -c %s "$f")" -eq "$want" ]; then return 0; fi
    sleep 2
  done
  echo "块 $i 失败"
  return 1
}
export -f fetch
export URL TMPD CHUNK TOTAL

seq 0 $((N-1)) | xargs -P "$PAR" -I{} bash -c 'fetch {}'

echo "拼接中 ..."
: > "$OUT"
for i in $(seq 0 $((N-1))); do cat "$TMPD/$(printf %06d $i)" >> "$OUT"; done

SZ=$(stat -c %s "$OUT")
if [ "$SZ" -eq "$TOTAL" ]; then
  echo "完成: $SZ 字节，校验通过"
  rm -rf "$TMPD"
else
  echo "大小不符: 得到 $SZ，应为 $TOTAL"
  exit 1
fi

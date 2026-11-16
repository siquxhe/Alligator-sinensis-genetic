#!/usr/bin/env bash
# RefSeq viral 分块下载：每块独立校验，失败只重下该块
set -uo pipefail
trap '' HUP TERM

D=/mnt/work/chicken/db/refseq
URL="https://ftp.ncbi.nlm.nih.gov/refseq/release/viral/viral.1.protein.faa.gz"
SZ=107365470
CHUNK=8388608          # 8 MB
PAR=6                  # 并发数
OUT=$D/viral.1.protein.faa.gz

mkdir -p "$D/parts"
cd "$D/parts"

N=$(( (SZ + CHUNK - 1) / CHUNK ))
echo "[$(date +%H:%M)] 共 $N 块，每块 $((CHUNK/1048576)) MB，并发 $PAR"

get_chunk() {
  local i=$1
  local start=$(( i * CHUNK ))
  local end=$(( start + CHUNK - 1 ))
  [ $end -ge $SZ ] && end=$(( SZ - 1 ))
  local want=$(( end - start + 1 ))
  local f="part.$(printf %02d $i)"
  local attempt=0
  while [ $attempt -lt 6 ]; do
    local have=$(stat -c%s "$f" 2>/dev/null || echo 0)
    if [ "$have" -eq "$want" ]; then return 0; fi
    attempt=$((attempt+1))
    curl -s --retry 2 --retry-delay 5 --max-time 900 -r ${start}-${end} -o "$f" "$URL" || true
    have=$(stat -c%s "$f" 2>/dev/null || echo 0)
    if [ "$have" -eq "$want" ]; then
      echo "  块 $i 完成 ($want 字节, 第 $attempt 次)"
      return 0
    fi
    echo "  块 $i 不完整 ($have/$want), 重试 $attempt"
    rm -f "$f"
  done
  echo "  块 $i 失败"
  return 1
}

running=0
fail=0
for i in $(seq 0 $((N-1))); do
  get_chunk $i &
  running=$((running+1))
  if [ $running -ge $PAR ]; then wait; running=0; fi
done
wait

# 拼接
echo "[$(date +%H:%M)] 拼接"
: > "$OUT"
ok=1
for i in $(seq 0 $((N-1))); do
  f="part.$(printf %02d $i)"
  start=$(( i * CHUNK ))
  end=$(( start + CHUNK - 1 ))
  [ $end -ge $SZ ] && end=$(( SZ - 1 ))
  want=$(( end - start + 1 ))
  have=$(stat -c%s "$f" 2>/dev/null || echo 0)
  if [ "$have" -ne "$want" ]; then echo "缺块 $i ($have/$want)"; ok=0; fi
  cat "$f" >> "$OUT"
done

if [ $ok -eq 1 ] && [ "$(stat -c%s "$OUT")" -eq "$SZ" ]; then
  echo "拼接完成 $(stat -c%s "$OUT") 字节"
  if gzip -t "$OUT" 2>/dev/null; then
    echo "gzip 校验通过"
    gzip -dc "$OUT" > "$D/refseq_viral.faa"
    echo "序列数: $(grep -c '^>' "$D/refseq_viral.faa")"
    echo "DONE"
  else
    echo "gzip 损坏"
  fi
else
  echo "拼接不完整，不删块文件以便续传"
fi

#!/bin/bash
# 补下 vOTU 目录（755 MB），校验序列数后再建索引
# 用法：nohup setsid bash 02b_votu.sh > votu.log 2>&1 &
set -uo pipefail

BASE=/mnt/work/chicken
RAW=$BASE/raw
REF=$BASE/refs
V=$RAW/representative_viral_19778_vOTUs.fasta
export PATH=$HOME/biotools/envs/virome/bin:$PATH
mkdir -p "$REF"

EXPECT=19778
URL="https://zenodo.org/api/records/15423614/files/representative_viral_19778_vOTUs.fasta/content"

echo "=== vOTU 目录 $(date) ==="

for attempt in 1 2 3 4 5; do
  n=$(grep -c '^>' "$V" 2>/dev/null || echo 0)
  sz=$(stat -c%s "$V" 2>/dev/null || echo 0)
  echo "[$attempt] 当前 $n 条 / $((sz/1024/1024)) MB"
  if [ "$n" -ge "$EXPECT" ]; then
    echo "序列数达标（$n ≥ $EXPECT）"
    break
  fi
  echo "续传中..."
  curl -sS -L --retry 5 --retry-delay 20 --max-time 3600 -C - -o "$V" "$URL" || echo "curl 返回非零，继续重试"
  sleep 5
done

n=$(grep -c '^>' "$V" 2>/dev/null || echo 0)
echo "最终序列数: $n（期望 $EXPECT）"
if [ "$n" -lt "$EXPECT" ]; then
  echo "ABORT: 序列数不足，不建索引"
  exit 1
fi

echo "[$(date +%H:%M)] 建 vOTU 索引"
bowtie2-build --threads 8 --quiet "$V" "$REF/votu" && echo "vOTU 索引完成"
touch "$REF/.VOTU_DONE"
echo "=== 结束 $(date) ==="

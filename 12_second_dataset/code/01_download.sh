#!/bin/bash
# 第二数据集下载：6 个鸡盲肠样本（NCBI ODP 镜像）+ 19,778 vOTU 目录
# 用法：nohup bash 01_download.sh > logs/download.log 2>&1 &
set -uo pipefail

BASE=/mnt/work/chicken
RAW=$BASE/raw
mkdir -p "$RAW/logs" "$BASE/bin"

RUNS="SRR6323088 SRR6323119 SRR6323120 SRR6323124 SRR6323125 SRR6323200"

echo "=== SRA 下载开始 $(date) ==="
for r in $RUNS; do
  out="$RAW/$r.sra"
  if [ -f "$RAW/.$r.done" ] && [ -s "$out" ]; then
    echo "[skip] $r 已完成 ($(du -h "$out" | cut -f1))"
    continue
  fi
  url="https://sra-pub-run-odp.s3.amazonaws.com/sra/$r/$r"
  echo "[$(date +%H:%M)] 开始 $r"
  curl -sS -L --retry 5 --retry-delay 15 --connect-timeout 30 -C - -o "$out" "$url" \
    && touch "$RAW/.$r.done" \
    && echo "[$(date +%H:%M)] 完成 $r  $(du -h "$out" | cut -f1)" \
    || echo "[$(date +%H:%M)] 失败 $r"
done

echo "=== vOTU 目录下载 $(date) ==="
VOTU="$RAW/representative_viral_19778_vOTUs.fasta"
if [ ! -s "$VOTU" ]; then
  curl -sS -L --retry 5 --retry-delay 15 -C - -o "$VOTU" \
    "https://zenodo.org/api/records/15423614/files/representative_viral_19778_vOTUs.fasta/content" \
    && echo "vOTU 完成 $(du -h "$VOTU" | cut -f1)" || echo "vOTU 失败"
else
  echo "[skip] vOTU 已存在"
fi

echo "=== 全部结束 $(date) ==="
touch "$RAW/.ALL_DONE"

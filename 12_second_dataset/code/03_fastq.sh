#!/bin/bash
# SRA → FASTQ 转换（.sra 落在 /mnt/work，临时文件也放工作盘，避免撑爆系统盘）
# 用法：nohup setsid bash 03_fastq.sh > fastq.log 2>&1 &
set -uo pipefail

BASE=/mnt/work/chicken
RAW=$BASE/raw
FQ=$BASE/fastq
export PATH=$HOME/.local/share/mamba/envs/sra/bin:$PATH
export TMPDIR=$BASE/tmp
mkdir -p "$FQ" "$TMPDIR"

RUNS="SRR6323088 SRR6323119 SRR6323120 SRR6323124 SRR6323125 SRR6323200"

echo "=== FASTQ 转换 $(date) ==="
for r in $RUNS; do
  if [ -f "$FQ/.$r.done" ]; then
    echo "[skip] $r 已转换"
    continue
  fi
  if [ ! -s "$RAW/$r.sra" ] || [ ! -f "$RAW/.$r.done" ]; then
    echo "[wait] $r 尚未下载完成，跳过"
    continue
  fi
  echo "[$(date +%H:%M)] 转换 $r"
  fasterq-dump --split-files --threads 6 --temp "$TMPDIR" \
      --outdir "$FQ" "$RAW/$r.sra" > "$FQ/$r.fasterq.log" 2>&1 \
    && gzip -f "$FQ/${r}_1.fastq" "$FQ/${r}_2.fastq" \
    && touch "$FQ/.$r.done" \
    && echo "[$(date +%H:%M)] 完成 $r  $(du -sh "$FQ" | cut -f1)" \
    || echo "[$(date +%H:%M)] 失败 $r（见 $FQ/$r.fasterq.log）"
done

echo "=== 结束 $(date) ==="

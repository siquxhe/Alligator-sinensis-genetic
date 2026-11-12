#!/bin/bash
# 第二数据集参考序列：鸡宿主基因组（GRCg6a）+ 19,778 vOTU 目录，并建 bowtie2 索引
# 用法：nohup setsid bash 02_refs.sh > refs.log 2>&1 &
set -uo pipefail

BASE=/mnt/work/chicken
REF=$BASE/refs
mkdir -p "$REF"
export PATH=$HOME/biotools/envs/virome/bin:$PATH

echo "=== 参考序列准备 $(date) ==="

# ---------- 1. 鸡宿主基因组
G=$REF/chicken.fna
if [ ! -s "$G" ]; then
  echo "[$(date +%H:%M)] 下载 GRCg6a"
  curl -sS -L --retry 5 --retry-delay 15 -C - -o "$REF/chicken.fna.gz" \
    "https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/002/315/GCF_000002315.6_GRCg6a/GCF_000002315.6_GRCg6a_genomic.fna.gz" \
    && gunzip -c "$REF/chicken.fna.gz" > "$G" \
    && echo "[$(date +%H:%M)] 基因组就绪 $(du -h "$G" | cut -f1)"
fi

if [ -s "$G" ] && [ ! -f "$REF/chicken.1.bt2" ]; then
  echo "[$(date +%H:%M)] 建宿主索引"
  bowtie2-build --threads 8 --quiet "$G" "$REF/chicken" && echo "宿主索引完成"
fi

# ---------- 2. vOTU 目录
V=$BASE/raw/representative_viral_19778_vOTUs.fasta
if [ -s "$V" ] && [ ! -f "$REF/votu.1.bt2" ]; then
  echo "[$(date +%H:%M)] 建 vOTU 索引（目录 $(du -h "$V" | cut -f1)）"
  bowtie2-build --threads 8 --quiet "$V" "$REF/votu" && echo "vOTU 索引完成"
elif [ ! -s "$V" ]; then
  echo "vOTU 目录尚未下载完成，跳过（稍后可重跑本脚本）"
fi

echo "=== 结束 $(date) ==="
touch "$REF/.REFS_DONE"

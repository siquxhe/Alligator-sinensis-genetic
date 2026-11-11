#!/bin/bash
# MAG 第 6 步：用 iPHoP 的宿主基因组库给 MAG 定分类（GTDB 谱系）
set -uo pipefail

B="$HOME/virome"
E="$HOME/biotools/envs/virome/bin"
export PATH="$E:$PATH"
MAGS="$B/07_mag/mag_final"
DB="/mnt/disk2t/iphop_db/extract/Sept_2021_pub/db/Host_Genomes/Host_Genomes"   # 完整宿主基因组库（74 GB，iPHoP 全库）
W="$B/work/mag_tax"
NTOP=${1:-3}          # 每个 MAG 取最长的几条 contig

mkdir -p "$W"
log() { echo "[$(date '+%F %T')] $*"; }

# ---- 1. 每个 MAG 取最长 N 条 contig ----
if [ ! -s "$W/mag_top.fa" ]; then
  log "提取每个 MAG 最长的 $NTOP 条 contig"
  : > "$W/mag_top.fa"
  for f in "$MAGS"/*.fa; do
    [ -s "$f" ] || continue
    mag=$(basename "$f" .fa)
    awk -v M="$mag" '
      /^>/ { if (seq!="") print hdr"\n"seq; hdr=">"M"|"substr($0,2); seq=""; next }
      { seq=seq $0 }
      END { if (seq!="") print hdr"\n"seq }
    ' "$f" | awk -v M="$mag" -v N="$NTOP" '
      /^>/ { n++; if (n>N) exit }
      { print }
    ' >> "$W/mag_top.fa"
  done
  log "  $(grep -c '^>' "$W/mag_top.fa") 条序列"
fi

# ---- 2. blastn ----
if [ -s "$W/mag_vs_host.tsv" ]; then
  log "blast 结果已存在，跳过"
else
  log "blastn vs 宿主基因组库（307 Gb）"
  blastn -task megablast -query "$W/mag_top.fa" -db "$DB" \
    -outfmt "6 qseqid sseqid pident length evalue bitscore" \
    -evalue 1e-20 -max_target_seqs 10 -num_threads 8 \
    -out "$W/mag_vs_host.tsv" > "$W/blast.log" 2>&1
fi
log "完成，$(wc -l < "$W/mag_vs_host.tsv") 条命中"

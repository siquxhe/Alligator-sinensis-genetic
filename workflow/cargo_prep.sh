#!/bin/bash
# 前噬菌体 cargo 注释 —— 第 1 步：汇总序列 + 建库
set -uo pipefail

B="$HOME/virome"
C="$B/cargo"
E="$HOME/biotools/envs/virome/bin"
export PATH="$E:$PATH"

mkdir -p "$C"/{input,db,work,results}

log() { echo "[$(date '+%T')] $*"; }

# ---------- 1. 汇总六样本的 provirus 核酸与蛋白 ----------
: > "$C/input/all_provirus.fna"
: > "$C/input/all_provirus.faa"
: > "$C/input/all_provirus_genes.tsv"
first=1
for s in W1 W2 W3 S1 S2 S3; do
  D="$B/work/$s/genomad/${s}.contigs_find_proviruses"
  [ -f "$D/${s}.contigs_provirus.fna" ] || { log "缺 $s"; continue; }
  # 序列头加样本前缀，避免跨样本撞名
  awk -v S="$s" '/^>/{sub(/^>/,">"S"|")} {print}' "$D/${s}.contigs_provirus.fna" >> "$C/input/all_provirus.fna"
  awk -v S="$s" '/^>/{sub(/^>/,">"S"|")} {print}' "$D/${s}.contigs_provirus_proteins.faa" >> "$C/input/all_provirus.faa"
  if [ $first -eq 1 ]; then
    head -1 "$D/${s}.contigs_provirus_genes.tsv" > "$C/input/all_provirus_genes.tsv"
    first=0
  fi
  awk -v S="$s" -F'\t' 'NR>1{$1=S"|"$1; print}' OFS='\t' "$D/${s}.contigs_provirus_genes.tsv" >> "$C/input/all_provirus_genes.tsv"
  log "  $s: $(grep -c '^>' "$D/${s}.contigs_provirus.fna") 条前噬菌体"
done

log "合计: $(grep -c '^>' "$C/input/all_provirus.fna") 条前噬菌体 / $(grep -c '^>' "$C/input/all_provirus.faa") 个蛋白 / $(($(wc -l < "$C/input/all_provirus_genes.tsv")-1)) 个基因"

# ---------- 2. 建 VFDB diamond 库 ----------
if [ ! -f "$C/db/VFDB.dmnd" ]; then
  log "解压 VFDB"
  zcat "$C/db/VFDB_setB_pro.fas.gz" > "$C/db/VFDB_pro.faa"
  log "VFDB 蛋白数: $(grep -c '^>' "$C/db/VFDB_pro.faa")"
  log "建 VFDB 索引（约 1-2 分钟）"
  diamond makedb --in "$C/db/VFDB_pro.faa" -d "$C/db/VFDB" --threads 8 2>&1 | tail -2
else
  log "VFDB 索引已存在"
fi
ls -lh "$C/db/VFDB.dmnd" 2>/dev/null | awk '{print "  VFDB.dmnd " $5}'

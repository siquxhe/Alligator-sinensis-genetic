#!/bin/bash
# B1: 对每个 spike 文库跑两种 read 层规则
#   R_rvdb : DIAMOND blastx vs RVDB（全部命中，pident>=40, 长度>=30）
#   R_votu : bowtie2 比对到本研究 vOTU 目录 (votu95)
# 输出 results/<tag>.hits.tsv 与 <tag>.votu.txt
set -uo pipefail
trap '' HUP TERM

E=$HOME/biotools/envs/virome/bin
export PATH=$E:$PATH
BASE=/mnt/work/chicken/b1
DB=/mnt/work/chicken/db/RVDBv32.dmnd
VOTU=$HOME/virome/work/votu/votu95
mkdir -p "$BASE/results"

cd "$BASE" || exit 1

for f1 in libs/*_1.fq.gz; do
  tag=$(basename "$f1" _1.fq.gz)
  out="$BASE/results/$tag"
  [ -s "$out.hits.tsv" ] && [ -s "$out.votu.txt" ] && { echo "[skip] $tag"; continue; }

  echo "[$(date +%H:%M)] $tag"
  : > "$out.hits.tsv"
  for mate in 1 2; do
    gzip -dc "libs/${tag}_${mate}.fq.gz" > /tmp/${tag}_${mate}.fq
    diamond blastx -q /tmp/${tag}_${mate}.fq -d "$DB" \
      --evalue 1e-5 --outfmt 6 qseqid stitle pident length \
      --threads 8 --max-target-seqs 1 >> "$out.hits.tsv" 2>>"$BASE/logs/${tag}.diamond.log"
    rm -f /tmp/${tag}_${mate}.fq
  done

  n=$(bowtie2 -x "$VOTU" -1 "libs/${tag}_1.fq.gz" -2 "libs/${tag}_2.fq.gz" \
        -p 8 --very-sensitive --no-unal 2>"$BASE/logs/${tag}.bowtie2.log" \
      | awk -F'\t' '$1 !~ /^@/ && $3 != "*" {n++} END{print n+0}')
  echo "$n" > "$out.votu.txt"
  echo "  RVDB 命中行 $(wc -l < "$out.hits.tsv")｜vOTU 比对 $n"
done

echo "=== 结束 $(date) ==="
touch "$BASE/results/.DONE"

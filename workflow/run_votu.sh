#!/bin/bash
# vOTU 聚类：6 样本病毒 contigs 合并 → CD-HIT-EST 95% ANI → 聚类表
# 口径：-c 0.95（一致性） -aS 0.85（较短序列覆盖度），与 IMG/VR 的 vOTU 定义一致
set -uo pipefail
cd "$HOME/virome" || exit 1

E="$HOME/biotools/envs/virome/bin"
OUT="work/votu"
mkdir -p "$OUT"

ALL="$OUT/virus_all.fna"
: > "$ALL"

# 合并：contig id 加样本前缀（各样本 contig 名会重复，如 k141_123）
for s in W1 W2 W3 S1 S2 S3; do
  f="work/$s/genomad/$s.contigs_summary/${s}.contigs_virus.fna"
  n=$(grep -c "^>" "$f")
  awk -v S="$s" '/^>/{print ">" S "__" substr($1,2); next} {print}' "$f" >> "$ALL"
  echo "  $s: $n 条"
done
echo "合并后: $(grep -c '^>' "$ALL") 条，$(du -h "$ALL" | cut -f1)"

echo "=== CD-HIT-EST 开始 $(date '+%T') ==="
"$E/cd-hit-est" -i "$ALL" -o "$OUT/votu95" \
  -c 0.95 -aS 0.85 -g 1 -d 0 -T 8 -M 0 \
  > "$OUT/cdhit.log" 2>&1
echo "=== 结束 $(date '+%T') ==="
tail -3 "$OUT/cdhit.log"

echo "vOTU 数: $(grep -c '^>' "$OUT/votu95")"

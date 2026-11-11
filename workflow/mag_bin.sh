#!/bin/bash
# MAG 第 2 步：MetaBAT2 分箱
set -uo pipefail

B="$HOME/virome"
E="$HOME/biotools/envs/virome/bin"
MB="$HOME/biotools/envs/metabat/bin"   # metabat2 2.12 会段错误，用 2.15
export PATH="$E:$PATH"
T=${1:-8}
ORDER="W1 W2 W3 S1 S2 S3"

log() { echo "[$(date '+%F %T')] $*"; }

for s in $ORDER; do
  M="$B/work/$s/mag"
  C="$B/work/$s/megahit/$s.contigs.fa"
  D="$M/$s.depth.txt"
  OUT="$M/bins"

  if [ -s "$D" ] && [ -d "$OUT" ] && [ "$(ls -1 "$OUT"/*.fa 2>/dev/null | wc -l)" -gt 0 ]; then
    log "$s 已分箱（$(ls -1 "$OUT"/*.fa | wc -l) 个 bin），跳过"
    continue
  fi
  [ -s "$D" ] || { log "$s 缺深度文件，跳过"; continue; }

  mkdir -p "$OUT"
  log "$s 分箱（minContig 1500）"
  # -m 1500: 最小 contig 长度；--unbinned 不要
  "$MB/metabat2" -i "$C" -a "$D" -o "$OUT/bin" -m 1500 -t "$T" \
    > "$M/metabat2.log" 2>&1
  n=$(ls -1 "$OUT"/*.fa 2>/dev/null | wc -l)
  log "$s 得到 $n 个 bin"
done

# 汇总所有 bin 到统一目录，命名 <sample>.bin.<n>.fa
ALL="$B/work/mag_all_bins"
mkdir -p "$ALL"
for s in $ORDER; do
  for f in "$B/work/$s/mag/bins"/*.fa; do
    [ -s "$f" ] || continue
    b=$(basename "$f" .fa)
    cp "$f" "$ALL/${s}.${b}.fa"
  done
done
log "合计 $(ls -1 "$ALL"/*.fa 2>/dev/null | wc -l) 个 bin 汇总到 $ALL"

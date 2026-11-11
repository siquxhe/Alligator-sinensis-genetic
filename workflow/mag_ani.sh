#!/bin/bash
# MAG 第 3.5 步：fastANI 全对全，供 95% ANI 去冗余
set -uo pipefail

B="$HOME/virome"
E="$HOME/biotools/envs/virome/bin"
export PATH="$E:$PATH"
BINS="$B/work/mag_all_bins"
W="$B/work/mag_fastani"

mkdir -p "$W"
log() { echo "[$(date '+%F %T')] $*"; }

# 只对候选（≥50% 完整）做 ANI，避免无用计算
CAND="$W/cand.list"
if [ -s "$B/work/mag_checkm/checkm_qa.tsv" ]; then
  awk -F'\t' 'NR>1 && $6+0 >= 50 {print $1}' "$B/work/mag_checkm/checkm_qa.tsv" > "$CAND"
else
  ls "$BINS"/*.fa | xargs -n1 basename | sed 's/\.fa$//' > "$CAND"
fi
n=$(wc -l < "$CAND")
log "候选 bin: $n"

: > "$W/q.list"; : > "$W/r.list"
while read -r b; do
  f="$BINS/$b.fa"
  [ -s "$f" ] && { echo "$f" >> "$W/q.list"; echo "$f" >> "$W/r.list"; }
done < "$CAND"

if [ -s "$W/ani.txt" ]; then
  log "ANI 结果已存在，跳过"
else
  log "运行 fastANI（$n × $n）"
  fastANI --ql "$W/q.list" --rl "$W/r.list" -o "$W/ani.txt" -t 8 \
    > "$W/fastani.log" 2>&1
fi
log "完成，$(wc -l < "$W/ani.txt" 2>/dev/null) 对 ANI 记录"

#!/bin/bash
# MAG 第 3 步：CheckM 质量评估 + 谱系
set -uo pipefail

B="$HOME/virome"
E="$HOME/biotools/envs/virome/bin"
export PATH="$E:$PATH"
BINS="$B/work/mag_all_bins"
OUT="$B/work/mag_checkm"
DATA="$B/db/checkm_data"

log() { echo "[$(date '+%F %T')] $*"; }

mkdir -p "$OUT"

# 设定 CheckM 数据根目录
if [ -d "$DATA/hmms" ] && [ -f "$DATA/taxon_marker_sets.tsv" ]; then
  checkm data setRoot "$DATA" > /dev/null 2>&1 && log "CheckM 数据根目录: $DATA"
else
  log "ERROR 未找到 CheckM 数据（$DATA），先解压"
  ls "$DATA" 2>/dev/null | head -5
  exit 1
fi

n=$(ls -1 "$BINS"/*.fa 2>/dev/null | wc -l)
log "待评估 bin: $n 个"

if [ -s "$OUT/lineage.ms" ]; then
  log "已有 lineage 结果，跳过评估"
else
  log "运行 lineage_wf（--reduced_tree，8 线程）"
  checkm lineage_wf -x fa --reduced_tree -t 8 --pplacer_threads 4 \
    "$BINS" "$OUT" > "$B/work/mag_checkm.log" 2>&1
fi

log "导出质量表"
checkm qa "$OUT/lineage.ms" "$OUT" -o 2 -f "$OUT/checkm_qa.tsv" \
  --tab_table -t 8 > /dev/null 2>&1

log "完成"
head -2 "$OUT/checkm_qa.tsv" 2>/dev/null

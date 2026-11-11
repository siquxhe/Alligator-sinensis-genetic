#!/bin/bash
# MAG 第 4 步：在 MAG 内预测前噬菌体（宿主=确证，不再是预测）
set -uo pipefail

B="$HOME/virome"
E="$HOME/biotools/envs/virome/bin"
export PATH="$E:$PATH"
BINS="${1:-$B/07_mag/mag_final}"   # 默认用去冗余后的最终 MAG
W="$B/work/mag_prophage"
DB="$B/db/genomad/genomad_db"

log() { echo "[$(date '+%F %T')] $*"; }
mkdir -p "$W"

log "输入目录: $BINS（$(ls -1 "$BINS"/*.fa 2>/dev/null | wc -l) 个 MAG）"

# ---- 1. 合并所有 bin 为一条 fasta，序列头保留 MAG 归属 ----
if [ ! -s "$W/mag_all.fa" ]; then
  log "合并 bin"
  : > "$W/mag_all.fa"
  for f in "$BINS"/*.fa; do
    [ -s "$f" ] || continue
    mag=$(basename "$f" .fa)
    awk -v M="$mag" '/^>/{sub(/^>/,">"M"|"); print; next} {print}' "$f" >> "$W/mag_all.fa"
  done
  log "合并完成：$(grep -c '^>' "$W/mag_all.fa") 条序列"
fi

# ---- 2. geNomad 在 MAG 内找前噬菌体 ----
if [ -d "$W/genomad" ] && compgen -G "$W/genomad/*_find_proviruses/*_provirus.fna" >/dev/null; then
  log "geNomad 结果已存在，跳过"
else
  log "geNomad end-to-end（含 find-proviruses）"
  "$E/genomad" end-to-end "$W/mag_all.fa" "$W/genomad" "$DB" \
    --threads 8 --splits 4 --cleanup > "$W/genomad.log" 2>&1 || { log "geNomad 失败"; exit 1; }
fi

# ---- 3. 汇总 provirus 序列 ----
PROV=$(ls "$W"/genomad/*_find_proviruses/*_provirus.fna 2>/dev/null | head -1)
if [ -z "$PROV" ]; then
  log "ERROR 未找到 provirus 序列文件"
  ls "$W/genomad" 2>/dev/null
  exit 1
fi
log "provirus 序列：$PROV（$(grep -c '^>' "$PROV") 条）"

# ---- 4. CheckV 评估这些前噬菌体 ----
if [ -s "$W/checkv/quality_summary.tsv" ]; then
  log "CheckV 结果已存在，跳过"
else
  log "CheckV 评估"
  "$E/checkv" end_to_end "$PROV" "$W/checkv" -t 8 > "$W/checkv.log" 2>&1
fi

log "完成"
head -1 "$W/checkv/quality_summary.tsv" 2>/dev/null

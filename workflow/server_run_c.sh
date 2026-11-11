#!/bin/bash
# ============================================================
# C 阶段：组装 → 病毒识别 → 完整性评估
#   用法： bash server_run_c.sh <样本ID> <run_accession> [线程数]
#   例：   bash server_run_c.sh S1 SRR14300940 8
#
#   输入： ~/virome/data/<RUN>.host_rm.{1,2}.fq.gz
#   输出： ~/virome/work/<SID>/
#           megahit/<SID>.contigs.fa
#           genomad/**/<...>_virus.fna
#           checkv/quality_summary.tsv
#           c_stage_summary.tsv
#
#   各步可重入：已完成的步骤会跳过
# ============================================================
set -uo pipefail

SID="${1:?用法: bash server_run_c.sh <样本ID> <run_accession> [线程]}"
RUN="${2:?缺少 run accession}"
T="${3:-8}"

E="$HOME/biotools/envs/virome/bin"
B="$HOME/virome"
W="$B/work/$SID"
DB="$B/db"
mkdir -p "$W"

# geNomad 需要能在 PATH 里找到 mmseqs
export PATH="$E:$PATH"

R1="$B/data/${RUN}.host_rm.1.fq.gz"
R2="$B/data/${RUN}.host_rm.2.fq.gz"
CONTIGS="$W/megahit/${SID}.contigs.fa"

log() { echo "[$(date '+%F %T')] $*"; }

# ---------- 1. 组装 ----------
if [ -s "$CONTIGS" ]; then
  log "组装已存在，跳过"
else
  log "MEGAHIT 开始"
  "$E/megahit" -1 "$R1" -2 "$R2" -o "$W/megahit" --out-prefix "$SID" \
    -t "$T" --min-contig-len 1000 -m 0.5 || { log "组装失败"; exit 1; }
fi
N_CTG=$(grep -c '^>' "$CONTIGS" 2>/dev/null || echo 0)
log "contigs: $N_CTG"

# ---------- 2. geNomad 病毒/质粒识别 ----------
if [ -d "$W/genomad" ] && compgen -G "$W/genomad/*_summary/*_virus.fna" >/dev/null; then
  log "geNomad 已存在，跳过"
else
  rm -rf "$W/genomad"      # 清理上次中断的残留，否则 geNomad 会拒绝写入
  log "geNomad 开始（MMseqs2 搜库，耗时较长）"
  "$E/genomad" end-to-end "$CONTIGS" "$W/genomad" "$DB/genomad/genomad_db" \
    --threads "$T" --splits 4 --cleanup || { log "geNomad 失败"; exit 1; }
fi

VIR=$(compgen -G "$W/genomad/*_summary/*_virus.fna" | head -1)
[ -s "$VIR" ] || { log "未产出病毒 contigs 文件，terminate"; exit 1; }
N_VIR=$(grep -c '^>' "$VIR")
log "病毒 contigs: $N_VIR"

# ---------- 3. CheckV 完整性 ----------
if [ -s "$W/checkv/quality_summary.tsv" ]; then
  log "CheckV 已存在，跳过"
else
  log "CheckV 开始"
  "$E/checkv" end_to_end "$VIR" "$W/checkv" -t "$T" \
    -d "$DB/checkv-db-v1.5" --remove_tmp || { log "CheckV 失败"; exit 1; }
fi

# ---------- 4. 汇总 ----------
"$E/python" "$B/scripts/summarize_c.py" "$SID" "$RUN" "$CONTIGS" "$VIR" "$W/checkv/quality_summary.tsv"
log "完成"

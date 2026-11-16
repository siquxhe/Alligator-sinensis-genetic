#!/usr/bin/env bash
# Wrapper for crispr_carriage.py — repo-native version.
#
# 来源：CRISPR_recording_package_2026-11-15.zip 内的 run_crispr_carriage.sh，
# 该版本按包内布局写死了两处路径（05_crispr_carriage.py、$HERE/06_mag_final_annotated.tsv），
# 放进本仓库会找不到文件。此处改为仓库布局，其余逻辑不变。
#
#   LIMIT=5 bash workflow/run_crispr_carriage.sh     # 冒烟测试（5 个 MAG）
#   LIMIT=0 bash workflow/run_crispr_carriage.sh     # 全量
#
#   所有路径均可用环境变量覆盖：
#   MAG_DIR=... CAS1_HMM=... CAS2_HMM=... OUT=... PYTHON=python bash workflow/run_crispr_carriage.sh
#
# 依赖：python3（或 PYTHON 指定的解释器）、minced、hmmsearch；
#       缺 minced/hmmsearch 时只告警不中断，但对应结果会是空的。

set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT="$HERE/crispr_carriage.py"

MAG_DIR="${MAG_DIR:-$HOME/virome/work/mag_all_bins}"
META="${META:-$HERE/../07_mag/mag_final_annotated.tsv}"
CAS1_HMM="${CAS1_HMM:-$HOME/biotools/hmm/Cas1.hmm}"
CAS2_HMM="${CAS2_HMM:-$HOME/biotools/hmm/Cas2.hmm}"
OUT="${OUT:-$HOME/virome/work/crispr_carriage}"
THREADS="${THREADS:-8}"
LIMIT="${LIMIT:-0}"
PYTHON="${PYTHON:-python3}"

log() { printf '[%s] %s\n' "$(date '+%H:%M:%S')" "$*"; }
die() { printf '[error] %s\n' "$*" >&2; exit 1; }

[[ -f "$SCRIPT" ]] || die "script not found: $SCRIPT"
command -v "$PYTHON" >/dev/null 2>&1 || die "$PYTHON not found (set PYTHON=python if needed)"
[[ -d "$MAG_DIR" ]] || die "MAG_DIR not found: $MAG_DIR"
[[ -f "$META" ]] || log "[warn] META not found: $META (taxonomy columns will be blank)"
command -v minced >/dev/null 2>&1 || log "[warn] minced not found; CRISPR arrays will be missing"
command -v hmmsearch >/dev/null 2>&1 || log "[warn] hmmsearch not found; Cas calls will be missing"
[[ -f "$CAS1_HMM" ]] || log "[warn] Cas1 HMM not found: $CAS1_HMM"
[[ -f "$CAS2_HMM" ]] || log "[warn] Cas2 HMM not found: $CAS2_HMM"

mkdir -p "$OUT"

log "MAG_DIR=$MAG_DIR"
log "META=$META"
log "OUT=$OUT"
log "THREADS=$THREADS"
log "LIMIT=$LIMIT (0 = all)"

args=(
  --mag-dir "$MAG_DIR"
  --meta "$META"
  --out "$OUT"
  --threads "$THREADS"
)

# 只把存在的 HMM 传进去，否则脚本会因文件缺失直接报错
if [[ -f "$CAS1_HMM" ]]; then
  args+=(--cas1-hmm "$CAS1_HMM")
fi
if [[ -f "$CAS2_HMM" ]]; then
  args+=(--cas2-hmm "$CAS2_HMM")
fi
if [[ "$LIMIT" != "0" ]]; then
  args+=(--limit "$LIMIT")
fi

"$PYTHON" "$SCRIPT" "${args[@]}"

log "done. outputs:"
log "  $OUT/per_mag.tsv"
log "  $OUT/summary.tsv"
log "  $OUT/by_phylum.tsv"
log "  $OUT/run.log"

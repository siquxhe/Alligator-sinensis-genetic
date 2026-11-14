#!/usr/bin/env bash
# =============================================================================
# check_rvdb_phage.sh —— 判定 RVDB(-prot) 参考库是否包含噬菌体序列
#
# 背景
#   RVDB 核酸库明确排除 bacterial viruses（Goodacre 2018; Chin 2025），
#   RVDB-prot 由 U-RVDB 转换而来，理应继承该范围，但官方未逐字声明。
#   本脚本用两种独立方式判定，二者一致才算定论。
#
# 用法
#   bash workflow/check_rvdb_phage.sh                    # 默认库 + 仅表头扫描
#   bash workflow/check_rvdb_phage.sh --db /path/db.faa  # 指定库
#   bash workflow/check_rvdb_phage.sh --probe probes.faa # 追加蛋白比对（需 diamond）
#   bash workflow/check_rvdb_phage.sh --sample 5         # 打印命中的表头样例
#
# 退出码
#   0 = 检出噬菌体（库含噬菌体）
#   1 = 未检出噬菌体（库不含噬菌体，与核酸 RVDB 一致）
#   2 = 无法判定（文件缺失 / 阳性对照失败）
#
# 判读规则
#   阳性对照（Retroviridae 等非噬菌体病毒）必须 >0，否则说明表头扫描本身失效，
#   此时阴性结果不可信 —— 这是本脚本唯一容易被误用的地方。
# =============================================================================
set -uo pipefail
export LC_ALL=C

DB="${HOME}/virome/00_db/RVDBv32_unique.fasta"
PROBE=""
OUTDIR="09_tables"
NSAMPLE=3

while [ $# -gt 0 ]; do
  case "$1" in
    --db)     DB="$2"; shift 2 ;;
    --probe)  PROBE="$2"; shift 2 ;;
    --out)    OUTDIR="$2"; shift 2 ;;
    --sample) NSAMPLE="$2"; shift 2 ;;
    -h|--help) sed -n '2,30p' "$0"; exit 0 ;;
    *) echo "未知参数: $1" >&2; exit 2 ;;
  esac
done

# 噬菌体相关分类单元（覆盖 Caudoviricetes 及其主要科、crAss 样病毒、旧目名）
PHAGE_KW='phage|Caudoviricetes|Caudovirales|Siphoviridae|Myoviridae|Podoviridae|Microviridae|Inoviridae|Crassvirales|crAssphage|Tevenvirinae|Autographiviridae|Straboviridae|Drexlerviridae|Herelleviridae|Ackermannviridae|Chaseviridae|Demerecviridae|Schitoviridae|Zobellviridae|Bacterial virus|bacteriophage'
# 阳性对照：非噬菌体病毒，任何病毒库都应有
CTRL_KW='Retroviridae|Herpesviridae|Poxviridae|Papillomaviridae|Adenoviridae|Polyomaviridae'

log() { printf '%s\n' "$*"; }
die() { printf '错误: %s\n' "$*" >&2; exit 2; }

[ -f "$DB" ] || die "找不到库文件: $DB（用 --db 指定）"
command -v grep >/dev/null || die "缺少 grep"

mkdir -p "$OUTDIR"
STAMP="$(date +%F)"
DB_TAG="$(basename "${DB%.*}")"
TSV="${OUTDIR}/rvdb_phage_check_${DB_TAG}_${STAMP}.tsv"

TOTAL=$(grep -c '^>' "$DB" || true)
[ "${TOTAL:-0}" -gt 0 ] || die "库文件里没有 FASTA 表头: $DB"

log "=================================================================="
log "RVDB 噬菌体含量核查"
log "  库文件 : $DB"
log "  序列数 : ${TOTAL}"
log "  日期   : ${STAMP}"
log "=================================================================="

count_kw() { grep -c -i -E "$1" "$DB" || true; }

PHAGE_HITS=$(count_kw "$PHAGE_KW")
CTRL_HITS=$(count_kw "$CTRL_KW")

printf 'check\tkeyword_group\thits\ttotal\tpct\tverdict\n' > "$TSV"
printf 'phage\tphage_taxa\t%s\t%s\t%.4f\t%s\n' \
  "$PHAGE_HITS" "$TOTAL" \
  "$(awk -v a="$PHAGE_HITS" -v b="$TOTAL" 'BEGIN{printf "%.4f", (b>0? a*100/b : 0)}')" \
  "$([ "$PHAGE_HITS" -gt 0 ] && echo detected || echo absent)" >> "$TSV"
printf 'control\tnon_phage_virus\t%s\t%s\t%.4f\t%s\n' \
  "$CTRL_HITS" "$TOTAL" \
  "$(awk -v a="$CTRL_HITS" -v b="$TOTAL" 'BEGIN{printf "%.4f", (b>0? a*100/b : 0)}')" \
  "$([ "$CTRL_HITS" -gt 0 ] && echo ok || echo FAILED)" >> "$TSV"

log ""
log "表头扫描"
log "  噬菌体相关表头 : ${PHAGE_HITS}"
log "  阳性对照表头   : ${CTRL_HITS}   （Retroviridae/Herpesviridae 等）"

if [ "$NSAMPLE" -gt 0 ] && [ "$PHAGE_HITS" -gt 0 ]; then
  log ""
  log "  命中样例（前 ${NSAMPLE} 条）:"
  grep -i -E "$PHAGE_KW" "$DB" | head -n "$NSAMPLE" | cut -c1-160 | sed 's/^/    /'
fi

# ---------------- 可选：蛋白比对（更硬的证据） ----------------
PROBE_VERDICT="skipped"
if [ -n "$PROBE" ]; then
  log ""
  log "蛋白比对（--probe）"
  [ -f "$PROBE" ] || die "找不到探针文件: $PROBE"
  if ! command -v diamond >/dev/null 2>&1; then
    log "  跳过：未找到 diamond（可用 conda 环境激活后重跑）"
    PROBE_VERDICT="no_diamond"
  else
    DMND="${DB}.dmnd"
    if [ ! -f "$DMND" ]; then
      log "  未找到 ${DMND}，正在建库（一次即可）..."
      diamond makedb --in "$DB" -d "$DB" >/dev/null 2>&1 || die "diamond makedb 失败"
    fi
    HITS=$(diamond blastp --query "$PROBE" --db "$DMND" \
             --evalue 1e-5 --max-target-seqs 1 --outfmt 6 --quiet 2>/dev/null | wc -l)
    PROBE_HITS=${HITS//[!0-9]/}
    PROBE_TOTAL=$(grep -c '^>' "$PROBE" || true)
    log "  探针数 ${PROBE_TOTAL}，命中 ${PROBE_HITS}"
    if [ "${PROBE_HITS:-0}" -gt 0 ]; then PROBE_VERDICT="detected"; else PROBE_VERDICT="absent"; fi
    printf 'probe\tphage_probe_blastp\t%s\t%s\t-\t%s\n' \
      "$PROBE_HITS" "$PROBE_TOTAL" "$PROBE_VERDICT" >> "$TSV"
  fi
fi

# ---------------- 判读 ----------------
log ""
log "判读"
if [ "$CTRL_HITS" -le 0 ]; then
  log "  结论：无法判定 —— 阳性对照 0 命中，说明表头不含可识别的分类名，"
  log "        阴性结果不可信。请改用 --probe 做蛋白比对。"
  RC=2
elif [ "$PHAGE_HITS" -eq 0 ] && [ "$PROBE_VERDICT" = "absent" ]; then
  log "  结论：库中未检出噬菌体（表头 0 命中 + 探针 0 命中）"
  log "        → C1/C2 应改称「对噬菌体缺失库的病毒样命中」，不得称 viral fraction。"
  RC=1
elif [ "$PHAGE_HITS" -eq 0 ] && [ "$PROBE_VERDICT" = "skipped" ]; then
  log "  结论：表头未见噬菌体（${PHAGE_HITS}/${TOTAL}），但无蛋白比对佐证。"
  log "        建议加 --probe 复验后再写入 Methods。"
  RC=1
elif [ "$PHAGE_HITS" -gt 0 ] && [ "$PROBE_VERDICT" = "absent" ]; then
  log "  结论：表头有噬菌体名但探针未命中 —— 可能仅零星收录，需人工检查样例。"
  RC=0
else
  log "  结论：检出噬菌体（表头 ${PHAGE_HITS} 条；探针 ${PROBE_VERDICT}）"
  log "        → 第二轴的解释不能归因于「库中无噬菌体」，需另找原因。"
  RC=0
fi

log ""
log "明细已写入: $TSV"
exit "$RC"

#!/usr/bin/env bash
# ============================================================
# 病毒 reads 筛查（B4）—— DIAMOND blastx vs RVDB-prot v32 (Unique)
#   用法： bash workflow/viral_screen.sh SRR14300938 [threads]
#   输入： 02_host_removed/<RUN>.host_rm.{1,2}.fq.gz
#   输出： 04_viral/<RUN>.R{1,2}.hits.tsv   （DIAMOND outfmt 6）
#          04_viral/<RUN>.viral_summary.tsv（本样本统计）
#          09_tables/viral_reads_summary.tsv（全部样本追加）
#
# 参数说明（写进方法学）：
#   --fast            DIAMOND 快速模式（灵敏度略降、速度约 10 倍）
#   -e 1e-5           期望值阈值
#   -k 1              每条 query 只留最佳命中
#   --query-cover 50  覆盖度 ≥50%（减少短片段假阳性）
#   后处理再筛 alignment length ≥ 30 aa、identity ≥ 40%
# ============================================================
set -uo pipefail
source "$(dirname "$0")/env.sh"

RUN="${1:?用法: bash workflow/viral_screen.sh <run_accession> [threads]}"
THREADS="${2:-8}"
mkdir -p 04_viral 09_tables

DB="00_db/RVDBv32"

for MATE in 1 2; do
  FQ="02_host_removed/${RUN}.host_rm.${MATE}.fq.gz"
  [ -f "$FQ" ] || { echo "缺少输入: $FQ" >&2; exit 1; }
  OUT="04_viral/${RUN}.R${MATE}.hits.tsv"
  CNT="04_viral/.${RUN}.R${MATE}.nreads"

  echo "==> $RUN R${MATE}: blastx 开始 $(date '+%H:%M:%S')"
  T0=$(date +%s)
  # 流式：解压 → fastq 转 fasta（截短 header）→ DIAMOND stdin
  zcat "$FQ" \
    | awk 'NR%4==1{sub(/^@/,">"); sub(/ .*/,""); print; next}
           NR%4==2{print}
           END{printf "%d\n", NR/4 > "'"$CNT"'"}' \
    | "$DIAMOND" blastx -d "$DB" -q - -o "$OUT" -f 6 \
        --fast -e 1e-5 -k 1 --query-cover 50 -p "$THREADS" \
        --quiet 2> "04_viral/${RUN}.R${MATE}.diamond.log"

  echo "    R${MATE} 用时 $(( $(date +%s) - T0 ))s，原始命中 $(wc -l < "$OUT") 行"
done

echo "==> 汇总 $RUN"
python workflow/summarize_viral.py "$RUN"

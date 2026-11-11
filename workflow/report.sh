#!/usr/bin/env bash
# ============================================================
# 汇总报告（multiqc）—— 任务 B5 辅助
#   用法： bash workflow/report.sh
#   扫描： 01_qc/（fastp json）、09_tables/（bowtie2 日志 + 各汇总表）
#   输出： 08_figures/multiqc/multiqc_report.html + multiqc_data/
# ============================================================
set -euo pipefail
source "$(dirname "$0")/env.sh"

OUT="08_figures/multiqc"
mkdir -p "$OUT"

echo "==> multiqc 汇总"
"$MULTIQC" 01_qc 09_tables -o "$OUT" --force --filename "multiqc_report.html" "$@"
echo "==> 报告: $OUT/multiqc_report.html"

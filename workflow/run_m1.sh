#!/usr/bin/env bash
# ============================================================
# M1 批量驱动：质控（B1）→ 去宿主（B2）
#   用法： bash workflow/run_m1.sh SRR14300938 SRR14300940 [threads]
#   说明： 串行执行，避免两个 bowtie2 同时加载 4.1 GB 索引把内存打满。
#   日志： 09_tables/run_logs/<RUN>.<step>.log
# ============================================================
set -uo pipefail
source "$(dirname "$0")/env.sh"

THREADS="${THREADS:-6}"
RUNS=("$@")
[ ${#RUNS[@]} -gt 0 ] || { echo "用法: bash workflow/run_m1.sh <RUN> [RUN ...]"; exit 1; }
# 若最后一个参数是纯数字，视为线程数
LAST="${RUNS[${#RUNS[@]}-1]}"
if [[ "$LAST" =~ ^[0-9]+$ && ${#RUNS[@]} -gt 1 ]]; then
  THREADS="$LAST"; unset 'RUNS[${#RUNS[@]}-1]'
fi

mkdir -p 09_tables/run_logs 01_qc 02_host_removed

echo "===== M1 批处理开始 $(date '+%F %T') | 样本数 ${#RUNS[@]} | 线程 $THREADS ====="
for RUN in "${RUNS[@]}"; do
  echo ""
  echo "########## $RUN ##########"

  # --- B1 质控 ---
  if [ -f "01_qc/${RUN}.clean.1.fq.gz" ]; then
    echo "[B1] 已存在，跳过"
  else
    T0=$(date +%s)
    bash workflow/qc.sh "$RUN" "$THREADS" 2>&1 | tee "09_tables/run_logs/${RUN}.qc.log"
    echo "[B1] 耗时 $(( $(date +%s) - T0 ))s"
  fi

  # --- B2 去宿主 ---
  if [ -f "02_host_removed/${RUN}.host_rm.1.fq.gz" ]; then
    echo "[B2] 已存在，跳过"
  else
    T0=$(date +%s)
    bash workflow/host_removal.sh "$RUN" "$THREADS" 2>&1 | tee "09_tables/run_logs/${RUN}.host_removal.log"
    echo "[B2] 耗时 $(( $(date +%s) - T0 ))s"
  fi
done

echo ""
echo "===== M1 批处理结束 $(date '+%F %T') ====="
echo ""
echo "== 汇总表 =="
[ -f 09_tables/host_removal_summary.tsv ] && column -t -s$'\t' 09_tables/host_removal_summary.tsv

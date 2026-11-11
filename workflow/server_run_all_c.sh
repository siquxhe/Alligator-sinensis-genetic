#!/bin/bash
# 批量跑 C 阶段：串行执行，避免 8 线程组装互相抢内存/CPU
set -uo pipefail
cd "$HOME/virome" || exit 1

# 样本ID  run_accession
SAMPLES="
W1 SRR14300938
W2 SRR14300939
W3 SRR14300942
S2 SRR14300941
S3 SRR14300943
"

echo "===== 批量 C 阶段开始 $(date '+%F %T') ====="
while read -r SID RUN; do
  [ -z "${SID:-}" ] && continue
  echo ""
  echo "########## $SID ($RUN) $(date '+%T') ##########"
  bash scripts/server_run_c.sh "$SID" "$RUN" 8
  echo "########## $SID 结束 $(date '+%T') ##########"
done <<< "$SAMPLES"

echo ""
echo "===== 全部完成 $(date '+%F %T') ====="
echo "=== 汇总 ==="
for f in work/*/c_stage_summary.tsv; do
  [ -f "$f" ] || continue
  tail -1 "$f"
done

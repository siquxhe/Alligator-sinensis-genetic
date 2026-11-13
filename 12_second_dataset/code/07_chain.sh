#!/bin/bash
# 等组装队列（05_assembly.sh）结束后，再启动纯单位对照，避免 CPU 争抢
# 用法：nohup setsid bash 07_chain.sh > logs/chain.log 2>&1 &
set -uo pipefail

BASE=/mnt/work/chicken
DONE="$BASE/results/.C4_DONE"

echo "=== 等待组装队列 $(date) ==="
while [ ! -f "$DONE" ]; do
  sleep 300
done
echo "=== 组装队列已完成，启动单位对照 $(date) ==="

cd "$BASE" || exit 1
bash bin/06_unit_test.sh

#!/bin/bash
# 98_safestop.sh — 干净停机准备：等当前样本 geNomad 出结果 → 停流水线 → 落盘 → 卸载 /mnt/work
#
# 用法：
#   bash 98_safestop.sh          # 等当前样本跑完再停（最多等 45 分钟）
#   bash 98_safestop.sh --now    # 立刻停（丢当前样本已算的部分）
#
# 结束后屏幕会打印「可以断电」，此时可直接关电源。
# 恢复供电后执行： bash /mnt/work/chicken/bin/99_resume.sh
set -uo pipefail

BASE=/mnt/work/chicken
SUM=$BASE/results/C4_summary.tsv
MODE=${1:-}

if [ ! -s "$SUM" ]; then
  echo "!! 找不到 $SUM，/mnt/work 可能未挂载，终止"
  exit 1
fi

if [ "$MODE" != "--now" ]; then
  CUR=$(wc -l < "$SUM")
  echo "[$(date '+%F %T')] 当前 C4 行数=$CUR，等当前样本落表（最多 45 分钟）..."
  for _ in $(seq 1 270); do
    sleep 10
    N=$(wc -l < "$SUM")
    if [ "$N" -gt "$CUR" ]; then
      echo "[$(date '+%F %T')] 新结果已写入（$CUR -> $N），当前样本已完成"
      break
    fi
    if ! pgrep -f "bin/05_assembly.sh" > /dev/null; then
      echo "[$(date '+%F %T')] 流水线已自行结束"
      break
    fi
  done
fi

echo "[$(date '+%F %T')] 停止流水线与 geNomad ..."
pkill -TERM -f "bin/05_assembly.sh" 2>/dev/null
pkill -TERM -f "genomad end-to-end" 2>/dev/null
sleep 5
pkill -KILL -f "genomad end-to-end" 2>/dev/null
pkill -KILL -f "bin/05_assembly.sh" 2>/dev/null
sleep 2

if pgrep -f "05_assembly|genomad end-to-end" > /dev/null; then
  echo "!! 仍有残留进程，请手动检查："
  pgrep -fa "05_assembly|genomad end-to-end"
else
  echo "[OK] 无残留进程"
fi

cd / || exit 1
sync; sync

echo "[$(date '+%F %T')] 卸载 /mnt/work ..."
if umount /mnt/work 2>/dev/null; then
  echo "[OK] /mnt/work 已正常卸载"
else
  echo "  正常卸载失败，尝试按 PID 释放占用后再卸 ..."
  fuser -km /mnt/work 2>/dev/null
  sleep 3
  if umount /mnt/work 2>/dev/null; then
    echo "[OK] /mnt/work 已卸载"
  else
    umount -l /mnt/work 2>/dev/null && echo "[OK] /mnt/work 延迟卸载（数据已 sync）" \
      || echo "!! 卸载失败，断电前请手动 umount /mnt/work"
  fi
fi
sync

echo
echo "=========================================="
echo "  可以断电：$(date '+%F %T')"
echo "  恢复供电后执行："
echo "    bash /mnt/work/chicken/bin/99_resume.sh"
echo "=========================================="

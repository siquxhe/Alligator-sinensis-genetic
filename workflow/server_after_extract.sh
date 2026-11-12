#!/bin/bash
# 解压结束后自动接 iPHoP：等 tar 进程消失 → 再跑后处理
# 由 systemd 在旧守候进程退出后拉起
set -uo pipefail

BASE=/mnt/work/iphop_db
LOG=$BASE/watch.log
log() { echo "[$(date '+%F %T')] $*" >> "$LOG"; }

if [ -f "$BASE/.iphop_done" ]; then
  log "iPHoP 已完成，无需重复"
  exit 0
fi

log "----- 等待解压结束 -----"
n=0
while pgrep -x tar > /dev/null; do
  n=$((n + 1))
  [ $((n % 10)) -eq 0 ] && log "  解压仍在进行（已等 $((n)) 分钟），文件 $(find "$BASE/extract" -type f 2>/dev/null | wc -l) 个"
  sleep 60
done

log "解压进程已结束，等待 60 秒让文件句柄释放"
sleep 60
exec bash "$HOME/biotools/server_postprocess_iphop.sh"

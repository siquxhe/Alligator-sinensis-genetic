#!/bin/bash
# 用 aria2c 重下 CheckM 数据（16 连接 + 断点续传 + 无限重试）
set -uo pipefail

DB="$HOME/virome/db"
U="https://zenodo.org/records/7401545/files/checkm_data_2015_01_16.tar.gz?download=1"
OUT="$DB/checkm_data_2015_01_16.tar.gz"
LOG="$DB/checkm_aria.log"

echo "[$(date '+%T')] 停止旧下载" >> "$LOG"

# 停旧的分段下载脚本（按脚本名，不会匹配到自己）
for p in $(pgrep -f "server_dl_bigfile.sh" 2>/dev/null); do kill "$p" 2>/dev/null; done
sleep 2
# 停所有 curl（aria2c 不用 curl）
for p in $(pgrep -x curl 2>/dev/null); do kill "$p" 2>/dev/null; done
sleep 3

rm -rf "$DB/checkm_data_2015_01_16.tar.gz.parts"
rm -f "$OUT" "$OUT.aria2"
mkdir -p "$DB"

echo "[$(date '+%T')] 启动 aria2c" >> "$LOG"
aria2c -x16 -s16 -k 4M \
  --max-tries=0 --retry-wait=3 \
  --continue=true --auto-file-renaming=false --allow-overwrite=true \
  --summary-interval=30 --console-log-level=warn \
  --dir="$DB" -o checkm_data_2015_01_16.tar.gz "$U" >> "$LOG" 2>&1

rc=$?
echo "[$(date '+%T')] aria2c 结束 rc=$rc，大小 $(stat -c %s "$OUT" 2>/dev/null)" >> "$LOG"
if [ "$(stat -c %s "$OUT" 2>/dev/null)" = "288590617" ]; then
  echo DONE > "$DB/.checkm_dl"
  echo "[$(date '+%T')] 大小校验通过" >> "$LOG"
fi

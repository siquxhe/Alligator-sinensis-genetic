#!/bin/bash
# 重启后自动续跑：机器近期在负载下反复重启，靠 cron @reboot 恢复
# 各步可重入，已完成的样本不会重跑
export PATH=$HOME/biotools/envs/virome/bin:$PATH
BASE=/mnt/work/chicken
cd "$BASE" || exit 1

# 等 60 秒让磁盘和网络就绪
sleep 60

# 若已有 05 在跑则不重复启动
if pgrep -f "bin/05_assembly.sh" > /dev/null; then
  echo "[$(date)] 05_assembly 已在运行，跳过"
  exit 0
fi

echo "[$(date)] @reboot 自动续跑 05_assembly" >> "$BASE/raw/logs/reboot.log"
# 串行：组装队列结束后接着跑纯单位对照（06 自身可重入）
setsid -f bash -c 'bash bin/05_assembly.sh >> "$BASE/raw/logs/assembly.log" 2>&1; bash bin/06_unit_test.sh >> "$BASE/raw/logs/unit.log" 2>&1' >> "$BASE/raw/logs/reboot.log" 2>&1

#!/bin/bash
# 等待 NTFS 脏页刷完 -> 删除解压后的 extract -> 启动 Windows 镜像生成
set -uo pipefail

LOG=/tmp/_cleanup.log
exec >> "$LOG" 2>&1

echo "=== WAIT FLUSH $(date) ==="

while true; do
    D=$(awk '/^Dirty:/{print $2}' /proc/meminfo)
    echo "$(date +%H:%M) Dirty=$((D / 1024))MB"
    if [ "$D" -lt 200000 ]; then
        break
    fi
    sleep 120
done

echo "=== FLUSH DONE $(date) ==="

if [ ! -f /mnt/usb2t/_iphop_backup/iPHoP.latest.tar.gz ]; then
    echo "ABORT: iPHoP.latest.tar.gz missing, refuse to delete"
    exit 1
fi

echo "=== BEFORE DELETE ==="
du -sh /mnt/usb2t/_iphop_backup 2>/dev/null

rm -rf /mnt/usb2t/_iphop_backup/extract

echo "=== DELETED $(date) ==="
du -sh /mnt/usb2t/_iphop_backup 2>/dev/null
df -h /mnt/usb2t | tail -1

sync
echo "=== SYNC DONE $(date) ==="

echo "=== START IMAGE $(date) ==="
/root/make_windows_vm.sh

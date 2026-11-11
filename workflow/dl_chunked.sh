#!/usr/bin/env bash
# ============================================================
# 通用分片下载器（单连接被限速时用）
#   用法： bash workflow/dl_chunked.sh <URL> <输出文件> [分片数]
#   原理： 先取 Content-Length，切成 N 段并行 curl -r，
#          逐段校验字节数，全部通过后按序拼接（避免稀疏写入）。
# ============================================================
set -uo pipefail
URL="${1:?用法: $0 <URL> <OUTFILE> [N]}"
OUT="${2:?缺少输出文件名}"
N="${3:-16}"

SIZE=$(curl -sIL --max-time 30 "$URL" | grep -i '^content-length:' | tail -1 | tr -d '\r' | awk '{print $2}')
[ -n "${SIZE:-}" ] && [ "$SIZE" -gt 0 ] || { echo "无法获取文件大小"; exit 1; }
CH=$(( (SIZE + N - 1) / N ))
echo "目标: $OUT  大小: $SIZE  分 $N 段，每段约 $(( CH/1048576 )) MB"

TMPD="$(dirname "$OUT")/.chunks_$(basename "$OUT")"
mkdir -p "$TMPD"

try_chunk() {
  local i=$1 from=$(( $1 * CH )) to=$(( $1 * CH + CH - 1 ))
  [ "$to" -ge "$SIZE" ] && to=$(( SIZE - 1 ))
  local exp=$(( to - from + 1 ))
  local f="$TMPD/p$i"
  # 已有且完整则跳过
  local have=0
  [ -f "$f" ] && have=$(stat -c%s "$f")
  [ "$have" = "$exp" ] && return 0
  for attempt in 1 2 3 4 5; do
    have=0; [ -f "$f" ] && have=$(stat -c%s "$f")
    [ "$have" -gt "$exp" ] && { rm -f "$f"; have=0; }
    curl -s --max-time 1800 --retry 3 --retry-delay 3 \
         -r $(( from + have ))-$to "$URL" >> "$f" 2>/dev/null
    have=$(stat -c%s "$f" 2>/dev/null || echo 0)
    [ "$have" = "$exp" ] && return 0
  done
  echo "  段 $i 失败：$have / $exp"
  return 1
}

for i in $(seq 0 $((N-1))); do
  try_chunk "$i" &
  # 控制并发
  while [ "$(jobs -r | wc -l)" -ge "$N" ]; do wait -n; done
done
wait

# 校验
ok=1
for i in $(seq 0 $((N-1))); do
  from=$(( i * CH )); to=$(( from + CH - 1 ))
  [ "$to" -ge "$SIZE" ] && to=$(( SIZE - 1 ))
  exp=$(( to - from + 1 ))
  act=$(stat -c%s "$TMPD/p$i" 2>/dev/null || echo 0)
  [ "$act" != "$exp" ] && { echo "  段 $i 不符: $act / $exp"; ok=0; }
done

if [ "$ok" = 1 ]; then
  : > "$OUT.tmp"
  for i in $(seq 0 $((N-1))); do cat "$TMPD/p$i" >> "$OUT.tmp"; done
  mv "$OUT.tmp" "$OUT"
  echo "完成: $OUT ($(stat -c%s "$OUT") 字节，目标 $SIZE)"
  for i in $(seq 0 $((N-1))); do rm -f "$TMPD/p$i"; done
  rmdir "$TMPD" 2>/dev/null
else
  echo "❌ 仍有分片不完整，保留 $TMPD 以便续传"
  exit 1
fi

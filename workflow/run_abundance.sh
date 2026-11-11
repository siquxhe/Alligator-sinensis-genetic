#!/bin/bash
# 丰度定量：所有样本 reads 比对到统一的 vOTU 代表序列集
#   - 统一参考，保证跨样本可比（而不是各比各的 contigs）
#   - bowtie2 --very-sensitive；不过滤多重比对，但去掉 secondary/supplementary
#   - 输出每样本每个 vOTU 的 read 数 + 比对总 reads（供 RPKM 归一化）
set -uo pipefail
cd "$HOME/virome" || exit 1

E="$HOME/biotools/envs/virome/bin"
V="work/votu"
A="$V/abund"
mkdir -p "$A"

# ---------- 1. 建索引 ----------
if [ -f "$V/votu95.1.bt2" ] || [ -f "$V/votu95.1.bt2l" ]; then
  echo "索引已存在"
else
  echo "=== bowtie2-build $(date '+%T') ==="
  "$E/bowtie2-build" --threads 8 "$V/votu95" "$V/votu95" 2>&1 | tail -2
fi

# ---------- 2. 逐样本比对 ----------
for pair in "W1 SRR14300938" "W2 SRR14300939" "W3 SRR14300942" \
            "S1 SRR14300940" "S2 SRR14300941" "S3 SRR14300943"; do
  set -- $pair
  SID=$1; RUN=$2
  OUT="$A/$SID.counts.tsv"
  if [ -s "$OUT" ]; then echo "$SID 已完成，跳过"; continue; fi

  echo "=== $SID ($RUN) 开始 $(date '+%T') ==="
  "$E/bowtie2" -x "$V/votu95" \
      -1 "data/${RUN}.host_rm.1.fq.gz" -2 "data/${RUN}.host_rm.2.fq.gz" \
      -p 8 --very-sensitive --no-unal \
      2> "$A/$SID.bowtie2.log" \
    | "$E/samtools" view -F 2304 - \
    | awk '$3 != "*" {print $3}' \
    | sort | uniq -c \
    | awk '{print $2"\t"$1}' \
    | sort > "$OUT"

  # 比对总 reads（paired 模式下 log 里的 reads 数 = fragment 数）
  FRAG=$(grep -m1 -oE "^[0-9]+ reads; of these" "$A/$SID.bowtie2.log" | grep -oE "[0-9]+")
  echo "$FRAG" > "$A/$SID.nfrag"
  ALIGNED=$(grep -m1 -oE "[0-9]+ \([0-9.]+%\) aligned concordantly 0 times|overall" "$A/$SID.bowtie2.log" | head -1)
  echo "  片段数 $FRAG，vOTU 命中 $(wc -l < "$OUT") 个，用时 $(date '+%T')"
done

echo "===== 全部完成 $(date '+%F %T') ====="

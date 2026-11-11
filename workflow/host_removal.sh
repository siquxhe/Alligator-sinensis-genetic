#!/usr/bin/env bash
# ============================================================
# 去宿主脚本（bowtie2）—— 任务 B2
#   用法： bash workflow/host_removal.sh SRR14300938 [线程数]
#   输入： 01_qc/<RUN>.clean.{1,2}.fq.gz（没有则回退到 00_raw/<RUN>_{1,2}.fastq.gz）
#   输出： 02_host_removed/<RUN>.host_rm.{1,2}.fq.gz
#          09_tables/host_removal_summary.tsv（逐样本追加）
#
# 说明（Windows 环境三个坑，务必保留这些写法）：
#   1. bowtie2 的 --un-conc-gz 由 perl 包装脚本实现，必须用 $PERL 调 wrapper，
#      不能直接调 bowtie2-align-s.exe（该二进制不支持 --un-conc）。
#   2. -S 必须给真实文件，不能是 /dev/null —— 包装脚本要回读 SAM 来拆分 reads。
#      配合 --no-unal，SAM 里只有比对上的少量 reads，体积很小，用完即删。
#   3. 需要 LC_ALL=C（在 env.sh 里已设），否则 perl 刷一堆 locale 警告。
# ============================================================
set -euo pipefail
source "$(dirname "$0")/env.sh"

RUN="${1:?用法: bash workflow/host_removal.sh <run_accession> [threads]}"
THREADS="${2:-8}"

# 优先用质控后的数据，没有就用原始数据
if [ -f "01_qc/${RUN}.clean.1.fq.gz" ]; then
  R1="01_qc/${RUN}.clean.1.fq.gz"; R2="01_qc/${RUN}.clean.2.fq.gz"; SRC="01_qc"
else
  R1="00_raw/${RUN}_1.fastq.gz"; R2="00_raw/${RUN}_2.fastq.gz"; SRC="00_raw"
fi
for f in "$R1" "$R2"; do
  [ -f "$f" ] || { echo "缺少输入文件: $f" >&2; exit 1; }
done

mkdir -p 02_host_removed 09_tables
TMP_SAM="02_host_removed/.${RUN}.tmp.sam"
PREFIX="02_host_removed/${RUN}.host_rm.fq.gz"
# bowtie2 把 .1/.2 插在 .gz 之前：<前缀去.gz>.1.gz
OUT1="${PREFIX%.gz}.1.gz"
OUT2="${PREFIX%.gz}.2.gz"
LOG="09_tables/${RUN}.bowtie2.log"

rm -f "$TMP_SAM" "$OUT1" "$OUT2"

echo "==> 去宿主: $RUN（输入来自 $SRC，threads=$THREADS）"
bt2 \
  -x "$HOST_IDX" \
  -1 "$R1" -2 "$R2" \
  -S "$TMP_SAM" \
  --un-conc-gz "$PREFIX" \
  --no-unal \
  -p "$THREADS" \
  > /dev/null 2> "$LOG"

# 统一改名成 <RUN>.host_rm.1.fq.gz / .2.fq.gz
if [ -f "$OUT1" ]; then
  mv "$OUT1" "02_host_removed/${RUN}.host_rm.1.fq.gz"
  mv "$OUT2" "02_host_removed/${RUN}.host_rm.2.fq.gz"
else
  echo "警告：未找到 --un-conc-gz 输出，检查 $LOG" >&2
fi
rm -f "$TMP_SAM"

# 解析比对率并追加汇总表
RATE=$(grep -oE '[0-9.]+% overall alignment rate' "$LOG" | grep -oE '^[0-9.]+' || echo "NA")
TOTAL=$(grep -oE '^[0-9]+ reads; of these:' "$LOG" | grep -oE '^[0-9]+' || echo "NA")
if [ ! -f 09_tables/host_removal_summary.tsv ]; then
  printf "run_accession\tinput\ttotal_reads\thost_aligned_pct\n" > 09_tables/host_removal_summary.tsv
fi
printf "%s\t%s\t%s\t%s\n" "$RUN" "$SRC" "$TOTAL" "$RATE" >> 09_tables/host_removal_summary.tsv

echo "==> 比对汇总:"
grep -E "reads; of these:|overall alignment rate" "$LOG" | sed 's/^/    /'
echo "==> 输出: 02_host_removed/${RUN}.host_rm.{1,2}.fq.gz"
echo "==> 宿主比对率: ${RATE}%  （已记入 09_tables/host_removal_summary.tsv）"

#!/bin/bash
# 单样本试水：去宿主 → 比对到 vOTU 目录 → 计算 C6 与 C5 代理值
# 用法：bash 04_pilot.sh SRR6323088
set -uo pipefail

BASE=/mnt/work/chicken
E=$HOME/biotools/envs/virome/bin
export PATH=$E:$PATH
S=${1:-SRR6323088}
FQ=$BASE/fastq
HR=$BASE/host_removed
MP=$BASE/mapping
OUT=$BASE/results
mkdir -p "$HR" "$MP" "$OUT"

echo "=== 试水 $S  $(date) ==="

# ---------- 1. 去宿主
if [ ! -s "$HR/$S.host_rm.fq.1.gz" ]; then
  echo "[$(date +%H:%M)] 去宿主"
  bowtie2 -x "$BASE/refs/chicken" \
    -1 "$FQ/${S}_1.fastq.gz" -2 "$FQ/${S}_2.fastq.gz" \
    -S /dev/null --un-conc-gz "$HR/$S.host_rm.fq.gz" --no-unal -p 6 \
    2> "$MP/$S.host.bowtie2.log"
fi

IN_FRAG=$(grep -m1 -oE "^[0-9]+ reads; of these" "$MP/$S.host.bowtie2.log" | grep -oE "^[0-9]+")
HOST_RATE=$(grep -m1 -oE "[0-9.]+% overall alignment rate" "$MP/$S.host.bowtie2.log" | grep -oE "^[0-9.]+")
echo "  输入片段 $IN_FRAG，宿主比对率 $HOST_RATE%"

# ---------- 2. 比对到 vOTU 目录（参数与主项目 run_abundance.sh 一致）
echo "[$(date +%H:%M)] 比对到 vOTU"
if [ ! -s "$MP/$S.votu.counts.tsv" ]; then
  bowtie2 -x "$BASE/refs/votu" \
    -1 "$HR/$S.host_rm.fq.1.gz" -2 "$HR/$S.host_rm.fq.2.gz" \
    -p 6 --very-sensitive --no-unal 2> "$MP/$S.votu.bowtie2.log" \
    | samtools view -F 2304 - \
    | awk '$3 != "*" {print $3}' \
    | sort | uniq -c \
    | awk '{print $2"\t"$1}' | sort > "$MP/$S.votu.counts.tsv"
fi

CLEAN_FRAG=$(grep -m1 -oE "^[0-9]+ reads; of these" "$MP/$S.votu.bowtie2.log" | grep -oE "^[0-9]+")
MAPPED=$(awk '{s+=$2} END{print s+0}' "$MP/$S.votu.counts.tsv")
VOTU_HIT=$(wc -l < "$MP/$S.votu.counts.tsv")

# ---------- 3. 汇总
awk -v s="$S" -v i="$IN_FRAG" -v c="$CLEAN_FRAG" -v m="$MAPPED" -v v="$VOTU_HIT" -v h="$HOST_RATE" '
BEGIN{
  ri=i*2; rc=c*2;
  printf "sample\treads_input\treads_clean\thost_removed_pct\tvotu_hits\treads_mapped\tpct_of_clean\tpct_of_input\thost_rate_bowtie2\n";
  printf "%s\t%d\t%d\t%.2f\t%d\t%d\t%.3f\t%.3f\t%s\n", s, ri, rc, (ri-rc)/ri*100, v, m, m/rc*100, m/ri*100, h;
}' > "$OUT/${S}_pilot.tsv"

echo
column -t -s$'\t' "$OUT/${S}_pilot.tsv"
echo
echo "对照：论文报告各肠段 mapped reads 为 1.10%–1.84%（盲肠 1.62% ± 0.693%）"
echo "=== 结束 $(date) ==="

#!/bin/bash
# 纯"统计单元"对照：同一套病毒 contigs，分别用 reads 与 contig 两种单位计算占比
#
# 设计要点：参考集完全相同（该样本 geNomad 判定的 *_virus.fna），只变计数单位。
#   A（reads 单位）= 比对到该病毒集的 reads / 全部 clean reads
#   B（contig 单位）= 该病毒集 contig 数 / 全部 contig 数
# 这样得到的比值才是干净的"单位效应"，不含参考库/工具的混淆。
#
# 用法：nohup setsid bash 06_unit_test.sh > logs/unit.log 2>&1 &
set -uo pipefail

BASE=/mnt/work/chicken
E=$HOME/biotools/envs/virome/bin
export PATH=$E:$PATH
HR=$BASE/host_removed
AS=$BASE/assembly
REF=$BASE/refs/unit
OUT=$BASE/results/unit
mkdir -p "$REF" "$OUT"

SAMPLES="SRR6323088 SRR6323119 SRR6323120 SRR6323124 SRR6323125 SRR6323200"

echo "=== 纯单位对照 $(date) ==="

for S in $SAMPLES; do
  VF=$(ls "$AS/$S/genomad/"*_summary/*_virus.fna 2>/dev/null | head -1)
  CTG="$AS/$S/$S.contigs.fa"
  if [ -z "${VF:-}" ] || [ ! -s "$VF" ] || [ ! -s "$CTG" ]; then
    echo "[skip] $S 缺少 geNomad 或组装产物"
    continue
  fi
  ROW="$OUT/$S.tsv"
  if [ -s "$ROW" ]; then
    echo "[skip] $S 已有结果"
    continue
  fi

  echo "[$(date +%H:%M)] $S"
  [ -f "$REF/$S.1.bt2" ] || bowtie2-build --threads 8 --quiet "$VF" "$REF/$S"

  N_VIR=$(grep -c '^>' "$VF")
  N_CTG=$(grep -c '^>' "$CTG")
  CLEAN_FRAG=$(( $(gzip -dc "$HR/$S.host_rm.fq.1.gz" | wc -l) / 4 ))

  MAPD=$(bowtie2 -x "$REF/$S" \
            -1 "$HR/$S.host_rm.fq.1.gz" -2 "$HR/$S.host_rm.fq.2.gz" \
            -p 8 --very-sensitive --no-unal 2> "$OUT/$S.bowtie2.log" \
          | awk -F'\t' '$1 !~ /^@/ && $3 != "*" {n++} END{print n+0}')

  awk -v s="$S" -v r="$MAPD" -v cf="$CLEAN_FRAG" -v v="$N_VIR" -v c="$N_CTG" '
  BEGIN{
    clean=r*0+cf*2; if(clean<=0){print "ERR"; exit}
    pr = r/clean*100;          # reads 单位
    pc = v/c*100;              # contig 单位
    printf "%s\t%d\t%d\t%d\t%d\t%.4f\t%.4f\t%s\n", s, clean, r, c, v, pr, pc, (pr>0? sprintf("%.3f", pc/pr) : "NA")
  }' > "$ROW"

  echo "  reads 单位 ${MAPD} / $((CLEAN_FRAG*2))；contig 单位 $N_VIR / $N_CTG"
done

echo
echo "=== 汇总 ==="
printf "sample\tclean_reads\treads_mapped\tcontigs\tviral_contigs\tpct_reads_unit\tpct_contig_unit\tratio_contig_over_reads\n" > "$BASE/results/unit_axis.tsv"
cat "$OUT"/SRR*.tsv 2>/dev/null >> "$BASE/results/unit_axis.tsv"
column -t -s$'\t' "$BASE/results/unit_axis.tsv"
echo "=== 结束 $(date) ==="
touch "$OUT/.DONE"

#!/bin/bash
# 扬子鳄主数据集的纯"计数单位"对照
# 参考集固定为各样本 geNomad 判定的病毒 contigs，只变读数单位：
#   A（reads 单位） = 比对到该病毒集的 reads / 全部 clean reads
#   B（contig 单位）= 该病毒集 contig 数 / 全部 contig 数
# 目的：给论文主数据集一个不含参考库混淆的"单位效应"数值
#
# 用法：nohup setsid bash 08_alligator_unit.sh > ~/virome/unit_alligator.log 2>&1 &
set -uo pipefail
trap '' HUP TERM

E=$HOME/biotools/envs/virome/bin
export PATH=$E:$PATH
BASE=$HOME/virome
WORK=$BASE/work
DATA=$BASE/data
OUT=$BASE/unit_alligator
REF=$OUT/idx
mkdir -p "$REF"

# SID: RUN  （与 viral_specific_estimate.tsv 一致）
PAIRS="W1:SRR14300938 W2:SRR14300939 W3:SRR14300942 S1:SRR14300940 S2:SRR14300941 S3:SRR14300943"

echo "=== 扬子鳄 纯单位对照 $(date) ==="

for p in $PAIRS; do
  SID=${p%%:*}
  RUN=${p##*:}
  VF=$(ls "$WORK/$SID/genomad/"*_summary/*_virus.fna 2>/dev/null | head -1)
  CTG="$WORK/$SID/megahit/$SID.contigs.fa"
  R1="$DATA/$RUN.host_rm.1.fq.gz"
  R2="$DATA/$RUN.host_rm.2.fq.gz"

  if [ -z "${VF:-}" ] || [ ! -s "$VF" ] || [ ! -s "$CTG" ] || [ ! -s "$R1" ]; then
    echo "[skip] $SID 缺文件（VF/CTG/R1）"; continue
  fi
  ROW="$OUT/$SID.tsv"
  if [ -s "$ROW" ]; then echo "[skip] $SID 已完成"; continue; fi

  echo "[$(date +%H:%M)] $SID ($RUN)"
  [ -f "$REF/$SID.1.bt2" ] || bowtie2-build --threads 8 --quiet "$VF" "$REF/$SID"

  N_VIR=$(grep -c '^>' "$VF")
  N_CTG=$(grep -c '^>' "$CTG")
  CLEAN_FRAG=$(( $(gzip -dc "$R1" | wc -l) / 4 ))

  MAPD=$(bowtie2 -x "$REF/$SID" -1 "$R1" -2 "$R2" \
            -p 8 --very-sensitive --no-unal 2> "$OUT/$SID.bowtie2.log" \
          | awk -F'\t' '$1 !~ /^@/ && $3 != "*" {n++} END{print n+0}')

  awk -v s="$SID" -v r="$MAPD" -v cf="$CLEAN_FRAG" -v v="$N_VIR" -v c="$N_CTG" '
  BEGIN{
    clean=cf*2; if(clean<=0){print "ERR"; exit}
    pr=r/clean*100; pc=v/c*100
    printf "%s\t%d\t%d\t%d\t%d\t%.4f\t%.4f\t%s\n", s, clean, r, c, v, pr, pc, (pr>0? sprintf("%.3f", pc/pr):"NA")
  }' > "$ROW"

  echo "  clean reads $((CLEAN_FRAG*2))｜viral $N_VIR/$N_CTG｜mapped $MAPD"
  cat "$ROW"
done

echo
echo "=== 汇总 ==="
printf "sample\tclean_reads\treads_mapped\tcontigs\tviral_contigs\tpct_reads_unit\tpct_contig_unit\tratio_contig_over_reads\n" > "$BASE/unit_axis_alligator.tsv"
cat "$OUT"/W*.tsv "$OUT"/S*.tsv 2>/dev/null >> "$BASE/unit_axis_alligator.tsv" || true
column -t -s$'\t' "$BASE/unit_axis_alligator.tsv"
echo "=== 结束 $(date) ==="
touch "$OUT/.DONE"

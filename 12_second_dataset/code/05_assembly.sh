#!/bin/bash
# 第二数据集：去宿主 → MEGAHIT 组装 → geNomad 识别 → C4 汇总
# 参数与主项目 workflow/server_run_c.sh 完全一致，保证 C4 跨宿主可比
# 用法：nohup setsid bash 05_assembly.sh > logs/assembly.log 2>&1 &
set -uo pipefail
trap '' HUP TERM   # 会话断开时不被带走

BASE=/mnt/work/chicken
E=$HOME/biotools/envs/virome/bin
export PATH=$E:$PATH
FQ=$BASE/fastq
HR=$BASE/host_removed
AS=$BASE/assembly
MP=$BASE/mapping
OUT=$BASE/results
DB=$HOME/virome/db/genomad/genomad_db

mkdir -p "$HR" "$AS" "$MP" "$OUT"

SUM=$OUT/C4_summary.tsv
if [ ! -s "$SUM" ]; then
  printf "sample\treads_input\treads_clean\thost_removed_pct\tcontigs\tviral_contigs\tpct_viral_contigs\n" > "$SUM"
fi

SAMPLES="SRR6323088 SRR6323119 SRR6323120 SRR6323124 SRR6323125 SRR6323200"

echo "=== 组装流水线开始 $(date) ==="

for S in $SAMPLES; do
  echo
  echo "--- $S  $(date +%H:%M) ---"

  # ---------- 1. 去宿主（与主项目同一命令）
  if [ ! -s "$HR/$S.host_rm.fq.1.gz" ]; then
    echo "[$(date +%H:%M)] 去宿主"
    bowtie2 -x "$BASE/refs/chicken" \
      -1 "$FQ/${S}_1.fastq.gz" -2 "$FQ/${S}_2.fastq.gz" \
      -S /dev/null --un-conc-gz "$HR/$S.host_rm.fq.gz" --no-unal -p 8 \
      2> "$MP/$S.host.bowtie2.log"
  fi
  IN_FRAG=$(grep -m1 -oE "^[0-9]+ reads; of these" "$MP/$S.host.bowtie2.log" 2>/dev/null | grep -oE "^[0-9]+")
  IN_FRAG=${IN_FRAG:-0}
  CLEAN_FRAG=$(( $(gzip -dc "$HR/$S.host_rm.fq.1.gz" | wc -l) / 4 ))

  # ---------- 2. MEGAHIT（默认预设，与主项目一致）
  C="$AS/$S/$S.contigs.fa"
  if [ ! -s "$C" ]; then
    echo "[$(date +%H:%M)] MEGAHIT 开始"
    rm -rf "$AS/$S"
    megahit -1 "$HR/$S.host_rm.fq.1.gz" -2 "$HR/$S.host_rm.fq.2.gz" \
      -o "$AS/$S" --out-prefix "$S" \
      -t 6 --min-contig-len 1000 -m 0.5 > "$AS/$S.megahit.log" 2>&1
  fi
  if [ ! -s "$C" ]; then
    echo "[$(date +%H:%M)] 组装失败，跳过 $S"
    continue
  fi
  N_CTG=$(grep -c '^>' "$C")
  echo "  contigs: $N_CTG"

  # ---------- 3. geNomad end-to-end
  G="$AS/$S/genomad"
  if ! compgen -G "$G/*_summary/*_virus.fna" >/dev/null 2>&1; then
    echo "[$(date +%H:%M)] geNomad 开始（MMseqs2 搜库，较慢）"
    rm -rf "$G"
    genomad end-to-end "$C" "$G" "$DB" --threads 4 --splits 2 --cleanup > "$AS/$S.genomad.log" 2>&1
  fi

  VF=$(ls "$G"/*_summary/*_virus.fna 2>/dev/null | head -1)
  if [ -n "${VF:-}" ] && [ -s "$VF" ]; then
    N_VIR=$(grep -c '^>' "$VF")
  else
    N_VIR=0
  fi

  PCT=$(awk -v v="$N_VIR" -v t="$N_CTG" 'BEGIN{if(t>0) printf "%.3f", v/t*100; else print "NA"}')
  HR_PCT=$(awk -v i="$IN_FRAG" -v c="$CLEAN_FRAG" 'BEGIN{if(i>0) printf "%.3f", (i-c)/i*100; else print "NA"}')

  # 幂等：先删除该样本的旧行，避免重启续跑时重复追加
  awk -F'\t' -v s="$S" 'NR==1 || $1 != s' "$SUM" > "$SUM.tmp" && mv "$SUM.tmp" "$SUM"
  printf "%s\t%d\t%d\t%s\t%d\t%d\t%s\n" "$S" "$IN_FRAG" "$CLEAN_FRAG" "$HR_PCT" "$N_CTG" "$N_VIR" "$PCT" >> "$SUM"
  echo "  病毒 contigs: $N_VIR  ($PCT%)"
  tail -1 "$SUM"
done

echo
echo "=== 全部结束 $(date) ==="
column -t -s$'\t' "$SUM"
touch "$OUT/.C4_DONE"

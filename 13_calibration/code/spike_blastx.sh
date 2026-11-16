#!/usr/bin/env bash
# 9 个 spike 文库 × 2 个库 的 blastx；为校准实验准备 hits
set -uo pipefail
trap '' HUP TERM

E=$HOME/biotools/envs/virome/bin
export PATH=$E:$PATH
LIBDIR=/mnt/work/chicken/b1/libs
OUT=/mnt/work/chicken/refcheck/spike
mkdir -p "$OUT"

declare -A DBS=(
  [phrog]=/mnt/work/chicken/db/phrog/phrog
  [refseq]=/mnt/work/chicken/db/refseq/refseq
)

for lv in L0p001 L0p01 L0p05; do
  for rep in R1 R2 R3; do
    tag="${lv}_${rep}"
    # 记录 read 数（R1+R2）
    if [ ! -s "$OUT/$tag.nreads" ]; then
      n1=$(( $(gzip -dc "$LIBDIR/${tag}_1.fq.gz" | wc -l) / 4 ))
      n2=$(( $(gzip -dc "$LIBDIR/${tag}_2.fq.gz" | wc -l) / 4 ))
      echo $(( n1 + n2 )) > "$OUT/$tag.nreads"
      echo "$tag reads: $((n1+n2))"
    fi
    for lib in phrog refseq; do
      h="$OUT/$tag.$lib.hits"
      if [ -s "$h" ] && [ "$(stat -c%s "$h")" -gt 0 ]; then
        echo "  [skip] $tag $lib"
        continue
      fi
      echo "  [$(date +%H:%M)] $tag $lib"
      : > "$h"
      for m in 1 2; do
        diamond blastx -q "$LIBDIR/${tag}_${m}.fq.gz" -d "${DBS[$lib]}.dmnd" \
          --evalue 1e-5 --outfmt 6 qseqid stitle pident length \
          --threads 8 --max-target-seqs 1 >> "$h" 2>/dev/null
      done
      echo "    命中 $(wc -l < "$h")"
    done
  done
done
echo "[$(date +%H:%M)] BLASTX_DONE"

#!/usr/bin/env bash
# RefSeq viral 建库 + W1 测算
set -uo pipefail
trap '' HUP TERM

E=$HOME/biotools/envs/virome/bin
export PATH=$E:$PATH
D=/mnt/work/chicken/db/refseq
B=/mnt/work/chicken/refcheck
FAA=$D/refseq_viral.faa

echo "[$(date +%H:%M)] 开始"

if [ ! -s "$D/refseq.dmnd" ]; then
  echo "[$(date +%H:%M)] 建库"
  diamond makedb --in "$FAA" -d "$D/refseq" --threads 8 >/dev/null 2>&1 || { echo "建库失败"; exit 1; }
fi
echo "库大小: $(ls -lh "$D/refseq.dmnd" | awk '{print $5}')"

if [ ! -s "$B/refseq.hits.tsv" ]; then
  echo "[$(date +%H:%M)] blastx W1 sub.fq"
  diamond blastx -q "$B/sub.fq" -d "$D/refseq.dmnd" \
    --evalue 1e-5 --outfmt 6 qseqid stitle pident length \
    --threads 8 --max-target-seqs 1 > "$B/refseq.hits.tsv" 2>/dev/null || { echo "blastx 失败"; exit 1; }
fi
echo "命中行: $(wc -l < "$B/refseq.hits.tsv")"

echo "[$(date +%H:%M)] 统计"
python3 "$B/refseq_count.py"
echo "[$(date +%H:%M)] DONE"

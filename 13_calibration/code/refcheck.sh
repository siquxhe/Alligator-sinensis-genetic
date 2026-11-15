#!/bin/bash
# 判定性实验：项目"RVDB"(78万条) vs 自建噬菌体蛋白库(来自 19,789 vOTU)
# 同一批 reads 子集上各跑一次 DIAMOND blastx，比较"病毒命中率"
#
# 用法：setsid -f bash refcheck.sh > logs/refcheck.log 2>&1
set -uo pipefail
trap '' HUP TERM

E=$HOME/biotools/envs/virome/bin
export PATH=$E:$PATH
BASE=/mnt/work/chicken/refcheck
VOTU=/mnt/work/chicken/raw/representative_viral_19778_vOTUs.fasta
OLDDB=/mnt/work/chicken/db/RVDBv32.dmnd
NEWDB=$BASE/phage.dmnd
R1=/home/wuyanching/virome/data/SRR14300938.host_rm.1.fq.gz
mkdir -p "$BASE/logs" "$BASE/prot"
cd "$BASE" || exit 1

NREADS=2500000   # 取 250 万对 = 500 万条 reads 做对比

# ---------- 1. 切分 vOTU 并并行 Prodigal
if [ ! -s "$BASE/prot/all.faa" ]; then
  echo "[$(date +%H:%M)] 切分 vOTU"
  seqkit split2 -p 8 -O "$BASE/split" "$VOTU" > /dev/null 2>&1
  echo "[$(date +%H:%M)] 并行 Prodigal"
  for f in "$BASE"/split/*.fasta; do
    b=$(basename "$f" .fasta)
    ( prodigal -i "$f" -a "$BASE/prot/$b.faa" -p meta -q -o /dev/null ) &
  done
  wait
  cat "$BASE"/prot/*.faa > "$BASE/prot/all.faa"
fi
echo "蛋白数: $(grep -c '^>' "$BASE/prot/all.faa")"

# ---------- 2. 建库
if [ ! -s "$NEWDB" ]; then
  echo "[$(date +%H:%M)] diamond makedb"
  diamond makedb --in "$BASE/prot/all.faa" -d "$BASE/phage" --threads 8 > /dev/null 2>&1
fi

# ---------- 3. 取同一批 reads 子集
if [ ! -s "$BASE/sub.fq" ]; then
  gzip -dc "$R1" | head -$((NREADS * 4)) > "$BASE/sub.fq"
fi
echo "子集 reads: $(( $(wc -l < "$BASE/sub.fq") / 4 ))"

# ---------- 4. 两个库各跑一次
for db in old new; do
  D=$([ "$db" = old ] && echo "$OLDDB" || echo "$NEWDB")
  [ -s "$BASE/$db.hits.tsv" ] && { echo "[skip] $db"; continue; }
  echo "[$(date +%H:%M)] DIAMOND vs $db"
  diamond blastx -q "$BASE/sub.fq" -d "$D" \
    --evalue 1e-5 --outfmt 6 qseqid stitle pident length \
    --threads 8 --max-target-seqs 1 > "$BASE/$db.hits.tsv" 2> "$BASE/logs/$db.diamond.log"
done

# ---------- 5. 汇总（pident>=40, len>=30）
$HOME/biotools/envs/virome/bin/python3 - "$BASE" <<'PY'
import sys, re
from pathlib import Path
B=Path(sys.argv[1])
tot=int((B/"sub.fq").read_text().count("\n@")/4) if False else 0
n=0
with open(B/"sub.fq") as f:
    for i,l in enumerate(f):
        if i%4==0: n+=1
print(f"查询 reads: {n}")
for tag in ["old","new"]:
    hits=set()
    with open(B/f"{tag}.hits.tsv") as f:
        for line in f:
            p=line.rstrip().split("\t")
            if len(p)<4: continue
            try:
                if float(p[2])<40 or int(p[3])<30: continue
            except ValueError: continue
            hits.add(p[0])
    print(f"  {tag}: 命中 reads {len(hits)}  占比 {len(hits)/n*100:.3f}%")
PY
echo "=== 结束 $(date) ==="

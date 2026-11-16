#!/bin/bash
# 六样本全量 PHROG 测算：逐样本 diamond blastx + 分类统计
set -uo pipefail
trap '' HUP TERM
exec 9>/tmp/phrog6.lock
flock -n 9 || exit 0   # 防止 cron 重叠

E=$HOME/biotools/envs/virome/bin
export PATH=$E:$PATH
B=/mnt/work/chicken/refcheck
cd "$B" || exit 1
DB=/mnt/work/chicken/db/phrog/phrog.dmnd
DATA=/home/wuyanching/virome/data
OUT=$B/phrog_6samples.tsv

if [ ! -s "$OUT" ]; then
  printf "sample\treads\ttotal\tstrict\tstructural\treplication\tother\ttotal_over_strict\n" > "$OUT"
fi

for pair in W1:SRR14300938 W2:SRR14300939 W3:SRR14300942 S1:SRR14300940 S2:SRR14300941 S3:SRR14300943; do
  SID=${pair%%:*}
  RUN=${pair##*:}
  if grep -q "^${SID}	" "$OUT" 2>/dev/null; then
    echo "[skip] $SID"
    continue
  fi
  echo "[$(date +%H:%M)] $SID ($RUN)"

  : > "/tmp/$SID.hits"
  for m in 1 2; do
    gzip -dc "$DATA/$RUN.host_rm.$m.fq.gz" > "/tmp/$SID.$m.fq"
    diamond blastx -q "/tmp/$SID.$m.fq" -d "$DB" \
      --evalue 1e-5 --outfmt 6 qseqid stitle pident length \
      --threads 8 --max-target-seqs 1 >> "/tmp/$SID.hits" 2>/dev/null
    rm -f "/tmp/$SID.$m.fq"
  done

  $E/python3 "$B/phrog6_count.py" "$SID" "/tmp/$SID.hits" "$DATA/$RUN.host_rm.1.fq.gz" >> "$OUT"
  tail -1 "$OUT"
  rm -f "/tmp/$SID.hits"
done

echo "=== 结束 $(date) ==="
touch "$B/.PHROG6_DONE"

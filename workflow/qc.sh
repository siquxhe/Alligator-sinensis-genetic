#!/usr/bin/env bash
# ============================================================
# 质控脚本（fastp）—— 任务 B1
#   用法： bash workflow/qc.sh SRR14300938 [线程数]
#   输入： 00_raw/<RUN>_1.fastq.gz  +  _2.fastq.gz
#   输出： 01_qc/<RUN>.clean.1.fq.gz / .2.fq.gz
#          01_qc/<RUN>.fastp.json     （供 multiqc 汇总）
#          01_qc/<RUN>.fastp.html
# ============================================================
set -euo pipefail
source "$(dirname "$0")/env.sh"

RUN="${1:?用法: bash workflow/qc.sh <run_accession> [threads]}"
THREADS="${2:-8}"

R1="00_raw/${RUN}_1.fastq.gz"
R2="00_raw/${RUN}_2.fastq.gz"
for f in "$R1" "$R2"; do
  [ -f "$f" ] || { echo "缺少输入文件: $f" >&2; exit 1; }
done

mkdir -p 01_qc
OUT1="01_qc/${RUN}.clean.1.fq.gz"
OUT2="01_qc/${RUN}.clean.2.fq.gz"

echo "==> fastp 质控: $RUN (threads=$THREADS)"
# -q 20 : 合格碱基阈值 Q20
# -l 50 : 最短保留长度 50 bp
# 其余用 fastp 默认（自动识别接头、polyG 修剪、滑窗质量剪切）
"$FASTP" \
  -i "$R1" -I "$R2" \
  -o "$OUT1" -O "$OUT2" \
  -q 20 -l 50 -w "$THREADS" \
  -j "01_qc/${RUN}.fastp.json" \
  -h "01_qc/${RUN}.fastp.html" \
  2> "01_qc/${RUN}.fastp.log"

# 从 json 里取关键数字（供 M1 表用）
python - "$RUN" "01_qc/${RUN}.fastp.json" << 'PY'
import json, sys
run, path = sys.argv[1], sys.argv[2]
d = json.load(open(path, encoding='utf-8'))
s = d.get('summary', {})
bf, af = s.get('before_filtering', {}), s.get('after_filtering', {})
print(f"    原始 reads      : {bf.get('total_reads', 0):,}")
print(f"    质控后 reads    : {af.get('total_reads', 0):,}")
print(f"    通过率          : {af.get('total_reads',0)/max(bf.get('total_reads',1),1)*100:.2f}%")
print(f"    Q30 比例        : 前 {bf.get('q30_rate',0)*100:.2f}% → 后 {af.get('q30_rate',0)*100:.2f}%")
print(f"    重复率          : {d.get('duplication',{}).get('rate',0)*100:.2f}%")
PY

echo "==> 输出: $OUT1 / $OUT2"

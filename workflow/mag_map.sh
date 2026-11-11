#!/bin/bash
# MAG 第 1 步：reads 回贴各自组装，生成 MetaBAT2 所需深度文件
set -uo pipefail

B="$HOME/virome"
E="$HOME/biotools/envs/virome/bin"
export PATH="$E:$PATH"
T=${2:-8}

# 样本 -> run 的映射
declare -A RUN=(
  [W1]=SRR14300938 [W2]=SRR14300939 [W3]=SRR14300942
  [S1]=SRR14300940 [S2]=SRR14300941 [S3]=SRR14300943
)
ORDER="W1 W2 W3 S1 S2 S3"
[ -n "${1:-}" ] && ORDER="$1"

log() { echo "[$(date '+%F %T')] $*"; }

for s in $ORDER; do
  r=${RUN[$s]}
  C="$B/work/$s/megahit/$s.contigs.fa"
  M="$B/work/$s/mag"
  mkdir -p "$M"
  R1="$B/data/${r}.host_rm.1.fq.gz"
  R2="$B/data/${r}.host_rm.2.fq.gz"

  [ -s "$C" ] || { log "$s 缺 contigs，跳过"; continue; }
  [ -s "$R1" ] && [ -s "$R2" ] || { log "$s 缺 reads，跳过"; continue; }

  if [ -s "$M/$s.depth.txt" ]; then
    log "$s 深度文件已存在，跳过"
    continue
  fi

  log "===== $s ($r) 开始 ====="

  # 建索引
  if [ ! -s "$M/bt2.1.bt2" ] && [ ! -s "$M/bt2.1.bt2l" ]; then
    log "  建 bowtie2 索引"
    bowtie2-build --threads "$T" "$C" "$M/bt2" > "$M/bt2_build.log" 2>&1 || { log "  建索引失败"; continue; }
  fi

  # 回贴 + 排序
  log "  比对 + 排序"
  bowtie2 -p "$T" -x "$M/bt2" -1 "$R1" -2 "$R2" 2> "$M/bowtie2.log" \
    | samtools sort -@ "$T" -m 2G -o "$M/$s.bam" - 2> "$M/sort.log"
  [ -s "$M/$s.bam" ] || { log "  比对失败"; continue; }
  samtools index -@ "$T" "$M/$s.bam"

  # 深度
  log "  计算深度"
  jgi_summarize_bam_contig_depths --outputDepth "$M/$s.depth.txt" "$M/$s.bam" > "$M/depth.log" 2>&1

  # 清理中间产物（BAM 保留供后续复核会太大，删除）
  rm -f "$M/$s.bam" "$M/$s.bam.bai"

  aln=$(grep -oE "[0-9.]+% overall alignment rate" "$M/bowtie2.log" | tail -1)
  log "$s 完成（比对率 $aln）"
done

log "全部完成"

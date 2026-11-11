#!/usr/bin/env bash
# 分片下载 + 校验 + 合并（从头下载，避免稀疏空洞问题）
# 用法: bash dl_split.sh <file> <target_bytes> <subdir> <run> [N]
set -u
dl_file() {
  f=$1; target=$2; sub=$3; run=$4; N=${5:-16}
  url="http://ftp.sra.ebi.ac.uk/vol1/fastq/SRR143/${sub}/${run}/${f}.fastq.gz"
  seg=$(( (target + N - 1) / N ))
  rm -f "${f}.p"*
  echo "[$f] 目标 $target 分 $N 段 每段 $((seg/1048576))MB"
  for i in $(seq 0 $((N-1))); do
    from=$(( i*seg )); to=$(( from + seg - 1 ))
    [ "$to" -ge $((target-1)) ] && to=$((target-1))
    [ "$from" -gt "$to" ] && continue
    curl -s --noproxy '*' -r ${from}-${to} --retry 8 --retry-delay 3 \
      -o "${f}.p${i}" "$url" &
  done
  wait
  # 校验段大小
  ok=1
  for i in $(seq 0 $((N-1))); do
    from=$(( i*seg )); to=$(( from + seg - 1 ))
    [ "$to" -ge $((target-1)) ] && to=$((target-1))
    [ "$from" -gt "$to" ] && continue
    exp=$(( to - from + 1 ))
    act=$(stat -c%s "${f}.p${i}" 2>/dev/null || echo 0)
    if [ "$act" != "$exp" ]; then echo "[$f] 段$i 不符 $act/$exp"; ok=0; fi
  done
  if [ "$ok" = "1" ]; then
    rm -f "${f}.fastq.gz"
    for i in $(seq 0 $((N-1))); do
      [ -f "${f}.p${i}" ] && cat "${f}.p${i}" >> "${f}.fastq.gz" && rm "${f}.p${i}"
    done
    echo "[$f] ✅ 合并完成 $(stat -c%s "${f}.fastq.gz") / $target"
  else
    echo "[$f] ❌ 有段失败，保留分片"
  fi
}

dl_file SRR14300939_1 1895779621 039 SRR14300939 16
dl_file SRR14300939_2 1913504767 039 SRR14300939 16

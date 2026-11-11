#!/usr/bin/env bash
# 分片下载剩余 6 个文件（从头下载，16 段并行）
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

dl_file SRR14300942_1 1589045303 042 SRR14300942 16
dl_file SRR14300942_2 1811637676 042 SRR14300942 16
dl_file SRR14300943_1 1887390617 043 SRR14300943 16
dl_file SRR14300943_2 1932865041 043 SRR14300943 16
dl_file SRR14300941_1 1963930612 041 SRR14300941 16
dl_file SRR14300941_2 2008499415 041 SRR14300941 16

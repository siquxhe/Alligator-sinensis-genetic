#!/bin/bash
# 分两步在服务器建环境：先轻量 CLI 工具（conda），再 pip 装 geNomad / CheckV
# 避免 geNomad 的 conda 依赖把 CUDA/nccl 版 TensorFlow（4GB）拉进来
set -uo pipefail

export MAMBA_ROOT_PREFIX="$HOME/biotools/mamba"
MM="$HOME/biotools/micromamba"
ENVP="$HOME/biotools/envs/virome"
CB="https://conda.anaconda.org"

echo "===== 阶段 1：CLI 工具 $(date '+%T') ====="
"$MM" create -y -p "$ENVP" \
  -c "$CB/conda-forge" -c "$CB/bioconda" \
  --no-channel-priority \
  megahit seqkit samtools hmmer prodigal diamond bowtie2 cd-hit python=3.11 pip \
  2>&1 | tail -25

echo "阶段 1 结果："
for t in megahit seqkit samtools hmmsearch prodigal diamond bowtie2 cd-hit; do
  [ -x "$ENVP/bin/$t" ] && echo "  OK   $t" || echo "  MISS $t"
done

echo "===== 阶段 2：pip 装 geNomad / CheckV $(date '+%T') ====="
PIP="$ENVP/bin/pip"
"$PIP" install -q --upgrade pip 2>&1 | tail -2
"$PIP" install --index-url https://mirrors.aliyun.com/pypi/simple/ \
  --trusted-host mirrors.aliyun.com \
  genomad checkv 2>&1 | tail -8

echo "阶段 2 结果："
"$ENVP/bin/python" -c "import genomad, checkv; print('  genomad', genomad.__version__)" 2>&1 | tail -2
[ -x "$ENVP/bin/genomad" ] && echo "  OK   genomad CLI" || echo "  MISS genomad CLI"
echo "===== 全部结束 $(date '+%T') ====="

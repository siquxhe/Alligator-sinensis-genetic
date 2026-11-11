#!/bin/bash
E="$HOME/biotools/envs/virome/bin"
echo "=== 工具版本 ==="
for t in megahit genomad checkv seqkit samtools diamond bowtie2 cd-hit prodigal hmmsearch; do
  printf "  %-12s " "$t"
  if [ -x "$E/$t" ]; then "$E/$t" --version 2>&1 | head -1; else echo "缺失"; fi
done
echo "=== TensorFlow ==="
"$E/python" - <<'PY'
import tensorflow as tf
print("  TF", tf.__version__)
print("  GPUs:", tf.config.list_physical_devices("GPU"))
PY

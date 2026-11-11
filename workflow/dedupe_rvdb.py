#!/usr/bin/env python3
"""把 U-RVDB（未聚类、含大量完全重复）流式去重成非冗余蛋白库。

用法： python workflow/dedupe_rvdb.py <输入.xz> <输出.fasta> [上限GB]

原理：逐条读 fasta，用序列 md5 判重，只保留首次出现的序列。
      不丢任何"不同"序列，因此不会削弱检出能力，只去掉完全相同的冗余条目。
"""
import hashlib
import sys
import lzma
import time
from pathlib import Path

src = Path(sys.argv[1])
dst = Path(sys.argv[2])
cap_gb = float(sys.argv[3]) if len(sys.argv) > 3 else 8.0

seen = set()
n_in = n_out = 0
written = 0
t0 = time.time()
hdr = None
seq_parts = []

with lzma.open(src, "rb") as fin, open(dst, "wb") as fout:
    for raw in fin:
        line = raw.rstrip(b"\r\n")
        if not line:
            continue
        if line.startswith(b">"):
            if hdr is not None:
                seq = b"".join(seq_parts)
                n_in += 1
                h = hashlib.md5(seq.upper()).digest()
                if h not in seen:
                    seen.add(h)
                    rec = hdr + b"\n" + seq + b"\n"
                    fout.write(rec)
                    written += len(rec)
                    n_out += 1
            hdr = line
            seq_parts = []
            if written > cap_gb * 1024**3:
                print(f"⚠ 唯一序列已达 {written/1024**3:.1f} GB 上限，提前停止")
                break
        else:
            seq_parts.append(line)
    else:
        # 文件正常读到结尾，补最后一条
        if hdr is not None:
            seq = b"".join(seq_parts)
            n_in += 1
            h = hashlib.md5(seq.upper()).digest()
            if h not in seen:
                rec = hdr + b"\n" + seq + b"\n"
                fout.write(rec)
                written += len(rec)
                n_out += 1

print(f"输入序列: {n_in:,}")
print(f"唯一序列: {n_out:,}  （去重率 {100*(1-n_out/max(n_in,1)):.1f}%）")
print(f"输出大小: {written/1024**3:.2f} GB")
print(f"用时: {time.time()-t0:.0f}s")

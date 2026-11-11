#!/usr/bin/env python3
"""S1 技术核查：读段特征与组装特征是否异常

抽样每样本 20 万条 read，统计长度、GC、质量、N 比例；
并统计该样本组装 contigs 的 GC 分布与长度分布。
"""
import gzip
import random
from pathlib import Path

BASE = Path.home() / "virome"
SAMPLES = {"W1": "SRR14300938", "W2": "SRR14300939", "W3": "SRR14300942",
           "S1": "SRR14300940", "S2": "SRR14300941", "S3": "SRR14300943"}
N = 200_000
random.seed(1)

print(f"{'样本':<4}{'平均长度':>10}{'GC%':>8}{'平均Q':>8}{'N%':>7}{'contig数':>10}{'contig_GC%':>12}")
for sid, run in SAMPLES.items():
    fq = BASE / "data" / f"{run}.host_rm.1.fq.gz"
    tot_len = gc = n_base = 0
    qsum = 0
    n = 0
    with gzip.open(fq, "rt", errors="replace") as fh:
        while n < N:
            h = fh.readline()
            if not h:
                break
            seq = fh.readline().strip()
            fh.readline()
            qual = fh.readline().strip()
            if not seq:
                continue
            L = len(seq)
            tot_len += L
            gc += seq.count("G") + seq.count("C")
            n_base += seq.count("N")
            qsum += sum(ord(c) - 33 for c in qual)
            n += 1

    # contigs GC
    fa = BASE / "work" / sid / "megahit" / f"{sid}.contigs.fa"
    c_n = c_gc = c_len = 0
    if fa.exists():
        with open(fa, errors="replace") as fh:
            for line in fh:
                if line.startswith(">"):
                    c_n += 1
                else:
                    s = line.strip()
                    c_len += len(s)
                    c_gc += s.count("G") + s.count("C")

    print(f"{sid:<4}{tot_len/n:>10.0f}{gc/(tot_len-n_base)*100:>8.1f}"
          f"{qsum/tot_len:>8.1f}{n_base/tot_len*100:>7.2f}"
          f"{c_n:>10,}{c_gc/c_len*100 if c_len else 0:>12.1f}")

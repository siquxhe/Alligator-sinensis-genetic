#!/usr/bin/env python3
"""诊断 S1 病毒占比偏低的原因

三个角度：
  1) 长度分层：各样本在不同长度段的病毒占比。若 S1 全段都低 → 真实差异；
     若只在短 contig 段低 → 识别灵敏度问题。
  2) 深度承载：用 MEGAHIT header 的 multi（平均覆盖度）× 长度，估算"病毒 contigs
     承载了总测序深度的多少"。反映病毒 reads 的去向，不受 contig 计数影响。
  3) 组装构成：各样本 contigs 按长度分层的数量。
"""
import re
from pathlib import Path

BASE = Path.home() / "virome"
CAT = BASE / "results" / "viral_catalog.tsv"
SAMPLES = ["W1", "W2", "W3", "S1", "S2", "S3"]
BINS = [(1000, 2000), (2000, 5000), (5000, 10000), (10000, 10**9)]
BIN_NAMES = ["1-2kb", "2-5kb", "5-10kb", ">10kb"]
pat = re.compile(r"multi=([\d.]+) len=(\d+)")

vir = {}
with open(CAT, encoding="utf-8") as fh:
    next(fh)
    for line in fh:
        p = line.rstrip("\n").split("\t")
        vir.setdefault(p[0], set()).add(p[3].split("|")[0])

layered = {}
for sid in SAMPLES:
    fa = BASE / "work" / sid / "megahit" / f"{sid}.contigs.fa"
    if not fa.exists():
        continue
    tot = [0] * 4
    vt = [0] * 4
    cov_all = cov_vir = 0.0
    vset = vir.get(sid, set())
    with open(fa, errors="replace") as fh:
        for line in fh:
            if not line.startswith(">"):
                continue
            m = pat.search(line)
            if not m:
                continue
            c, L = float(m.group(1)), int(m.group(2))
            is_v = line[1:].split()[0] in vset
            cov_all += c * L
            if is_v:
                cov_vir += c * L
            for i, (lo, hi) in enumerate(BINS):
                if lo <= L < hi:
                    tot[i] += 1
                    if is_v:
                        vt[i] += 1
                    break
    layered[sid] = (tot, vt, cov_all, cov_vir)

print("=" * 76)
print("角度 1：长度分层的病毒占比（病毒数/该层总数）")
print("=" * 76)
print(f"{'样本':<5}" + "".join(f"{n:>16}" for n in BIN_NAMES))
for sid in SAMPLES:
    if sid not in layered:
        continue
    tot, vt, _, _ = layered[sid]
    cells = [f"{vt[i]}/{tot[i]}" if tot[i] else "-" for i in range(4)]
    print(f"{sid:<5}" + "".join(f"{c:>16}" for c in cells))

print()
print("=" * 76)
print("角度 2：病毒 contigs 承载的测序深度比例")
print("=" * 76)
print(f"{'样本':<5}{'总深度':>14}{'病毒深度':>14}{'深度占比':>10}{'contig占比':>12}")
for sid in SAMPLES:
    if sid not in layered:
        continue
    tot, vt, ca, cv = layered[sid]
    print(f"{sid:<5}{ca/1e9:>14.2f}{cv/1e9:>14.2f}"
          f"{cv/ca*100:>9.1f}%{sum(vt)/sum(tot)*100:>11.1f}%")

print()
print("=" * 76)
print("角度 3：组装构成（contigs 数按长度分层）")
print("=" * 76)
print(f"{'样本':<5}" + "".join(f"{n:>12}" for n in BIN_NAMES) + f"{'合计':>10}")
for sid in SAMPLES:
    if sid not in layered:
        continue
    tot = layered[sid][0]
    print(f"{sid:<5}" + "".join(f"{t:>12,}" for t in tot) + f"{sum(tot):>10,}")

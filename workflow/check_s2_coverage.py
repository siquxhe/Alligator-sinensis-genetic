#!/usr/bin/env python3
"""核查 S2 病毒 contig 数量异常：对比病毒 vs 全部 contig 的组装覆盖度

MEGAHIT 的 contig header 形如：
  >k141_12345 flag=1 multi=3.5000 len=1000
其中 multi 是该 contig 的平均覆盖度。若病毒 contig 的覆盖度显著低于全局，
说明它们多半是低丰度碎片，其"病毒比例高"更可能来自组装碎片化而非病毒富集。
"""
import re
import statistics as st
from pathlib import Path

BASE = Path.home() / "virome"
CAT = BASE / "results" / "viral_catalog.tsv"
pat = re.compile(r"multi=([\d.]+)")

for sid in ["S2", "W3", "S1"]:
    ids = set()
    with open(CAT, encoding="utf-8") as fh:
        next(fh)
        for line in fh:
            p = line.rstrip("\n").split("\t")
            if p[0] == sid:
                ids.add(p[3].split("|")[0])
    fa = BASE / "work" / sid / "megahit" / f"{sid}.contigs.fa"
    if not fa.exists():
        print(f"{sid}: 无组装文件")
        continue
    cov_all, cov_vir, len_vir = [], [], []
    with open(fa, errors="replace") as fh:
        cur_len, cur_cov, cur_id = 0, None, None
        for line in fh:
            if line.startswith(">"):
                if cur_id is not None and cur_cov is not None:
                    cov_all.append(cur_cov)
                    if cur_id in ids:
                        cov_vir.append(cur_cov)
                        len_vir.append(cur_len)
                cur_id = line[1:].split()[0]
                m = pat.search(line)
                cur_cov = float(m.group(1)) if m else None
                cur_len = 0
            elif cur_id is not None:
                cur_len += len(line.strip())
        if cur_id is not None and cur_cov is not None:
            cov_all.append(cur_cov)
            if cur_id in ids:
                cov_vir.append(cur_cov); len_vir.append(cur_len)

    def q(v, p):
        v = sorted(v)
        return v[int(len(v) * p)] if v else 0

    print(f"\n=== {sid} ===")
    print(f"  contigs: {len(cov_all):,}   病毒: {len(cov_vir):,} "
          f"({len(cov_vir)/len(cov_all)*100:.1f}%)")
    print(f"  覆盖度 全部: 中位 {st.median(cov_all):.1f}  四分位 {q(cov_all,.25):.1f}–{q(cov_all,.75):.1f}")
    if cov_vir:
        print(f"  覆盖度 病毒: 中位 {st.median(cov_vir):.1f}  四分位 {q(cov_vir,.25):.1f}–{q(cov_vir,.75):.1f}")
        low = sum(1 for c in cov_vir if c < 2)
        print(f"  病毒中 覆盖度<2 的比例: {low/len(cov_vir)*100:.0f}%")

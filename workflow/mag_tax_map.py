#!/usr/bin/env python3
"""把 MAG 的 blast 命中映射成 GTDB 谱系

输入
  work/mag_tax/mag_vs_host.tsv        blastn 结果（qseqid = MAG|contig）
  host_pred/db2/host_genomes.tsv      Genome(GCA) -> Repr_taxonomy
输出
  work/mag_tax/mag_taxonomy.tsv
"""
import re
import sys
from collections import Counter
from pathlib import Path

import pandas as pd

B = Path.home() / "virome"
W = B / "work" / "mag_tax"
HOST = B / "host_pred" / "db2" / "host_genomes.tsv"

# ---------- 1. blast 结果 ----------
hits = pd.read_csv(W / "mag_vs_host.tsv", sep="\t", header=None,
                   names=["q", "s", "pident", "length", "evalue", "bitscore"])
hits["mag"] = hits.q.str.split("|").str[0]
print(f"blast 命中 {len(hits)} 条，涉及 MAG {hits.mag.nunique()} 个")

# 从 sseqid 里抠 GC[AF]_xxxx.x
hits["gca"] = hits.s.str.extract(r"(GC[AF]_\d+\.\d)", expand=False)
print(f"  可提取到 GCA/GCF 的命中: {hits.gca.notna().sum()}（其余为 IMG 编号，无分类映射）")

# ---------- 2. 分类表（只读需要的行）----------
need = set(hits.gca.dropna())
print(f"  需查分类的基因组: {len(need)}")
tax = {}
with open(HOST, "r", encoding="utf-8", errors="replace") as fh:
    header = fh.readline()
    for line in fh:
        p = line.rstrip("\n").split("\t")
        if len(p) < 6:
            continue
        if p[0] in need:
            tax[p[0]] = p[5]
print(f"  匹配到分类: {len(tax)}")

hits["lineage"] = hits.gca.map(tax)
hit = hits.dropna(subset=["lineage"]).copy()
print(f"  有分类的命中: {len(hit)}")

LV = {"d": "domain", "p": "phylum", "c": "class",
      "o": "order", "f": "family", "g": "genus", "s": "species"}

rows = []
for mag, sub in hit.groupby("mag"):
    # 取每个命中基因组的最高 bitscore，按位次投票（越靠前权重越高）
    best = sub.sort_values("bitscore", ascending=False)
    ranks = {v: Counter() for v in LV.values()}
    for i, r in best.head(10).iterrows():
        for part in str(r.lineage).split(";"):
            part = part.strip()
            if len(part) > 3 and part[1:3] == "__":
                k = part[0]
                if k in LV:
                    ranks[LV[k]][part[3:]] += 1
    row = {"mag": mag, "n_hits": len(sub),
           "best_pident": round(best.pident.max(), 1)}
    for v in LV.values():
        row[v] = ranks[v].most_common(1)[0][0] if ranks[v] else ""
    # 一致度：该层级的得票占比
    row["genus_conf"] = (round(ranks["genus"].most_common(1)[0][1] / sum(ranks["genus"].values()), 2)
                         if ranks["genus"] else 0)
    rows.append(row)

out = pd.DataFrame(rows).sort_values("mag")
out.to_csv(W / "mag_taxonomy.tsv", sep="\t", index=False)
print(f"\n已写出 {W/'mag_taxonomy.tsv'}（{len(out)} 个 MAG）")
print(out[["mag", "phylum", "class", "order", "genus", "best_pident"]].head(15).to_string(index=False))
print("\n门分布：")
print(out.phylum.value_counts().to_string())

#!/usr/bin/env python3
"""CRISPR spacer 匹配结果的宿主注释

输入
  hq_vs_spacers.tsv   blastn 输出（已按 mismatch<=1、length>=30 过滤为 strict.tsv）
  db2/host_genomes.tsv  Genome(GCA/GCF) -> Repr_taxonomy
输出
  results/host_prediction.tsv   每个病毒 contig 的候选宿主
  results/host_summary.tsv      宿主分类分布
"""
import csv
import re
from collections import Counter, defaultdict
from pathlib import Path

BASE = Path.home() / "virome" / "host_pred"
RES = BASE / "results"
RES.mkdir(parents=True, exist_ok=True)

# ---- 宿主基因组注释表 ----
tax = {}
with open(BASE / "db2" / "host_genomes.tsv", encoding="utf-8", errors="replace") as fh:
    rd = csv.DictReader(fh, delimiter="\t")
    for r in rd:
        g = r.get("Genome", "").strip()
        t = r.get("Repr_taxonomy", "").strip()
        if g and t:
            tax[g] = t
print(f"宿主注释表: {len(tax):,} 个基因组")

# ---- 解析 blast 结果 ----
pat_gcf = re.compile(r"^(GC[AF]_\d+\.\d+)")
pat_img = re.compile(r"^(\d+)_")

rows = []
with open(BASE / "strict.tsv", encoding="utf-8") as fh:
    for line in fh:
        p = line.rstrip("\n").split("\t")
        if len(p) < 6:
            continue
        q, s, pid, aln, mm = p[0], p[1], float(p[2]), int(p[3]), int(p[4])
        head = s.split(":")[0]
        m1 = pat_gcf.match(head)
        m2 = pat_img.match(head)
        host_id = m1.group(1) if m1 else (f"IMG_{m2.group(1)}" if m2 else "NA")
        lineage = tax.get(host_id, "")
        # 提取门与属
        phy = fam = gen = ""
        if lineage:
            for part in lineage.split(";"):
                if part.startswith("p__"): phy = part[3:]
                elif part.startswith("f__"): fam = part[3:]
                elif part.startswith("g__"): gen = part[3:]
        rows.append({
            "virus_contig": q, "host_genome": host_id, "host_phylum": phy,
            "host_family": fam, "host_genus": gen,
            "identity": pid, "aln_len": aln, "mismatch": mm,
            "annotated": "yes" if lineage else "no",
        })

print(f"CRISPR 命中 {len(rows)} 条，涉及病毒 {len({r['virus_contig'] for r in rows})} 个")
ann = [r for r in rows if r["annotated"] == "yes"]
print(f"其中宿主可注释 {len(ann)} 条，涉及病毒 "
      f"{len({r['virus_contig'] for r in ann})} 个")

with open(RES / "host_prediction.tsv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0]) if rows else [], delimiter="\t")
    w.writeheader()
    w.writerows(rows)

# ---- 汇总 ----
per_virus = defaultdict(set)
for r in ann:
    if r["host_genus"]:
        per_virus[r["virus_contig"]].add(r["host_genus"])

genus_cnt = Counter()
phy_cnt = Counter()
for r in ann:
    if r["host_genus"]:
        genus_cnt[r["host_genus"]] += 1
    if r["host_phylum"]:
        phy_cnt[r["host_phylum"]] += 1

summ = []
summ.append(("CRISPR 严格命中（≤1 mismatch, ≥30bp）", len(rows), ""))
summ.append(("涉及病毒 contig", len({r['virus_contig'] for r in rows}), "占 202 条的 %.1f%%"
             % (len({r['virus_contig'] for r in rows}) / 202 * 100)))
summ.append(("其中宿主可注释的病毒", len({r['virus_contig'] for r in ann}), ""))
for g, n in genus_cnt.most_common(12):
    summ.append((f"宿主属: {g}", n, "spacer 条数"))
for p, n in phy_cnt.most_common(8):
    summ.append((f"宿主门: {p}", n, "spacer 条数"))

with open(RES / "host_summary.tsv", "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh, delimiter="\t")
    w.writerow(["指标", "数值", "说明"])
    w.writerows(summ)

print("\n=== 汇总 ===")
for k, v, note in summ:
    print(f"  {k:<44} {v:>6}  {note}")

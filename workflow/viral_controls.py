#!/usr/bin/env python3
"""病毒信号交叉验证 —— 汇总统计与随机期望

产出：
  09_tables/viral_controls_summary.tsv   三组对照（基线/重排reads/反转库）的命中率
  09_tables/viral_concordance_test.tsv   双端一致性的观测值 vs 独立随机期望

随机期望的算法：
  若 R1、R2 的物种归属彼此独立，则两端落到同一物种的概率为 Σ_i p_i·q_i
  （p_i、q_i 分别为两端在物种 i 上的命中频率）。观测值远高于该期望，
  说明两端的命中不是彼此独立的噪声，而是来自同一段真实同源序列。
"""
import csv
from collections import Counter
from pathlib import Path

PROJ = Path(__file__).resolve().parent.parent
CTL = PROJ / "04_viral" / "controls"
VDIR = PROJ / "04_viral"
TAB = PROJ / "09_tables"

N_QUERY = 4_000_000
RUNS = ["SRR14300938", "SRR14300939", "SRR14300942",
        "SRR14300940", "SRR14300941", "SRR14300943"]

# ---- 1) 三组对照命中率 ---------------------------------------------------
combos = [
    ("real reads x RVDBv32 (baseline)", CTL / "real_vs_real.tsv"),
    ("shuffled reads x RVDBv32 (null 1)", CTL / "shuf_vs_real.tsv"),
    ("real reads x reversed RVDB (null 2)", CTL / "real_vs_rev.tsv"),
]
rows = []
for label, f in combos:
    n = sum(1 for _ in open(f, encoding="utf-8", errors="replace")) if f.exists() else 0
    # 零命中时用 rule of three 给 95% 置信上界：3/N
    upper = 3 / N_QUERY * 100 if n == 0 else None
    rows.append({
        "comparison": label,
        "queries": N_QUERY,
        "hits": n,
        "hit_rate_pct": f"{n/N_QUERY*100:.4f}",
        "rate_95ci_upper_pct": f"{upper:.6f}" if upper else "",
    })

with open(TAB / "viral_controls_summary.tsv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0]), delimiter="\t")
    w.writeheader()
    w.writerows(rows)
print("=== 零假设对照 ===")
for r in rows:
    print(f"  {r['comparison']:<38} {r['hits']:>6} 条  {r['hit_rate_pct']}%")

# ---- 2) 双端一致性 vs 独立随机期望 --------------------------------------
import re

FA = PROJ / "00_db" / "RVDBv32_unique.fasta"
sps = {}
pat = re.compile(r"\[([^\]]+)\]\s*$")
with open(FA, encoding="utf-8", errors="replace") as fh:
    for line in fh:
        if not line.startswith(">"):
            continue
        hid = line[1:].strip()
        parts = hid.split("|")
        if len(parts) < 3:
            continue
        m = pat.search(hid)
        sps[parts[2]] = m.group(1) if m else "unclassified"


def species_counts(run, mate):
    c = Counter()
    f = VDIR / f"{run}.R{mate}.hits.tsv"
    with open(f, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            p = line.rstrip("\n").split("\t")
            if len(p) < 12:
                continue
            if float(p[2]) < 40 or int(p[3]) < 30:
                continue
            c[sps.get(p[1].split("|")[2] if "|" in p[1] else p[1], "unknown")] += 1
    return c


conc_rows = []
for run in RUNS:
    c1, c2 = species_counts(run, 1), species_counts(run, 2)
    n1, n2 = sum(c1.values()), sum(c2.values())
    # Σ p_i·q_i：两端独立时的同物种期望概率
    exp = sum(c1[k] / n1 * c2.get(k, 0) / n2 for k in c1) * 100
    # 观测值已在 viral_paired_concordance.tsv 中
    conc_rows.append({"run_accession": run,
                      "expected_same_taxon_pct": f"{exp:.2f}",
                      "_obs": None})

obs = {}
with open(TAB / "viral_paired_concordance.tsv", encoding="utf-8") as fh:
    for r in csv.DictReader(fh, delimiter="\t"):
        obs[r["run_accession"]] = float(r["same_taxon_pct"])

for r in conc_rows:
    o = obs[r["run_accession"]]
    e = float(r["expected_same_taxon_pct"])
    r["observed_same_taxon_pct"] = f"{o:.1f}"
    r["enrichment_fold"] = f"{o/e:.0f}" if e > 0 else "NA"
    del r["_obs"]

with open(TAB / "viral_concordance_test.tsv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=list(conc_rows[0]), delimiter="\t")
    w.writeheader()
    w.writerows(conc_rows)

print("\n=== 双端一致性：观测 vs 独立随机期望 ===")
for r in conc_rows:
    print(f"  {r['run_accession']}: 观测 {r['observed_same_taxon_pct']}%  "
          f"期望 {r['expected_same_taxon_pct']}%  "
          f"富集 {r['enrichment_fold']} 倍")

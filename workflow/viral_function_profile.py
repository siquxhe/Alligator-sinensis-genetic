#!/usr/bin/env python3
"""病毒命中按蛋白功能归类 —— 判断信号是"真病毒基因"还是"保守管家酶"

背景：RVDB 里大量巨型病毒（Mimiviridae/Megaviridae 等）携带从宿主"偷"来的代谢基因。
肠道细菌/宿主 reads 打到这些保守酶上也会被判为"病毒命中"，从而虚高病毒占比。
本脚本把命中按功能分箱，给出可解释的构成。

用法： python workflow/viral_function_profile.py
输出： 09_tables/viral_function_profile.tsv
"""
import csv
import re
from collections import Counter, defaultdict
from pathlib import Path

PROJ = Path(__file__).resolve().parent.parent
FA = PROJ / "00_db" / "RVDBv32_unique.fasta"
VDIR = PROJ / "04_viral"
TAB = PROJ / "09_tables"

RUNS = ["SRR14300938", "SRR14300939", "SRR14300942",
        "SRR14300940", "SRR14300941", "SRR14300943"]

# 分类规则：按顺序匹配，先命中者优先（结构 > 复制 > 代谢 > 假设蛋白）
RULES = [
    ("Structural / virion", [
        "capsid", "coat protein", "major head", "minor head", "tail", "portal",
        "terminase", "baseplate", "spike", "fiber", "virion", "envelope",
        "glycoprotein", "neck", "tape measure", "sheath", "prohead"]),
    ("Replication / transcription", [
        "polymerase", "replicase", "helicase", "primase", "integrase",
        "transposase", "nuclease", "ligase", "single-strand", "ssdna",
        "replication", "transcription", "rna-dependent", "rdrp", "polyprotein"]),
    ("Metabolic / housekeeping", [
        "synthase", "synthetase", "lyase", "dehydrogenase", "kinase",
        "reductase", "transferase", "hydrolase", "peptidase", "protease",
        "isomerase", "mutase", "phosphatase", "oxidase", "atpase",
        "transporter", "permease", "ribosomal", "trna", "lacz", "cad protein",
        "chaperone", "hsp", "glutamine", "asparagine", "thymidylate",
        "adenylosuccinate", "carbamoyl"]),
]
HYPOTHETICAL = ("hypothetical", "uncharacterized", "unknown protein",
                "putative protein", "orf")


def classify(d):
    low = d.lower()
    for cat, kws in RULES:
        if any(k in low for k in kws):
            return cat
    if any(k in low for k in HYPOTHETICAL):
        return "Hypothetical / uncharacterized"
    return "Other annotated"


# ---- 建 蛋白 accession → (描述, 物种) ------------------------------------
print("解析参考库注释 ...")
desc, sps = {}, {}
pat = re.compile(r"\[([^\]]+)\]\s*$")
with open(FA, encoding="utf-8", errors="replace") as fh:
    for line in fh:
        if not line.startswith(">"):
            continue
        hid = line[1:].strip()
        p = hid.split("|")
        if len(p) < 6:
            continue
        m = pat.search(hid)
        sps[p[2]] = m.group(1) if m else "unclassified"
        desc[p[2]] = pat.sub("", p[5]).strip() or "hypothetical protein"
print(f"  {len(desc):,} 条")

CATS = ["Structural / virion", "Replication / transcription",
        "Metabolic / housekeeping", "Hypothetical / uncharacterized",
        "Other annotated"]

per_sample = {}
cat_species = defaultdict(Counter)
for run in RUNS:
    c = Counter()
    for mate in (1, 2):
        with open(VDIR / f"{run}.R{mate}.hits.tsv", encoding="utf-8",
                  errors="replace") as fh:
            for line in fh:
                f = line.rstrip("\n").split("\t")
                if len(f) < 12 or float(f[2]) < 40 or int(f[3]) < 30:
                    continue
                sid = f[1].split("|")[2] if "|" in f[1] else f[1]
                d = desc.get(sid, "unknown")
                cat = classify(d)
                c[cat] += 1
                if cat in ("Structural / virion", "Replication / transcription"):
                    cat_species[cat][sps.get(sid, "unknown")] += 1
    per_sample[run] = c
    tot = sum(c.values())
    print(f"{run}: {tot:,} 条命中  " +
          "  ".join(f"{k.split('/')[0].strip()[:12]}={v/tot*100:.1f}%"
                    for k, v in c.most_common()))

rows = []
for run in RUNS:
    c = per_sample[run]
    tot = sum(c.values())
    row = {"run_accession": run, "total_hits": tot}
    for cat in CATS:
        row[cat] = f"{c.get(cat, 0)/tot*100:.1f}"
    vir = (c.get("Structural / virion", 0) + c.get("Replication / transcription", 0))
    row["viral_specific_pct"] = f"{vir/tot*100:.1f}"
    rows.append(row)

# 合并行
tot_all = sum(sum(per_sample[r].values()) for r in RUNS)
merged = {"run_accession": "ALL"}
for cat in CATS:
    merged[cat] = f"{sum(per_sample[r].get(cat,0) for r in RUNS)/tot_all*100:.1f}"
vir_all = sum(per_sample[r].get("Structural / virion", 0) +
              per_sample[r].get("Replication / transcription", 0) for r in RUNS)
merged["viral_specific_pct"] = f"{vir_all/tot_all*100:.1f}"
merged["total_hits"] = tot_all
rows.append(merged)

fields = ["run_accession", "total_hits"] + CATS + ["viral_specific_pct"]
with open(TAB / "viral_function_profile.tsv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=fields, delimiter="\t")
    w.writeheader()
    w.writerows(rows)

print("\n=== 功能构成（%）===")
print(f"{'sample':<12}{'struct':>8}{'repl':>8}{'metab':>8}{'hypo':>8}{'other':>8}{'真病毒':>8}")
for r in rows:
    print(f"{r['run_accession']:<12}{r['Structural / virion']:>8}"
          f"{r['Replication / transcription']:>8}"
          f"{r['Metabolic / housekeeping']:>8}"
          f"{r['Hypothetical / uncharacterized']:>8}"
          f"{r['Other annotated']:>8}{r['viral_specific_pct']:>8}")

print("\n=== 结构/复制类命中主要指向哪些物种 ===")
for cat, cnt in cat_species.items():
    tot = sum(cnt.values())
    print(f"  [{cat}] {tot:,} 条")
    for sp, n in cnt.most_common(5):
        print(f"     {n:>6} ({n/tot*100:>4.1f}%)  {sp[:60]}")

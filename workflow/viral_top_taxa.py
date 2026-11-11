#!/usr/bin/env python3
"""统计各样本命中的病毒分类（从 RVDB 蛋白头解析物种名）

用法： python workflow/viral_top_taxa.py

输入： 00_db/RVDBv32_unique.fasta（构建 sseqid → 描述 映射）
       04_viral/<RUN>.R{1,2}.hits.tsv
输出： 09_tables/viral_top_taxa.tsv（每样本 Top 15）
"""
import csv
import re
from collections import Counter, defaultdict
from pathlib import Path

PROJ = Path(__file__).resolve().parent.parent
FA = PROJ / "00_db" / "RVDBv32_unique.fasta"
VDIR = PROJ / "04_viral"
OUT = PROJ / "09_tables" / "viral_top_taxa.tsv"
MIN_LEN, MIN_PIDENT = 30, 40.0

# 1) 建 蛋白accession → species 映射
#    头格式：>acc|GENBANK|<p_acc>|GENBANK|<n_acc>|<descr> [Species name]
#    注意：DIAMOND 的 sseqid 会被空格截断，物种名只存在于完整表头里，必须用 p_acc 关联。
sps = {}
pat = re.compile(r"\[([^\]]+)\]\s*$")
with open(FA, "r", encoding="utf-8", errors="replace") as fh:
    for line in fh:
        if not line.startswith(">"):
            continue
        hid = line[1:].strip()
        parts = hid.split("|")
        if len(parts) < 3:
            continue
        key = parts[2]
        m = pat.search(hid)
        sps[key] = m.group(1) if m else "unclassified"

print(f"参考库物种映射: {len(sps):,} 条")

rows = []
counts = []
for hits in sorted(VDIR.glob("*.R1.hits.tsv")):
    run = hits.name.split(".")[0]
    per_species = defaultdict(set)   # species -> set(read ids)
    total_reads_hit = 0
    for mate in (1, 2):
        f = VDIR / f"{run}.R{mate}.hits.tsv"
        if not f.exists():
            continue
        with open(f, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                p = line.rstrip("\n").split("\t")
                if len(p) < 12:
                    continue
                q, sid, pident, alen = p[0], p[1], float(p[2]), int(p[3])
                if alen < MIN_LEN or pident < MIN_PIDENT:
                    continue
                sp = sps.get(sid.split("|")[2] if "|" in sid else sid, "unknown")
                per_species[sp].add(q)
    tot = sum(len(v) for v in per_species.values())
    counts.append({"run_accession": run, "viral_reads": tot,
                   "n_species": len(per_species)})
    top = sorted(per_species.items(), key=lambda kv: -len(kv[1]))[:15]
    for rank, (sp, reads) in enumerate(top, 1):
        rows.append({
            "run_accession": run, "rank": rank, "species": sp,
            "reads": len(reads),
            "pct_of_viral_reads": f"{(len(reads)/tot*100 if tot else 0):.1f}",
        })
    print(f"{run}: 命中 {tot:,} 条 reads，涉及 {len(per_species):,} 个物种")

with open(OUT, "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=["run_accession", "rank", "species", "reads", "pct_of_viral_reads"],
                       delimiter="\t")
    w.writeheader()
    w.writerows(rows)
print(f"\n已写出 {OUT}")

# 每样本病毒种数（供作图引用，避免在图里写死数字）
CNT = PROJ / "09_tables" / "viral_species_counts.tsv"
with open(CNT, "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=["run_accession", "viral_reads", "n_species"],
                       delimiter="\t")
    w.writeheader()
    w.writerows(counts)
print(f"已写出 {CNT}")

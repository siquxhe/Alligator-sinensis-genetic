#!/usr/bin/env python3
"""汇总 6 个样本的 C 阶段结果，并接上病毒 contig 的分类

输入（服务器 ~/virome/work/<SID>/）
  megahit/<SID>.contigs.fa
  genomad/<SID>.contigs_summary/<SID>.contigs_virus_summary.tsv   ← 含 taxonomy 列
  checkv/quality_summary.tsv

输出（~/virome/results/）
  all_c_summary.tsv        每样本一行，正文表格用
  viral_catalog.tsv        每条病毒 contig 一行（含分类与完整性）
  taxonomy_by_sample.tsv   样本 × 分类纲 的计数（含中高质量数）
  hq_genomes.tsv           仅 Complete/High/Medium 的候选基因组
"""
import csv
from collections import Counter, defaultdict
from pathlib import Path

BASE = Path.home() / "virome"
WORK = BASE / "work"
OUT = BASE / "results"
OUT.mkdir(exist_ok=True)

SAMPLES = [
    ("W1", "SRR14300938", "winter"),
    ("W2", "SRR14300939", "winter"),
    ("W3", "SRR14300942", "winter"),
    ("S1", "SRR14300940", "summer"),
    ("S2", "SRR14300941", "summer"),
    ("S3", "SRR14300943", "summer"),
]
HQ = {"Complete", "High-quality", "Medium-quality"}


def fasta_stats(path):
    n = total = cur = 0
    lens = []
    with open(path, "r", errors="replace") as fh:
        for line in fh:
            if line.startswith(">"):
                if n:
                    lens.append(cur); total += cur
                n += 1; cur = 0
            else:
                cur += len(line.strip())
    if n:
        lens.append(cur); total += cur
    if not lens:
        return 0, 0, 0
    lens.sort(reverse=True)
    acc = 0
    for L in lens:
        acc += L
        if acc >= total / 2:
            return n, total, L
    return n, total, lens[-1]


def read_tsv(p):
    if not p.exists():
        return []
    with open(p, encoding="utf-8", errors="replace") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def split_lineage(tax):
    """Viruses;Realm;Kingdom;Phylum;Class;Order;Family;Genus;Species"""
    if not tax or tax.lower().startswith("unclassified"):
        return {"class": "Unclassified", "family": "", "genus": ""}
    p = [x.strip() for x in tax.split(";")]
    g = lambda i: p[i] if i < len(p) else ""
    return {"class": g(4) or "Unclassified", "family": g(6), "genus": g(7)}


summary_rows, catalog_rows, tax_rows = [], [], []
tax_counter = defaultdict(Counter)      # (sid, class) -> n
tax_hq = defaultdict(Counter)           # (sid, class) -> n_hq

for sid, run, season in SAMPLES:
    w = WORK / sid
    contigs = w / "megahit" / f"{sid}.contigs.fa"
    if not contigs.exists():
        print(f"[跳过] {sid}: 组装未完成")
        continue

    n_ctg, tot_ctg, n50 = fasta_stats(contigs)
    vs = read_tsv(w / "genomad" / f"{sid}.contigs_summary" / f"{sid}.contigs_virus_summary.tsv")
    qc = read_tsv(w / "checkv" / "quality_summary.tsv")
    qmap = {r["contig_id"]: r for r in qc}

    n_vir = len(vs)
    vir_len = sum(int(float(r["length"])) for r in vs) if vs else 0
    qual = Counter()
    n_hq = 0

    for r in vs:
        cid = r["seq_name"]
        q = qmap.get(cid, {})
        quality = q.get("checkv_quality", "Not-determined")
        qual[quality] += 1
        if quality in HQ:
            n_hq += 1
        lin = split_lineage(r.get("taxonomy", ""))
        tax_counter[sid][lin["class"]] += 1
        if quality in HQ:
            tax_hq[sid][lin["class"]] += 1
        catalog_rows.append({
            "sample_id": sid, "run_accession": run, "season": season,
            "contig_id": cid,
            "length": int(float(r["length"])),
            "virus_score": r.get("virus_score", ""),
            "checkv_quality": quality,
            "completeness": q.get("completeness", ""),
            "contamination": q.get("contamination", ""),
            "class": lin["class"], "family": lin["family"],
            "taxonomy": r.get("taxonomy", ""),
        })

    top_class, top_n = ("", 0)
    if tax_counter[sid]:
        top_class, top_n = tax_counter[sid].most_common(1)[0]

    summary_rows.append({
        "sample_id": sid, "run_accession": run, "season": season,
        "contigs_n": n_ctg,
        "contigs_total_Mb": f"{tot_ctg/1e6:.1f}",
        "contigs_N50_kb": f"{n50/1e3:.1f}",
        "viral_contigs_n": n_vir,
        "viral_total_Mb": f"{vir_len/1e6:.2f}",
        "viral_pct_of_contigs": f"{(n_vir/n_ctg*100 if n_ctg else 0):.2f}",
        "checkv_Complete": qual.get("Complete", 0),
        "checkv_High": qual.get("High-quality", 0),
        "checkv_Medium": qual.get("Medium-quality", 0),
        "checkv_Low": qual.get("Low-quality", 0),
        "checkv_NotDetermined": qual.get("Not-determined", 0),
        "hq_genomes_n": n_hq,
        "hq_pct_of_viral": f"{(n_hq/n_vir*100 if n_vir else 0):.1f}",
        "top_class": top_class,
        "top_class_pct": f"{(top_n/n_vir*100 if n_vir else 0):.1f}",
    })
    print(f"{sid}: contigs={n_ctg:,} 病毒={n_vir} 中高质量={n_hq} 主导={top_class}")

# ---- 写表 ----
def write(path, rows, fields=None):
    if not rows:
        print(f"[空] {path.name}")
        return
    fields = fields or list(rows[0])
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, delimiter="\t")
        w.writeheader(); w.writerows(rows)
    print(f"已写出 {path}")


write(OUT / "all_c_summary.tsv", summary_rows)
write(OUT / "viral_catalog.tsv", catalog_rows)

# 分类构成表：样本 × 纲
for sid, counter in tax_counter.items():
    for cls, n in counter.items():
        tax_rows.append({
            "sample_id": sid, "class": cls,
            "n_contigs": n, "pct_of_viral": "",
            "n_hq": tax_hq[sid].get(cls, 0),
        })
tot_by = Counter()
for sid, counter in tax_counter.items():
    tot_by[sid] = sum(counter.values())
for r in tax_rows:
    t = tot_by[r["sample_id"]]
    r["pct_of_viral"] = f"{(r['n_contigs']/t*100 if t else 0):.1f}"
tax_rows.sort(key=lambda r: (r["sample_id"], -r["n_contigs"]))
write(OUT / "taxonomy_by_sample.tsv", tax_rows)

# 中高质量基因组
hq = [r for r in catalog_rows if r["checkv_quality"] in HQ]
hq.sort(key=lambda r: (r["sample_id"], -float(r["completeness"] or 0)))
write(OUT / "hq_genomes.tsv", hq)

print(f"\n共 {len(catalog_rows)} 条病毒 contigs，其中中高质量 {len(hq)} 条")

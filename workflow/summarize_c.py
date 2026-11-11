#!/usr/bin/env python3
"""汇总单个样本的 C 阶段结果 → c_stage_summary.tsv

用法： python summarize_c.py <SID> <RUN> <contigs.fa> <virus.fna> <checkv_quality.tsv>

统计项：
  - contigs 总数 / N50 / 总长度
  - 病毒 contigs 数
  - CheckV 质量分级构成（完整/高质量/中等/低质量/未确定）
  - 最高质量病毒 contig（长度、完整性、可能的分类）
"""
import csv
import sys
from pathlib import Path


def fasta_stats(path):
    """按记录统计（多行序列需累积到下一个 '>' 才算一条）"""
    n = 0
    total = 0
    lens = []
    cur = 0
    with open(path, "r", errors="replace") as fh:
        for line in fh:
            if line.startswith(">"):
                if n:
                    lens.append(cur)
                    total += cur
                n += 1
                cur = 0
            else:
                cur += len(line.strip())
    if n:
        lens.append(cur)
        total += cur
    if not lens:
        return 0, 0, 0
    lens.sort(reverse=True)
    half = total / 2
    acc = 0
    n50 = 0
    for L in lens:
        acc += L
        if acc >= half:
            n50 = L
            break
    return n, total, n50


sid, run, contigs, virus, qf = sys.argv[1:6]

n_ctg, tot_ctg, n50 = fasta_stats(contigs)
n_vir, tot_vir, n50_vir = fasta_stats(virus) if Path(virus).exists() else (0, 0, 0)

qual = {"Complete": 0, "High-quality": 0, "Medium-quality": 0,
        "Low-quality": 0, "Not-determined": 0}
best = ("", 0, "", "")
if Path(qf).exists():
    with open(qf, encoding="utf-8", errors="replace") as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            q = r.get("checkv_quality", "Not-determined")
            qual[q] = qual.get(q, 0) + 1
            try:
                comp = float(r.get("completeness", 0) or 0)
            except ValueError:
                comp = 0.0
            if comp > best[1]:
                best = (r.get("contig_id", ""), comp,
                        r.get("contig_length", ""), r.get("taxonomy", "") or "")

row = {
    "sample_id": sid,
    "run_accession": run,
    "contigs_n": n_ctg,
    "contigs_total_Mb": f"{tot_ctg/1e6:.1f}",
    "contigs_N50_kb": f"{n50/1e3:.1f}",
    "viral_contigs_n": n_vir,
    "viral_total_Mb": f"{tot_vir/1e6:.2f}",
    "viral_N50_kb": f"{n50_vir/1e3:.1f}",
    "viral_frac_of_contigs_pct": f"{(n_vir/n_ctg*100 if n_ctg else 0):.2f}",
    "checkv_Complete": qual.get("Complete", 0),
    "checkv_High": qual.get("High-quality", 0),
    "checkv_Medium": qual.get("Medium-quality", 0),
    "checkv_Low": qual.get("Low-quality", 0),
    "checkv_Undetermined": qual.get("Not-determined", 0),
    "best_contig": best[0],
    "best_completeness": f"{best[1]:.1f}",
    "best_length": best[2],
    "best_taxonomy": best[3],
}

out = Path(contigs).parent.parent / "c_stage_summary.tsv"
with open(out, "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=list(row), delimiter="\t")
    w.writeheader()
    w.writerow(row)

print(f"  汇总 → {out}")
for k, v in row.items():
    print(f"    {k:<28} {v}")

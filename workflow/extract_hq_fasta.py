#!/usr/bin/env python3
"""从各样本的 geNomad 输出中提取 202 条中高质量基因组的序列

输出：~/virome/host_pred/input/hq_genomes.fna（每条 header 带样本与质量标签）
"""
import csv
from pathlib import Path

BASE = Path.home() / "virome"
OUT = BASE / "host_pred" / "input"
OUT.mkdir(parents=True, exist_ok=True)

rows = []
with open(BASE / "05_c_stage" / "hq_genomes_with_abundance.tsv", encoding="utf-8") as fh:
    for r in csv.DictReader(fh, delimiter="\t"):
        rows.append(r)

by_sample = {}
for r in rows:
    by_sample.setdefault(r["sample_id"], []).append(r)

written = 0
missing = []
with open(OUT / "hq_genomes.fna", "w") as fo:
    for sid, recs in by_sample.items():
        want = {r["contig_id"]: r for r in recs}
        fna = BASE / "work" / sid / "genomad" / f"{sid}.contigs_summary" / f"{sid}.contigs_virus.fna"
        if not fna.exists():
            print(f"[缺] {fna}")
            continue
        cur_id, cur_seq = None, []
        with open(fna, errors="replace") as fh:
            for line in fh:
                if line.startswith(">"):
                    if cur_id is not None and cur_id in want:
                        r = want[cur_id]
                        fo.write(f">{sid}|{cur_id}|{r['checkv_quality']}|"
                                 f"{r['completeness']}|{r['rpkm']}\n")
                        fo.write("".join(cur_seq) + "\n")
                        written += 1
                    cur_id = line[1:].split()[0]
                    cur_seq = []
                else:
                    cur_seq.append(line.strip())
            if cur_id is not None and cur_id in want:
                r = want[cur_id]
                fo.write(f">{sid}|{cur_id}|{r['checkv_quality']}|"
                         f"{r['completeness']}|{r['rpkm']}\n")
                fo.write("".join(cur_seq) + "\n")
                written += 1

print(f"提取 {written} / {len(rows)} 条")
if written < len(rows):
    print("注意：部分 contig_id 在 fasta 中未找到（可能是 provirus 子序列命名差异）")

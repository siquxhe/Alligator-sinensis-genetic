#!/usr/bin/env python3
"""汇总单个样本的病毒 reads 统计（B4/B5）

用法： python workflow/summarize_viral.py <RUN>

输入： 04_viral/<RUN>.R{1,2}.hits.tsv   DIAMOND outfmt 6
       04_viral/.<RUN>.R{1,2}.nreads   该 mate 筛查的 reads 数
输出： 04_viral/<RUN>.viral_summary.tsv
       09_tables/viral_reads_summary.tsv（追加/更新该 run）
"""
import csv
import sys
from pathlib import Path

PROJ = Path(__file__).resolve().parent.parent
VDIR = PROJ / "04_viral"
AGG = PROJ / "09_tables" / "viral_reads_summary.tsv"

MIN_LEN = 30      # 比对长度（aa）
MIN_PIDENT = 40.0  # 一致性 %

run = sys.argv[1]


def load_mate(mate):
    hits_f = VDIR / f"{run}.R{mate}.hits.tsv"
    cnt_f = VDIR / f".{run}.R{mate}.nreads"
    n_reads = int(float(cnt_f.read_text().strip())) if cnt_f.exists() else 0
    raw = 0
    passed = set()
    if hits_f.exists():
        with open(hits_f, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                parts = line.rstrip("\n").split("\t")
                if len(parts) < 12:
                    continue
                raw += 1
                q, pident, alen = parts[0], float(parts[2]), int(parts[3])
                if alen >= MIN_LEN and pident >= MIN_PIDENT:
                    passed.add(q)
    return n_reads, raw, len(passed), passed


n1, raw1, pass1, set1 = load_mate(1)
n2, raw2, pass2, set2 = load_mate(2)

# 配对层面的命中：同一 read id 在 R1/R2 命中都算该 read；总数按 read 计
total_reads = n1 + n2
total_hits = pass1 + pass2
pct = (total_hits / total_reads * 100) if total_reads else 0.0

row = {
    "run_accession": run,
    "reads_R1": n1, "hits_R1_raw": raw1, "hits_R1_pass": pass1,
    "pct_R1": f"{(pass1/n1*100 if n1 else 0):.3f}",
    "reads_R2": n2, "hits_R2_raw": raw2, "hits_R2_pass": pass2,
    "pct_R2": f"{(pass2/n2*100 if n2 else 0):.3f}",
    "reads_total": total_reads,
    "hits_total": total_hits,
    "viral_reads_pct": f"{pct:.3f}",
    "filter": f"len>={MIN_LEN}aa;pident>={MIN_PIDENT}%;e<=1e-5;qc>=50%",
}

# 单样本汇总
out = VDIR / f"{run}.viral_summary.tsv"
with open(out, "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=list(row), delimiter="\t")
    w.writeheader()
    w.writerow(row)

# 追加/更新总表
rows = []
if AGG.exists():
    with open(AGG, encoding="utf-8") as fh:
        rows = [r for r in csv.DictReader(fh, delimiter="\t") if r["run_accession"] != run]
rows.append(row)
rows.sort(key=lambda r: r["run_accession"])
with open(AGG, "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=list(row), delimiter="\t")
    w.writeheader()
    w.writerows(rows)

print(f"    reads: {total_reads:,}  病毒 reads: {total_hits:,}  → {pct:.3f}%")
print(f"    R1 {pass1:,}/{n1:,}  R2 {pass2:,}/{n2:,}")

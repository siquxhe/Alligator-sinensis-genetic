#!/usr/bin/env python3
"""汇总 vOTU 丰度矩阵

输入（~/virome/work/votu/abund/）
  <SID>.counts.tsv   代表序列 id \t read 数
  <SID>.nfrag        bowtie2 报告的 fragment 数（paired 模式，×2 = 总 reads）

输出（~/virome/results/）
  votu_abundance_counts.tsv   vOTU × 样本 原始 read 数
  votu_abundance_rpkm.tsv     vOTU × 样本 RPKM
  abundance_summary.tsv       每样本：总 reads、病毒 reads、映射率
"""
import csv
from collections import defaultdict
from pathlib import Path

BASE = Path.home() / "virome"
A = BASE / "work" / "votu" / "abund"
RES = BASE / "results"
RES.mkdir(exist_ok=True)
SAMPLES = ["W1", "W2", "W3", "S1", "S2", "S3"]

# ---- 代表序列 → vOTU 映射 ----
rep2votu = {}
lens = {}
with open(RES / "votu_members.tsv", encoding="utf-8") as fh:
    for r in csv.DictReader(fh, delimiter="\t"):
        key = f"{r['sample_id']}__{r['contig_id']}"
        if r["is_representative"] == "yes":
            rep2votu[key] = r["votu_id"]
            lens[r["votu_id"]] = int(r["length"])
print(f"代表序列 {len(rep2votu):,} 条")

# ---- 读计数 ----
counts = defaultdict(dict)      # votu -> {sample: n}
totals = {}
for sid in SAMPLES:
    cf = A / f"{sid}.counts.tsv"
    nf = A / f"{sid}.nfrag"
    if not cf.exists():
        print(f"[跳过] {sid}")
        continue
    frag = int(nf.read_text().strip()) if nf.exists() else 0
    totals[sid] = frag * 2          # 总 reads（双端）
    miss = 0
    unmapped_id = 0
    with open(cf, encoding="utf-8") as fh:
        for line in fh:
            p = line.rstrip("\n").split("\t")
            if len(p) < 2:
                continue
            sid_seq, n = p[0], int(p[1])
            v = rep2votu.get(sid_seq)
            if v is None:
                miss += 1
                continue
            counts[v][sid] = counts[v].get(sid, 0) + n
    print(f"{sid}: 总 reads {totals[sid]:,}，命中 vOTU {len([1 for v in counts if sid in counts[v]]):,} 个"
          + (f"，未映射序列 {miss}" if miss else ""))

# ---- 矩阵 ----
all_votu = sorted(counts)
rows = []
for v in all_votu:
    d = counts[v]
    rows.append({"votu_id": v, "length": lens.get(v, 0),
                 **{s: d.get(s, 0) for s in SAMPLES}})

def write(path, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]), delimiter="\t")
        w.writeheader()
        w.writerows(rows)
    print(f"已写出 {path}")

write(RES / "votu_abundance_counts.tsv", rows)

# ---- RPKM ----
rpk_rows = []
for r in rows:
    L_kb = r["length"] / 1000 if r["length"] else 0
    rec = {"votu_id": r["votu_id"], "length": r["length"]}
    for s in SAMPLES:
        M = totals.get(s, 0) / 1e6
        rec[s] = round(r[s] / (L_kb * M), 4) if (L_kb and M) else 0
    rpk_rows.append(rec)
write(RES / "votu_abundance_rpkm.tsv", rpk_rows)

# ---- 每样本汇总 ----
summ = []
for s in SAMPLES:
    if s not in totals:
        continue
    n_reads = sum(r[s] for r in rows)
    tot = totals[s]
    detected = sum(1 for r in rows if r[s] > 0)
    # 检出定义：RPKM ≥ 1
    rp_det = sum(1 for r in rpk_rows if r[s] >= 1)
    summ.append({
        "sample_id": s,
        "total_reads": tot,
        "viral_reads": n_reads,
        "viral_reads_pct": f"{n_reads/tot*100:.2f}" if tot else "0",
        "votu_detected_any": detected,
        "votu_rpkm_ge1": rp_det,
        "total_rpkm": f"{sum(r[s] for r in rpk_rows):.0f}",
    })

with open(RES / "abundance_summary.tsv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=list(summ[0]), delimiter="\t")
    w.writeheader()
    w.writerows(summ)

print("\n=== 每样本病毒 reads 占比 ===")
print(f"{'样本':<4}{'总reads':>14}{'病毒reads':>12}{'占比':>8}{'RPKM≥1的vOTU':>14}")
for r in summ:
    print(f"{r['sample_id']:<4}{r['total_reads']:>14,}{r['viral_reads']:>12,}"
          f"{r['viral_reads_pct']:>7}%{r['votu_rpkm_ge1']:>14,}")

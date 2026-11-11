#!/usr/bin/env python3
"""病毒信号交叉验证 —— 基于已有 DIAMOND 命中结果的严格性分析

回答三个问题：
  1) 阈值阶梯：随着一致性/比对长度收紧，病毒 reads 占比如何衰减？
     真实信号应当平缓衰减，假信号（保守域/低复杂度）会断崖式消失。
  2) 双端一致性：R1 与 R2 都命中的 read 对里，两端是否指向同一物种？
     真实病毒片段两端应指向同一分类单元；随机命中则彼此无关。
  3) 靶标集中度：命中是否挤在极少数参考蛋白上？
     若是，说明命中的是共享保守域，而非真正的病毒基因组片段。

输入： 04_viral/<RUN>.R{1,2}.hits.tsv、00_db/RVDBv32_unique.fasta、
       09_tables/viral_reads_summary.tsv（取 reads_total 作分母）
输出： 09_tables/viral_stringency_ladder.tsv
       09_tables/viral_validation_summary.tsv
       09_tables/viral_subject_concentration.tsv
"""
import csv
import re
from collections import Counter, defaultdict
from pathlib import Path

PROJ = Path(__file__).resolve().parent.parent
VDIR = PROJ / "04_viral"
FA = PROJ / "00_db" / "RVDBv32_unique.fasta"
TAB = PROJ / "09_tables"

RUNS = ["SRR14300938", "SRR14300939", "SRR14300942",
        "SRR14300940", "SRR14300941", "SRR14300943"]

# ---- 蛋白 accession → 物种（DIAMOND 的 sseqid 会被空格截断，必须用第 3 段）----
print("构建物种映射 ...")
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
print(f"  {len(sps):,} 条参考蛋白")

reads_total = {}
with open(TAB / "viral_reads_summary.tsv", encoding="utf-8") as fh:
    for r in csv.DictReader(fh, delimiter="\t"):
        reads_total[r["run_accession"]] = int(r["reads_total"])


def load_hits(run, mate):
    """返回 [(qid, sseqid, pident, alen, bitscore)]"""
    f = VDIR / f"{run}.R{mate}.hits.tsv"
    out = []
    if not f.exists():
        return out
    with open(f, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            p = line.rstrip("\n").split("\t")
            if len(p) < 12:
                continue
            out.append((p[0], p[1], float(p[2]), int(p[3]), float(p[11])))
    return out


# ---- 阈值阶梯 -------------------------------------------------------------
LADDER = [
    ("e1e-5, id>=40, len>=30 (current)", 40.0, 30, 0.0),
    ("id>=50, len>=40", 50.0, 40, 0.0),
    ("id>=60, len>=50", 60.0, 50, 0.0),
    ("id>=70, len>=50", 70.0, 50, 0.0),
    ("id>=80, len>=50", 80.0, 50, 0.0),
    ("id>=90, len>=50", 90.0, 50, 0.0),
]

ladder_rows = []
summary_rows = []
conc_rows = []
conc_rows_detail = []

for run in RUNS:
    h1, h2 = load_hits(run, 1), load_hits(run, 2)
    denom = reads_total[run]

    # --- 阶梯 ---
    for label, min_id, min_len, _ in LADDER:
        s1 = {q for q, _, pid, al, _ in h1 if pid >= min_id and al >= min_len}
        s2 = {q for q, _, pid, al, _ in h2 if pid >= min_id and al >= min_len}
        n = len(s1) + len(s2)
        sp_hit = {(x.split("|")[2] if "|" in x else x)
                  for q, x, pid, al, _ in h1 + h2 if pid >= min_id and al >= min_len}
        ladder_rows.append({
            "run_accession": run, "threshold": label,
            "viral_reads": n, "viral_reads_pct": f"{n/denom*100:.4f}",
            "n_taxa": len(sp_hit),
        })

    # --- 双端一致性（用当前阈值）---
    m1 = {}
    for q, x, pid, al, _ in h1:
        if pid >= 40 and al >= 30:
            m1[q] = sps.get(x.split("|")[2] if "|" in x else x, "unknown")
    m2 = {}
    for q, x, pid, al, _ in h2:
        if pid >= 40 and al >= 30:
            m2[q] = sps.get(x.split("|")[2] if "|" in x else x, "unknown")

    both = set(m1) & set(m2)
    agree = sum(1 for q in both if m1[q] == m2[q])
    agree_rate = (agree / len(both) * 100) if both else 0.0
    both_frac = (len(both) / (len(m1) + len(m2)) * 100) if (m1 or m2) else 0.0
    conc_rows.append({
        "run_accession": run,
        "hits_R1": len(m1), "hits_R2": len(m2),
        "pairs_both_hit": len(both),
        "pairs_same_taxon": agree,
        "same_taxon_pct": f"{agree_rate:.1f}",
        "both_hit_frac_of_hits_pct": f"{both_frac:.1f}",
    })

    # --- 靶标集中度 ---
    subj = Counter()
    for q, x, pid, al, _ in h1:
        if pid >= 40 and al >= 30:
            subj[x] += 1
    total = sum(subj.values())
    top10 = sum(c for _, c in subj.most_common(10))
    conc_rows_detail.append({
        "run_accession": run,
        "passing_hits_R1": total,
        "distinct_subject_proteins": len(subj),
        "top1_pct": f"{(subj.most_common(1)[0][1]/total*100):.2f}" if total else "0",
        "top10_pct": f"{(top10/total*100):.1f}" if total else "0",
        "top1_protein": subj.most_common(1)[0][0] if subj else "",
    })
    print(f"{run}: 阶梯完成，双端同源 {agree_rate:.1f}%（{len(both):,} 对两端都命中）")


def write(path, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]), delimiter="\t")
        w.writeheader()
        w.writerows(rows)
    print(f"已写出 {path.name}")


write(TAB / "viral_stringency_ladder.tsv", ladder_rows)
write(TAB / "viral_paired_concordance.tsv", conc_rows)
write(TAB / "viral_subject_concentration.tsv", conc_rows_detail)

#!/usr/bin/env python3
"""汇总 M1 表（B5）：把 fastp JSON + bowtie2 去宿主结果合并成 09_tables/M1_summary.csv

用法：
    python workflow/build_m1_table.py            # 不统计去宿主后的 reads 数
    COUNT_READS=1 python workflow/build_m1_table.py   # 额外逐条统计（慢，但精确）

说明：
- 本表只写"真实算出来的数"，没有的数据留空，绝不估算填数。
- reads 统一用"条"(mates)，同时给 pairs 列，避免与样本表混淆
  （fastp 的 total_reads 是双端合计，样本表里存的是 pairs）。
"""
import csv, json, os, subprocess, sys
from pathlib import Path

PROJ = Path(__file__).resolve().parent.parent
SHEET = PROJ / "metadata" / "sample_sheet.csv"
QC = PROJ / "01_qc"
HR = PROJ / "02_host_removed"
HOST_SUM = PROJ / "09_tables" / "host_removal_summary.tsv"
VIRAL_SUM = PROJ / "09_tables" / "viral_reads_summary.tsv"
OUT = PROJ / "09_tables" / "M1_summary.csv"

count_reads = os.environ.get("COUNT_READS") == "1"


def count_gz_reads(path: Path) -> int:
    """流式统计 fastq.gz 条数（每 4 行 1 条）。"""
    try:
        p = subprocess.run(["zcat", str(path)], capture_output=True, text=True, check=True)
        return len(p.stdout.splitlines()) // 4
    except Exception:
        return -1


# 读样本表
rows = list(csv.DictReader(open(SHEET, encoding="utf-8-sig")))

# 读 bowtie2 汇总
host = {}
if HOST_SUM.exists():
    for r in csv.DictReader(open(HOST_SUM, encoding="utf-8"), delimiter="\t"):
        host[r["run_accession"]] = r

# 读病毒筛查汇总
viral = {}
if VIRAL_SUM.exists():
    for r in csv.DictReader(open(VIRAL_SUM, encoding="utf-8"), delimiter="\t"):
        viral[r["run_accession"]] = r

fields = [
    "sample_id", "run_accession", "season",
    "reads_raw_pairs", "reads_raw_mates", "reads_clean_mates", "pass_rate_pct",
    "q30_before_pct", "q30_after_pct", "dup_rate_pct",
    "host_aligned_pct", "reads_after_host_rm_mates", "viral_reads_pct",
]

out_rows = []
for r in rows:
    run = r["run_accession"]
    f = QC / f"{run}.fastp.json"
    rec = {k: "" for k in fields}
    rec.update({
        "sample_id": r["sample_id"], "run_accession": run, "season": r["season"],
        "reads_raw_pairs": r.get("reads_raw", ""),
    })
    if f.exists():
        d = json.load(open(f, encoding="utf-8"))
        s = d.get("summary", {})
        bf, af = s.get("before_filtering", {}), s.get("after_filtering", {})
        raw = bf.get("total_reads", 0)
        clean = af.get("total_reads", 0)
        rec["reads_raw_mates"] = raw
        rec["reads_clean_mates"] = clean
        rec["pass_rate_pct"] = f"{clean / raw * 100:.2f}" if raw else ""
        rec["q30_before_pct"] = f"{bf.get('q30_rate', 0) * 100:.2f}"
        rec["q30_after_pct"] = f"{af.get('q30_rate', 0) * 100:.2f}"
        rec["dup_rate_pct"] = f"{d.get('duplication', {}).get('rate', 0) * 100:.2f}"
    if run in host:
        rec["host_aligned_pct"] = host[run].get("host_aligned_pct", "")
        act = HR / f"{run}.host_rm.1.fq.gz"
        if act.exists():
            if count_reads:
                n = count_gz_reads(act)
                rec["reads_after_host_rm_mates"] = n * 2 if n > 0 else ""
            else:
                rec["reads_after_host_rm_mates"] = "未统计"
    if run in viral:
        rec["viral_reads_pct"] = viral[run].get("viral_reads_pct", "")
        # 病毒筛查时已逐条统计过去宿主后的 reads 数，直接用它（比重新解压计数快）
        tot = viral[run].get("reads_total", "")
        if tot:
            rec["reads_after_host_rm_mates"] = tot
    out_rows.append(rec)

OUT.parent.mkdir(parents=True, exist_ok=True)
with open(OUT, "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=fields)
    w.writeheader()
    w.writerows(out_rows)

print(f"已写出 {OUT}")
print()
widths = {k: max(len(k), *(len(str(r[k])) for r in out_rows)) if out_rows else len(k) for k in fields}
print("  ".join(k.ljust(widths[k]) for k in fields[:9]))
for r in out_rows:
    print("  ".join(str(r[k]).ljust(widths[k]) for k in fields[:9]))

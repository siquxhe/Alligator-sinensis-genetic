#!/usr/bin/env python3
"""
B1 分析：三条 read 层规则对已知 spike 的回收率与偏倚

核心量
------
recovery = 被检出的 spike reads / spike reads 总数
           —— 干净地衡量"规则能不能把已知成分找回来"，不受背景自身病毒信号干扰

reported = 规则报出的病毒 reads / 全部 reads
           —— 这是使用者实际看到的数；它 = 背景病毒信号 + spike 回收量

对 reported 的偏倚，只在"背景病毒信号已知"时才可算；本文用 recovery 作为主指标，
reported 与真值之差作为"绝对偏倚的上界"（因为背景贡献 ≥ 0）。

用法：python3 analyze_b1.py
"""
import re
from collections import defaultdict
from pathlib import Path

import numpy as np

BASE = Path("/mnt/work/chicken/b1")
OUT = Path("/mnt/work/chicken/b1/analysis")
OUT.mkdir(exist_ok=True)

STRUCT = ["capsid", "coat protein", "major head", "minor head", "tail", "portal",
          "terminase", "baseplate", "spike", "fiber", "virion", "envelope",
          "glycoprotein", "neck", "tape measure", "sheath", "prohead"]
REPL = ["polymerase", "replicase", "helicase", "primase", "integrase",
        "transposase", "nuclease", "ligase", "single-strand", "ssdna",
        "replication", "transcription", "rna-dependent", "rdrp", "polyprotein"]


def is_strict(desc: str) -> bool:
    d = desc.lower()
    return any(k in d for k in STRUCT) or any(k in d for k in REPL)


def load_truth():
    rows = {}
    with open(BASE / "truth.tsv") as f:
        next(f)
        for line in f:
            tag, lvl, rep, nbg, nsp, tf = line.rstrip("\n").split("\t")
            rows[tag] = dict(level=float(lvl), rep=int(rep),
                             n_bg=int(nbg), n_spike=int(nsp), true_frac=float(tf))
    return rows


def count_hits(path: Path):
    """返回 (全部命中 reads 集合, strict 命中 reads 集合)"""
    allr, strictr = set(), set()
    if not path.exists():
        return allr, strictr
    with open(path) as f:
        for line in f:
            p = line.rstrip("\n").split("\t")
            if len(p) < 4:
                continue
            rid, desc, pid, ln = p[0], p[1], p[2], p[3]
            try:
                if float(pid) < 40 or int(ln) < 30:
                    continue
            except ValueError:
                continue
            rid = re.sub(r"/[12]$", "", rid)
            allr.add(rid)
            if is_strict(desc):
                strictr.add(rid)
    return allr, strictr


def main():
    truth = load_truth()
    rows = []
    for tag, t in sorted(truth.items()):
        allr, strictr = count_hits(BASE / "results" / f"{tag}.hits.tsv")
        votu = BASE / "results" / f"{tag}.votu.txt"
        votu_all = 0
        if votu.exists():
            # 只有总比对数，没有 read id；spike 侧需另算，这里先记总计
            votu_all = int(votu.read_text().strip() or 0)

        n_reads = 2 * (t["n_bg"] + t["n_spike"])
        n_spike_reads = 2 * t["n_spike"]

        spike_all = sum(1 for r in allr if r.startswith("SPIKE_"))
        spike_strict = sum(1 for r in strictr if r.startswith("SPIKE_"))

        rows.append(dict(
            tag=tag, level=t["level"], rep=t["rep"],
            total_reads=n_reads, spike_reads=n_spike_reads,
            true_frac=t["true_frac"],
            # R_rvdb_all
            rec_rvdb_all=spike_all / n_spike_reads,
            est_rvdb_all=len(allr) / n_reads,
            # R_rvdb_strict
            rec_rvdb_strict=spike_strict / n_spike_reads,
            est_rvdb_strict=len(strictr) / n_reads,
            # R_votu（只知总数，spike 回收率留空）
            est_votu=votu_all / n_reads,
        ))

    # 输出明细
    hdr = ["tag", "level", "rep", "true_frac", "rec_rvdb_all", "est_rvdb_all",
           "rec_rvdb_strict", "est_rvdb_strict", "est_votu"]
    with open(OUT / "b1_detail.tsv", "w") as f:
        f.write("\t".join(hdr) + "\n")
        for r in rows:
            f.write("\t".join(f"{r[h]:.6g}" if isinstance(r[h], float) else str(r[h])
                              for h in hdr) + "\n")

    # 按水平汇总（中位与范围，n=3）
    print(f"{'水平':<8}{'规则':<18}{'回收率中位':>10}{'范围':>16}{'报出占比':>12}{'真值':>9}{'倍数':>8}")
    summary = []
    for lvl in sorted({r["level"] for r in rows}):
        sub = [r for r in rows if r["level"] == lvl]
        for rule, rec, est in [
            ("RVDB 全命中", "rec_rvdb_all", "est_rvdb_all"),
            ("RVDB 严格类别", "rec_rvdb_strict", "est_rvdb_strict"),
        ]:
            recs = np.array([r[rec] for r in sub])
            ests = np.array([r[est] for r in sub])
            print(f"{lvl*100:>6.1f}%  {rule:<16}{np.median(recs):>10.3f}"
                  f"   [{recs.min():.3f}, {recs.max():.3f}]"
                  f"{np.median(ests)*100:>11.3f}%{lvl*100:>8.2f}%{np.median(ests)/lvl:>8.2f}")
            summary.append((lvl, rule, np.median(recs), recs.min(), recs.max(),
                            np.median(ests), np.median(ests) / lvl))
        ests = np.array([r["est_votu"] for r in sub])
        print(f"{lvl*100:>6.1f}%  {'vOTU 目录':<16}{'n/a':>10}{'':>16}"
              f"{np.median(ests)*100:>11.3f}%{lvl*100:>8.2f}%{np.median(ests)/lvl:>8.2f}")

    with open(OUT / "b1_summary.tsv", "w") as f:
        f.write("level\trule\trecovery_median\trecovery_min\trecovery_max\test_median\tfold_vs_truth\n")
        for s in summary:
            f.write("\t".join(f"{x:.6g}" if isinstance(x, float) else str(x) for x in s) + "\n")
    print("\n输出:", OUT / "b1_detail.tsv", OUT / "b1_summary.tsv")


if __name__ == "__main__":
    main()

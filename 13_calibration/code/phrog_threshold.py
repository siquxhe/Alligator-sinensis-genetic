#!/usr/bin/env python3
"""PHROG 阈值敏感性：类别筛选倍数是否依赖 identity/length 阈值

输入 phrog.hits.tsv（blastx, outfmt: qseqid stitle pident length）
输出每 (pident, length) 组合下的 total / strict / 比值
"""
import csv
import re
import sys
from collections import Counter

HITS = "/mnt/work/chicken/refcheck/phrog.hits.tsv"
ANN = "/mnt/work/chicken/db/phrog/phrog_annot_v4.tsv"
N_READS = 2_500_000  # sub.fq 的 R1 条数

STRUCT = {"head and packaging", "tail", "connector", "virion", "neck", "baseplate"}
REPL = {"DNA, RNA and nucleotide metabolism", "transcription regulation"}


def load_ann():
    ann = {}
    with open(ANN) as f:
        for r in csv.DictReader(f, delimiter="\t"):
            ann[r["phrog"]] = r["category"]
    return ann


def classify(ann, sid):
    m = re.search(r"(\d+)", sid)
    if not m:
        return "other"
    cat = ann.get(m.group(1))
    if cat in STRUCT:
        return "structural"
    if cat in REPL:
        return "replication"
    return "other"


def main():
    ann = load_ann()
    # read -> (pident, length, class)；每 read 只保留首条（--max-target-seqs 1）
    rows = []
    with open(HITS) as f:
        for line in f:
            p = line.rstrip("\n").split("\t")
            if len(p) < 4:
                continue
            try:
                pid = float(p[2])
                ln = int(p[3])
            except ValueError:
                continue
            rows.append((p[0], pid, ln, classify(ann, p[1])))
    # 去重：同 read 取 identity 最高者
    best = {}
    for rid, pid, ln, cls in rows:
        if rid not in best or pid > best[rid][0]:
            best[rid] = (pid, ln, cls)
    print(f"读入命中行 {len(rows)}, 唯一 reads {len(best)}, 查询 reads {N_READS:,}")
    print()

    hdr = f"{'pident':>7} {'len':>5} | {'total':>8} {'total%':>7} | {'strict':>7} {'strict%':>8} | {'ratio':>6}"
    print(hdr)
    print("-" * len(hdr))
    for pid_min in [40, 50, 60, 70, 80, 90]:
        for len_min in [30, 50, 100]:
            c = Counter()
            for pid, ln, cls in best.values():
                if pid >= pid_min and ln >= len_min:
                    c[cls] += 1
            tot = sum(c.values())
            strict = c["structural"] + c["replication"]
            if strict == 0:
                continue
            print(
                f"{pid_min:>7} {len_min:>5} | {tot:>8} {tot/N_READS*100:>6.3f}% | "
                f"{strict:>7} {strict/N_READS*100:>7.3f}% | {tot/strict:>5.2f}x"
            )
        print()

    # 高阈值下各类别构成
    print("=== 各类别绝对量随阈值变化（len>=30）===")
    print(f"{'pident':>7} | {'structural':>10} {'replication':>11} {'other':>9}")
    for pid_min in [40, 50, 60, 70, 80, 90]:
        c = Counter()
        for pid, ln, cls in best.values():
            if pid >= pid_min and ln >= 30:
                c[cls] += 1
        print(f"{pid_min:>7} | {c['structural']:>10} {c['replication']:>11} {c['other']:>9}")


if __name__ == "__main__":
    main()

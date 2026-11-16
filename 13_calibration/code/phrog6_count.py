#!/usr/bin/env python3
"""单样本 PHROG 命中分类统计：输出一行 TSV

用法：python3 phrog6_count.py <SID> <hits.tsv> <R1.fq.gz>
"""
import csv
import gzip
import re
import sys
from collections import Counter

ANN = "/mnt/work/chicken/db/phrog/phrog_annot_v4.tsv"
STRUCT = {"head and packaging", "tail", "connector", "virion", "neck", "baseplate"}
REPL = {"DNA, RNA and nucleotide metabolism", "transcription regulation"}


def main():
    sid, hits_f, r1 = sys.argv[1], sys.argv[2], sys.argv[3]

    ann = {}
    with open(ANN) as f:
        for r in csv.DictReader(f, delimiter="\t"):
            ann[r["phrog"]] = r["category"]

    def cls(k):
        v = ann.get(k)
        if v in STRUCT:
            return "structural"
        if v in REPL:
            return "replication"
        return "other"

    seen = {}
    with open(hits_f) as f:
        for line in f:
            p = line.rstrip("\n").split("\t")
            if len(p) < 4:
                continue
            try:
                if float(p[2]) < 40 or int(p[3]) < 30:
                    continue
            except ValueError:
                continue
            if p[0] in seen:
                continue
            m = re.search(r"(\d+)", p[1])
            seen[p[0]] = cls(m.group(1)) if m else "other"

    n = 0
    with gzip.open(r1, "rt") as f:
        for i, _ in enumerate(f):
            if i % 4 == 0:
                n += 1
    N = n * 2

    c = Counter(seen.values())
    tot = len(seen)
    st = c["structural"]
    rp = c["replication"]
    ot = c["other"]
    strict = st + rp
    ratio = (tot / strict) if strict else 0.0
    cols = [sid, N, tot, strict, st, rp, ot, round(ratio, 2)]
    print("\t".join(str(x) for x in cols))


if __name__ == "__main__":
    main()

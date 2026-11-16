#!/usr/bin/env python3
"""交叉验证 A：自建 vOTU 蛋白库 + PHROG 注释

两条独立通路的组合：
  reads --blastx--> 自建库蛋白 --> (blastp vs PHROG) --> category
与 PHROG 全库直接 blastx（5.17x）互相独立：
  序列来源不同（19,789 vOTU vs 868k PHROG 蛋白）
  注释来源相同（PHROG 本体注释）
"""
import csv
import re
import subprocess
import sys
from collections import Counter

E = "/home/wuyanching/biotools/envs/virome/bin"
BASE = "/mnt/work/chicken/refcheck"
PROT = f"{BASE}/prot/all.faa"
PHROG_DB = "/mnt/work/chicken/db/phrog/phrog.dmnd"
ANN = "/mnt/work/chicken/db/phrog/phrog_annot_v4.tsv"
READ_HITS = f"{BASE}/new.hits.tsv"      # reads vs 自建库（blastx）
PROT_HITS = f"{BASE}/prot_vs_phrog.tsv"  # 自建库蛋白 vs PHROG（blastp）
N_READS = 2_500_000

STRUCT = {"head and packaging", "tail", "connector", "virion", "neck", "baseplate"}
REPL = {"DNA, RNA and nucleotide metabolism", "transcription regulation"}


def run_blastp():
    import os
    if os.path.exists(PROT_HITS) and os.path.getsize(PROT_HITS) > 0:
        print("blastp 结果已存在，跳过")
        return
    print("自建库蛋白 vs PHROG 建库（blastp）...")
    cmd = [
        f"{E}/diamond", "blastp", "-q", PROT, "-d", PHROG_DB,
        "--evalue", "1e-5", "--outfmt", "6", "qseqid", "stitle", "pident", "length",
        "--threads", "8", "--max-target-seqs", "1", "-o", PROT_HITS,
    ]
    subprocess.run(cmd, check=True)
    print(f"完成，行数 {sum(1 for _ in open(PROT_HITS))}")


def main():
    run_blastp()

    ann = {}
    with open(ANN) as f:
        for r in csv.DictReader(f, delimiter="\t"):
            ann[r["phrog"]] = r["category"]

    def cls_of_phrog(sid):
        m = re.search(r"(\d+)", sid)
        cat = ann.get(m.group(1)) if m else None
        if cat in STRUCT:
            return "structural"
        if cat in REPL:
            return "replication"
        return "other"

    # 蛋白 -> 类别（40%/30aa 同阈值，保证与 PHROG 那一版可比）
    # key 统一取 header 第一个空格前的部分，两侧才能对上
    prot_cls = {}
    for line in open(PROT_HITS):
        p = line.rstrip("\n").split("\t")
        if len(p) < 4:
            continue
        try:
            if float(p[2]) < 40 or int(p[3]) < 30:
                continue
        except ValueError:
            continue
        prot_cls[p[0].split()[0]] = cls_of_phrog(p[1])
    prot_annotated = len(prot_cls)

    n_prot = 0
    with open(PROT) as f:
        for line in f:
            if line.startswith(">"):
                n_prot += 1
    print(f"\n自建库蛋白 {n_prot:,}, 其中 {prot_annotated:,} 获 PHROG 注释 "
          f"({prot_annotated/n_prot*100:.1f}%)")

    # read -> 类别（取其命中的蛋白的类别）
    read_cls = {}
    for line in open(READ_HITS):
        p = line.rstrip("\n").split("\t")
        if len(p) < 4:
            continue
        try:
            if float(p[2]) < 40 or int(p[3]) < 30:
                continue
        except ValueError:
            continue
        if p[0] in read_cls:
            continue
        key = p[1].split()[0]          # 与 prot_cls 的 key 归一化方式一致
        read_cls[p[0]] = prot_cls.get(key, "unannotated")

    c = Counter(read_cls.values())
    tot = len(read_cls)
    strict = c["structural"] + c["replication"]
    print(f"\n=== 结果（reads 级）===")
    print(f"总命中 {tot:,}  ({tot/N_READS*100:.3f}%)")
    for k in ["structural", "replication", "unannotated", "other"]:
        print(f"  {k:12s} {c[k]:>7,}  ({c[k]/N_READS*100:.3f}%)")
    print(f"严格(结构+复制) {strict:,}  ({strict/N_READS*100:.3f}%)")
    if strict:
        print(f"\n总/严格 = {tot/strict:.2f}x")
    print(f"\n对照: PHROG 全库 5.79% / 1.12% = 5.17x")


if __name__ == "__main__":
    main()

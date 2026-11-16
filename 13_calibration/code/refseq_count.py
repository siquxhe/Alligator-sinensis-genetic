#!/usr/bin/env python3
"""交叉验证 B：RefSeq viral 独立库 + 独立注释

与 PHROG 那版的区别：
  序列来源：RefSeq viral（参考病毒基因组）vs PHROG（噬菌体蛋白家族）
  注释来源：RefSeq protein name 关键词 vs PHROG 本体 category
  分类规则：与旧库（RVDB 78万）那版完全同一套关键词，保证可比

基线：
  旧库 78万 + 关键词   -> 0.839% / 严格   = 6.85x（W1）
  PHROG + 本体注释      -> 5.790% / 1.120% = 5.17x（W1）
"""
import subprocess
import sys
from collections import Counter

E = "/home/wuyanching/biotools/envs/virome/bin"
BASE = "/mnt/work/chicken/refcheck"
HITS = f"{BASE}/refseq.hits.tsv"
N_READS = 2_500_000

# 与 refcheck 旧库那一版完全一致的关键词表
STRUCT = ["capsid", "coat protein", "major head", "minor head", "tail", "portal",
          "terminase", "baseplate", "spike", "fiber", "virion", "envelope",
          "glycoprotein", "neck", "tape measure", "sheath", "prohead"]
REPL = ["polymerase", "replicase", "helicase", "primase", "integrase", "transposase",
        "nuclease", "ligase", "single-strand", "ssdna", "replication", "transcription",
        "rna-dependent", "rdrp", "polyprotein"]


def classify(desc):
    d = desc.lower()
    if any(k in d for k in STRUCT):
        return "structural"
    if any(k in d for k in REPL):
        return "replication"
    return "other"


def main():
    seen = {}
    for line in open(HITS):
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
        seen[p[0]] = classify(p[1])

    c = Counter(seen.values())
    tot = len(seen)
    strict = c["structural"] + c["replication"]
    print("=== RefSeq viral（W1, 250 万条 R1）===")
    print(f"总命中 {tot:,}  ({tot/N_READS*100:.3f}%)")
    for k in ["structural", "replication", "other"]:
        print(f"  {k:12s} {c[k]:>7,}  ({c[k]/N_READS*100:.3f}%)")
    print(f"严格(结构+复制) {strict:,}  ({strict/N_READS*100:.3f}%)")
    if strict:
        print(f"\n总/严格 = {tot/strict:.2f}x")
    else:
        print("\n严格为 0，无法计算比值")
    print("\n对照: 旧库 6.85x | PHROG 5.17x | 自建库+PHROG注释 5.05x")


if __name__ == "__main__":
    main()

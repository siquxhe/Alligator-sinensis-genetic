#!/usr/bin/env python3
"""16S 群落相似性：无参考 k-mer 谱比较

目的：判断 A.F5（对应宏基因组 S1）的菌群更像夏季（A.F3/A.F4）还是冬季（H.F1/H.F2/H.F6）。

方法：每样本抽样 3 万条 read，统计 15-mer 频次（仅保留出现 ≥2 次的），
两两计算余弦相似度。16S 高变区决定群落差异，k-mer 谱能反映整体组成相似性，
不需要参考数据库，也不引入分类器偏差。
"""
import gzip
import math
import random
from collections import Counter
from pathlib import Path

D = Path.home() / "virome" / "16s"
S = [("AF3", "summer"), ("AF4", "summer"), ("AF5", "summer"),
     ("HF1", "winter"), ("HF2", "winter"), ("HF6", "winter")]
K = 15
N = 30_000
random.seed(7)


def kmer_profile(fq, n=N):
    c = Counter()
    nread = 0
    with gzip.open(fq, "rt", errors="replace") as fh:
        while nread < n:
            h = fh.readline()
            if not h:
                break
            seq = fh.readline().strip().upper()
            fh.readline()
            fh.readline()
            if len(seq) < K:
                continue
            for i in range(len(seq) - K + 1):
                k = seq[i:i + K]
                if "N" in k:
                    continue
                c[k] += 1
            nread += 1
    # 去低频噪声
    return {k: v for k, v in c.items() if v >= 2}, nread


def cosine(a, b):
    if not a or not b:
        return 0.0
    common = set(a) & set(b)
    dot = sum(a[k] * b[k] for k in common)
    na = math.sqrt(sum(v * v for v in a.values()))
    nb = math.sqrt(sum(v * v for v in b.values()))
    return dot / (na * nb) if na and nb else 0.0


profs = {}
for lab, season in S:
    fq = D / f"{lab}.fq.gz"
    if not fq.exists() or fq.stat().st_size < 100_000:
        print(f"[跳过] {lab} 未下载完整")
        continue
    p, n = kmer_profile(fq)
    profs[lab] = p
    print(f"{lab}: {n:,} 条 read，{len(p):,} 个 15-mer")

labs = [l for l, _ in S if l in profs]
season = dict(S)
print("\n=== 15-mer 余弦相似度 ===")
print("      " + "".join(f"{l:>8}" for l in labs))
M = {}
for a in labs:
    row = f"  {a:<4}"
    for b in labs:
        v = cosine(profs[a], profs[b])
        M[(a, b)] = v
        row += f"{v:>8.3f}"
    print(row)

# 分组平均
def mean_pair(a_set, b_set, same=False):
    vals = []
    for x in a_set:
        for y in b_set:
            if x == y:
                continue
            if same and x > y:
                continue
            vals.append(M[(x, y)])
    return sum(vals) / len(vals) if vals else 0

summer = [l for l in labs if season[l] == "summer"]
winter = [l for l in labs if season[l] == "winter"]

print("\n=== 分组平均相似度 ===")
if len(summer) >= 2:
    ss = [M[(a, b)] for i, a in enumerate(summer) for b in summer[i+1:]]
    print(f"  夏季内部（{'+'.join(summer)}）: {sum(ss)/len(ss):.4f}")
if len(winter) >= 2:
    ww = [M[(a, b)] for i, a in enumerate(winter) for b in winter[i+1:]]
    print(f"  冬季内部（{'+'.join(winter)}）: {sum(ww)/len(ww):.4f}")
cross = [M[(a, b)] for a in summer for b in winter]
print(f"  夏冬之间: {sum(cross)/len(cross):.4f}")

print("\n=== 每个样本与季节组的平均相似度 ===")
print(f"{'样本':<6}{'季节':<8}{'vs 夏季':>10}{'vs 冬季':>10}{'更接近':>10}")
for l in labs:
    vs_s = [M[(l, x)] for x in summer if x != l]
    vs_w = [M[(l, x)] for x in winter if x != l]
    ms = sum(vs_s)/len(vs_s) if vs_s else 0
    mw = sum(vs_w)/len(vs_w) if vs_w else 0
    closer = "夏季" if ms > mw else "冬季"
    print(f"{l:<6}{season[l]:<8}{ms:>10.4f}{mw:>10.4f}{closer:>10}")

# ---- 保存相似度矩阵（供作图复现）----
import csv
from pathlib import Path as _P
out = _P.home() / "virome" / "results" / "16s_kmer_similarity.tsv"
out.parent.mkdir(exist_ok=True)
with open(out, "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh, delimiter="\t")
    w.writerow(["sample_id"] + labs)
    for a in labs:
        w.writerow([a] + [f"{M[(a,b)]:.4f}" for b in labs])
print(f"\n已写出 {out}")

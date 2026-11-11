#!/usr/bin/env python3
"""解析 CD-HIT 聚类结果，生成 vOTU 表与分布统计

输出（~/virome/results/）
  votu_members.tsv   每个 contig 的归属：vOTU、样本、是否代表序列、长度
  votu_presence.tsv  每个 vOTU 的分布：出现在几个样本、哪些样本、成员数
  votu_stats.tsv     汇总统计：总 vOTU 数、共享模式、季节共享
"""
import csv
import re
from collections import Counter, defaultdict
from pathlib import Path

BASE = Path.home() / "virome"
CLSTR = BASE / "work" / "votu" / "votu95.clstr"
OUT = BASE / "results"
OUT.mkdir(exist_ok=True)

SAMPLES = ["W1", "W2", "W3", "S1", "S2", "S3"]
SEASON = {"W1": "winter", "W2": "winter", "W3": "winter",
          "S1": "summer", "S2": "summer", "S3": "summer"}

# CD-HIT 成员行形如：0	4301nt, >W1__k141_123... *
# 或带相似度：1	4200nt, >S2__k141_456... at 95.2%
member_re = re.compile(r"^\d+\s+(\d+)nt,\s+>(\S+?)\.\.\.\s*(\*)?(.*)$")

members = []
cur = -1
with open(CLSTR, encoding="utf-8", errors="replace") as fh:
    for line in fh:
        line = line.rstrip("\n")
        if line.startswith(">Cluster"):
            cur = int(line.split()[1])
            continue
        m = member_re.match(line)
        if not m or cur < 0:
            continue
        length, seqid, is_rep, _ = m.groups()
        if "__" in seqid:
            sample, contig = seqid.split("__", 1)
        else:
            sample, contig = "NA", seqid
        members.append({
            "votu_id": f"vOTU_{cur:05d}",
            "sample_id": sample,
            "contig_id": contig,
            "length": int(length),
            "is_representative": "yes" if is_rep else "no",
        })

print(f"解析 {len(members):,} 条 contig，{len({m['votu_id'] for m in members}):,} 个 vOTU")

# ---- 每个 vOTU 的分布 ----
by_votu = defaultdict(list)
for m in members:
    by_votu[m["votu_id"]].append(m)

presence = []
for vid, mem in by_votu.items():
    samples = sorted({m["sample_id"] for m in mem})
    presence.append({
        "votu_id": vid,
        "n_samples": len(samples),
        "n_contigs": len(mem),
        "samples": ",".join(samples),
        "n_seasons": len({SEASON[s] for s in samples if s in SEASON}),
        "rep_length": max(m["length"] for m in mem if m["is_representative"] == "yes")
        if any(m["is_representative"] == "yes" for m in mem) else mem[0]["length"],
    })

# ---- 写表 ----
def write(path, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]), delimiter="\t")
        w.writeheader()
        w.writerows(rows)
    print(f"已写出 {path}")

write(OUT / "votu_members.tsv", members)
presence.sort(key=lambda r: (-r["n_samples"], r["votu_id"]))
write(OUT / "votu_presence.tsv", presence)

# ---- 统计 ----
n_votu = len(presence)
per_sample = Counter(m["sample_id"] for m in members)
votu_per_sample = defaultdict(set)
for m in members:
    votu_per_sample[m["sample_id"]].add(m["votu_id"])

share = Counter(r["n_samples"] for r in presence)
season_share = Counter(r["n_seasons"] for r in presence)

stats = []
stats.append(("总病毒 contigs", len(members), ""))
stats.append(("总 vOTU 数", n_votu, ""))
stats.append(("clustering 归并率", f"{(1-n_votu/len(members))*100:.1f}%", "被合并的 contig 比例"))
for s in SAMPLES:
    stats.append((f"{s} 的 contig 数", per_sample[s], ""))
    stats.append((f"{s} 的 vOTU 数", len(votu_per_sample[s]),
                  f"占该样本 contig 的 {len(votu_per_sample[s])/per_sample[s]*100:.1f}%"))
stats.append(("单样本特有 vOTU", share.get(1, 0), f"{share.get(1,0)/n_votu*100:.1f}%"))
stats.append(("跨 ≥2 样本共享 vOTU", sum(v for k, v in share.items() if k >= 2),
              f"{sum(v for k,v in share.items() if k>=2)/n_votu*100:.1f}%"))
stats.append(("六样本共有 vOTU", share.get(6, 0), ""))
stats.append(("仅冬季出现（2-3 个冬样本）", season_share.get(1, 0), "严格单季节"))
stats.append(("跨季节 vOTU", season_share.get(2, 0), "冬夏都检出"))

with open(OUT / "votu_stats.tsv", "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh, delimiter="\t")
    w.writerow(["指标", "数值", "说明"])
    w.writerows(stats)

print("\n=== 汇总 ===")
for k, v, note in stats:
    print(f"  {k:<28} {v:>8}  {note}")

print("\n=== 共享样本数分布 ===")
for k in sorted(share):
    print(f"  出现在 {k} 个样本: {share[k]:>5} 个 vOTU ({share[k]/n_votu*100:>5.1f}%)")

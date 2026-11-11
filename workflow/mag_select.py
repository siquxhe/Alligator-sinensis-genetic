#!/usr/bin/env python3
"""MAG 筛选与去冗余

输入
  work/mag_checkm/checkm_qa.tsv   CheckM qa --tab_table 输出
  work/mag_fastani/ani.txt        fastANI 全对全结果
  work/mag_all_bins/*.fa          全部 bin

输出（07_mag/）
  mag_quality.tsv      全部 bin 的质量与谱系
  mag_final.tsv        去冗余后的 MAG（≥50% 完整、≤10% 污染、95% ANI 去重）
  mag_final/           代表 MAG 的 fasta
"""
import re
import shutil
from pathlib import Path

import pandas as pd

import sys
ROOT = Path(__file__).resolve().parents[1]
W = Path.home() / "virome" / "work"
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "07_mag"
OUT.mkdir(parents=True, exist_ok=True)

MIN_COMP, MAX_CONT, ANI_CUT = 50.0, 10.0, 95.0

# ---------- 1. CheckM 结果 ----------
qa = pd.read_csv(W / "mag_checkm" / "checkm_qa.tsv", sep="\t")
qa.columns = [c.strip() for c in qa.columns]
# 列名形如 "Bin Id", "Marker Lineage", "Completeness", "Contamination"
ren = {}
for c in qa.columns:
    lc = c.lower()
    if "bin id" in lc: ren[c] = "bin"
    elif "lineage" in lc: ren[c] = "lineage"
    elif lc == "completeness": ren[c] = "completeness"
    elif lc == "contamination": ren[c] = "contamination"
    elif "strain heterogeneity" in lc: ren[c] = "strain_het"
qa = qa.rename(columns=ren)
qa["bin"] = qa["bin"].astype(str)
qa["sample_id"] = qa["bin"].str.split(".").str[0]
qa[["completeness", "contamination"]] = qa[["completeness", "contamination"]].astype(float)


def rank(lineage):
    """从 CheckM 谱系列出 p__ / c__ / o__ / f__"""
    d = {}
    for m in re.finditer(r"([kpcofgs])__([^;]+)", str(lineage)):
        d[m.group(1)] = m.group(2).strip()
    return d


for lvl, name in [("p", "phylum"), ("c", "class"), ("o", "order"), ("f", "family")]:
    qa[name] = qa["lineage"].map(lambda x: rank(x).get(lvl, ""))

qa["quality"] = "Low"
qa.loc[qa.completeness >= 50, "quality"] = "Medium"
qa.loc[qa.completeness >= 70, "quality"] = "High"
qa.loc[(qa.completeness >= 90) & (qa.contamination <= 5), "quality"] = "Near-complete"
qa["score"] = qa.completeness - 5 * qa.contamination
qa.to_csv(OUT / "mag_quality.tsv", sep="\t", index=False)

print(f"全部 bin: {len(qa)}")
print(qa.quality.value_counts().to_string())

# ---------- 2. 候选（MIMAG medium 及以上）----------
cand = qa[(qa.completeness >= MIN_COMP) & (qa.contamination <= MAX_CONT)].copy()
print(f"\n候选（≥{MIN_COMP}% 完整、≤{MAX_CONT}% 污染）: {len(cand)}")

# ---------- 3. fastANI 去冗余 ----------
ani_file = W / "mag_fastani" / "ani.txt"
reps = []
if ani_file.exists() and ani_file.stat().st_size > 0:
    ani = pd.read_csv(ani_file, sep="\t", header=None,
                      names=["q", "r", "ani", "mapped", "total"])
    ani["q"] = ani.q.map(lambda p: Path(p).stem)
    ani["r"] = ani.r.map(lambda p: Path(p).stem)
    # 只看候选之间的 ANI
    cs = set(cand.bin)
    ani = ani[ani.q.isin(cs) & ani.r.isin(cs)]
    neigh = {}
    for row in ani.itertuples():
        if row.ani >= ANI_CUT:
            neigh.setdefault(row.q, set()).add(row.r)
            neigh.setdefault(row.r, set()).add(row.q)
    # 贪心：按质量分降序，已被代表覆盖的跳过
    assigned = {}
    for b in cand.sort_values("score", ascending=False).bin:
        if b in assigned:
            continue
        assigned[b] = b
        for nb in neigh.get(b, ()):
            if nb not in assigned:
                assigned[nb] = b
    cand["rep"] = cand.bin.map(lambda b: assigned.get(b, b))
    reps = cand[cand.bin == cand.rep].copy()
    cand["redundant_of"] = cand.bin.map(lambda b: "" if assigned.get(b, b) == b else assigned.get(b, b))
    print(f"fastANI 95% ANI 去冗余后代表 MAG: {len(reps)}（合并了 {len(cand) - len(reps)} 个）")
else:
    cand["rep"] = cand.bin
    cand["redundant_of"] = ""
    reps = cand.copy()
    print("未找到 fastANI 结果，跳过去冗余")

# ---------- 4. 复制代表 MAG ----------
dst = OUT / "mag_final"
if dst.exists():
    shutil.rmtree(dst)
dst.mkdir()
for b in reps.bin:
    src = W / "mag_all_bins" / f"{b}.fa"
    if src.exists():
        shutil.copy(src, dst / f"{b}.fa")

cand.sort_values(["sample_id", "score"], ascending=[True, False]).to_csv(
    OUT / "mag_all_candidates.tsv", sep="\t", index=False)
reps = reps.sort_values(["sample_id", "score"], ascending=[True, False])
reps.to_csv(OUT / "mag_final.tsv", sep="\t", index=False)

print(f"\n最终 MAG: {len(reps)} 条，共 {len(reps.phylum.unique())} 个门")
print(reps.groupby("sample_id").size().to_string())
print("\n门分布：")
print(reps.phylum.value_counts().to_string())

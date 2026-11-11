#!/usr/bin/env python3
"""Figure M2 — 肠道病毒组随宿主生理状态变化，而非日历季节

三个面板：
  A  碱基组成（GC）与病毒丰度的关系：六样本落成两组
  B  病毒组结构（Bray-Curtis 距离，vOTU 丰度加权）
  C  细菌 16S 群落相似度（k-mer 余弦）—— 独立验证 A.F5 的"错季"状态

数据
  ../../05_c_stage/sample_gc_viral.tsv
  ../../05_c_stage/votu_abundance_rpkm.tsv
  ../../05_c_stage/16s_kmer_similarity.tsv
输出
  ../output/FigM2_host_state_viral_community.pdf / .png (300 dpi)
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.gridspec import GridSpec
from matplotlib.lines import Line2D

PROJ = Path(__file__).resolve().parents[3]
D = PROJ / "05_c_stage"
OUT = Path(__file__).resolve().parents[1] / "output"
OUT.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans"],
    "font.size": 7,
    "axes.linewidth": 0.6,
    "axes.labelsize": 7.5,
    "xtick.labelsize": 6.8,
    "ytick.labelsize": 6.8,
    "xtick.major.width": 0.6,
    "ytick.major.width": 0.6,
    "xtick.major.size": 2.5,
    "ytick.major.size": 2.5,
    "legend.frameon": False,
    "legend.fontsize": 6.3,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
})

C_WINTER, C_SUMMER = "#0072B2", "#E69F00"
C_ODD = "#D55E00"

meta = pd.read_csv(D / "sample_gc_viral.tsv", sep="\t")
meta["color"] = meta["season"].map({"winter": C_WINTER, "summer": C_SUMMER})

fig = plt.figure(figsize=(7.09, 2.85))
gs = GridSpec(1, 3, figure=fig, width_ratios=[1.18, 1, 1],
              wspace=0.58, left=0.075, right=0.975, top=0.80, bottom=0.20)

# ===== A：GC vs 病毒丰度 ===================================================
axA = fig.add_subplot(gs[0])
# 手动指定标签偏移，避免重叠
LABEL_POS = {
    "W1": (1.0, 0.15), "W2": (0.9, -0.15), "W3": (-1.35, 1.15),
    "S1": (0.35, -1.35), "S2": (1.0, 0.25), "S3": (0.95, -0.35),
}
for _, r in meta.iterrows():
    odd = r["sample_id"] == "S1"
    axA.scatter(r["gc_pct"], r["viral_reads_pct"],
                s=95 if odd else 60,
                facecolors="none" if odd else r["color"],
                edgecolors=C_ODD if odd else "white",
                linewidths=1.5 if odd else 0.6, zorder=4 if odd else 3)
    dx, dy = LABEL_POS[r["sample_id"]]
    axA.annotate(f"{r['sample_id']} ({r['individual']})",
                 (r["gc_pct"], r["viral_reads_pct"]),
                 xytext=(r["gc_pct"] + dx, r["viral_reads_pct"] + dy),
                 fontsize=6.0, color="#333333", va="center")

axA.set_xlabel("Read GC content (%)")
axA.set_ylabel("Viral reads (%)")
axA.set_xlim(37.5, 52.5)
axA.set_ylim(-1.2, 17.5)
axA.set_title("A   Two community types  (blue = hibernating, orange = active;\n"
              "      red ring = active season but hibernating state)",
              loc="left", fontsize=7.2, pad=5)
for sp in ("top", "right"):
    axA.spines[sp].set_visible(False)

# ===== B：病毒组 Bray-Curtis ===============================================
S = ["W1", "W2", "W3", "S1", "S2", "S3"]
r = pd.read_csv(D / "votu_abundance_rpkm.tsv", sep="\t").set_index("votu_id")[S]
M = np.zeros((6, 6))
for i, a in enumerate(S):
    for j, b in enumerate(S):
        va, vb = r[a].values, r[b].values
        M[i, j] = np.abs(va - vb).sum() / (va + vb).sum()

axB = fig.add_subplot(gs[1])
im = axB.imshow(M, cmap="YlOrRd", vmin=0, vmax=1)
axB.set_xticks(range(6)); axB.set_yticks(range(6))
axB.set_xticklabels(S); axB.set_yticklabels(S)
for lab, s in zip(axB.get_xticklabels(), S):
    lab.set_color(C_WINTER if s[0] == "W" else C_SUMMER)
for lab, s in zip(axB.get_yticklabels(), S):
    lab.set_color(C_WINTER if s[0] == "W" else C_SUMMER)
for i in range(6):
    for j in range(6):
        if i != j:
            axB.text(j, i, f"{M[i,j]:.2f}", ha="center", va="center",
                     fontsize=5.4, color="white" if M[i, j] > 0.55 else "#222222")
axB.set_title("B   Viral community (Bray-Curtis)", loc="left", fontsize=7.6, pad=5)
cb = fig.colorbar(im, ax=axB, fraction=0.046, pad=0.04)
cb.ax.tick_params(labelsize=5.8, width=0.5, length=2)
cb.set_label("Distance", fontsize=6.3)
for sp in axB.spines.values():
    sp.set_visible(False)

# ===== C：16S 相似度 =======================================================
six = pd.read_csv(D / "16s_kmer_similarity.tsv", sep="\t").set_index("sample_id")
order16 = ["HF2", "HF1", "HF6", "AF5", "AF4", "AF3"]
lbl16 = ["W1/F2", "W2/F1", "W3/F6", "S1/F5", "S2/F4", "S3/F3"]
Cmat = six.loc[order16, order16].values

axC = fig.add_subplot(gs[2])
im2 = axC.imshow(Cmat, cmap="viridis", vmin=0.2, vmax=1)
axC.set_xticks(range(6)); axC.set_yticks(range(6))
axC.set_xticklabels(lbl16, rotation=30, ha="right", fontsize=6.0)
axC.tick_params(axis="y", pad=1.5)
axC.set_yticklabels(lbl16)
for lab, s in zip(axC.get_xticklabels(), order16):
    lab.set_color(C_WINTER if s[0] == "H" else C_SUMMER)
for lab, s in zip(axC.get_yticklabels(), order16):
    lab.set_color(C_WINTER if s[0] == "H" else C_SUMMER)
for i in range(6):
    for j in range(6):
        if i != j:
            axC.text(j, i, f"{Cmat[i,j]:.2f}", ha="center", va="center",
                     fontsize=5.4, color="white" if Cmat[i, j] < 0.7 else "#222222")
axC.set_title("C   16S community (k-mer cosine)", loc="left", fontsize=7.6, pad=5)
cb2 = fig.colorbar(im2, ax=axC, fraction=0.046, pad=0.04)
cb2.ax.tick_params(labelsize=5.8, width=0.5, length=2)
cb2.set_label("Similarity", fontsize=6.3)
for sp in axC.spines.values():
    sp.set_visible(False)

for ext in ("pdf", "png"):
    fig.savefig(OUT / f"FigM2_host_state_viral_community.{ext}",
                dpi=300, bbox_inches="tight", facecolor="white")

print("已输出：")
for f in sorted(OUT.iterdir()):
    print(f"  {f.name}  {f.stat().st_size/1024:.0f} KB")
print("\n关键数值：")
print(f"  S1 与冬季样本病毒距离: {[f'{M[3,i]:.2f}' for i in (0,1,2)]}")
print(f"  S1 与夏季样本病毒距离: {[f'{M[3,i]:.2f}' for i in (4,5)]}")
_i5 = order16.index("AF5")
_w = [i for i, x in enumerate(order16) if x.startswith("H")]
_s = [i for i, x in enumerate(order16) if x.startswith("A") and x != "AF5"]
print(f"  AF5 与冬季 16S 相似度: {Cmat[_i5, _w].mean():.3f}")
print(f"  AF5 与夏季 16S 相似度: {Cmat[_i5, _s].mean():.3f}")

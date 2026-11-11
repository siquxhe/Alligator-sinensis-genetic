#!/usr/bin/env python3
"""Figure M3 — 202 条中高质量病毒基因组景观

三个面板：
  A  长度 × 完整性 × 丰度：单条基因组的质量画像
  B  各样本产出的基因组数（按 CheckV 质量分级）
  C  完整度与长度的关系：短 contig 难以被判为完整，是方法学边界而非生物学差异

数据：../../05_c_stage/hq_genomes_with_abundance.tsv
输出：../output/FigM3_viral_genome_landscape.pdf / .png
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
    "legend.fontsize": 6.2,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
})

C_WINTER, C_SUMMER = "#0072B2", "#E69F00"
h = pd.read_csv(D / "hq_genomes_with_abundance.tsv", sep="\t")
h["color"] = h["season"].map({"winter": C_WINTER, "summer": C_SUMMER})

fig = plt.figure(figsize=(7.09, 2.85))
gs = GridSpec(1, 3, figure=fig, width_ratios=[1.28, 0.85, 1.0],
              wspace=0.40, left=0.068, right=0.985, top=0.86, bottom=0.20)

# ===== A：长度 × 完整性 × 丰度 =============================================
axA = fig.add_subplot(gs[0])
sizes = 8 + 34 * (np.log10(h["rpkm"] + 1) / np.log10(h["rpkm"].max() + 1))
axA.scatter(h["length"] / 1000, h["completeness"], s=sizes,
            c=h["color"], alpha=0.72, edgecolors="white", linewidths=0.35, zorder=3)
axA.set_xscale("log")
axA.set_xlabel("Genome length (kb, log scale)")
axA.set_ylabel("Completeness (%)")
axA.set_xlim(3, 300)
axA.set_ylim(40, 104)
axA.set_xticks([4, 10, 30, 100, 200])
axA.set_xticklabels(["4", "10", "30", "100", "200"])
axA.set_title("A   202 medium/high-quality genomes\n      (blue = winter, orange = summer)",
              loc="left", fontsize=7.2, pad=5)
for sp in ("top", "right"):
    axA.spines[sp].set_visible(False)

# 丰度图例（三个尺寸）
ref = [1, 10, 100]
handles = [Line2D([], [], marker="o", ls="", mfc="#999999", mec="white", ms=np.sqrt(8 + 34*(np.log10(v+1)/np.log10(h["rpkm"].max()+1)))*0.95,
                  label=f"RPKM {v}") for v in ref]
leg = axA.legend(handles=handles, loc="lower right", labelspacing=0.8,
                 handletextpad=0.8, borderpad=0.6, title="Abundance",
                 title_fontsize=6.2, frameon=True, facecolor="white",
                 edgecolor="none", framealpha=0.9)
leg._legend_box.align = "left"

# ===== B：各样本产出数 =====================================================
axB = fig.add_subplot(gs[1])
order = ["W1", "W2", "W3", "S1", "S2", "S3"]
qual_order = ["Complete", "High-quality", "Medium-quality"]
qual_colors = ["#005A8C", "#2E9BC6", "#A8D5E5"]
qual_label = {"Complete": "Complete", "High-quality": "High", "Medium-quality": "Medium"}
ct = pd.crosstab(h["sample_id"], h["checkv_quality"]).reindex(order).fillna(0)
bottom = np.zeros(len(order))
x = np.arange(len(order))
for q, col in zip(qual_order, qual_colors):
    vals = ct[q].values if q in ct else np.zeros(len(order))
    axB.bar(x, vals, bottom=bottom, width=0.68, color=col, edgecolor="white",
            linewidth=0.4, label=qual_label[q])
    bottom += vals
axB.set_xticks(x)
axB.set_xticklabels(order)
for lab, s in zip(axB.get_xticklabels(), order):
    lab.set_color(C_WINTER if s[0] == "W" else C_SUMMER)
axB.set_ylabel("Genomes (n)")
axB.set_ylim(0, 80)
axB.set_title("B   Yield per sample", loc="left", fontsize=7.6, pad=5)
for sp in ("top", "right"):
    axB.spines[sp].set_visible(False)
axB.legend(loc="upper left", handlelength=0.9, handleheight=0.8, labelspacing=0.3,
           borderpad=0.4)
for xi, tot in zip(x, bottom):
    axB.text(xi, tot + 1.2, f"{int(tot)}", ha="center", va="bottom", fontsize=6.2,
             color="#333333")

# ===== C：完整度 vs 长度（按质量分组）=====================================
axC = fig.add_subplot(gs[2])
rng = np.random.default_rng(3)
for i, q in enumerate(qual_order):
    sub = h[h["checkv_quality"] == q]
    jitter = rng.uniform(-0.16, 0.16, len(sub))
    axC.scatter(np.full(len(sub), i) + jitter, sub["length"] / 1000,
                s=13, c=qual_colors[i], alpha=0.75, edgecolors="white", linewidths=0.3)
    med = sub["length"].median() / 1000
    axC.hlines(med, i - 0.28, i + 0.28, color="#222222", lw=1.1, zorder=5)
    axC.text(i, 260, f"n={len(sub)}", ha="center", fontsize=6.0, color="#444444")

axC.set_xticks(range(3))
axC.set_xticklabels(["Complete", "High", "Medium"], fontsize=6.5)
axC.set_yscale("log")
axC.set_ylabel("Genome length (kb, log scale)")
axC.set_ylim(2.5, 330)
axC.set_yticks([5, 10, 30, 100, 200])
axC.set_yticklabels(["5", "10", "30", "100", "200"])
axC.set_title("C   Longer contigs pass stricter checks", loc="left", fontsize=7.6, pad=5)
for sp in ("top", "right"):
    axC.spines[sp].set_visible(False)

for ext in ("pdf", "png"):
    fig.savefig(OUT / f"FigM3_viral_genome_landscape.{ext}",
                dpi=300, bbox_inches="tight", facecolor="white")

print("已输出：")
for f in sorted(OUT.iterdir()):
    print(f"  {f.name}  {f.stat().st_size/1024:.0f} KB")
print("\n关键数值：")
print(f"  基因组总数 {len(h)}，Complete {len(h[h.checkv_quality=='Complete'])}")
print("  各质量长度中位: " + ", ".join(
    f"{q.split('-')[0]} {h[h.checkv_quality==q]['length'].median()/1000:.1f} kb" for q in qual_order))
print(f"  RPKM 中位 {h['rpkm'].median():.1f}，最大 {h['rpkm'].max():.1f}")

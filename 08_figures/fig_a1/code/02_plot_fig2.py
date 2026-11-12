#!/usr/bin/env python3
"""
Fig 2 —— 五口径下"病毒占比"的跨度

科学论断
--------
同一批 6 个宏基因组，仅因"口径"不同（严格性 / 参考空间 / 统计单元），
病毒占比可以从 0.089% 变到 15.23%，跨度 171 倍。

面板
----
A  五口径 × 六样本的点图（log10 y 轴），C3 以文献区间灰带表示
B  相邻口径之间的放大倍数（C2/C1、C5/C2、C4/C2），量化差异来源

输入
----
output/Table1_five_denominators.tsv

输出
----
output/Fig2_five_denominators.pdf   （矢量，投稿用）
output/Fig2_five_denominators.png   （300 dpi 预览）
"""

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
FIG = HERE.parent
OUT = FIG / "output"

SAMPLES = ["W1", "W2", "W3", "S1", "S2", "S3"]

# Okabe-Ito 色盲安全调色板
COLORS = ["#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00"]
MARKERS = ["o", "s", "^", "D", "v", "P"]

LABELS = {
    "C1": "C1\nstrict\ncategories",
    "C2": "C2\nbroad\n(all hits)",
    "C3": "C3\nliterature\nreported",
    "C4": "C4\ncontig\ncounts",
    "C5": "C5\nvOTU\nreference",
}

C3_LOW, C3_HIGH = 0.04, 4.03


def style() -> None:
    mpl.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
            "font.size": 8,
            "axes.labelsize": 8,
            "axes.titlesize": 9,
            "xtick.labelsize": 7,
            "ytick.labelsize": 7,
            "axes.linewidth": 0.7,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        }
    )


def main() -> None:
    style()
    t = pd.read_csv(OUT / "Table1_five_denominators.tsv", sep="\t")
    t = t.set_index("口径")

    fig, (ax1, ax2) = plt.subplots(
        1, 2, figsize=(7.2, 3.4), gridspec_kw={"width_ratios": [1.55, 1]}
    )

    codes = ["C1", "C2", "C3", "C4", "C5"]
    xpos = np.arange(len(codes))

    # ---------------- Panel A
    # C3 文献区间
    ax1.axhspan(C3_LOW, C3_HIGH, xmin=0.492, xmax=0.584, color="0.88", zorder=0, linewidth=0)
    ax1.text(2, C3_HIGH * 1.35, "reported range\n0.04–4.03%", ha="center", va="bottom", fontsize=6, color="0.35")

    for i, s in enumerate(SAMPLES):
        xs, ys = [], []
        for j, c in enumerate(codes):
            v = t.loc[c, s]
            if pd.notna(v):
                xs.append(j)
                ys.append(float(v))
        ax1.scatter(
            xs,
            ys,
            s=26,
            marker=MARKERS[i],
            facecolor=COLORS[i],
            edgecolor="white",
            linewidth=0.5,
            label=s,
            zorder=3,
        )

    # 每个口径的中位数横线
    for j, c in enumerate(codes):
        vals = [float(t.loc[c, s]) for s in SAMPLES if pd.notna(t.loc[c, s])]
        if vals:
            ax1.hlines(np.median(vals), j - 0.28, j + 0.28, color="0.25", linewidth=1.0, zorder=2)

    ax1.set_yscale("log")
    ax1.set_ylim(0.05, 40)
    ax1.set_xticks(xpos)
    ax1.set_xticklabels([LABELS[c] for c in codes], fontsize=6.5)
    ax1.set_ylabel("Viral fraction of reads (%)")
    ax1.set_title("A  Five definitions, one dataset", loc="left", fontweight="bold")
    ax1.legend(
        title="Sample", title_fontsize=6.5, fontsize=6.5, frameon=False,
        loc="upper left", ncol=3, handletextpad=0.3, columnspacing=0.8,
    )
    ax1.grid(axis="y", color="0.9", linewidth=0.5, zorder=0)
    ax1.set_axisbelow(True)

    # 171× 跨度标注（放在 C1 左侧，避开数据点）
    ax1.annotate(
        "",
        xy=(-0.42, 0.0891),
        xytext=(-0.42, 15.23),
        arrowprops=dict(arrowstyle="<->", color="#D55E00", linewidth=0.9, shrinkA=0, shrinkB=0),
    )
    # 171× 为"全口径 × 全样本"的 min–max 跨度，非同一样本内的比较（见 figA1_log）
    ax1.text(
        -0.66, 1.15, "171×\noverall", color="#D55E00", fontsize=8.0, fontweight="bold",
        rotation=90, ha="center", va="center", linespacing=1.2,
    )
    ax1.set_xlim(-0.85, 4.45)

    # ---------------- Panel B：相邻口径放大倍数
    ratios = []
    names = []
    for a, b in [("C1", "C2"), ("C2", "C5"), ("C2", "C4")]:
        ra = [float(t.loc[b, s]) / float(t.loc[a, s]) for s in SAMPLES]
        ratios.append(ra)
        names.append(f"{b}/{a}")

    bp = ax2.boxplot(
        ratios, orientation="vertical", widths=0.5, patch_artist=True,
        medianprops=dict(color="0.2", linewidth=1.0),
        flierprops=dict(marker="o", markersize=3, markerfacecolor="none", markeredgecolor="0.4", linewidth=0.5),
        whiskerprops=dict(linewidth=0.7), capprops=dict(linewidth=0.7),
    )
    for patch, c in zip(bp["boxes"], ["#56B4E9", "#009E73", "#CC79A7"]):
        patch.set_facecolor(c)
        patch.set_alpha(0.55)
        patch.set_edgecolor("0.3")
        patch.set_linewidth(0.7)

    for i, ra in enumerate(ratios, start=1):
        jitter = np.random.default_rng(0).normal(0, 0.045, len(ra))
        ax2.scatter(i + jitter, ra, s=18, color="0.25", zorder=3, linewidth=0)

    ax2.axhline(1, color="0.5", linewidth=0.7, linestyle="--", zorder=1)
    ax2.set_yscale("log")
    ax2.set_ylim(0.8, 70)
    ax2.set_xticks([1, 2, 3])
    ax2.set_xticklabels(["category filter\nC2 / C1", "reference space\nC5 / C2", "statistical unit\nC4 / C2"], fontsize=6.0)
    ax2.set_ylabel("Fold change")
    ax2.set_title("B  What drives the gap", loc="left", fontweight="bold")
    ax2.grid(axis="y", color="0.9", linewidth=0.5, zorder=0)
    ax2.set_axisbelow(True)

    # 倍数标注：统一放在箱体上方，避免飘到画布边缘
    for i, ra in enumerate(ratios, start=1):
        ax2.text(i, 42, f"{np.median(ra):.1f}×", ha="center", va="center", fontsize=7.5, color="0.15", fontweight="bold")

    fig.tight_layout(pad=0.6)
    fig.savefig(OUT / "Fig2_five_denominators.pdf", bbox_inches="tight")
    fig.savefig(OUT / "Fig2_five_denominators.png", dpi=300, bbox_inches="tight")

    print("Fig 2 已输出:")
    print(f"  {OUT / 'Fig2_five_denominators.pdf'}")
    print(f"  {OUT / 'Fig2_five_denominators.png'}")
    print()
    for n, ra in zip(names, ratios):
        print(f"  {n}: median {np.median(ra):.1f}×  (range {min(ra):.1f}–{max(ra):.1f}×)")


if __name__ == "__main__":
    main()

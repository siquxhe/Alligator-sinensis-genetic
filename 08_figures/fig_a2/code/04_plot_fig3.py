#!/usr/bin/env python3
"""
Fig 3 —— "共享 vOTU"是一个阈值的函数

科学论断
--------
同一批 6 个样本，contig 层面共享 vOTU 为 0，reads 层面从 783 到 1 不等。
"六个样本零共享"不是生物学结论，是"用什么算存在"的产物。

面板
----
A  6 样本共享 vOTU 数随判定阈值变化（log10 y）；contig 基线为 0
B  单样本特有 vOTU 比例随阈值变化（U 型：两端高，机制不同）
C  15 个样本对的 Jaccard 相似度：contig 口径 vs reads 口径

输入
----
matrices/threshold_sweep.tsv、matrices/jaccard_pairs.tsv

输出
----
output/Fig3_shared_votu.pdf   （矢量）
output/Fig3_shared_votu.png   （300 dpi）
"""

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
FIG = HERE.parent
MAT = FIG / "matrices"
OUT = FIG / "output"
OUT.mkdir(exist_ok=True)

C_CONTIG = "#D55E00"   # 朱红：contig 口径
C_READS = "#0072B2"    # 蓝：reads 口径


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
    sw = pd.read_csv(MAT / "threshold_sweep.tsv", sep="\t")
    jac = pd.read_csv(MAT / "jaccard_pairs.tsv", sep="\t")

    fig, axes = plt.subplots(1, 3, figsize=(7.2, 2.9))
    ax1, ax2, ax3 = axes

    xlab = ["contig", "RPKM>0", "≥0.01", "≥0.1", "≥1", "≥10"]
    xpos = np.arange(len(xlab))

    # ---------------- A：共享 vOTU 数
    shared = sw["shared_all6"].values.astype(float)
    heights = shared.copy()
    heights[0] = 0.4  # contig=0 在 log 轴上用下限占位

    colors = [C_CONTIG] + [C_READS] * 5
    ax1.bar(xpos, heights, width=0.62, color=colors, edgecolor="0.25", linewidth=0.5, zorder=3)

    for i, v in enumerate(shared):
        if v == 0:
            ax1.text(i, 0.45, "0", ha="center", va="bottom", fontsize=7, fontweight="bold", color=C_CONTIG)
        else:
            ax1.text(i, v * 1.25, f"{int(v)}", ha="center", va="bottom", fontsize=6.5, color="0.2")

    ax1.set_yscale("log")
    ax1.set_ylim(0.35, 3000)
    ax1.set_xticks(xpos)
    ax1.set_xticklabels(xlab, rotation=35, ha="right", fontsize=6.5)
    ax1.set_ylabel("vOTUs shared by all 6 samples")
    ax1.set_title("A  Shared vOTUs depend on threshold", loc="left", fontweight="bold")
    ax1.grid(axis="y", color="0.9", linewidth=0.5, zorder=0)
    ax1.set_axisbelow(True)

    # ---------------- B：单样本特有比例
    sing = sw["singleton_pct"].values.astype(float)
    ax2.plot(xpos, sing, "-o", color="0.25", markersize=4.5, linewidth=1.0, zorder=3,
             markerfacecolor="white", markeredgewidth=1.0)
    ax2.scatter(xpos[:1], sing[:1], s=34, color=C_CONTIG, zorder=4, edgecolor="white", linewidth=0.5)
    ax2.scatter(xpos[1:], sing[1:], s=34, color=C_READS, zorder=4, edgecolor="white", linewidth=0.5)

    ax2.set_xticks(xpos)
    ax2.set_xticklabels(xlab, rotation=35, ha="right", fontsize=6.5)
    ax2.set_ylabel("Singleton vOTUs (%)")
    ax2.set_ylim(0, 95)
    ax2.set_title("B  Two peaks, two causes", loc="left", fontweight="bold")
    ax2.grid(axis="y", color="0.9", linewidth=0.5, zorder=0)
    ax2.set_axisbelow(True)

    # 两个峰的注释
    ax2.annotate("assembly\nfragmentation", xy=(0, 84.5), xytext=(0.35, 66),
                 fontsize=6, color=C_CONTIG, ha="left", va="center",
                 arrowprops=dict(arrowstyle="->", color=C_CONTIG, linewidth=0.6))
    ax2.annotate("true sample-\nspecific viruses", xy=(5, 55.2), xytext=(3.1, 30),
                 fontsize=6, color=C_READS, ha="left", va="center",
                 arrowprops=dict(arrowstyle="->", color=C_READS, linewidth=0.6))

    # ---------------- C：Jaccard 对比
    lim = 0.045
    ax3.plot([0, lim], [0, lim], color="0.6", linewidth=0.7, linestyle="--", zorder=1)
    ax3.scatter(jac["jaccard_contig"], jac["jaccard_reads_rpkm1"],
                s=26, color=C_READS, edgecolor="white", linewidth=0.5, zorder=3, alpha=0.85)

    ax3.set_xlim(0, lim)
    ax3.set_ylim(0, lim)
    ax3.set_xlabel("Jaccard (contig presence)")
    ax3.set_ylabel("Jaccard (reads RPKM≥1)")
    ax3.set_title("C  Every pair, both ways", loc="left", fontweight="bold")
    ax3.grid(color="0.93", linewidth=0.5, zorder=0)
    ax3.set_axisbelow(True)

    ax3.text(lim * 0.97, lim * 0.90,
             f"median\n{jac.jaccard_contig.median():.3f} → {jac.jaccard_reads_rpkm1.median():.3f}\n"
             f"{jac.jaccard_reads_rpkm1.median()/jac.jaccard_contig.median():.1f}×",
             ha="right", va="top", fontsize=6.3, color="0.3")

    fig.tight_layout(pad=0.5)
    fig.savefig(OUT / "Fig3_shared_votu.pdf", bbox_inches="tight")
    fig.savefig(OUT / "Fig3_shared_votu.png", dpi=300, bbox_inches="tight")

    print("Fig 3 已输出:")
    print(f"  {OUT / 'Fig3_shared_votu.pdf'}")
    print(f"  {OUT / 'Fig3_shared_votu.png'}")


if __name__ == "__main__":
    main()

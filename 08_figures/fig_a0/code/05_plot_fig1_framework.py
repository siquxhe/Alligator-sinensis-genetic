#!/usr/bin/env python3
"""
Fig 1 —— 病毒占比的四个决策维度

定位
----
这是一张概念/示意图，不依赖新计算；但每个维度标注了**在本批数据上的实测影响**，
使它与泛泛的流程图不同：读者能直接看到"哪个选择真正改变了结论"。

四个维度
--------
1. 分母 (Denominator)        影响 1.1×（本例小，因宿主占比低）
2. 参考空间 (Reference space) 影响 5.6×
3. 证据门槛 (Evidence threshold) 影响 7.1×
4. 统计单元 (Statistical unit)   影响 5.4×

实测极值：0.089% – 15.23%，总跨度 171×
（各维度倍数为"其余维度固定时的比值"，不可直接相乘——口径组合不完全正交）

输出
----
output/Fig1_framework.pdf / .png
"""

from pathlib import Path
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

HERE = Path(__file__).resolve().parent
FIG = HERE.parent
OUT = FIG / "output"
OUT.mkdir(exist_ok=True)

BLUE = "#0072B2"
ORANGE = "#D55E00"
GREEN = "#009E73"
GREY = "#6E6E6E"

DIMS = [
    {
        "name": "Denominator",
        "sub": "what counts as 100%",
        "options": ["All clean reads", "Host-depleted reads", "Total vOTUs"],
        "fold": "1.1×",
        "note": "small here —\nhost fraction is low",
        "color": GREY,
    },
    {
        "name": "Reference space",
        "sub": "what you compare against",
        "options": ["Public nr", "Local vOTUs", "Contig set"],
        "fold": "5.6×",
        "note": "local DB recovers\nmore viral reads",
        "color": BLUE,
    },
    {
        "name": "Evidence threshold",
        "sub": "how much proof is required",
        "options": ["Any hit", "Functional only", "ANI + coverage"],
        "fold": "7.1×",
        "note": "largest single\neffect here",
        "color": ORANGE,
    },
    {
        "name": "Statistical unit",
        "sub": "reads or fragments",
        "options": ["Read counts", "RPKM weighted", "Presence / absence"],
        "fold": "5.4×",
        "note": "contig-level inflation\n≠ more virus",
        "color": GREEN,
    },
]


def style() -> None:
    mpl.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
            "font.size": 8,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        }
    )


def box(ax, x, y, w, h, text, fc="white", ec="0.55", fs=6.6, tc="0.15", bold=False, lw=0.7):
    p = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.02,rounding_size=0.06",
        facecolor=fc, edgecolor=ec, linewidth=lw, zorder=2,
    )
    ax.add_patch(p)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
            fontsize=fs, color=tc, zorder=3,
            fontweight="bold" if bold else "normal", linespacing=1.25)
    return p


def main() -> None:
    style()
    fig, ax = plt.subplots(figsize=(7.2, 4.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10.4)
    ax.axis("off")

    # ---------------- 标题
    ax.text(0.15, 10.05, "One dataset, four decisions, 171-fold range",
            fontsize=10, fontweight="bold", color="0.1", ha="left", va="top")
    ax.text(0.15, 9.55,
            "Each row is a choice that must be made before any viral fraction can be reported.",
            fontsize=7.2, color="0.35", ha="left", va="top", style="italic")

    # ---------------- 左：输入
    box(ax, 0.15, 7.55, 1.55, 1.05, "6 fecal\nmetagenomes\nPRJNA539906", fc="#F2F2F2", fs=6.2)
    ax.annotate("", xy=(2.05, 8.05), xytext=(1.72, 8.05),
                arrowprops=dict(arrowstyle="-|>", color="0.45", linewidth=0.9))

    # ---------------- 四个维度
    y0 = 8.55
    row_h = 1.75
    opt_w, opt_h = 1.26, 0.52
    x_opt0 = 3.72

    for i, d in enumerate(DIMS):
        y = y0 - i * row_h

        # 维度名（左）
        ax.text(1.95, y + 0.58, d["name"], fontsize=7.0, fontweight="bold",
                color=d["color"], ha="left", va="center")
        ax.text(1.95, y + 0.26, d["sub"], fontsize=5.5, color="0.45",
                ha="left", va="center", style="italic")

        # 选项框
        for j, opt in enumerate(d["options"]):
            x = x_opt0 + j * (opt_w + 0.16)
            fc = "#FFFFFF" if j == 0 else ("#F7FBFF" if d["color"] == BLUE else "white")
            box(ax, x, y + 0.05, opt_w, opt_h, opt, fs=5.9, ec="0.65", lw=0.55)

        # 影响倍数（移入列内，注释置于其下方，避免与箭头冲突）
        ax.text(8.55, y + 0.46, d["fold"], fontsize=10.5, fontweight="bold",
                color=d["color"], ha="center", va="center")
        ax.text(8.55, y + 0.10, d["note"], fontsize=5.0, color="0.42",
                ha="center", va="center", linespacing=1.35)

    # ---------------- 结果区
    box(ax, 1.95, 0.62, 6.40, 1.30,
        "Viral fraction of a gut metagenome\n"
        "0.089 % — 0.122 %  (strict)      0.675 % — 0.702 %  (permissive)\n"
        "contig level  1.4 % — 13.3 %      vOTU level  2.1 % — 15.2 %",
        fc="#FFF8F2", ec=ORANGE, fs=6.8, lw=0.9)

    ax.text(8.35, 2.06, "171× overall span", fontsize=8.5, fontweight="bold",
            color=ORANGE, ha="right", va="bottom")

    # ---------------- 底部注
    ax.text(0.15, 0.12,
            "Fold ranges are measured in this dataset with the other three dimensions held fixed; "
            "they are not strictly multiplicative.",
            fontsize=5.8, color="0.5", ha="left", va="bottom")

    fig.tight_layout(pad=0.3)
    fig.savefig(OUT / "Fig1_framework.pdf", bbox_inches="tight")
    fig.savefig(OUT / "Fig1_framework.png", dpi=300, bbox_inches="tight")

    print("Fig 1 已输出:")
    print(f"  {OUT / 'Fig1_framework.pdf'}")
    print(f"  {OUT / 'Fig1_framework.png'}")


if __name__ == "__main__":
    main()

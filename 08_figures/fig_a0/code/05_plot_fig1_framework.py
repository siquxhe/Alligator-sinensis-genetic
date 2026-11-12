#!/usr/bin/env python3
"""
Fig 1 —— 病毒占比的四个决策维度

定位
----
概念图，但每个维度标注的是**在本批数据上实测的倍数**，且这些倍数来自
`08_figures/fig_a1/output/Table1_five_denominators.tsv`，不是脚本里的字面量。
上游一重算，本图跟着变；若数值漂移超出断言范围，直接报错而不是静默出图。

四个维度
--------
1. 分母 (Denominator)          C2 / C6   实测 ≈1.01×（粪便样本中几乎无影响）
2. 参考空间 (Reference space)   C5 / C2   实测 ≈5.6×
3. 类别筛选 (Category filter)   C2 / C1   实测 ≈7.1×（最大单项效应）
4. 统计单元 (Statistical unit)  C4 / C2   实测 ≈5.4×

全口径极值 0.089% – 15.23%，总跨度 ≈171×。
该跨度须分解：同一样本内 C5/C1 已达 22–125×（纯定义效应），
跨样本的 C1 极差仅 1.37×（样本效应）。171× ≈ 125× × 1.37×。

注意：这些倍数不可相乘——各比值来自不同样本与不同口径组合，口径不完全正交。

输入
----
../fig_a1/output/Table1_five_denominators.tsv

输出
----
output/Fig1_framework.pdf / .png
"""

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

HERE = Path(__file__).resolve().parent
FIG = HERE.parent
OUT = FIG / "output"
OUT.mkdir(exist_ok=True)
TAB = FIG.parent / "fig_a1" / "output" / "Table1_five_denominators.tsv"

SAMPLES = ["W1", "W2", "W3", "S1", "S2", "S3"]

BLUE = "#0072B2"
ORANGE = "#D55E00"
GREEN = "#009E73"
GREY = "#7A7A7A"


# ---------------------------------------------------------------- 读上游
def load_numbers() -> dict:
    t = pd.read_csv(TAB, sep="\t").set_index("口径")

    def vals(code: str) -> np.ndarray:
        return np.array([float(t.loc[code, s]) for s in SAMPLES])

    c1, c2, c4, c5, c6 = (vals(c) for c in ["C1", "C2", "C4", "C5", "C6"])

    # 各维度倍数：逐样本求比值后取中位，避免单样本极值主导
    fold_cat = float(np.median(c2 / c1))     # 类别筛选
    fold_ref = float(np.median(c5 / c2))     # 参考空间
    fold_unit = float(np.median(c4 / c2))    # 统计单元
    fold_den = float(np.max(c2 / c6))        # 分母（取最大影响）

    # 同一批定义、同一样本内的定义效应
    within = c5 / c1
    # 样本效应：固定最严口径 C1 时的跨样本极差
    sample_effect = float(c1.max() / c1.min())

    allv = np.concatenate([c1, c2, c4, c5, c6])
    gmin, gmax = float(allv.min()), float(allv.max())

    return dict(
        c1=(float(c1.min()), float(c1.max())),
        c2=(float(c2.min()), float(c2.max())),
        c4=(float(c4.min()), float(c4.max())),
        c5=(float(c5.min()), float(c5.max())),
        fold_cat=fold_cat,
        fold_ref=fold_ref,
        fold_unit=fold_unit,
        fold_den=fold_den,
        within=(float(within.min()), float(within.max())),
        sample_effect=sample_effect,
        gmin=gmin,
        gmax=gmax,
        overall=gmax / gmin,
    )


def check(n: dict) -> None:
    """与上游输出一致性断言：数值漂移即报错，不静默出图。"""
    assert 6.7 <= n["fold_cat"] <= 7.6, f"类别筛选倍数异常 {n['fold_cat']:.2f}，请重跑 fig_a1"
    assert 5.0 <= n["fold_ref"] <= 6.5, f"参考空间倍数异常 {n['fold_ref']:.2f}，请重跑 fig_a1"
    assert 5.0 <= n["fold_unit"] <= 6.0, f"统计单元倍数异常 {n['fold_unit']:.2f}，请重跑 fig_a1"
    assert n["fold_den"] <= 1.05, f"分母倍数异常 {n['fold_den']:.3f}，检查 C6 分母是否为去宿主前计数"
    assert 155 <= n["overall"] <= 185, f"总跨度异常 {n['overall']:.0f}×，请重跑 fig_a1"
    assert n["gmin"] < 0.1 and n["gmax"] > 15.0, "极值区间不符合预期"


def build_dims(n: dict) -> list[dict]:
    den = f"{n['fold_den']:.2f}×" if n["fold_den"] < 1.05 else f"{n['fold_den']:.1f}×"
    return [
        {
            "name": "Denominator",
            "sub": "what counts as 100%",
            "options": ["All QC reads\n(host retained)", "Host-depleted\nreads"],
            "fold": den,
            "note": "host depletion\nchanges <1.2% here;\nnot so in tissue",
            "color": GREY,
        },
        {
            "name": "Reference space",
            "sub": "what you compare against",
            "options": ["RVDB-prot", "Local vOTUs", "nr (literature)"],
            "fold": f"{n['fold_ref']:.1f}×",
            "note": "local DB recovers\nmore viral reads",
            "color": BLUE,
        },
        {
            "name": "Category filter",
            "sub": "which viral-like hits count",
            "options": ["Any viral-\nlike hit", "Structural +\nreplication", "Genome-\nresolved"],
            "fold": f"{n['fold_cat']:.1f}×",
            "note": "excludes metabolic /\nhousekeeping categories\n(homology, not proof)",
            "color": ORANGE,
        },
        {
            "name": "Statistical unit",
            "sub": "what you count",
            "options": ["Read counts", "RPKM weighted", "Presence /\nabsence"],
            "fold": f"{n['fold_unit']:.1f}×",
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
            fontweight="bold" if bold else "normal", linespacing=1.2)
    return p


def main() -> None:
    n = load_numbers()
    check(n)
    DIMS = build_dims(n)

    style()
    fig, ax = plt.subplots(figsize=(7.2, 4.9))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10.4)
    ax.axis("off")

    # ---------------- 标题
    ax.text(0.15, 10.32, f"One dataset, four decisions, {n['overall']:.0f}-fold range",
            fontsize=10, fontweight="bold", color="0.1", ha="left", va="top")
    ax.text(0.15, 9.94,
            f"Within a single sample, definitions alone span "
            f"{n['within'][0]:.0f}–{n['within'][1]:.0f}×; across samples the extreme reaches "
            f"{n['overall']:.0f}×.",
            fontsize=7.0, color="0.35", ha="left", va="top", style="italic")
    ax.text(0.15, 9.58,
            "Each row is a choice that must be made before any viral fraction can be reported.",
            fontsize=7.0, color="0.35", ha="left", va="top", style="italic")

    # ---------------- 左侧输入
    y0 = 8.25
    row_h = 1.62
    opt_w, opt_h = 1.26, 0.58
    x_opt0 = 3.72
    y_first_center = y0 + 0.31

    box(ax, 0.15, y_first_center - 0.52, 1.50, 1.04,
        "6 fecal\nmetagenomes\nPRJNA539906", fc="#F2F2F2", fs=6.2)
    ax.annotate("", xy=(1.90, y_first_center), xytext=(1.68, y_first_center),
                arrowprops=dict(arrowstyle="-|>", color="0.45", linewidth=0.9))

    # ---------------- 四个维度
    for i, d in enumerate(DIMS):
        y = y0 - i * row_h

        ax.text(1.95, y + 0.42, d["name"], fontsize=7.0, fontweight="bold",
                color=d["color"], ha="left", va="center")
        ax.text(1.95, y + 0.13, d["sub"], fontsize=5.5, color="0.45",
                ha="left", va="center", style="italic")

        for j, opt in enumerate(d["options"]):
            x = x_opt0 + j * (opt_w + 0.16)
            box(ax, x, y + 0.02, opt_w, opt_h, opt, fs=5.7, ec="0.65", lw=0.55)

        ax.text(8.62, y + 0.44, d["fold"], fontsize=10.5, fontweight="bold",
                color=d["color"], ha="center", va="center")
        ax.text(8.62, y - 0.02, d["note"], fontsize=4.9, color="0.42",
                ha="center", va="center", linespacing=1.35)

    # ---------------- 结果区
    c1lo, c1hi = n["c1"]
    c2lo, c2hi = n["c2"]
    c4lo, c4hi = n["c4"]
    c5lo, c5hi = n["c5"]
    box(ax, 1.95, 1.08, 6.40, 1.38,
        "Viral fraction of a gut metagenome\n"
        f"{c1lo:.3f} % — {c1hi:.3f} %   (strict)        "
        f"{c2lo:.3f} % — {c2hi:.3f} %   (broad)\n"
        f"contig level  {c4lo:.1f} % — {c4hi:.1f} %      "
        f"vOTU level  {c5lo:.1f} % — {c5hi:.1f} %",
        fc="#FFF8F2", ec=ORANGE, fs=6.8, lw=0.9)

    ax.text(8.35, 2.62, f"{n['overall']:.0f}× overall span", fontsize=8.5, fontweight="bold",
            color=ORANGE, ha="right", va="bottom")

    # ---------------- 底部注
    ax.text(0.15, 0.42,
            "Fold ranges are measured in this dataset with the other dimensions held fixed; "
            "they are not strictly multiplicative. Values are read from Table 1 at run time.",
            fontsize=5.8, color="0.5", ha="left", va="bottom")

    fig.tight_layout(pad=0.3)
    fig.savefig(OUT / "Fig1_framework.pdf", bbox_inches="tight")
    fig.savefig(OUT / "Fig1_framework.png", dpi=300, bbox_inches="tight")

    print("Fig 1 已输出:")
    print(f"  {OUT / 'Fig1_framework.pdf'}")
    print(f"  {OUT / 'Fig1_framework.png'}")
    print()
    print(f"  分母 C2/C6      {n['fold_den']:.3f}×")
    print(f"  参考空间 C5/C2  {n['fold_ref']:.2f}×")
    print(f"  类别筛选 C2/C1  {n['fold_cat']:.2f}×")
    print(f"  统计单元 C4/C2  {n['fold_unit']:.2f}×")
    print(f"  同一样本内 C5/C1 {n['within'][0]:.1f}–{n['within'][1]:.1f}×")
    print(f"  样本效应         {n['sample_effect']:.2f}×")
    print(f"  总跨度           {n['overall']:.0f}×  ({n['gmin']:.4g}% – {n['gmax']:.4g}%)")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Figure M1 (v2) — 按交叉验证后的新口径重画

与 v1 的差别
  v1 用单一"病毒样 reads 0.69%"作为结论，并把 best-hit 物种构成画成主面板；
  交叉验证表明 47.4% 的命中落在巨型病毒携带的管家酶上、仅 1.3% 落在结构蛋白上，
  且信号在 60% 一致性处断崖。故 v2：
    - 保留 QC 与宿主率（事实层）；
    - 新增"信号强度随阈值衰减"面板（C），把断崖与 G1 门槛画在一起；
    - 用"功能构成"（D）取代物种构成，直接呈现 47.4% 管家酶这一关键事实。

数据来源
  ../../09_tables/M1_summary.csv
  ../../09_tables/viral_stringency_ladder.tsv
  ../../09_tables/viral_function_profile.tsv
  ../../09_tables/viral_specific_estimate.tsv

输出
  ../output/FigM1_v2_signal_validation.pdf / .png (300 dpi)
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
TAB = PROJ / "09_tables"
OUT = Path(__file__).resolve().parents[1] / "output"
OUT.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans"],
    "font.size": 7,
    "axes.linewidth": 0.6,
    "axes.labelsize": 7.5,
    "xtick.labelsize": 7,
    "ytick.labelsize": 7,
    "xtick.major.width": 0.6,
    "ytick.major.width": 0.6,
    "xtick.major.size": 2.5,
    "ytick.major.size": 2.5,
    "legend.frameon": False,
    "legend.fontsize": 6.2,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
})

C_WINTER, C_SUMMER, C_GREY = "#0072B2", "#E69F00", "#666666"

m1 = pd.read_csv(TAB / "M1_summary.csv")
order = ["W1", "W2", "W3", "S1", "S2", "S3"]
m1["sample_id"] = pd.Categorical(m1["sample_id"], order, ordered=True)
m1 = m1.sort_values("sample_id").reset_index(drop=True)
season_col = {"winter": C_WINTER, "summer": C_SUMMER}
cols = [season_col[s] for s in m1["season"]]
y = np.arange(len(m1))[::-1]
w_mask = (m1["season"] == "winter").to_numpy()

fig = plt.figure(figsize=(7.09, 6.15))
gs = GridSpec(3, 2, figure=fig, height_ratios=[0.92, 1.10, 1.02],
              width_ratios=[0.86, 1.14], hspace=0.62, wspace=0.34,
              left=0.105, right=0.978, top=0.945, bottom=0.075)

# ===== A：质控 ============================================================
axA = fig.add_subplot(gs[0, :])
before = m1["q30_before_pct"].to_numpy()
after = m1["q30_after_pct"].to_numpy()
for yi, b, a in zip(y, before, after):
    axA.annotate("", xy=(a, yi), xytext=(b, yi),
                 arrowprops=dict(arrowstyle="-|>,head_width=0.15,head_length=0.35",
                                 color="#BBBBBB", lw=1.0, shrinkA=2.5, shrinkB=2.5))
axA.scatter(before, y, s=20, facecolors="white", edgecolors=C_GREY,
            linewidths=0.8, zorder=3)
axA.scatter(after, y, s=26, c=cols, edgecolors="white", linewidths=0.5, zorder=4)
for yi, (_, r) in zip(y, m1.iterrows()):
    axA.text(r["q30_after_pct"] + 0.35, yi,
             f"{r['q30_after_pct']:.1f}%   (retained {r['pass_rate_pct']:.1f}%)",
             va="center", ha="left", fontsize=6.2, color="#333333")
axA.set_yticks(y)
axA.set_yticklabels(list(order))
for lab, s in zip(axA.get_yticklabels(), m1["season"]):
    lab.set_color(season_col[s])
axA.set_ylim(-0.7, len(m1) - 0.3)
axA.set_xlim(before.min() - 1.2, after.max() + 7.4)
axA.set_xticks([85, 90, 95, 100])
axA.set_xlabel("Q30 bases (%)")
axA.set_title("A   Read quality before (open) and after (filled) trimming",
              loc="left", fontsize=8, pad=6)
for sp in ("top", "right"):
    axA.spines[sp].set_visible(False)

# ===== B：宿主去除率 ======================================================
axB = fig.add_subplot(gs[1, 0])
host = m1["host_aligned_pct"].to_numpy()
axB.scatter(np.zeros(w_mask.sum()), host[w_mask], s=34, c=C_WINTER,
            edgecolors="white", linewidths=0.5, zorder=3)
axB.scatter(np.ones((~w_mask).sum()), host[~w_mask], s=34, c=C_SUMMER,
            edgecolors="white", linewidths=0.5, zorder=3)
for xi, sub in ((0, host[w_mask]), (1, host[~w_mask])):
    med = np.median(sub)
    axB.hlines(med, xi - 0.22, xi + 0.22, color="#333333", lw=1.2, zorder=4)
    axB.text(xi + 0.28, med, f"{med:.2f}%", va="center", ha="left",
             fontsize=6.2, color="#333333")
axB.set_yscale("log")
axB.set_xlim(-0.5, 1.75)
axB.set_ylim(0.04, 6)
axB.set_xticks([0, 1])
axB.set_xticklabels(["Winter", "Summer"])
axB.set_ylabel("Host-aligned reads (%)")
axB.set_title("B   Host depletion", loc="left", fontsize=8, pad=6)
for sp in ("top", "right"):
    axB.spines[sp].set_visible(False)

# ===== C：信号随阈值衰减 ==================================================
axC = fig.add_subplot(gs[1, 1])
lad = pd.read_csv(TAB / "viral_stringency_ladder.tsv", sep="\t")
label_map = {
    "e1e-5, id>=40, len>=30 (current)": "id\u226540\nlen\u226530",
    "id>=50, len>=40": "id\u226550\nlen\u226540",
    "id>=60, len>=50": "id\u226560\nlen\u226550",
    "id>=70, len>=50": "id\u226570\nlen\u226550",
    "id>=80, len>=50": "id\u226580\nlen\u226550",
    "id>=90, len>=50": "id\u226590\nlen\u226550",
}
lad["short"] = lad["threshold"].map(label_map)
xs_order = list(label_map.values())
piv = lad.pivot_table(index="short", columns="run_accession",
                      values="viral_reads_pct").reindex(xs_order)

FLOOR = 2e-5  # 对数轴上的"检出下限"占位
xs = np.arange(len(xs_order))
for run in piv.columns:
    vals = piv[run].to_numpy(dtype=float)
    plotted = np.where(vals > 0, vals, FLOOR)
    axC.plot(xs, plotted, color="#CCCCCC", lw=0.8, zorder=1)
mean_vals = piv.mean(axis=1).to_numpy(dtype=float)
axC.plot(xs, np.where(mean_vals > 0, mean_vals, FLOOR), color="#222222",
         lw=1.4, marker="o", ms=3.2, zorder=3, label="Mean of 6 samples")
axC.plot([], [], color="#CCCCCC", lw=0.8, label="Individual samples")
zero_x = [i for i, v in enumerate(mean_vals) if v <= 0]
if zero_x:
    axC.scatter(zero_x, [FLOOR] * len(zero_x), marker="v", s=26,
                facecolors="white", edgecolors="#222222", linewidths=0.9,
                zorder=4)
    axC.text(np.mean(zero_x) + 0.15, FLOOR * 2.4, "no reads\ndetected",
             ha="center", va="bottom", fontsize=6.0, color="#444444")

axC.axhline(0.01, color="#D55E00", lw=0.9, ls=(0, (4, 2.5)), zorder=2)
axC.text(3.30, 0.0125, "G1 threshold 0.01%", color="#D55E00",
         fontsize=6.0, ha="left", va="bottom")

axC.set_yscale("log")
axC.set_ylim(1e-5, 5)
axC.set_xlim(-0.35, len(xs) - 0.35)
axC.set_xticks(xs)
axC.set_xticklabels(xs_order, fontsize=6.3)
axC.set_ylabel("Viral-like reads (%)")
axC.set_xlabel("Alignment stringency")
axC.set_title("C   Signal collapses above 60% identity", loc="left",
              fontsize=8, pad=6)
for sp in ("top", "right"):
    axC.spines[sp].set_visible(False)
axC.legend(loc="upper right", handlelength=1.3)

# 三种口径的数值角标（放左下空白区，避开曲线与 G1 线）
spec = pd.read_csv(TAB / "viral_specific_estimate.tsv", sep="\t")
axC.text(0.055, 0.035,
         f"viral-like  {spec['viral_like_pct'].astype(float).mean():.3f}%\n"
         f"viral-specific  {spec['viral_specific_pct'].astype(float).mean():.3f}%\n"
         f"structural only  {spec['structural_only_pct'].astype(float).mean():.4f}%",
         transform=axC.transAxes, ha="left", va="bottom", fontsize=6.0,
         color="#333333", linespacing=1.35)

# ===== D：功能构成 ========================================================
axD = fig.add_subplot(gs[2, :])
fp = pd.read_csv(TAB / "viral_function_profile.tsv", sep="\t")
fp = fp[fp["run_accession"] != "ALL"].copy()
fp["sample_id"] = fp["run_accession"].map(dict(zip(m1["run_accession"], m1["sample_id"])))
fp = fp.set_index("sample_id").loc[order]

CATS = ["Structural / virion", "Replication / transcription",
        "Metabolic / housekeeping", "Hypothetical / uncharacterized",
        "Other annotated"]
CAT_COLORS = ["#0072B2", "#56B4E9", "#D55E00", "#999999", "#DDDDDD"]
CAT_LABELS = ["Structural / virion", "Replication / transcription",
              "Metabolic / housekeeping (host-derived)", 
              "Hypothetical / uncharacterized", "Other annotated"]

left = np.zeros(len(fp))
for cat, col, lab in zip(CATS, CAT_COLORS, CAT_LABELS):
    vals = fp[cat].to_numpy(dtype=float)
    axD.barh(y, vals, left=left, height=0.62, color=col, edgecolor="white",
             linewidth=0.4, label=lab)
    left += vals
axD.set_yticks(y)
axD.set_yticklabels(list(order))
for lab, s in zip(axD.get_yticklabels(), m1["season"]):
    lab.set_color(season_col[s])
axD.set_ylim(-0.7, len(m1) - 0.3)
axD.set_xlim(0, 100)
axD.set_xlabel("Composition of viral-like reads (%)")
axD.set_title("D   Half of the signal is host-derived metabolic genes; structural genes are only "
              f"{fp['Structural / virion'].astype(float).mean():.1f}%",
              loc="left", fontsize=8, pad=6)
for sp in ("top", "right"):
    axD.spines[sp].set_visible(False)

axD.legend(ncol=5, loc="upper center", bbox_to_anchor=(0.5, -0.30),
           handlelength=1.0, handleheight=0.8, columnspacing=1.0,
           labelspacing=0.3)

for ext in ("pdf", "png"):
    fig.savefig(OUT / f"FigM1_v2_signal_validation.{ext}",
                dpi=300, bbox_inches="tight", facecolor="white")

print("已输出：")
for f in sorted(OUT.glob("FigM1_v2*")):
    print(f"  {f.name}  {f.stat().st_size/1024:.0f} KB")

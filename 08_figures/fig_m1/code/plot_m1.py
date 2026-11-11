#!/usr/bin/env python3
"""Figure M1 — 中国扬子鳄圈养种群粪便宏基因组测序基础图（A/B/C 三面板）

数据来源
  ../../09_tables/M1_summary.csv        每样本 QC / 宿主 / 病毒指标
  ../../09_tables/viral_top_taxa.tsv    每样本病毒类群 Top15 占比

输出
  ../output/FigM1_sequencing_landscape.pdf   （矢量，投稿主文件）
  ../output/FigM1_sequencing_landscape.png   （300 dpi 预览）

设计约束
  - 图内文字全部英文（GR13）
  - Okabe-Ito 色盲安全配色
  - n=3/组，故一律画个体点 + 组均值短横线，不画箱线图（避免暗示不存在的分布）
  - 无多余装饰：仅保留左/下轴线
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

# ---- 全局样式 -------------------------------------------------------------
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
    "legend.fontsize": 6.5,
    "pdf.fonttype": 42,      # 字体内嵌为 TrueType，期刊要求可编辑
    "ps.fonttype": 42,
})

C_WINTER = "#0072B2"
C_SUMMER = "#E69F00"
C_GREY = "#666666"
C_LIGHT = "#BBBBBB"

# ---- 数据 -----------------------------------------------------------------
m1 = pd.read_csv(TAB / "M1_summary.csv")
order = ["W1", "W2", "W3", "S1", "S2", "S3"]
m1["sample_id"] = pd.Categorical(m1["sample_id"], order, ordered=True)
m1 = m1.sort_values("sample_id").reset_index(drop=True)
season_col = {"winter": C_WINTER, "summer": C_SUMMER}
cols = [season_col[s] for s in m1["season"]]

taxa = pd.read_csv(TAB / "viral_top_taxa.tsv", sep="\t")
piv = (taxa.pivot_table(index="species", columns="run_accession",
                        values="pct_of_viral_reads", aggfunc="sum")
       .reindex(columns=m1["run_accession"]).fillna(0.0))
mean_share = piv.mean(axis=1).sort_values(ascending=False)

N_TAXA = 8
top_taxa = list(mean_share.head(N_TAXA).index)
shown = piv.loc[top_taxa]
other = (100 - shown.sum(axis=0)).clip(lower=0)

# 每样本"其余类群"的数量（写成区间，避免在图例里写死数字）
counts = (pd.read_csv(TAB / "viral_species_counts.tsv", sep="\t")
          .set_index("run_accession").reindex(m1["run_accession"]))
n_present = (shown > 0).sum(axis=0).to_numpy()
n_other = counts["n_species"].to_numpy() - n_present
other_label = (f"Other taxa (n = {n_other.min():.0f}\u2013{n_other.max():.0f} "
               f"per sample)")

# ---- 画布 -----------------------------------------------------------------
fig = plt.figure(figsize=(7.09, 5.90))          # 180 mm 宽
gs = GridSpec(3, 2, figure=fig,
              height_ratios=[1.0, 1.15, 0.95],
              width_ratios=[1, 1],
              hspace=0.55, wspace=0.30,
              left=0.115, right=0.975, top=0.945, bottom=0.085)

y = np.arange(len(m1))[::-1]
ylabels = [f"{s}" for s in m1["sample_id"]]

# ===== Panel A：质控前后 Q30 + 通过率 ======================================
axA = fig.add_subplot(gs[0, :])
before = m1["q30_before_pct"].to_numpy()
after = m1["q30_after_pct"].to_numpy()

for yi, b, a in zip(y, before, after):
    axA.annotate("", xy=(a, yi), xytext=(b, yi),
                 arrowprops=dict(arrowstyle="-|>,head_width=0.15,head_length=0.35",
                                 color=C_LIGHT, lw=1.0,
                                 shrinkA=2.5, shrinkB=2.5))
axA.scatter(before, y, s=20, facecolors="white", edgecolors=C_GREY,
            linewidths=0.8, zorder=3, label="Before (raw)")
axA.scatter(after, y, s=26, c=cols, edgecolors="white", linewidths=0.5,
            zorder=4, label="After (clean)")

for yi, (_, r) in zip(y, m1.iterrows()):
    axA.text(r["q30_after_pct"] + 0.35, yi,
             f"{r['q30_after_pct']:.1f}%  (pass {r['pass_rate_pct']:.1f}%)",
             va="center", ha="left", fontsize=6.3, color="#333333")

axA.set_yticks(y)
axA.set_yticklabels(ylabels)
# 季节用刻度标签颜色编码，省掉一处图例、避免压住标题
for lab, s in zip(axA.get_yticklabels(), m1["season"]):
    lab.set_color(season_col[s])
axA.set_ylim(-0.7, len(m1) - 0.3)
axA.set_xlim(before.min() - 1.2, after.max() + 6.2)
axA.set_xlabel("Q30 bases (%)")
axA.set_title("A   Read quality: before (open) and after (filled) trimming",
              loc="left", fontsize=8, pad=6)
for sp in ("top", "right"):
    axA.spines[sp].set_visible(False)

# ===== Panel B1：宿主比对率（对数轴） =====================================
axB1 = fig.add_subplot(gs[1, 0])
host = m1["host_aligned_pct"].to_numpy()
axB1.scatter(np.zeros_like(host, dtype=float), host, s=34, c=cols,
             edgecolors="white", linewidths=0.5, zorder=3)

w_mask = (m1["season"] == "winter").to_numpy()
axB1.scatter(np.zeros(w_mask.sum()), host[w_mask], s=34, c=C_WINTER,
             edgecolors="white", linewidths=0.5, zorder=3)
axB1.scatter(np.ones((~w_mask).sum()), host[~w_mask], s=34, c=C_SUMMER,
             edgecolors="white", linewidths=0.5, zorder=3)
for xi, sub in ((0, host[w_mask]), (1, host[~w_mask])):
    axB1.hlines(np.median(sub), xi - 0.22, xi + 0.22, color="#333333",
                lw=1.2, zorder=4)
    axB1.text(xi, np.median(sub) * 1.9, f"median {np.median(sub):.2f}%",
              ha="center", va="bottom", fontsize=6.2, color="#333333")

axB1.set_yscale("log")
axB1.set_xlim(-0.5, 1.5)
axB1.set_ylim(0.04, 6)
axB1.set_xticks([0, 1])
axB1.set_xticklabels(["Winter", "Summer"])
axB1.set_ylabel("Host-aligned reads (%)")
axB1.set_title("B   Host depletion and viral signal", loc="left",
               fontsize=8, pad=6)
for sp in ("top", "right"):
    axB1.spines[sp].set_visible(False)

# ===== Panel B2：病毒 reads 占比 ==========================================
axB2 = fig.add_subplot(gs[1, 1])
vir = m1["viral_reads_pct"].to_numpy()
axB2.scatter(np.zeros(w_mask.sum()), vir[w_mask], s=34, c=C_WINTER,
             edgecolors="white", linewidths=0.5, zorder=3)
axB2.scatter(np.ones((~w_mask).sum()), vir[~w_mask], s=34, c=C_SUMMER,
             edgecolors="white", linewidths=0.5, zorder=3)
for xi, sub in ((0, vir[w_mask]), (1, vir[~w_mask])):
    axB2.hlines(np.median(sub), xi - 0.22, xi + 0.22, color="#333333",
                lw=1.2, zorder=4)

# 组内标注会压住数据点，改为左上角单行角标
axB2.text(-0.42, 0.7255,
          f"median {np.median(vir[w_mask]):.3f}%  vs  "
          f"{np.median(vir[~w_mask]):.3f}%",
          ha="left", va="top", fontsize=6.2, color="#333333")

axB2.set_xlim(-0.5, 1.5)
axB2.set_ylim(0.655, 0.732)
axB2.set_xticks([0, 1])
axB2.set_xticklabels(["Winter", "Summer"])
axB2.set_ylabel("Viral-like reads (%)")
axB2.set_title("", loc="left", fontsize=8)
for sp in ("top", "right"):
    axB2.spines[sp].set_visible(False)# ===== Panel C：病毒类群构成 ==============================================
axC = fig.add_subplot(gs[2, :])
palette = ["#0072B2", "#E69F00", "#009E73", "#CC79A7",
           "#56B4E9", "#D55E00", "#F0E442", "#7F7F7F"]
left = np.zeros(len(m1))
for i, sp_name in enumerate(top_taxa):
    vals = shown.loc[sp_name].to_numpy(dtype=float)
    axC.barh(y, vals, left=left, height=0.62, color=palette[i],
             edgecolor="white", linewidth=0.4, label=sp_name)
    left += vals
axC.barh(y, other.to_numpy(dtype=float), left=left, height=0.62,
         color="#E5E5E5", edgecolor="white", linewidth=0.4,
         label=other_label)

axC.set_yticks(y)
axC.set_yticklabels(ylabels)
axC.set_ylim(-0.7, len(m1) - 0.3)
axC.set_xlim(0, 100)
axC.set_xlabel("Share of viral-like reads (%)")
axC.set_title("C   No dominant taxon: viral signal is evenly spread across hundreds of taxa",
              loc="left", fontsize=8, pad=6)
for sp in ("top", "right"):
    axC.spines[sp].set_visible(False)
axC.legend(ncol=3, loc="upper center", bbox_to_anchor=(0.5, -0.42),
           handlelength=1.0, handleheight=0.8, columnspacing=1.2,
           labelspacing=0.35)

# ---- 保存 -----------------------------------------------------------------
for ext in ("pdf", "png"):
    fig.savefig(OUT / f"FigM1_sequencing_landscape.{ext}",
                dpi=300, bbox_inches="tight", facecolor="white")
print("已输出：")
for f in sorted(OUT.iterdir()):
    print(f"  {f.name}  {f.stat().st_size/1024:.0f} KB")

print("\n关键数值（用于图注）：")
print(f"  宿主中位数 冬 {np.median(host[w_mask]):.2f}% / 夏 {np.median(host[~w_mask]):.2f}%")
print(f"  病毒均值   冬 {vir[w_mask].mean():.3f}% / 夏 {vir[~w_mask].mean():.3f}%")
print(f"  Top1 类群平均占比 {mean_share.iloc[0]:.2f}%")
print(f"  前 {N_TAXA} 类群合计平均 {mean_share.head(N_TAXA).sum():.1f}%")

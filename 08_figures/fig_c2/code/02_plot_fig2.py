#!/usr/bin/env python3
"""CR-01 Fig 2: detection envelope. Draws A (V_min vs receptors) and B (n x s heatmap).

Reads matrices/ produced by 01_compute_envelope.py; writes output/Fig2_*.{pdf,png}.
Figure text in English (GR13). Two panels only (GR7).
"""
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LogNorm

HERE = Path(__file__).resolve().parent
FIG = HERE.parent
MAT, OUT, RAW = FIG / "matrices", FIG / "output", FIG / "raw_data"
OUT.mkdir(exist_ok=True)

p = pd.read_csv(RAW / "params.tsv", sep="\t")
d = dict(zip(p["symbol"], p["baseline"]))
pr, i0, s0 = d["per_receptor_fraction"], d["i"], d["s"]
meta, env_lo, env_hi = d["metagenome_fraction"], d["env_abundance_low"], d["env_abundance_high"]
qk, qu = d["q_known"], d["q_unknown"]

NS = np.arange(1, 31)

# ---------- style ----------
mpl.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 7,
    "axes.linewidth": 0.6,
    "axes.labelsize": 7.5,
    "xtick.labelsize": 6.5,
    "ytick.labelsize": 6.5,
    "legend.fontsize": 6.5,
    "pdf.fonttype": 42,
})
C_KNOWN, C_UNKNOWN = "#1f4e79", "#c0504d"      # colour-blind safe pair

fig, (axA, axB) = plt.subplots(
    1, 2, figsize=(7.1, 2.95), gridspec_kw={"width_ratios": [1.05, 1.0], "wspace": 0.52}
)

# ================= Panel A: V_min vs receptor count =================
r = NS * pr
v_known = 1 / (r * i0 * s0 * qk)
v_unknown = 1 / (r * i0 * s0 * qu)

axA.axhspan(env_lo, env_hi, color="#d9d9d9", alpha=0.55, zorder=0)
axA.plot(NS, v_known, color=C_KNOWN, lw=1.3, label="known target (q = 0.1)")
axA.plot(NS, v_unknown, color=C_UNKNOWN, lw=1.3, ls="--", label="unknown target (q = 0.01)")

axA.axvline(meta / pr, color="#555555", lw=0.7, ls=":", zorder=1)
axA.text(meta / pr - 1.2, 2.2e9, "coverage parity\nwith metagenome\n(33 receptors)",
         fontsize=5.6, color="#333333", ha="right", va="center")

axA.set_yscale("log")
axA.set_xlim(0, 36)
axA.set_ylim(1e3, 1e12)
axA.set_xlabel("Functional receptors expressed in one strain (n)")
axA.set_ylabel(r"Detection floor $V_{\min}$ (particles mL$^{-1}$)")
axA.set_yticks(10.0 ** np.arange(4, 13, 2))
axA.legend(loc="upper right", frameon=False, handlelength=1.6)

axA.text(1.2, 1.35e4, "environmental abundance\n$10^{4}$–$10^{10}$ mL$^{-1}$",
         fontsize=5.6, color="#444444", va="bottom")

# highlight the most optimistic corner
best_v = 1 / ((30 * pr) * 0.5 * 1e-3 * 0.5)
axA.plot([30], [best_v], marker="o", ms=3.2, mfc="white", mec="#2e7d32", mew=1.0, zorder=5)
axA.annotate("best case\n(i=0.5, s=10$^{-3}$, q=0.5)",
             xy=(30, best_v), xytext=(17.5, 1.3e4),
             fontsize=5.6, color="#2e7d32",
             arrowprops=dict(arrowstyle="-", lw=0.5, color="#2e7d32",
                             shrinkA=1, shrinkB=3))

axA.set_title("A   Detection floor per receptor budget", loc="left", fontsize=7.5, pad=5)

# ================= Panel B: heatmap n x s =================
grid = pd.read_csv(MAT / "vmin_grid_known.tsv", sep="\t", index_col=0)
s_vals = np.array([float(c) for c in grid.columns])
Z = grid.values                                   # rows: n=1..30, cols: s

mesh = axB.pcolormesh(s_vals, grid.index.values, np.log10(Z),
                      cmap="viridis_r", shading="auto", vmin=5.5, vmax=11.1)
lvl = [6, 8, 10]
axB.contour(s_vals, grid.index.values, np.log10(Z),
            levels=lvl, colors="#1a1a1a", linewidths=0.55, linestyles="--")

axB.set_xscale("log")
axB.set_xlabel(r"Spacer acquisition probability $s$")
axB.set_ylabel("Functional receptors (n)")
axB.set_title("B   Envelope for known targets (q = 0.1)", loc="left", fontsize=7.5, pad=5)

cb = fig.colorbar(mesh, ax=axB, fraction=0.046, pad=0.03)
cb.set_label(r"$\log_{10} V_{\min}$ (particles mL$^{-1}$)", fontsize=6.5)
cb.ax.tick_params(labelsize=6, width=0.5)

for ax in (axA, axB):
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    ax.tick_params(width=0.5, length=2.5)

fig.subplots_adjust(left=0.075, right=0.965, top=0.90, bottom=0.155)
for ext, dpi in (("pdf", None), ("png", 300)):
    path = OUT / f"Fig2_detection_envelope.{ext}"
    fig.savefig(path, dpi=dpi, bbox_inches="tight")
    print("saved", path)

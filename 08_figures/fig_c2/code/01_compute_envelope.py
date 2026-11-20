#!/usr/bin/env python3
"""CR-01 Fig 2: detection envelope of engineered-receptor baiting.

Model (outline §3): P = r x i x s x q ; V_min = 1/P  (1 mL sample, E = 1)

Reads only raw_data/params.tsv, writes matrices/ and output/.
All inputs are order-of-magnitude scenario parameters, NOT measurements.
"""
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
FIG = HERE.parent
RAW, MAT, OUT = FIG / "raw_data", FIG / "matrices", FIG / "output"
for d in (MAT, OUT):
    d.mkdir(exist_ok=True)

p = pd.read_csv(RAW / "params.tsv", sep="\t")
d = dict(zip(p["symbol"], p["baseline"]))

pr = d["per_receptor_fraction"]      # 0.0009 per receptor
i0, s0 = d["i"], d["s"]
meta = d["metagenome_fraction"]
env_lo, env_hi = d["env_abundance_low"], d["env_abundance_high"]

NS = np.arange(1, 31)
S_GRID = 10 ** np.arange(-6, -1.75, 0.25)          # 1e-6 .. ~1e-2
Q = {"known": d["q_known"], "unknown": d["q_unknown"]}

# ---------- 1. envelope grids (n x s), one per q ----------
rows = []
for tag, q in Q.items():
    r = NS * pr
    vmin = 1.0 / (r[:, None] * i0 * S_GRID[None, :] * q)
    df = pd.DataFrame(vmin, index=NS, columns=[f"{x:.2e}" for x in S_GRID])
    df.index.name = "n_receptor"
    df.to_csv(MAT / f"vmin_grid_{tag}.tsv", sep="\t")

# ---------- 2. key numbers at baseline i, s ----------
key = []
for n in (1, 3, 10, 30):
    r = n * pr
    for tag, q in Q.items():
        vmin = 1.0 / (r * i0 * s0 * q)
        key.append({"n_receptor": n, "coverage_r": r, "scenario": tag,
                    "V_min_per_mL": vmin})
key = pd.DataFrame(key)
key.to_csv(MAT / "key_numbers.tsv", sep="\t", index=False)

# ---------- 3. receptor budget to reach a target ----------
def n_required(target_vmin, q, i=i0, s=s0):
    return 1.0 / (target_vmin * pr * i * s * q)

budget = []
for target_name, target in [("metagenome_3pct_coverage", None),
                            ("env_high_1e10", env_hi),
                            ("env_low_1e4", env_lo)]:
    for tag, q in Q.items():
        if target is None:
            n = meta / pr                      # coverage parity, q-independent
            label = "coverage parity with metagenome (3%)"
        else:
            n = n_required(target, q)
            label = f"V_min <= {target:.0e}"
        budget.append({"target": target_name, "scenario": tag,
                       "n_receptor_required": n, "label": label})
budget = pd.DataFrame(budget)
budget.to_csv(MAT / "receptor_budget.tsv", sep="\t", index=False)

# ---------- 4. best case (all parameters at their most optimistic) ----------
best_r = 30 * d["per_receptor_fraction"]
best = {
    "n": 30,
    "r": best_r,
    "i": d["i"] if False else 0.5,
    "s": 0.001,
    "q": 0.5,
}
best["P"] = best["r"] * best["i"] * best["s"] * best["q"]
best["V_min"] = 1 / best["P"]

# ---------- 5. three levers: how far each must move ALONE to reach env_lo ----------
# Anchor point: 30 receptors, 1 mL, baseline i/s/q (the "realistic engineered" corner).
# Each lever is moved on its own; the point is that they are not substitutes.
def vmin(n, v=1.0, i=i0, s=s0, q=Q["known"]):
    return 1.0 / (n * pr * i * s * q * v)

anchor = vmin(30)
factor = anchor / env_lo                      # how many fold P must rise
levers = pd.DataFrame([
    {"lever": "n_receptor", "anchor_value": 30, "needed_value": 30 * factor,
     "needed_multiple": factor, "unit": "receptors",
     "note": "coverage alone; >1e5 receptors is not an engineering question"},
    {"lever": "sample_volume_v", "anchor_value": 1, "needed_value": factor,
     "needed_multiple": factor, "unit": "mL",
     "note": "3.7 L per sample; practical ceiling ~100 mL (outline §3)"},
    {"lever": "i*s*q", "anchor_value": i0 * s0 * Q["known"],
     "needed_value": i0 * s0 * Q["known"] * factor,
     "needed_multiple": factor, "unit": "per phage",
     "note": "needs 3.7e3x over baseline; most optimistic set gives 250x"},
])
levers.to_csv(MAT / "lever_sensitivity.tsv", sep="\t", index=False)

# conjunction table: what combinations actually reach env_lo
O = {"baseline (i=0.1,s=1e-4,q=0.1)": (i0, s0, Q["known"]),
     "optimistic (i=0.5,s=1e-3,q=0.5)": (0.5, 0.001, 0.5)}
combo = []
for n in (30, 1111):
    for v in (1, 100):
        for tag, (ii, ss, qq) in O.items():
            x = vmin(n, v, ii, ss, qq)
            combo.append({"n_receptor": n, "v_mL": v, "params": tag,
                          "coverage_r": n * pr, "i_s_q": ii * ss * qq,
                          "V_min": x, "reaches_1e4": x <= env_lo})
combo = pd.DataFrame(combo)
combo.to_csv(MAT / "conjunction.tsv", sep="\t", index=False)

# ---------- 6. 10x perturbation check at the anchor ----------
pert = []
for name, f in [("n x0.1", 0.1), ("n x10", 10.0)]:
    pert.append({"perturbed": name, "V_min": vmin(30 * f)})
for name, f in [("v x0.1", 0.1), ("v x10", 10.0)]:
    pert.append({"perturbed": name, "V_min": vmin(30, 1.0 * f)})
for name, f in [("i*s*q x0.1", 0.1), ("i*s*q x10", 10.0)]:
    pert.append({"perturbed": name, "V_min": vmin(30, 1.0, i0 * f, s0, Q["known"])})
pert = pd.DataFrame(pert)
pert.to_csv(MAT / "perturbation_10x.tsv", sep="\t", index=False)

# ---------- report ----------
lines = []
lines.append("CR-01 Fig 2 · detection envelope")
lines.append("=" * 62)
lines.append(f"model            : P = r x i x s x q ;  V_min = 1/P")
lines.append(f"per-receptor      : {pr:.4f}  (1 of 1100 phages, Zeng & Salmond 2020)")
lines.append(f"baseline i, s     : {i0}, {s0}")
lines.append(f"metagenome frac   : {meta:.4f}")
lines.append(f"env abundance     : {env_lo:.0e} - {env_hi:.0e} particles/mL")
lines.append("")
lines.append("Key numbers at baseline (i=0.1, s=1e-4)")
lines.append(f"{'n':>3} {'r':>8} {'known V_min':>14} {'unknown V_min':>15}")
for n in (1, 3, 10, 30):
    r = n * pr
    vk = 1 / (r * i0 * s0 * Q["known"])
    vu = 1 / (r * i0 * s0 * Q["unknown"])
    lines.append(f"{n:>3} {r:8.4f} {vk:14.2e} {vu:15.2e}")
lines.append("")
lines.append("Receptor budget")
for _, row in budget.iterrows():
    lines.append(f"  {row['label']:<44} {row['scenario']:<8} n = {row['n_receptor_required']:.3g}")
lines.append("")
lines.append("Most optimistic corner (n=30, i=0.5, s=1e-3, q=0.5)")
lines.append(f"  r = {best['r']:.4f}, P = {best['P']:.2e}, V_min = {best['V_min']:.2e} particles/mL")
lines.append(f"  -> {'still above' if best['V_min'] > env_lo else 'reaches'} the low-abundance end ({env_lo:.0e})")
lines.append("")
lines.append(f"Three levers, each moved ALONE (anchor n=30, v=1 mL, baseline i/s/q = {anchor:.2e})")
lines.append(f"  to reach {env_lo:.0e}: P must rise by {factor:.3g}x")
for _, row in levers.iterrows():
    lines.append(f"  {row['lever']:<18} {row['anchor_value']:>10.3g} -> {row['needed_value']:<10.3g} {row['unit']}")
lines.append("")
lines.append("Conjunction: which combinations actually reach env_lo")
for _, row in combo.iterrows():
    flag = "OK " if row["reaches_1e4"] else "no "
    lines.append(f"  {flag}n={row['n_receptor']:>4}  v={row['v_mL']:>3.0f} mL  {row['params']:<38} V_min={row['V_min']:.2e}")
lines.append("")
lines.append(f"10x perturbation at the anchor ({anchor:.2e}) — does the conclusion flip?")
for _, row in pert.iterrows():
    flag = "FLIPS" if row["V_min"] <= env_lo else "holds"
    lines.append(f"  {row['perturbed']:<12} V_min={row['V_min']:.2e}  {flag}")
lines.append(f"  range {pert['V_min'].min():.1f} - {pert['V_min'].max():.1f} ; low-abundance end is {env_lo:.0e}")

txt = "\n".join(lines)
(OUT / "key_numbers.txt").write_text(txt, encoding="utf-8")
print(txt)

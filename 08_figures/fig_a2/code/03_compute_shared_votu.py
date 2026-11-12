#!/usr/bin/env python3
"""
Fig 3 —— 共享 vOTU 数与丰度阈值的关系

科学论断
--------
"六样本零共享"在很大程度上是组装伪影。
同一批数据，contig 层面 6 个样本共享的 vOTU 为 0；
但换成 reads 层面（RPKM 阈值），共享数从 783 到 1 不等——
结论完全取决于"什么算存在"。

这个图回答一个具体问题：
报告"共享 vOTU 数"时，若不说阈值，数字没有意义。

输出
----
matrices/threshold_sweep.tsv   各 RPKM 阈值下 n_samples 的分布（含 contig 基线）
matrices/jaccard_pairs.tsv     15 个样本对的 Jaccard 相似度（contig vs reads 两种口径）
"""

from pathlib import Path
from itertools import combinations

import pandas as pd

HERE = Path(__file__).resolve().parent
FIG = HERE.parent
RAW = FIG / "raw_data"
MAT = FIG / "matrices"
MAT.mkdir(exist_ok=True)

SAMPLES = ["W1", "W2", "W3", "S1", "S2", "S3"]
THRESHOLDS = [0.0, 0.01, 0.1, 1.0, 10.0]


def load():
    rpkm = pd.read_csv(RAW / "votu_abundance_rpkm.tsv", sep="\t")
    pres = pd.read_csv(RAW / "votu_presence.tsv", sep="\t")
    return rpkm, pres


def contig_membership(pres: pd.DataFrame) -> pd.DataFrame:
    """把 samples 字段（"W1,W2"）展开成 0/1 矩阵。"""
    rows = []
    for _, r in pres.iterrows():
        mem = set(str(r["samples"]).split(",")) if pd.notna(r["samples"]) else set()
        rows.append({s: int(s in mem) for s in SAMPLES} | {"votu_id": r["votu_id"]})
    return pd.DataFrame(rows).set_index("votu_id")


def jaccard(df_a: pd.DataFrame, df_b: pd.DataFrame) -> float:
    """两个 0/1 Series 的 Jaccard。"""
    inter = int(((df_a == 1) & (df_b == 1)).sum())
    union = int(((df_a == 1) | (df_b == 1)).sum())
    return inter / union if union else 0.0


def main() -> None:
    rpkm, pres = load()
    rpkm = rpkm.set_index("votu_id")

    # ---------------- 1. 阈值 sweep
    records = []

    # contig 基线
    cm = pres["n_samples"].value_counts()
    records.append(
        {
            "threshold": "contig",
            "n_total": len(pres),
            **{f"n{k}": int(cm.get(k, 0)) for k in range(1, 7)},
            "shared_all6": int(cm.get(6, 0)),
            "singleton": int(cm.get(1, 0)),
            "singleton_pct": round(cm.get(1, 0) / len(pres) * 100, 1),
        }
    )

    for t in THRESHOLDS:
        mat = rpkm[SAMPLES] >= t if t > 0 else rpkm[SAMPLES] > 0
        n = mat.sum(axis=1)
        vc = n.value_counts()
        label = f"RPKM>{t:g}" if t == 0 else f"RPKM>={t:g}"
        detected = int((n > 0).sum())
        records.append(
            {
                "threshold": label,
                "n_total": detected,
                **{f"n{k}": int(vc.get(k, 0)) for k in range(1, 7)},
                "shared_all6": int(vc.get(6, 0)),
                "singleton": int(vc.get(1, 0)),
                "singleton_pct": round(vc.get(1, 0) / detected * 100, 1) if detected else 0.0,
            }
        )

    sweep = pd.DataFrame(records)
    sweep.to_csv(MAT / "threshold_sweep.tsv", sep="\t", index=False)

    # ---------------- 2. 样本对 Jaccard
    cmat = contig_membership(pres).reindex(rpkm.index).fillna(0).astype(int)
    rmat = (rpkm[SAMPLES] >= 1).astype(int)

    pairs = []
    for a, b in combinations(SAMPLES, 2):
        pairs.append(
            {
                "pair": f"{a}-{b}",
                "jaccard_contig": round(jaccard(cmat[a], cmat[b]), 4),
                "jaccard_reads_rpkm1": round(jaccard(rmat[a], rmat[b]), 4),
                "n_contig_a": int(cmat[a].sum()),
                "n_contig_b": int(cmat[b].sum()),
                "n_reads_a": int(rmat[a].sum()),
                "n_reads_b": int(rmat[b].sum()),
            }
        )
    jac = pd.DataFrame(pairs)
    jac["ratio"] = (jac["jaccard_reads_rpkm1"] / jac["jaccard_contig"].replace(0, pd.NA)).round(2)
    jac.to_csv(MAT / "jaccard_pairs.tsv", sep="\t", index=False)

    # ---------------- 诊断
    print("=" * 74)
    print("共享 vOTU 随阈值变化")
    print("=" * 74)
    print(sweep[["threshold", "n_total", "shared_all6", "singleton", "singleton_pct"]].to_string(index=False))
    print()
    print("样本对 Jaccard（contig vs reads RPKM>=1）")
    print("-" * 74)
    print(jac[["pair", "jaccard_contig", "jaccard_reads_rpkm1"]].head(6).to_string(index=False))
    print(f"  ... 共 {len(jac)} 对")
    print()
    print(f"contig  Jaccard 中位: {jac.jaccard_contig.median():.4f}")
    print(f"reads   Jaccard 中位: {jac.jaccard_reads_rpkm1.median():.4f}")
    print(f"倍数: {jac.jaccard_reads_rpkm1.median() / jac.jaccard_contig.median():.1f}×")
    print()
    print(f"输出: {MAT / 'threshold_sweep.tsv'}")
    print(f"      {MAT / 'jaccard_pairs.tsv'}")


if __name__ == "__main__":
    main()

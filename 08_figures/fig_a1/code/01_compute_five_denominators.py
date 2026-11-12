#!/usr/bin/env python3
"""
五口径病毒占比计算 —— Table 1 与 Fig 2 的数据源

科学问题
--------
同一批肠道宏基因组，"病毒占比"在不同定义下差多少？
本脚本把"占比"拆成五个互不等价的口径，逐样本计算。

五个口径
--------
C1  structural + replication/transcription hits / all clean reads
    reference = RVDB-prot v32 Unique       assignment = category filter
C2  all viral-like hits / all clean reads
    reference = RVDB-prot v32 Unique       assignment = no category filter
C3  literature value
    reference = nr + MEGAN4 LCA (Tang 2019)  assignment = LCA（文献值，非本批重算）
C4  viral contigs / all contigs
    reference = geNomad                    assignment = contig count
C5  vOTU-mapped reads / all clean reads
    reference = this study's 9,980 vOTUs   assignment = read count

差异来源
--------
C1 vs C2  → 类别筛选（是否排除代谢/持家、其他已注释、未知功能）
C2 vs C5  → 参考空间（RVDB-prot v32 Unique vs 本批 9,980 vOTU）
C2 vs C4  → 统计单元（reads 计数 vs contig 计数）

输入 raw_data/
--------------
viral_reads_summary.tsv   ORF 比对的病毒 reads 数（C1/C2 分子）
host_removal_summary.tsv  宿主比对率（C2 分母调整）
votu_abundance_counts.tsv vOTU 的 reads 计数（C5 分子）
all_c_summary.tsv         contig 统计与 viral_pct_of_contigs（C4）

输出
----
matrices/five_denominators_long.tsv   长表：样本 × 口径 × 数值
output/Table1_five_denominators.tsv   宽表：口径 × 样本
output/Table1_five_denominators.md    Markdown 版（供稿件直接引用）

用法
----
python code/01_compute_five_denominators.py
"""

from pathlib import Path
import pandas as pd

# ---------------------------------------------------------------- 路径
HERE = Path(__file__).resolve().parent
FIG = HERE.parent
RAW = FIG / "raw_data"
MAT = FIG / "matrices"
OUT = FIG / "output"
MAT.mkdir(exist_ok=True)
OUT.mkdir(exist_ok=True)

SAMPLES = ["W1", "W2", "W3", "S1", "S2", "S3"]

# C3：Tang et al. 2019 (Front Microbiol 10:2409) 原文报告的病毒 reads 占比区间
C3_LITERATURE = {"low": 0.04, "high": 4.03}


def load():
    vr = pd.read_csv(RAW / "viral_reads_summary.tsv", sep="\t")
    hr = pd.read_csv(RAW / "host_removal_summary.tsv", sep="\t")
    ac = pd.read_csv(RAW / "all_c_summary.tsv", sep="\t")
    vc = pd.read_csv(RAW / "votu_abundance_counts.tsv", sep="\t")
    vse = pd.read_csv(RAW / "viral_specific_estimate.tsv", sep="\t")
    return vr, hr, ac, vc, vse


def main() -> None:
    vr, hr, ac, vc, vse = load()

    # run_accession → sample_id（all_c_summary 是唯一同时含两者的表）
    run2sample = dict(zip(ac["run_accession"], ac["sample_id"]))

    # ---------------- C1 严格 / C2 宽
    # viral_specific_estimate 区分了"有功能蛋白证据"与"仅命中结构蛋白"两类，
    # 二者的比值即"是否要求功能证据"这一维度的影响。
    vr["sample_id"] = vr["run_accession"].map(run2sample)
    hr["sample_id"] = hr["run_accession"].map(run2sample)
    df = vr[["sample_id", "run_accession", "reads_total", "hits_total"]].merge(
        hr[["sample_id", "total_reads", "host_aligned_pct"]], on="sample_id", how="left"
    )
    df = df.merge(
        vse[["sample_id", "viral_specific_pct", "viral_like_pct", "structural_only_pct"]],
        on="sample_id",
        how="left",
    )
    # 注：nonhost_reads 曾用于"去宿主分母"口径，最终未纳入 canonical 五口径；
    # 若将来增加 C6（非宿主分母），在此恢复计算。
    _ = df["reads_total"] * (1 - df["host_aligned_pct"] / 100)  # reserved for C6
    df["C1_pct"] = df["viral_specific_pct"]   # 严格：需功能蛋白证据
    df["C2_pct"] = df["viral_like_pct"]       # 宽：含仅结构蛋白命中

    # ---------------- C4: 病毒 contig / 全部 contig
    df = df.merge(
        ac[["sample_id", "contigs_n", "viral_contigs_n", "viral_pct_of_contigs"]],
        on="sample_id",
        how="left",
    )
    df["C4_pct"] = df["viral_pct_of_contigs"]

    # ---------------- C5: vOTU 比对 reads / 全部 reads
    votu_totals = {s: float(vc[s].sum()) for s in SAMPLES}
    df["votu_reads"] = df["sample_id"].map(votu_totals)
    df["C5_pct"] = df["votu_reads"] / df["reads_total"] * 100

    df = df.set_index("sample_id").loc[SAMPLES].reset_index()

    # ---------------- 组装宽表
    rows = []

    def add(code: str, label: str, numerator: str, denominator: str, ref: str, assign: str, values: dict, note: str = ""):
        nums = [v for v in values.values() if v is not None]
        rng = f"{min(nums):.4g}–{max(nums):.4g}" if nums else "—"
        rows.append(
            {
                "口径": code,
                "定义": label,
                "分子": numerator,
                "分母": denominator,
                "参考空间": ref,
                "赋值方式": assign,
                **values,
                "范围(最小-最大)": rng,
                "备注": note,
            }
        )

    add(
        "C1",
        "严格：仅结构 + 复制/转录",
        "结构 + 复制/转录类别的病毒命中 reads",
        "全部 clean reads",
        "RVDB-prot v32 Unique",
        "类别筛选",
        {s: round(float(df.loc[df.sample_id == s, "C1_pct"].iloc[0]), 4) for s in SAMPLES},
        "排除代谢/持家、其他已注释、未知功能三类",
    )
    add(
        "C2",
        "宽：全部病毒样命中",
        "全部病毒样命中 reads",
        "全部 clean reads",
        "RVDB-prot v32 Unique",
        "不筛选",
        {s: round(float(df.loc[df.sample_id == s, "C2_pct"].iloc[0]), 4) for s in SAMPLES},
        "不排除代谢/持家/未知类别",
    )
    add(
        "C3",
        "原文报告口径（文献值）",
        "—",
        "—",
        "nr + MEGAN4 LCA",
        "LCA 归属",
        {s: None for s in SAMPLES},
        f"Tang 2019 报告区间 {C3_LITERATURE['low']}–{C3_LITERATURE['high']}%，非本批重算",
    )
    add(
        "C4",
        "病毒 contig / 全部 contig",
        "病毒 contig 数",
        "全部 contig 数",
        "geNomad 判定",
        "计数",
        {s: round(float(df.loc[df.sample_id == s, "C4_pct"].iloc[0]), 4) for s in SAMPLES},
        "统计单元为 contig，非 reads",
    )
    add(
        "C5",
        "vOTU 比对 reads / 全部 reads",
        "比对到本批 vOTU 的 reads",
        "全部 clean reads",
        "本批 9,980 vOTU",
        "计数",
        {s: round(float(df.loc[df.sample_id == s, "C5_pct"].iloc[0]), 6) for s in SAMPLES},
        "参考空间仅覆盖本批组装出的 vOTU",
    )

    table = pd.DataFrame(rows)

    # ---------------- 长表
    long = df.melt(
        id_vars=["sample_id"],
        value_vars=["C1_pct", "C2_pct", "C4_pct", "C5_pct"],
        var_name="metric",
        value_name="pct",
    )
    long["metric"] = long["metric"].str.replace("_pct", "", regex=False)
    long.to_csv(MAT / "five_denominators_long.tsv", sep="\t", index=False)

    # ---------------- 输出
    table.to_csv(OUT / "Table1_five_denominators.tsv", sep="\t", index=False)

    with open(OUT / "Table1_five_denominators.md", "w", encoding="utf-8") as fh:
        fh.write("# Table 1. 五口径下的病毒 reads 占比（%）\n\n")
        fh.write("Six fecal shotgun metagenomes of *Alligator sinensis* (PRJNA539906).\n\n")
        header = "| 口径 | 定义 | " + " | ".join(SAMPLES) + " | 范围 |"
        sep = "|---|---|" + "---|" * len(SAMPLES) + "---|"
        fh.write(header + "\n" + sep + "\n")
        for _, r in table.iterrows():
            cells = []
            for s in SAMPLES:
                v = r[s]
                cells.append("—" if pd.isna(v) else f"{v:.4g}")
            fh.write(f"| **{r['口径']}** | {r['定义']} | " + " | ".join(cells) + f" | {r['范围(最小-最大)']} |\n")
        fh.write("\n**差异来源**：C1↔C2 差在类别筛选（是否排除代谢/持家、其他已注释、未知功能）；C2↔C5 差在参考空间（RVDB vs 本批 vOTU）；C2↔C4 差在统计单元（reads 计数 vs contig 计数）。\n")
        fh.write("\n**C3 说明**：原文数值不可在本批数据上重算（无原始 ORF 比对输出），故以文献报告区间呈现，不作为可比数值。\n")

    # ---------------- 控制台诊断
    print("=" * 72)
    print("五口径病毒占比（%）")
    print("=" * 72)
    print(table[["口径", *SAMPLES]].to_string(index=False))
    print()
    print("诊断信息")
    print("-" * 72)
    rng = {c: (table.loc[table.口径 == c, SAMPLES].values.astype(float).min(),
               table.loc[table.口径 == c, SAMPLES].values.astype(float).max())
           for c in ["C1", "C2", "C4", "C5"]}
    for c, (lo, hi) in rng.items():
        print(f"  {c}: {lo:.4g} – {hi:.4g}%   (跨样本 {hi/lo:.1f}×)" if lo > 0 else f"  {c}: {lo:.4g} – {hi:.4g}%")
    vmin = min(lo for lo, _ in rng.values())
    vmax = max(hi for _, hi in rng.values())
    print(f"  口径间最大跨度: {vmax/vmin:.0f}×  ({vmin:.3g}% → {vmax:.4g}%)")
    print()
    print(f"输出: {OUT / 'Table1_five_denominators.tsv'}")
    print(f"      {OUT / 'Table1_five_denominators.md'}")


if __name__ == "__main__":
    main()

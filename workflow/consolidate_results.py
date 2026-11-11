"""把散落在各阶段的结果合并为两张主表 + 一份关键数值清单。"""
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / "05_c_stage"
T = ROOT / "09_tables"
H = ROOT / "06_host" / "full_iphop"
OUT = T / "consolidated"
OUT.mkdir(exist_ok=True)

# ---------------- 样本级 ----------------
m1 = pd.read_csv(T / "M1_summary.csv")
cs = pd.read_csv(D / "all_c_summary.tsv", sep="\t")
ab = pd.read_csv(D / "abundance_summary.tsv", sep="\t")
gc = pd.read_csv(D / "sample_gc_viral.tsv", sep="\t")
tx = pd.read_csv(D / "taxonomy_by_sample.tsv", sep="\t")
vs = pd.read_csv(D / "votu_stats.tsv", sep="\t")

# vOTU 统计表是长格式，抽出「每样本 vOTU 数」
vmap = {}
for _, r in vs.iterrows():
    key = str(r.iloc[0])
    if key.endswith("的 vOTU 数"):
        vmap[key.split(" ")[0]] = int(r.iloc[1])
votu_n = pd.Series(vmap, name="votu_n")
votu_n.index.name = "sample_id"
votu_n = votu_n.reset_index()

# 优势纲占比
cau = (tx[tx["class"] == "Caudoviricetes"]
       .set_index("sample_id")["pct_of_viral"].rename("caudoviricetes_pct"))

# 宿主覆盖
hg = pd.read_csv(H / "Host_prediction_to_genus_m90.csv")


def parse(s):
    p = s.split("|")
    return p[0], "|".join(p[1:-3]), p[-3]


hg[["sample_id", "contig", "quality"]] = hg["Virus"].apply(lambda s: pd.Series(parse(s)))
host_n = hg.drop_duplicates(["sample_id", "contig"]).groupby("sample_id").size().rename("host_predicted_n")

df = (gc[["sample_id", "run_accession", "individual", "collection_date", "season"]]
      .merge(m1[["sample_id", "reads_raw_pairs", "reads_clean_mates", "pass_rate_pct", "q30_after_pct",
                 "host_aligned_pct", "viral_reads_pct", "viral_specific_pct"]], on="sample_id")
      .merge(cs[["sample_id", "contigs_n", "contigs_total_Mb", "contigs_N50_kb",
                 "viral_contigs_n", "viral_total_Mb", "viral_pct_of_contigs",
                 "checkv_Complete", "checkv_High", "checkv_Medium", "hq_genomes_n"]], on="sample_id")
      .merge(ab[["sample_id", "viral_reads_pct", "votu_rpkm_ge1"]], on="sample_id",
             suffixes=("", "_abund"))
      .merge(gc[["sample_id", "gc_pct", "viral_contig_pct"]], on="sample_id")
      .merge(cau, on="sample_id")
      .merge(host_n, on="sample_id", how="left")
      .merge(votu_n, on="sample_id", how="left"))

df["host_predicted_pct"] = (df["host_predicted_n"] / df["hq_genomes_n"] * 100).round(1)
df = df.rename(columns={
    "viral_reads_pct": "viral_like_pct_M1",
    "viral_reads_pct_abund": "viral_reads_pct_mapped",
    "viral_contig_pct": "viral_pct_contigs_check",
})

order = ["sample_id", "run_accession", "individual", "collection_date", "season",
         "reads_raw_pairs", "reads_clean_mates", "q30_after_pct", "pass_rate_pct", "host_aligned_pct",
         "viral_like_pct_M1", "viral_specific_pct",
         "contigs_n", "contigs_total_Mb", "contigs_N50_kb",
         "viral_contigs_n", "viral_total_Mb", "viral_pct_of_contigs", "caudoviricetes_pct",
         "checkv_Complete", "checkv_High", "checkv_Medium", "hq_genomes_n",
         "votu_n", "votu_rpkm_ge1", "viral_reads_pct_mapped",
         "gc_pct", "host_predicted_n", "host_predicted_pct"]
df = df[order]
df.to_csv(OUT / "master_sample_table.tsv", sep="\t", index=False)

# 合计行
tot = {
    "sample_id": "TOTAL", "reads_raw_pairs": df["reads_raw_pairs"].sum(),
    "reads_clean_mates": df["reads_clean_mates"].sum(),
    "contigs_n": df["contigs_n"].sum(), "contigs_total_Mb": round(df["contigs_total_Mb"].sum(), 1),
    "viral_contigs_n": df["viral_contigs_n"].sum(),
    "viral_total_Mb": round(df["viral_total_Mb"].sum(), 2),
    "checkv_Complete": df["checkv_Complete"].sum(), "checkv_High": df["checkv_High"].sum(),
    "checkv_Medium": df["checkv_Medium"].sum(), "hq_genomes_n": df["hq_genomes_n"].sum(),
    "host_predicted_n": df["host_predicted_n"].sum(),
}
pd.DataFrame([tot]).to_csv(OUT / "master_sample_table_total.tsv", sep="\t", index=False)

# ---------------- 基因组级 ----------------
g = pd.read_csv(D / "hq_genomes_with_abundance.tsv", sep="\t")
g["key"] = g["sample_id"] + "||" + g["contig_id"]
host = hg.sort_values("Confidence score", ascending=False).drop_duplicates(["sample_id", "contig"])
host["key"] = host["sample_id"] + "||" + host["contig"]
host["host_phylum"] = host["Host genus"].str.extract(r"p__([^;]+)")[0]
host["host_genus"] = host["Host genus"].str.extract(r"g__([^;]+)")[0]
gm = g.merge(host[["key", "host_phylum", "host_genus", "Confidence score", "List of methods"]],
             on="key", how="left")
gm["is_provirus"] = gm["contig_id"].str.contains("provirus")
# 以"是否匹配到预测记录"为准（个别记录只定到域/门，无属名）
gm["has_host"] = gm["Confidence score"].notna()
gm = gm.drop(columns=["key"])
gm = gm.sort_values(["sample_id", "length"], ascending=[True, False])
gm.to_csv(OUT / "master_genome_table.tsv", sep="\t", index=False)

print(f"样本表: {df.shape[0]} 行 × {df.shape[1]} 列")
print(f"基因组表: {gm.shape[0]} 行 × {gm.shape[1]} 列（有宿主 {gm['has_host'].sum()}，前噬菌体 {gm['is_provirus'].sum()}）")
print(f"\n输出目录: {OUT}")

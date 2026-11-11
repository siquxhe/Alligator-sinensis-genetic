#!/usr/bin/env python3
"""整合 MAG 与前噬菌体结果

产出（07_mag/）
  mag_final_annotated.tsv   44 条 MAG：质量 + CheckM 谱系 + GTDB 分类
  prophage_in_mags.tsv      19 条 MAG 内前噬菌体：宿主 MAG 及其完整分类 + CheckV 质量
"""
from pathlib import Path

import pandas as pd

D = Path(__file__).resolve().parents[1] / "07_mag"

# ---------- MAG ----------
mag = pd.read_csv(D / "mag_final.tsv", sep="\t")
# mag_final.tsv 里已有 CheckM 谱系解析出的同名列（多数为空），先改名避免冲突
mag = mag.rename(columns={"phylum": "ckm_phylum", "class": "ckm_class",
                          "order": "ckm_order", "family": "ckm_family"})
tax = pd.read_csv(D / "mag_taxonomy.tsv", sep="\t")
mag = mag.merge(tax, left_on="bin", right_on="mag", how="left")
mag["tax_src"] = mag["genus"].notna().map({True: "blast vs iPHoP host genomes (GTDB)",
                                           False: "CheckM lineage only"})
mag["phylum"] = mag["phylum"].fillna(mag["ckm_phylum"])
mag["class"] = mag["class"].fillna(mag["ckm_class"])
mag["order"] = mag["order"].fillna(mag["ckm_order"])
mag["family"] = mag["family"].fillna(mag["ckm_family"])
cols = ["bin", "sample_id", "quality", "completeness", "contamination",
        "Genome size (bp)", "# contigs", "N50 (contigs)", "GC",
        "phylum", "class", "order", "family", "genus", "best_pident", "tax_src"]
mag_out = mag[cols].rename(columns={"Genome size (bp)": "size_bp",
                                    "# contigs": "n_contigs",
                                    "N50 (contigs)": "N50",
                                    "best_pident": "blast_pident"})
mag_out = mag_out.sort_values(["sample_id", "completeness"], ascending=[True, False])
mag_out.to_csv(D / "mag_final_annotated.tsv", sep="\t", index=False)

print(f"=== 最终 MAG: {len(mag_out)} 条 ===")
print(f"  有 GTDB 分类: {mag_out.phylum.notna().sum()}")
print(mag_out.quality.value_counts().to_string())
print("\n按样本：")
print(mag_out.groupby("sample_id").size().to_string())
print("\n门分布：")
print(mag_out.phylum.value_counts().to_string())

# ---------- MAG 内前噬菌体 ----------
pv = pd.read_csv(D / "mag_all_provirus.tsv", sep="\t")
pv["mag"] = pv.seq_name.str.split("|").str[0]
pv["contig"] = pv.source_seq.str.split("|").str[1]

cv = pd.read_csv(D / "quality_summary.tsv", sep="\t")
cv = cv[["contig_id", "checkv_quality", "miuvig_quality", "completeness",
         "completeness_method", "contamination", "proviral_length", "host_genes"]]
cv = cv.rename(columns={"contig_id": "seq_name",
                        "completeness": "checkv_completeness"})

pv = pv.merge(cv, on="seq_name", how="left")
mref = mag_out[["bin", "sample_id", "phylum", "class", "order", "family",
                "genus", "completeness", "contamination", "quality"]].rename(
    columns={"completeness": "mag_completeness",
             "contamination": "mag_contamination",
             "quality": "mag_quality"})
pv = pv.merge(mref, left_on="mag", right_on="bin", how="left")
pv["size_kb"] = (pv.length / 1000).round(1)

out = pv[["mag", "sample_id", "contig", "start", "end", "size_kb", "n_genes",
          "v_vs_c_score", "in_seq_edge",
          "phylum", "class", "order", "family", "genus",
          "mag_completeness", "mag_contamination", "mag_quality",
          "checkv_quality", "miuvig_quality", "checkv_completeness",
          "proviral_length", "host_genes", "integrases"]]
out.to_csv(D / "prophage_in_mags.tsv", sep="\t", index=False)

print(f"\n=== MAG 内前噬菌体: {len(out)} 条 ===")
print("CheckV 质量：")
print(out.checkv_quality.value_counts().to_string())
print("\nMIUViG 质量：")
print(out.miuvig_quality.value_counts().to_string())
print("\n按宿主门：")
print(out.phylum.value_counts().to_string())
print("\n高质量的那几条：")
hq = out[out.checkv_quality.isin(["High-quality", "Complete"])]
for _, r in hq.iterrows():
    print(f"  {r['mag']:<12} {str(r['genus']):<16} {r.size_kb:>6.1f} kb  "
          f"完整 {r.checkv_completeness}  {r.checkv_quality}")

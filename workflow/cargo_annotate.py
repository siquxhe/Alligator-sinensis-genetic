#!/usr/bin/env python3
"""前噬菌体 cargo 注释整合（v2）

判定原则
--------
1. 噬菌体自身基因（结构/包装、裂解、溶源、复制重组、噬菌体特有未知蛋白）**不算 cargo**。
2. cargo = 有明确**细菌来源**功能的基因，即前噬菌体从宿主获得并携带的辅助基因。
3. 距前噬菌体两端 <500 bp 的基因标 `boundary`（可能是 att 位点附近带进来的宿主侧翼序列），
   汇总时同时给出"全部 cargo"和"剔除 boundary"两个口径。

输入（07_cargo/）：all_provirus_genes.tsv, vfdb_hits.tsv, card_hits.tsv, provirus_list.tsv
输出（07_cargo/）：cargo_gene_table.tsv, cargo_provirus_table.tsv, cargo_category_summary.tsv
"""
import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / "07_cargo"

# ============ 1. 读基因表 ============
COLS20 = ["gene", "start", "end", "length", "strand", "gc_content",
          "genetic_code", "rbs_motif", "marker", "evalue", "bitscore",
          "uscg", "plasmid_hallmark", "virus_hallmark", "taxid", "taxname",
          "annotation_conjscan", "annotation_amr", "annotation_accessions",
          "annotation_description"]
g = pd.read_csv(D / "all_provirus_genes.tsv", sep="\t", header=None,
                names=COLS20, dtype=str)
g = g[g["gene"] != "gene"].reset_index(drop=True)
g[["start", "end", "length"]] = g[["start", "end", "length"]].astype(int)

pat = re.compile(r"^(?P<sample>[^|]+)\|(?P<contig>[^|]+)\|provirus_(?P<ps>\d+)_(?P<pe>\d+)_(?P<gno>\d+)$")
g = pd.concat([g, g["gene"].str.extract(pat)], axis=1).dropna(subset=["ps"])
for c in ("ps", "pe", "gno"):
    g[c] = g[c].astype(int)
g["provirus_id"] = (g["sample"] + "|" + g["contig"] + "|provirus_"
                    + g["ps"].astype(str) + "_" + g["pe"].astype(str))
g["prov_len"] = g["pe"] - g["ps"]
g["rel_pos"] = ((g["start"] - g["ps"]) / g["prov_len"]).clip(0, 1)
g["edge_dist"] = pd.concat([g["start"] - g["ps"], g["pe"] - g["end"]], axis=1).min(axis=1)
g["boundary"] = g["edge_dist"] < 500

# ============ 2. 噬菌体自身功能 vs 细菌来源 cargo ============
# ---- 判定顺序：先看是否带噬菌体特异标识，再判宿主来源 cargo ----
# 带这些词的一律归为噬菌体自身
PHAGE_MARK = re.compile(
    r"phage|prophage|bacteriophage|terminase|capsid|portal|tail|baseplate|sheath|"
    r"tape measure|tape-measure|\btac\b|holin|lysin|lysozyme|muramidase|spanin|"
    r"endolysin|amidase|integrase|excisionase|recombinase|repressor|\bcii\b|\bcro\b|"
    r"ninb|\bogr\b|virion|connector|adaptor|scaffold|decorat|prohead|bppu|xkd|hk97|"
    r"pbsx|tp901|\bgp[0-9]|mu-like|lambdoid|siphovir|myovir|podovir|"
    r"antirepressor|intron endonuclease|\bhnh\b|pyocin|orf2/g2p|mystery|stealth",
    re.I)

# 噬菌体模块细分
PHAGE_MODULE = [
    ("噬菌体-包装/结构", ["terminase", "capsid", "portal", "tail", "baseplate", "sheath",
                    "tape measure", "tape-measure", "connector", "adaptor", "scaffold",
                    "head", "neck", "prohead", "bppu", "virion", "decorat", "fiber"]),
    ("噬菌体-裂解", ["holin", "lysin", "lysozyme", "muramidase", "spanin", "endolysin",
                "amidase", "lysis"]),
    ("噬菌体-溶源/调控", ["integrase", "excisionase", "recombinase", "repressor", "cii",
                   "cro", "ninb", "ogr", "antirepressor", "lysogeny"]),
    ("噬菌体-复制/重组", ["dna polymerase", "helicase", "primase", "replication",
                   "exonuclease", "endonuclease", "resolvase", "recombination",
                   "nuclease", "atpase", "maturase", "glucosyltransferase",
                   "deoxyribosyltransferase"]),
]

# 宿主来源辅助基因（cargo）
CARGO_KW = [
    ("毒素-抗毒素", ["pare", "rele", "mazf", "maze", "vapc", "vapb", "higb", "higa",
                 "pemk", "ccdb", "doc toxin", "toxin-antitoxin", "toxin"]),
    ("毒力/氧化应激", ["superoxide dismutase", "sodc", "catalase", "kata", "phospholipase",
                  "collagenase", "adhesin", "hemolysin", "heme uptake", "cysteine hydrolase",
                  "siderophore", "invasion"]),
    ("抗防御/DNA 修饰", ["methyltransferase", "methylase", "dam", "dcm", "ardc",
                    "antirestriction", "restriction", "break"]),
    ("代谢 AMG", ["cyanase", "rhodanese", "phosphatase", "dehydrogenase", "synthase",
              "hydrolase", "kinase", "isomerase", "reductase", "oxidase", "chitinase",
              "carbonic anhydrase", "glutathione", "thioredoxin", "protease",
              "peptidase", "clpp", "proteasome", "ascorbate"]),
    ("转座/移动元件", ["transposase", "insertion sequence", "is element", "mobc", "relaxase"]),
    ("细菌调控", ["lexa", "rcsb", "xerd", "nucleoid", "gyrase", "dnaa", "hd a", "hda"]),
]


def classify(desc):
    """返回 (bucket, category)"""
    if pd.isna(desc) or str(desc).strip() in ("NA", ""):
        return "未注释", "未注释"
    d = str(desc)
    if PHAGE_MARK.search(d):
        for cat, kws in PHAGE_MODULE:
            if any(k in d.lower() for k in kws):
                return "噬菌体固有", cat
        return "噬菌体固有", "噬菌体-其他"
    for cat, kws in CARGO_KW:
        if any(k in d.lower() for k in kws):
            return "宿主来源", cat
    return "其他已注释", "待判读"


_cl = g["annotation_description"].map(classify)
g["bucket"] = [x[0] for x in _cl]
g["func_cat"] = [x[1] for x in _cl]
g["is_phage_intrinsic"] = g["bucket"] == "噬菌体固有"
g["is_cargo"] = g["bucket"] == "宿主来源"

# ============ 3. VFDB ============
v = pd.read_csv(D / "vfdb_hits.tsv", sep="\t", header=None,
                names=["q", "s", "pid", "length", "mm", "go", "qs", "qe",
                       "ss", "se", "ev", "bs", "slen", "st"])
v["qcov"] = v["length"] / v["slen"] * 100
v = v[(v.pid >= 30) & (v.qcov >= 70)].copy()
# header: VFG037029(gb|WP_xxx) (katA) catalase [KatA (VF0454) - Stress survival] [Species]
v["vf_gene"] = v["st"].str.extract(r"\)\s*\(([^)]+)\)")[0]
v["vf_desc"] = (v["st"].str.replace(r"^VFG\d+\([^)]*\)\s*", "", regex=True)
                        .str.extract(r"^\([^)]*\)\s*([^\[]+)\[")[0].str.strip())
v["vf_class"] = v["st"].str.extract(r"\[([^\]]+)\]\s*\[")[0]
v["vf_species"] = v["st"].str.extract(r"\[([^\]]+)\]\s*$")[0]
vb = v.sort_values("bs", ascending=False).drop_duplicates("q")
vb = vb[["q", "vf_gene", "vf_desc", "vf_class", "vf_species", "pid", "qcov", "bs"]]
vb.columns = ["gene", "vf_gene", "vf_desc", "vf_class", "vf_species",
              "vf_pident", "vf_qcov", "vf_bitscore"]

# ============ 4. CARD ============
c = pd.read_csv(D / "card_hits.tsv", sep="\t", header=None,
                names=["q", "s", "pid", "length", "mm", "go", "qs", "qe",
                       "ss", "se", "ev", "bs", "slen", "st"])
c["qcov"] = c["length"] / c["slen"] * 100
c = c[(c.pid >= 30) & (c.qcov >= 70)].copy()
c["aro"] = c["s"].str.split("|").str[2]
c["amr_gene"] = c["s"].str.split("|").str[3]
cb = c.sort_values("bs", ascending=False).drop_duplicates("q")
cb = cb[["q", "amr_gene", "aro", "pid", "qcov"]]
cb.columns = ["gene", "amr_gene", "aro", "card_pident", "card_qcov"]

g = g.merge(vb, on="gene", how="left").merge(cb, on="gene", how="left")

# ---- VFDB 命中回填 cargo 判定 ----
# 只有"确是细菌毒力/应激因子"的命中才算 cargo；
# ligA（连接酶）、clpP（蛋白酶）、rcsB（调控）属看家/调控基因，不计入。
VF_CARGO = {"kata", "kate", "katb", "sodc", "sodci", "sodb", "soda"}
VF_CLASS_CARGO = re.compile(r"heme uptake|iron|siderophore|toxin", re.I)
_vf_g = g["vf_gene"].fillna("").str.lower()
_vf_c = g["vf_class"].fillna("")
_vf_hit_cargo = _vf_g.isin(VF_CARGO) | _vf_c.str.contains(VF_CLASS_CARGO, na=False)
# 这些命中即便代码对上也不算 cargo
_vf_exclude = _vf_g.isin({"liga", "clpp", "rcsb"})
_vf_hit_cargo &= ~_vf_exclude

g.loc[_vf_hit_cargo & ~g["is_cargo"], "bucket"] = "宿主来源"
g.loc[_vf_hit_cargo & ~g["is_cargo"], "func_cat"] = "毒力/氧化应激"
g.loc[_vf_hit_cargo & ~g["is_cargo"], "is_cargo"] = True
# 已有 cargo 判定但被 VFDB 指为毒力的，升级类别
g.loc[_vf_hit_cargo & g["is_cargo"], "func_cat"] = "毒力/氧化应激"

# ============ 5. 逐基因判定 ============
# AMR 有效性：CARD 里 gyrA/gyrB/rpoB/uhpA 等是"突变模型"，不是可转移基因
MUT = re.compile(r"gyrA|gyrB|parC|rpoB|uhpA|16S|23S|rrs|rrl", re.I)
_is_mut = g["amr_gene"].fillna("").str.contains(MUT, na=False)
_has_amr = g["amr_gene"].notna()
g["amr_type"] = None
g.loc[_has_amr & _is_mut, "amr_type"] = "突变模型（非获得性）"
g.loc[_has_amr & ~_is_mut, "amr_type"] = "需人工判读"


def verdict(r):
    """最终 cargo 判词"""
    parts = []
    if pd.notna(r.vf_gene):
        parts.append(f"VFDB:{r.vf_gene}")
    if pd.notna(r.amr_gene):
        parts.append(f"CARD:{r.amr_gene}[{r.amr_type}]")
    if r.is_cargo:
        parts.append(r.func_cat)
    return ";".join(dict.fromkeys(parts))


g["cargo_evidence"] = g.apply(verdict, axis=1)
g.to_csv(D / "cargo_gene_table.tsv", sep="\t", index=False)

# ============ 6. 逐前噬菌体 ============
hq = pd.read_csv(D / "provirus_list.tsv", sep="\t")
hq["provirus_id"] = hq["sample_id"] + "|" + hq["contig_id"]

rows = []
for pid, sub in g.groupby("provirus_id"):
    cargo = sub[sub.is_cargo]
    cats = sorted(set(cargo.func_cat))
    rows.append({
        "provirus_id": pid,
        "sample_id": pid.split("|")[0],
        "prov_len_kb": round(sub.prov_len.iloc[0] / 1000, 1),
        "n_genes": len(sub),
        "n_annotated": int((sub.func_cat != "未注释").sum()),
        "annot_pct": round((sub.func_cat != "未注释").mean() * 100, 1),
        "n_cargo": len(cargo),
        "cargo_cats": ";".join(cats) if cats else "",
        "cargo_genes": " | ".join(
            (str(r.annotation_description)[:34] if pd.notna(r.annotation_description)
             else (f"VFDB:{r.vf_gene}" if pd.notna(r.vf_gene) else "?"))
            for _, r in cargo.head(4).iterrows()),
        "n_boundary": int(sub.boundary.sum()),
        "vfdb_hits": int(sub.vf_gene.notna().sum()),
        "card_hits": int(sub.amr_gene.notna().sum()),
        "has_integrase": bool(sub.annotation_description.fillna("")
                              .str.contains("integrase|excisionase|recombinase", case=False).any()),
        "has_lysin": bool(sub.annotation_description.fillna("")
                          .str.contains("lysin|endolysin|holin", case=False).any()),
        "has_terminase": bool(sub.annotation_description.fillna("")
                              .str.contains("terminase", case=False).any()),
        "has_capsid": bool(sub.annotation_description.fillna("")
                           .str.contains("capsid", case=False).any()),
        "has_tail": bool(sub.annotation_description.fillna("")
                         .str.contains("tail", case=False).any()),
    })
pv = pd.DataFrame(rows).merge(
    hq[["provirus_id", "quality", "completeness", "rpkm", "host_genus", "host_phylum"]],
    on="provirus_id", how="left")
pv["in_hq_set"] = pv["quality"].notna()
pv = pv.sort_values(["sample_id", "prov_len_kb"], ascending=[True, False])
pv.to_csv(D / "cargo_provirus_table.tsv", sep="\t", index=False)

# ============ 7. 汇总 ============
cs = (g[g.is_cargo].groupby("func_cat")
      .agg(n_genes=("gene", "size"),
           n_provirus=("provirus_id", "nunique"))
      .reset_index())
cs["pct_provirus"] = (cs.n_provirus / g.provirus_id.nunique() * 100).round(1)
cs = cs.sort_values("n_provirus", ascending=False)
cs.to_csv(D / "cargo_category_summary.tsv", sep="\t", index=False)

# ============ 8. 打印 ============
n_pv = g.provirus_id.nunique()
print(f"前噬菌体 {n_pv} 条 | 基因 {len(g)} | 有注释 {(g.func_cat != '未注释').sum()} "
      f"({(g.func_cat != '未注释').mean()*100:.0f}%)")
print(f"  噬菌体固有 {(g.func_cat == '噬菌体固有').sum()} | 细菌来源 cargo {g.is_cargo.sum()} "
      f"| 未注释 {(g.func_cat == '未注释').sum()}")
print(f"  边界基因(<500bp) {g.boundary.sum()}")
print("\n=== 噬菌体模块完整性 ===")
for c_ in ["has_terminase", "has_capsid", "has_tail", "has_lysin", "has_integrase"]:
    print(f"  {c_:<14} {pv[c_].sum():>2}/{len(pv)}  ({pv[c_].mean()*100:.0f}%)")
print("\n=== cargo 类别 ===")
print(cs.to_string(index=False))
print("\n=== 带 VFDB 命中的前噬菌体 ===")
for _, r in pv[pv.vfdb_hits > 0].iterrows():
    print(f"  {r.provirus_id:<46} {r.host_genus or '-':<14} VF={r.vfdb_hits} CARD={r.card_hits}")
print("\n中高质量基因组内前噬菌体: ", pv.in_hq_set.sum())

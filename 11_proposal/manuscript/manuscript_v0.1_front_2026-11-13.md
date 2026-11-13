# Manuscript draft v0.1 — front half

**日期** 2026-11-13　|　**范围** Title / Abstract / Introduction / Results 5.1–5.3
**状态** 初稿，待内部审阅；Methods、Discussion、cross-host 一节未写
**约定** 正文英文；`[CIT]` 为待补引用占位，**不得凭印象填写**，须逐条核 PMID/DOI
**依据** `11_proposal/论文提纲_方法学_v2_2026-11-12.md`；数值均来自 Table 1 / Fig 2 / Fig 3

---

## Title

**Definitions, not data: a 171-fold range in the reported viral fraction of a single gut metagenome**

*Alternatives*
- One dataset, four decisions: how reporting choices determine the viral fraction of vertebrate gut metagenomes
- Mind the denominator: four reporting decisions that shift a viral fraction by two orders of magnitude

---

## Abstract

Viral reads typically account for less than one percent of a host-associated shotgun metagenome, yet the resulting percentages are quoted, compared across studies, and increasingly used to benchmark tools. How such a percentage is computed is rarely stated. Using six fecal metagenomes of the Chinese alligator (*Alligator sinensis*), we computed the viral fraction of reads under six reporting definitions that differ along four axes: the denominator, the reference space, the functional categories retained, and the statistical unit. Across definitions and samples the fraction spanned 171-fold, from 0.089% to 15.2%. Most of this range is attributable to definition rather than to biology: within a single sample, definitions alone spanned 22.2- to 124.8-fold, whereas the residual sample effect contributed only 1.37-fold. Median fold changes were 7.1 for the category filter, 5.6 for the reference space, 5.4 for the statistical unit and 1.01 for the denominator; these effects are not multiplicative. The same sensitivity applies to presence-absence: the number of vOTUs detected in all six samples ranged from 0, when presence was called from contigs, to 783 at a permissive read threshold. We propose an eight-item minimum reporting checklist that makes each of these decisions explicit at no additional sequencing cost.

*(~200 words)*

---

## Introduction

Shotgun metagenomes of host-associated microbial communities routinely yield a viral signal of well under one percent of reads [CIT]. That number travels: it is used to argue that the virome is a minor or a major component of a system, to compare hosts and habitats, and increasingly as a reference point against which detection tools are tuned [CIT]. Its small magnitude is precisely what makes it fragile, because at this scale the difference between 0.1% and 0.01% can be produced by decisions taken long before any biological question is asked.

Reporting conventions at the read level are, however, largely unstandardised. The MIUViG standard specifies what must accompany an uncultivated viral genome — its origin, quality, annotation, taxonomy, biogeographic distribution and predicted host — but it does not define how to compute a fraction of reads, nor which reads should be counted as viral [CIT: Roux et al., Nat Biotechnol 2019]. As a consequence, two studies can report "the viral fraction" while measuring different quantities, and a reader has no way to tell.

That tool choice matters is well established. A benchmark of eleven viral prediction tools on low-abundance metagenomes found precision ranging from 10% to 100% depending on the tool, and concluded that the best performance came not from any single tool but from specific two-tool combinations followed by taxonomic filtering [CIT: bioRxiv 2026.10.14.759168, preprint]. Similarly, host read removal has been benchmarked across methods and human reference assemblies, with measurable consequences for retained read composition and for downstream metrics such as average nucleotide identity and diversity [CIT: Forbes et al., Cell Reports Methods 2025]. These are tool-level effects, and they are increasingly well characterised.

What has not been separated is the contribution of the reporting decision itself, with the tools held fixed. Consider four choices that precede any reported fraction: what counts as the denominator; which reference space the reads are compared against; which functional categories of hits are retained; and what statistical unit is counted. If these choices alone move the number substantially, then cross-study comparison fails even when every laboratory uses the same assembler, the same database and the same alignment thresholds — a stricter and less forgiving claim than "tools differ".

Here we quantify that contribution on a single dataset, so that tools and data are constant by construction. Using six fecal metagenomes of the Chinese alligator, we computed the viral fraction of reads under six definitions that vary one axis at a time, and we asked how much of the observed range is definition and how much is sample. We then applied the same logic to a second, threshold-driven quantity — the number of vOTUs shared across samples — and translated the results into a minimum reporting checklist. We do not claim an ecological result, we do not identify a correct definition, and we do not argue that any of the six is preferable; the claim is narrower, and we hope harder to dismiss: at this signal scale, the definition is a larger source of variation than the biology.

---

## Results

### A fraction cannot be reported before four decisions are made

Every reported viral fraction is the product of four choices, whether or not they are stated (Fig. 1). The denominator decides what counts as 100%: all reads, or reads remaining after host removal. The reference space decides what the reads are compared against: a public protein database, a study-assembled catalog, or the values reported by an earlier study. The category filter decides which hits are admitted: any viral-like hit, or only those annotated to categories whose viral origin is unambiguous. The statistical unit decides what is counted: reads, contigs, or abundance-weighted values.

We measured each choice with the other three held fixed, across six fecal metagenomes of *Alligator sinensis* (PRJNA539906; n = 6). Median fold changes were 7.1 for the category filter, 5.6 for the reference space, 5.4 for the statistical unit and 1.01 for the denominator (Fig. 1). These values are not multiplicative: their product (≈217) exceeds the observed overall span of 171-fold, because each ratio is computed within a different sample and a different pair of definitions.

The near-unity value of the denominator deserves comment, because it is a null result and we report it as such. Host reads made up only 0.07–2.51% of these libraries, so removing them changed the fraction by at most 1.2% (Fig. 2A, Table 1, C2 versus C6). This is a property of fecal samples with low host content, not a general rule: in high-host or low-viral-biomass material the same axis can dominate, and the choice of host-removal method is itself a variable that must be declared [CIT: Forbes et al. 2025].

### Six definitions of one measurement span 171-fold

Applying the six definitions to the same six samples produced fractions from 0.089% to 15.2%, a 171-fold range (Fig. 2A; Table 1). The extremes were not the same sample measured two ways, but two different samples under two different definitions (0.089%, sample W2, strict category filter; 15.2%, sample S3, vOTU reference). The range therefore conflates two sources of variation, and we separated them.

Within any single sample, changing the definition alone spanned 22.2- to 124.8-fold. Holding the strictest definition fixed and varying the sample instead spanned only 1.37-fold. The observed 171-fold is their product (124.8 × 1.37 ≈ 171): the definition effect is the larger term by roughly two orders of magnitude, and it is the term that a reader cannot see in a published percentage.

The six definitions behave as their construction predicts. The category filter produces the largest step, 7.1-fold, from 0.089–0.122% (strict) to 0.675–0.702% (broad), because 47.4% of viral-like hits are annotated to metabolic and housekeeping categories that are shared with bacteria [CIT: CheckAMG, bioRxiv 2026.09.23.753886, preprint]. This is a homology problem, not a question of how much evidence is required: the excluded genes are functional proteins, and no sequence-based rule can decide whether a given hit is a genuine auxiliary metabolic gene or a bacterial homolog. The reference space contributes a further 5.6-fold, and the statistical unit 5.4-fold, when reads are replaced by contigs.

### Shared vOTUs are a function of the detection threshold

The same dependence appears in a quantity that is not a fraction at all. Counting the vOTUs detected in all six samples gave 0 when presence was called at the contig level; 783 at RPKM > 0; 517 at RPKM ≥ 0.01; 63 at RPKM ≥ 0.1; 5 at RPKM ≥ 1; and 1 at RPKM ≥ 10 (Fig. 3A). The direction of the change is monotonic, but its interpretation is not: "no vOTU is shared" and "783 vOTUs are shared" are both correct statements about the same six libraries.

The proportion of vOTUs found in a single sample is likewise threshold-dependent, and its shape is informative (Fig. 3B). It is 84.5% when presence is called from contigs, falls to 6.0–10.8% at permissive read thresholds, and rises again to 49.4% and 55.2% at RPKM ≥ 1 and ≥ 10 — although the last two are computed over the 6,041 and 310 vOTUs that pass those thresholds, not over the full catalog. The two ends of this U-shape have opposite causes. At the contig end, the high value reflects assembly fragmentation: the same virus assembled into different fragments in different samples cannot be clustered into a shared vOTU. At the stringent end, it reflects genuine sample specificity of abundant viruses. A single reported value, without its threshold, cannot distinguish the two.

Sample-to-sample similarity shows the same ambiguity with less drama: median Jaccard similarity across the 15 sample pairs was 0.0065 when computed from contig presence and 0.0234 when computed from abundance-weighted reads at RPKM ≥ 1, a 3.6-fold difference in the same direction (Fig. 3C). Throughout, the low absolute values are consistent with the individual specificity widely reported for viromes [CIT]; the point here is not that the communities are dissimilar, but that the degree of dissimilarity is partly a property of the method used to measure it.

---

## 待补引用清单（写作时逐条核实）

| 编号 | 位置 | 需要什么 | 状态 |
|---|---|---|---|
| CIT-1 | Intro ¶1 | 病毒 reads 常 <1% 的权威综述或代表性研究 | ⬜ 待检索 |
| CIT-2 | Intro ¶1 | "该数字被广泛用于跨研究比较"的例证 | ⬜ 待检索 |
| CIT-3 | Intro ¶2 | MIUViG（Roux et al., Nat Biotechnol 2019;37:29–37, doi:10.1038/nbt.4306） | ✅ 已核实 |
| CIT-4 | Intro ¶3 | 病毒识别工具基准（bioRxiv 2026.10.14.759168，**预印本**） | ✅ 已核实，需标 preprint |
| CIT-5 | Intro ¶3 | Forbes et al., Cell Reports Methods 2025, doi:10.1016/j.crmeth.2025.101218 | ✅ 已核实 |
| CIT-6 | Results 5.1 | 同上（Forbes） | ✅ |
| CIT-7 | Results 5.2 | CheckAMG（bioRxiv 2026.09.23.753886，**预印本**，PMID 42818345） | ✅ |
| CIT-8 | Results 5.3 | 病毒组高度个体特异性的代表性研究 | ⬜ 待检索 |
| CIT-9 | Methods（未写） | Tang et al., Front Microbiol 2019;10:2409 | ✅ |

---

## 写作说明（内部）

**为什么不写 Methods。** 前半部分先把"问题—做法—结果"立住；Methods 依赖最终参数表（尤其 geNomad 版本、DIAMOND 参数），等 cross-host 一节定了再一次性写，避免两次返工。

**哪些数字是从表里取的、哪些是算的。** 22.2/124.8/1.37/171 来自 `01_compute_five_denominators.py` 的诊断输出，与 Table 1 一致；47.4% 来自 `viral_function_profile.tsv` 的 ALL 行；0/783/517/63/5/1 与 84.5/6.0/10.8/49.4/55.2 来自 `threshold_sweep.tsv`。**写作时不得凭记忆改数。**

**已避开的三处过度表述。**
1. 不说"分母不重要"，只说"在本批低宿主粪便样本中 ≤1.2%，且去除方法本身是必须声明的变量"。
2. 不说"类别筛选=要求更多证据"，明写是同源性问题。
3. 不说"六样本零共享"，明写这是 contig 层面的判定结果，并给出三种阈值下的对照。

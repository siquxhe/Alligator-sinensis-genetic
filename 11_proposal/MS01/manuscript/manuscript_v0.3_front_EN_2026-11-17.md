# Manuscript front half — English v0.3

> **已被 v0.4 取代（2026-11-20 标注）**：本文是 2026-11-17 的快照，其中 "roughly six-fold" 一项已被纠正——
> 同样本同参数为 **4.96×**，匹配实验为 **6.89×**，两者相差 40% 且不调和。
> 数字与正文一律以 `manuscript_v0.4_full_EN_2026-11-19.md` 为准；本文保留作版本对照，不再单独维护。


**日期** 2026-11-17　|　**范围** Title / Abstract / Introduction / Results 5.1–5.4
**状态** 投稿英文稿第一版，由中文 v0.2 回译并逐数核对；Methods、Discussion 未写
**约定** `[CIT-n]` 为待补引用占位，**不得凭印象填写**；数值全部取自 Table 1 / Table 2 / Fig 1–3 与 `13_calibration/`
**依据** `manuscript_v0.2_front_中文_2026-11-13.md`（唯一准据）；英文措辞参考 v0.1，**数字一个未沿用**

> 相对 v0.1 的三处论断变更：171× → **25.9×**；"定义压倒生物学（约 90 倍）" → **"定义与样本同量级"**；
> "两个数量级" → **一个数量级以内**（26 倍）。v0.1 已标"暂停维护"，不得与本稿混用。

---

## Title

**Four reporting decisions, only one of which moves the number: a 26-fold range in the viral fraction of one gut metagenome dataset**

*Alternatives*
- One dataset, four decisions: how reporting choices set the viral fraction of vertebrate gut metagenomes
- Mind the denominator: how four reporting decisions shift a viral fraction by more than an order of magnitude

---

## Abstract

Viral reads typically account for less than one percent of a host-associated shotgun metagenome, yet the resulting percentages are quoted, compared across studies, and increasingly used to benchmark tools. How such a percentage is computed is rarely stated. Using six fecal metagenomes of the Chinese alligator (*Alligator sinensis*), we computed the viral fraction of reads under six reporting definitions that differ along four axes: the denominator, the reference space, the functional categories retained, and the counting unit. Across definitions and samples the fraction spanned 26-fold, from 0.59% to 15.2% — far less than the 171-fold we obtained when the same reads were screened against a general viral database, a difference traceable to that database's near-absence of phage proteins. More importantly, only one of the four decisions moves the number: the category filter changes the fraction 4.6-fold (2.6–5.2, n = 6), whereas the reference space, the counting unit and the denominator each change it by 1.0–1.1-fold. That fold change survived four independent checks: a different reference database (3.6–6.9-fold), a different read source (5.05 versus 5.17-fold), a stricter identity threshold of 90% (4.4-fold), and randomized decoy sequences (0 hits). Sample-to-sample variation was 1.6–7.1-fold, the same order of magnitude as the definition effect — which is why the definition has to be stated, not because definition overwhelms biology. We then calibrated the detection step with spike-ins of known abundance: recovery was 88.8% under the broad and 59.7% under the strict definition, and calibration returned estimates to within 1.2 percentage points of the known value. Spike-ins below about 1% could not be separated from background (a 0.1% spike raised the reading by 2.0% relative), and public datasets rarely carry the technical controls needed to trace absolute bias. We close with an eight-item minimum reporting checklist that makes each of these decisions explicit at no additional sequencing cost.

*(~285 words)*

---

## Introduction

Shotgun metagenomes of host-associated microbial communities routinely yield a viral signal well under one percent of reads [CIT-1]. That number travels: it is used to argue that the virome is a minor or a major component of a system, to compare hosts and habitats, and increasingly as a reference point against which detection tools are tuned [CIT-2]. Its small magnitude is precisely what makes it fragile, because at this scale the difference between 0.1% and 0.01% can be produced by decisions taken long before any biological question is asked.

Reporting conventions at the read level are, however, largely unstandardised. The MIUViG standard specifies what must accompany an uncultivated viral genome — its origin, quality, annotation, taxonomy, biogeographic distribution and predicted host — but it does not define how to compute a fraction of reads, nor which reads should count as viral [CIT-3]. As a consequence, two studies can both report "the viral fraction" while measuring different quantities, and a reader has no way to tell.

That tool choice matters is well established. A benchmark of eleven viral prediction tools on low-abundance metagenomes found precision ranging from 10% to 100%, and concluded that the best performance came not from any single tool but from specific two-tool combinations followed by taxonomic filtering [CIT-4]. Host read removal has likewise been benchmarked across methods and reference assemblies, with measurable consequences for the retained read composition and for downstream metrics such as average nucleotide identity and diversity [CIT-5]. These are tool-level effects, and they are increasingly well characterised.

What has not been separated is the contribution of the reporting decision itself, with the tools held fixed. Four choices precede any reported fraction: what counts as the denominator; which reference space the reads are compared against; which functional categories of hits are retained; and what statistical unit is counted. If these choices alone move the number substantially, then cross-study comparison fails even when every laboratory uses the same assembler, the same database and the same alignment thresholds — a stricter and less forgiving claim than "tools differ".

Here we quantify that contribution on a single dataset, so that tools and data are constant by construction. Using six fecal metagenomes of the Chinese alligator, we computed the viral fraction of reads under six definitions that vary one axis at a time, and asked how much of the observed range is definition and how much is sample. We then applied the same logic to a second, threshold-driven quantity — the number of vOTUs shared across samples — and translated the results into a minimum reporting checklist. We do not claim an ecological result, we do not identify a correct definition, and we do not argue that any of the six is preferable. The claim is narrower, and we hope harder to dismiss: at this signal scale, the definition and the biology contribute variation of the same order.

---

## Results

### 5.1 A fraction cannot be reported before four decisions are made

Every reported viral fraction is the outcome of four choices, whether or not they are stated (Fig. 1). The **denominator** decides what counts as 100%: all reads, or reads remaining after host removal. The **reference space** decides what the reads are compared against: a public protein database, a study-assembled catalogue, or values reported by an earlier study. The **category filter** decides which hits are admitted: any viral-like hit, or only those annotated to categories whose viral origin is unambiguous. The **counting unit** decides what is counted: reads, contigs, or abundance-weighted values.

One methodological qualification is needed up front. As implemented here, the fourth axis changes the detection level as well — at the read level hits are called by protein alignment, at the contig level by gene-based genome assignment. It therefore returns an upper bound for that axis rather than a pure unit effect. We separated the two with a controlled comparison in 5.2.

We measured each choice with the other three held fixed, across six fecal metagenomes of *Alligator sinensis* (PRJNA539906; n = 6). Median fold changes were 4.6 for the category filter, 1.1 for the reference space, 1.0 for the counting unit and 1.01 for the denominator (Fig. 1). That is, of the four decisions that all have to be declared, **only one materially changes the number**; the other three are near-null in this dataset. These fold changes are neither multiplicative nor additive: a median ratio identifies which axis matters, and cannot be used to reconstruct the overall span, which is set by the extremes of four definitions across six samples (26-fold measured). The reference-space value deserves emphasis: it is **1.1-fold, not 5.6-fold**. An initial calculation with RVDB-prot gave 5.6-fold, but that database contains almost no phage proteins (see 5.2); with a phage-specific database the effect all but disappears.

The near-unity denominator needs separate comment, because it is a null result and we report it as such. Host reads made up only 0.07–2.51% of these libraries, so removing them changed the fraction by at most 1.2% (Fig. 2A, Table 1, C2 versus C6). This is a property of fecal samples with low host content, not a general rule: in high-host or low-viral-biomass material the same axis can become the dominant source, and the choice of host-removal method is itself a variable that must be declared [CIT-5].

### 5.2 Six definitions of one measurement span 26-fold

Applying the six definitions to the same six samples produced fractions from **0.59% to 15.2%, a 26-fold range** (Fig. 2A; Table 1). The extremes are not one sample measured two ways but **two different samples under two different definitions** (0.59%: sample W2, strict category filter; 15.2%: sample S3, vOTU reference). The range therefore conflates two sources of variation, and we separated them.

Within any single sample, the four definitions spanned **4.7–8.4-fold**. Conversely, holding a definition fixed and varying the sample spanned 1.6-fold (broad), 3.1-fold (strict) and 7.1-fold (vOTU reference). **Definition and sample effects are of the same order** — the opposite of our initial conclusion that definition exceeded sample by roughly ninety-fold, which was inflated by a reference database that lacked phage proteins. Being of the same order does not make the decision optional: precisely because the two are comparable, a value obtained under one definition cannot be told apart from a difference between samples.

The six definitions behave as their construction predicts. The category filter produces the largest step, **4.6-fold**, from 0.59–1.82% (strict) to 2.89–4.71% (broad), because only **19.3%** of broad hits fall in the structural or replication/transcription categories: **55.2% have unknown function**, 10.4% are moron or auxiliary metabolic genes, 10.6% fall into other annotated categories, and 4.0% relate to integration and excision [CIT-6]. **This is a problem of attributability, not of how much evidence is demanded**: the excluded hits are proteins like any other, and no sequence-based rule can decide whether a given hit came from a virion, a prophage remnant, or a cellular homologue. It is worth noting that more than half of the hits carry no functional description at all — **in this field, half of what passes for "viral protein" is uncharacterised, and the definition forces us to adjudicate that half**.

The reference space retains only **1.1-fold** (0.63–3.23) once a phage-specific database is used. Our initial 5.6-fold was traced, after the fact, not to a general property of "switching databases" but to **a compositional defect of the database used**: the project's RVDB-prot v32 Unique contains 783,103 proteins, dominated by eukaryotic and RNA viruses (SARS-CoV-2, marine RNA viruses, insect viruses), with phage proteins severely underrepresented. Screening the same reads against PHROG (868,340 proteins) raised total hits from 0.84% to 4.17%, roughly six-fold; randomized decoy sequences returned 0 hits, ruling out false positives. **The correct statement for this axis is therefore conditional: it moves the number only when the reference database systematically lacks the target group — and that kind of absence announces itself nowhere.**

The fourth axis was originally recorded as 5.4-fold (C4/C2), but that figure **cannot be read as a unit effect**, because it changes two things at once: the counting unit (reads versus contigs) and the detection level (read-level protein alignment versus contig-level genome assignment). To separate them we mapped each sample's reads back onto **its own** viral contig set, so that the reference set was identical and only the unit changed.

Across the six samples the contig-to-read ratio was **0.485, 0.853, 1.606, 1.479, 1.129 and 0.896**, median **1.01**. Changing the unit therefore does not change the estimate on average, but the ratio scatters **3.3-fold** between samples (0.49–1.61); within the same samples, the read-based fraction itself spans 7.97-fold and the contig-based fraction 9.44-fold.

The point of this control is not a different number but a different attribution: **almost all of the 5.4-fold came from the detection method and the reference set, while the counting unit itself has a median effect of 1.0-fold.** Calling that axis "statistical unit" would systematically overstate the role of the unit, and would invite the reading that switching from reads to contigs explains most of the disagreement. We therefore label the item "counting unit (including detection level)" in Table 2, and recommend that the two be reported separately.

### 5.3 The number of shared vOTUs is a function of the detection threshold

The same dependence appears in a quantity that is not a fraction at all. Counting the vOTUs detected in all six samples gave **0** when presence was called at the contig level; **783** at RPKM > 0; 517 at RPKM ≥ 0.01; 63 at RPKM ≥ 0.1; **5** at RPKM ≥ 1; and **1** at RPKM ≥ 10 (Fig. 3A). The direction of change is monotonic, but its interpretation is not: "no vOTU is shared" and "783 vOTUs are shared" are both correct statements about the same six libraries.

The proportion of vOTUs found in a single sample is likewise threshold-dependent, and its shape is informative (Fig. 3B). It is 84.5% when presence is called from contigs, falls to 6.0–10.8% at permissive read thresholds, and rises again to 49.4% and 55.2% at RPKM ≥ 1 and ≥ 10 — although the last two are computed over the 6,041 and 310 vOTUs that pass those thresholds, not over the full catalogue of 9,980. **The two ends of this U-shape have opposite causes.** At the contig end, the high value reflects assembly fragmentation: the same virus assembled into different fragments in different samples cannot be clustered into one vOTU. At the stringent end, it reflects genuine sample specificity of abundant viruses. A single reported value, without its threshold, cannot distinguish the two.

Sample-to-sample similarity shows the same ambiguity with less drama: median Jaccard similarity across the 15 sample pairs was 0.0065 when computed from contig presence and 0.0234 when computed from abundance-weighted reads at RPKM ≥ 1, a 3.6-fold difference in the same direction (Fig. 3C). Both absolute values are low, consistent with the individual specificity widely reported for viromes [CIT-7]; the point here is not that the communities are dissimilar, but that **the degree of dissimilarity is partly a property of the method used to measure it.**

### 5.4 Spike-in calibration against a known truth: what can and cannot be corrected

Every fold change above rests on the assumption that the measurement itself is accurate, and that assumption had not been tested. We spiked three pure-culture phages from three different families (T4, Lambda, T7) into a real fecal background at 0.1%, 1% and 5%, in triplicate at each level, with the true value known to four decimal places, and then measured them with the same rules.

**The linearity of the model is exact.** Under a given rule, the reading is strictly linear in the spiked fraction (`est(f) = B(1−f) + rec·f`; R² = 1.000 for all four rules). The intercept of that regression is the background reading B and the slope is the recovery:

| Rule | Background B | Recovery (rec) | Error after calibration |
|---|---|---|---|
| PHROG / broad | 4.156% | **88.75%** | ≤0.2 pp |
| PHROG / strict | 0.799% | **59.74%** | ≤0.5 pp |
| RefSeq / broad | 1.267% | 89.28% | ≤0.5 pp |
| RefSeq / strict | 0.335% | 55.07% | ≤1.2 pp |

**First conclusion: the cost of a strict definition is sensitivity, not accuracy.** Its background reading is indeed lower (0.8% against 4.2%), but its recovery is only 59.7% — **four tenths of the true viruses are missed**, so calibration has to multiply by 1.67 and magnifies the noise accordingly; the broad definition multiplies by 1.13. Looking stricter is not the same as being closer to the truth. The criterion should be the residual uncertainty after calibration, which scales as 1/rec.

**Second conclusion: low fractions cannot be separated from background, and that is not a question of accuracy.** A 0.1% spike raised the reading by only 2.0% relative to background (+0.085 percentage points), whereas a 5% spike raised it by 102%. In a sample whose background is of order 4%, differences below roughly 1% therefore cannot be resolved at all — **what should be reported is a limit of detection, not a precise value.**

**Third conclusion: the label "strict" hides another 3-fold of freedom.** Decomposing the combined definition, structural proteins alone give **14.9-fold** (5.4–21.0), replication/transcription genes alone **6.6-fold** (4.9–7.0), and only their combination 4.6-fold; structural proteins account for a median of just 31.3% of the strict category. **We criticise others for leaving the definition unstated, yet our own "strict" is equally a word that needs defining.**

**Fourth conclusion: the dominant bias is procedural, not statistical, and it is not recoverable.** These data come from total-DNA metagenomics (direct column extraction, without viral-particle enrichment), so the 20–75% extraction recoveries reported for enrichment protocols do not apply; the full-chain recovery of this dataset is estimated at about **0.76** (0.85 × 0.89), corresponding to a calibration factor of about 1.3. But the original study **used no internal standard** (no ERCC, no phage spike), while viral sequences make up only 0.1–5% of total DNA and are therefore a very low-abundance template — **library amplification bias can be neither quantified nor reconstructed afterwards.** This is not a failing of one study; it is a failing of current data-sharing practice.

---

## 待补引用清单（内部，写投稿版前逐条核实）

| 编号 | 位置 | 需要什么 | 状态 |
|---|---|---|---|
| CIT-1 | Intro ¶1 | 病毒 reads 通常 <1% 的权威出处 | ⬜ 待检索 |
| CIT-2 | Intro ¶1 | "该数字被广泛用于跨研究比较"的例证 | ⬜ 待检索 |
| CIT-3 | Intro ¶2 | MIUViG，Roux et al., Nat Biotechnol 2019;37:29–37, doi:10.1038/nbt.4306 | ✅ 已核实 |
| CIT-4 | Intro ¶3 | 病毒识别工具基准，bioRxiv 2026.10.14.759168（**预印本**） | ✅ 已核实 |
| CIT-5 | Intro ¶3 / 5.1 | Forbes et al., Cell Reports Methods 2025, doi:10.1016/j.crmeth.2025.101218 | ✅ 已核实 |
| CIT-6 | 5.2 | CheckAMG，bioRxiv 2026.09.23.753886（**预印本**，PMID 42818345） | ✅ 已核实 |
| CIT-7 | 5.3 | 病毒组个体特异性的代表性研究 | ⬜ 待检索 |
| CIT-8 | Methods（未写） | Tang et al., Front Microbiol 2019;10:2409 | ✅ 已核实 |

## 数值溯源表（内部，改稿必回表）

| 数字 | 值 | 来源 |
|---|---|---|
| 总跨度 26 倍（25.9×） | 15.229 / 0.589 | `Table1_five_denominators.tsv`，复算 |
| C1 严格 | 0.589–1.818% | `09_tables/phrog_6samples.tsv` |
| C2 宽 | 2.890–4.708% | 同上 |
| 类别筛选 4.6（2.6–5.2） | C2/C1 六样本中位 | 同上，复算 |
| 参考空间 1.1（0.63–3.23） | C5/C2 六样本中位 | 同上，复算 |
| 计数对象 1.01（0.49–1.61） | 受控对照中位 | `unit_axis_alligator.tsv` |
| 分母 1.01（1.00–1.01） | C2/C6 | `Table1_five_denominators.tsv` |
| 样本内极差 4.7–8.4 | 逐样本极值 | `02_plot_fig2.py` 运行时输出 |
| 样本效应 1.6 / 3.1 / 7.1 | C2 / C1 / C5 极差 | 同上 |
| 四库比值 3.6–6.9 | 四库交叉验证 | `09_tables/reference_library_comparison.tsv` |
| 序列来源 5.05 vs 5.17 | sub.fq vs 全量 | `10_reports/MS01/phrog_library_report.md` |
| 90% 阈值 4.4、诱饵 0 命中 | 阈值扫描与诱饵 | `13_calibration/参考库核查_2026-11-15.md` |
| PHROG 构成 19.3 / 55.2 / 10.4 / 10.6 / 4.0 | 宽口径命中分类 | `phrog_6samples.tsv` + 类别分解 |
| 命中 0.84 → 4.17% | RVDB 对 PHROG | `参考库核查_2026-11-15.md` |
| 回收率 88.75 / 59.74 / 89.28 / 55.07 | 四规则 | `13_calibration/校准_2026-11-16.md` §三 |
| 校准后误差 ≤0.2 / 0.5 / 0.5 / 1.2 pp | 四规则 | 同上 §四 |
| 结构 14.9（5.4–21.0）/ 复制 6.6（4.9–7.0）/ 合并 4.6 | 严格类内部分解 | `复核_B方案_2026-11-16.md` §五 |
| 全链条 0.76（0.85×0.89）→ 1.3 | 流程回收 | `B2评估_2026-11-16.md` §十二 |
| 阈值序列 0/783/517/63/5/1；84.5/6.0–10.8/49.4/55.2；6,041 与 310；9,980 | 阈值扫描 | `threshold_sweep.tsv` |
| Jaccard 0.0065 / 0.0234（3.6×） | 15 对样本 | `fig_a2` 扫描输出 |
| 单样本 reads 跨 7.97、contig 跨 9.44 | 同一批样本 | `unit_axis_alligator.tsv` 复算 |

## 写作说明（内部）

**标题里的一处精确化。** 中文稿与 v0.1 均写 "a single gut metagenome"，但 26 倍是**六样本 × 六定义**的极值之比，
单样本内只有 4.7–8.4 倍。严格说这 26 倍跨越了样本，若标题写 "single metagenome" 会被审稿人直接指出。
故改为 "one gut metagenome dataset"，保留"同一批数据"的修辞对比，同时不假称来自单一样本。
若要更强的表述，可改为 "across six metagenomes from one host species"，但那会削弱"数据相同"这一对照。

**翻译而非重写。** 本稿严格跟随中文 v0.2 的段落顺序与论证顺序，只做英文表达层面的重组：拆长句、补连接词、把"也就是说"类的口头过渡换成书面过渡。**未新增任何主张**，也未删减任何限定条件。

**一处有意的偏离。** 中文 v0.2 §5.4 有一句"（此处曾误写为'高估 42 倍'，那是对两个不同分母的读数相除，已撤回。）"——这是内部修订痕迹，投稿文本不宜出现（读者没有"上一版"可比），故移到本说明里保留记录。同样，5.1/5.2 里"初版 5.6 倍"改为"an initial calculation with RVDB-prot gave 5.6-fold"，读作分析过程而非稿件历史。

**单位统一。** 校准误差一律用 percentage points（pp），避免与相对误差混淆；正文中的"1.2 个百分点"即指此。中文稿写"≤1.2%"，英文按 pp 展开。

**两条没有写进正文的限定**（留给 Discussion）：
1. 六样本同一宿主，样本效应被低估；跨宿主时该效应应更大。
2. 第二数据集（鸡肠道）同一受控对照的中位比值为 0.554，与扬子鳄的 1.01 方向、量级都不同，说明**单位效应本身不稳定**，不能外推——这条是 Table 2 第 4 项"建议分开报告"的直接理由，但目前只有两个数据集，尚不足以作为独立结论。

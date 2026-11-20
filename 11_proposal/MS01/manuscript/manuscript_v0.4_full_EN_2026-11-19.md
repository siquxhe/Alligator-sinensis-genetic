# Manuscript — English v0.4 (full draft)

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

Shotgun metagenomes of host-associated microbial communities yield a viral signal of at most a few percent of reads, and usually far less [CIT-1]. That number travels: it is used to argue that the virome is a minor or a major component of a system, to compare hosts and habitats, and increasingly as a reference point against which detection tools are tuned [CIT-2]. Its small magnitude is precisely what makes it fragile, because at this scale the difference between 0.1% and 0.01% can be produced by decisions taken long before any biological question is asked.

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

The reference space retains only **1.1-fold** (0.63–3.23) once a phage-specific database is used. Our initial 5.6-fold was traced, after the fact, not to a general property of "switching databases" but to **a compositional defect of the database used**: the project's RVDB-prot v32 Unique contains 783,103 proteins, dominated by eukaryotic and RNA viruses (SARS-CoV-2, marine RNA viruses, insect viruses), with phage proteins severely underrepresented. Screening the same reads against PHROG (868,340 proteins) raised total hits from 0.84% to 4.17%, roughly six-fold; under matched search settings, in which only the library varies, the effect is **6.9-fold** (Materials and Methods). Randomized decoy sequences returned 0 hits, ruling out false positives. **The correct statement for this axis is therefore conditional: it moves the number only when the reference database systematically lacks the target group — and that kind of absence announces itself nowhere.**

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

## Discussion

**Of the four decisions, only one moves the number.** Any viral-fraction estimate requires four choices: what counts as the denominator, which reference space is searched, which functional categories are retained, and whether reads or contigs are counted. Holding the data and the tools fixed, only the third one matters materially — excluding metabolic, housekeeping and functionally unannotated hits lowers the fraction 4.6-fold (2.6–5.2, n = 6). The other three each move it by 1.0–1.1-fold. This asymmetry is inconvenient for a field whose methods sections routinely specify the aligner and the e-value while leaving the counted categories unstated, even though that is the choice with the larger effect.

**The reference-space result is conditional, and the condition is invisible.** Within this study, moving between two phage-specific references — the PHROG protein database and the study's own 9,980 vOTUs — changes the fraction by only 1.1-fold. Moving from a general viral database to a phage-specific one changes it 6.9-fold. Both statements are correct, and the difference between them is the whole point: **a reference space matters only when it systematically lacks the target group, and that kind of absence announces itself nowhere.** RVDB-prot v32 Unique, with 783,103 proteins dominated by eukaryotic and RNA viruses, is not a defective database; it is a database built for a different question, and its construction explicitly excludes bacterial viruses [CIT-9]. That exclusion is stated in the original publication, but not in the name, the file header, or the size of the download. A user who screens a gut metagenome against it will obtain a number, and the number will be wrong by roughly sevenfold, with no error message.

**The revision of our own estimate can be located precisely, which is itself the argument.** Our initial analysis reported a 171-fold span; the present one reports 26-fold. The contraction ratio is 6.60, the increase in the strict-category floor is 6.62, and the library effect measured under identical search settings is 6.89 — three independent quantities that agree. The entire revision is therefore attributable to the reference space, not to a threshold change, not to a parameter change, and not to a software version. We report this because it is a rare case in which a published-style number can be traced back to a single cause; in most retractions of this kind the original intermediate files are gone, and the cause remains a conjecture. **The ability to locate the cause depended on the raw reads and the intermediate hit tables still existing.** Reanalysability is not a luxury.

**Definition and biology are of the same order, which is why the definition must be stated.** Sample-to-sample variation spans 1.6-fold (broad), 3.1-fold (strict) and 7.1-fold (vOTU reference), against a 4.6-fold definition effect. Our initial claim that definition exceeded biology by roughly ninetyfold was an artefact of the reference-space defect described above. The corrected claim is weaker and more useful: because the two contributions are comparable, **a value obtained under one definition cannot be distinguished from a difference between samples** — the ambiguity is not resolved by more sequencing, only by stating the definition.

**Calibration corrects sensitivity, not composition.** Spike-ins of known abundance returned recoveries of 88.75% (broad) and 59.74% (strict), and applying them brought estimates to within 0.2 and 0.5 percentage points of truth. But the intercept of the same regression — the background reading B, 4.156% and 0.799% — cannot be decomposed by this design: it pools genuine viral signal with homology-driven misassignment, and treating it as false positives would drive the strict estimate negative. Two consequences follow. First, in a sample whose background is of order 4%, a 0.1% spike raises the reading by 2.0% relative and cannot be resolved; **what should be reported is a limit of detection, not a precise value.** Second, the largest bias in these data is procedural rather than statistical: the libraries were prepared without an internal standard, from a template in which viral DNA is a minor component, so amplification bias can be neither quantified nor reconstructed after the fact. Spike-in calibration, however well designed, cannot recover what was never measured.

**Two limits on generality.** First, all six libraries come from one host species, so the sample effect measured here is a within-species effect and is almost certainly an underestimate of the between-host variation that a cross-species comparison would encounter; the 26-fold span should be read as a lower bound on the definition-and-sample range, not as a property of gut metagenomes in general. Second, the counting-unit effect does not replicate in direction. Mapping reads back to each sample's own viral contigs, so that only the unit changes, gives a median contig-to-read ratio of 1.01 (0.49–1.61) in the alligator libraries but 0.554 (0.49–0.68) in an independently processed chicken gut dataset. A ratio near 1 means the two units agree on average; a ratio near 0.5 means contig counting loses half the signal. **That the direction differs between two datasets processed by the same rules is precisely why the unit should be reported separately rather than assumed to be interchangeable.**

**What we are not claiming.** We do not identify a correct definition, we do not argue that any of the six is preferable, and we do not claim an ecological result. The claim is narrower: at this signal scale, the reporting decisions contribute variation of the same order as the biology, one of them dominates, and none of them is currently stated. The eight-item checklist in Table 2 makes each decision explicit at no additional sequencing cost; its value is that it converts an unstated choice into a recordable one.

**Limitations.** The sample size is six, the host range is one species, and the spike-in experiment is in silico — it mixes reads by proportion and therefore bypasses extraction, library preparation and amplification, so extraction efficiency is assumed to be 100%, an assumption that real capsid lysis resistance can violate by orders of magnitude. The calibration therefore bounds the detection step, not the full chain. The decoy control rules out false positives from the search itself (0 hits in 2,499,996 reads against a shuffled database) but does not address misassignment between genuine viral and bacterial homologues, which is a property of the reference content rather than of the search.

---

## Materials and Methods

**Metagenomes and host removal.** Six fecal metagenomes of the Chinese alligator (*Alligator sinensis*) were retrieved from PRJNA539906, comprising three hibernation-season libraries (W1–W3; SRR14300938, SRR14300939, SRR14300942) and three active-season libraries (S1–S3; SRR14300940, SRR14300941, SRR14300943). All were paired-end. Reads were quality-filtered with fastp 1.0.1 using `-q 20 -l 50`, with adapter detection, poly-G trimming and sliding-window quality cutting at default settings. Host reads were removed with bowtie2 2.5.5 against the *A. sinensis* reference GCA_000455745.1 (3.0 Gb; ENA AVPB01000001) using `--un-conc-gz --no-unal` and default sensitivity; the proportion of reads aligning to the host ranged from 0.07% to 2.51% across libraries, and 18.8–24.0 million read pairs per library were retained.

**Assembly, viral contigs and vOTU catalogue.** Each library was assembled independently with MEGAHIT 1.2.9 using `--min-contig-len 1000`, yielding 15,076–38,043 contigs per library (N50 4.2–6.4 kb). Viral contigs were identified with geNomad 1.13.0 (`end-to-end --splits 4 --cleanup`, all thresholds at default) and quality-assessed with CheckV 1.1.1; 213–5,074 contigs per library were classified as viral, of which 202 were high-quality genomes. Viral contigs from all six libraries were pooled and clustered with CD-HIT-EST 4.8.1 at `-c 0.95 -aS 0.85 -g 1`, i.e. 95% average nucleotide identity over 85% of the shorter sequence, the vOTU definition used by IMG/VR, yielding 9,980 vOTUs. Reads were mapped to the representative vOTU set with bowtie2 (`--very-sensitive --no-unal`) and counted from alignments retaining primary hits only (`samtools view -F 2304`); multi-mapping reads were not deduplicated, so the vOTU count measures reads aligning to the catalogue rather than unique assignment, and is not equivalent to the single-best-hit counting used for the protein search.

**Read-level protein homology search.** Reads were searched against PHROG v4 (868,340 proteins) with DIAMOND 2.0.4 `blastx` using `--evalue 1e-5 --max-target-seqs 1`, retaining the best hit per query. Hits were filtered to ≥40% amino acid identity and ≥30 aa alignment length, then deduplicated by read. Each read was assigned to one functional category through the PHROG annotation table: structural (head and packaging, tail, connector, virion, neck, baseplate), replication/transcription (DNA, RNA and nucleotide metabolism; transcription regulation), or other, the last pooling unannotated hits together with bacterial-homologous metabolic and housekeeping genes. The strict definition counts structural and replication/transcription hits; the broad definition counts all hits. Denominators are host-depleted reads with both mates counted; the host-retained control (C6) uses `total_reads × 2` from the host-removal step, so that numerator and denominator differ only in whether host reads were removed.

**The six definitions.** C1 (strict) and C2 (broad) use PHROG v4 with a category filter and no filter respectively; C3 is the range reported by Tang et al. (2019) for the same host species, obtained with nr + MEGAN4 lowest-common-ancestor assignment and therefore not recomputed here; C4 is the ratio of geNomad-classified viral contigs to all contigs; C5 is the ratio of vOTU-mapped reads to host-depleted reads; C6 is C2 with host reads retained in the denominator. Full definitions, per-sample values and denominators are given in Table 1.

**Reference-space comparison and decoy control.** The initial analysis in this project screened reads against RVDB-prot v32 Unique (783,103 proteins) with DIAMOND 2.2.8 using `--fast -e 1e-5 -k 1 --query-cover 50`. That parameter set cannot be reproduced on DIAMOND 2.0.4, which no longer accepts `--fast`; the two pipelines therefore differ in library, parameters and software version at once, and the figures they produced as originally run (0.84% and 4.17% in Results) are not directly comparable. The causal attribution rests instead on a matched comparison in which only the library varies: a common query set of 2,499,996 reads (416,666 per library, sampled with a fixed seed), one DIAMOND version (2.0.4), one parameter set (`--evalue 1e-5 --max-target-seqs 1`, no sensitivity or coverage options), and the same post-filter. Under these conditions RVDB-prot v32 Unique returned 19,994 reads (0.800%) and PHROG v4 returned 137,770 reads (5.511%), a 6.89-fold difference attributable to the reference space alone. Because the matched comparison counts one mate only, its percentages are not comparable to the both-mates denominators used elsewhere; only the ratio is. A shuffled PHROG database returned 0 hits in the same 2,499,996 reads, while the unshuffled database returned 137,770, confirming that the search itself was functional.

**Spike-in calibration.** Three pure-culture phages from different families (T4, Lambda, T7) were mixed in silico into 2 million read pairs of host-depleted W1 background at 0.1%, 1% and 5% (true fractions 0.1000%, 1.0000%, 5.0000%), in triplicate at each level, giving nine libraries. All nine were processed with the same search and filtering rules as the real data. For each rule the reading was modelled as `est(f) = B(1 − f) + rec·f`, where B is the background reading and rec the recovery; the model was fitted across the nine libraries and gave R² = 1.000 for all four rules. Recovery was 88.75% (broad) and 59.74% (strict), with background readings of 4.156% and 0.799%. Because the mixing is in silico, extraction, library preparation and amplification are bypassed; the calibration therefore characterises the detection step only.

**Software and data availability.** fastp 1.0.1, bowtie2 2.5.5, samtools 1.25, MEGAHIT 1.2.9, geNomad 1.13.0, CheckV 1.1.1, CD-HIT 4.8.1, DIAMOND 2.0.4, PHROG v4 (868,340 proteins). All versions were read from the executables used, not from documentation. Analysis scripts and intermediate tables are available at [repository to be assigned]; raw reads are available under PRJNA539906.

---

## 待补引用清单（内部，写投稿版前逐条核实）

| 编号 | 位置 | 引用 | 状态 |
|---|---|---|---|
| CIT-1 | Intro ¶1 | Shkoporov & Hill 2019, *Cell Host Microbe* 25:195, doi:10.1016/j.chom.2019.01.017（肠道病毒组综述）；实测值另引 CIT-8 | ✅ 2026-11-19 OpenAlex 核实 |
| CIT-2 | Intro ¶1 | Hegarty et al. 2024, *mSystems* 9:e0110523, doi:10.1128/msystems.01105-23（以病毒占比为基准调参的实例） | ✅ 已核实 |
| CIT-3 | Intro ¶2 | MIUViG, Roux et al., *Nat Biotechnol* 2019;37:29–37, doi:10.1038/nbt.4306 | ✅ 已核实 |
| CIT-4 | Intro ¶3 | 病毒识别工具基准, bioRxiv 2026.10.14.759168（**预印本**） | ✅ 已核实 |
| CIT-5 | Intro ¶3 / 5.1 | Forbes et al., *Cell Rep Methods* 2025, doi:10.1016/j.crmeth.2025.101218 | ✅ 已核实 |
| CIT-6 | 5.2 | CheckAMG, bioRxiv 2026.09.23.753886（**预印本**，PMID 42818345） | ✅ 已核实 |
| CIT-7 | 5.3 / Discussion | Reyes et al. 2010, *Nature* 466:334, doi:10.1038/nature09199；Garmaeva et al. 2021, *Cell Rep* 35:109132, doi:10.1016/j.celrep.2021.109132 | ✅ 2026-11-19 OpenAlex 核实 |
| CIT-8 | Methods · 6.1 | Tang et al. 2019, *Front Microbiol* 10:2409, doi:10.3389/fmicb.2019.02409（C3 文献值来源） | ✅ 已核实 |
| CIT-9 | Discussion ¶2 | Goodacre et al. 2018, *mSphere* 3:e00069-18, doi:10.1128/mspheredirect.00069-18（**RVDB 构建原则明确排除噬菌体**） | ✅ 2026-11-19 OpenAlex 核实 |

**CIT-1 的一处措辞调整（2026-11-19）**：原句 "well under one percent of reads" 找不到能直接支撑的单一出处——
这是领域常识而非某篇论文的结论。检索后改为 "at most a few percent, and usually far less"，
由综述（CIT-1）与实测区间 0.04–4.03%（CIT-8）共同支撑。**降强度不是因为证据更弱，而是因为原来的强度无法被引用兑现。**

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
| **库效应 6.89×（0.800 vs 5.511%）** | 同版本 2.0.4、同参数、同批 2,499,996 reads，只换库 | `13_calibration/库效应分离_2026-11-19.md` |
| 诱饵 0 / 2,499,996（正向 5.511%） | 打乱 PHROG vs 真实 PHROG | `13_calibration/诱饵重跑_2026-11-18.md` |
| 鸡 contig/read 中位 0.554（0.49–0.68） | 6 样本方向一致 | `12_second_dataset/results/unit_axis.tsv` |

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

---

**v0.4 补齐 Discussion 与 Methods（2026-11-19）。** 三处实质改动：

1. **Methods 的参数全部来自脚本实测与二进制版本输出**，不是文档转录。逐条清单与来源行号见
   `plans/MS01_Methods参数清单_2026-11-19.md`；版本号七项均现场运行取得。
2. **补了一个此前没有的对照。** 原先「换库导致 6 倍差异」混着参数与版本（初版 DIAMOND 2.2.8 用
   `--fast --query-cover 50`，现版 2.0.4 **不支持 `--fast`**，实测报 `Error: Invalid option: fast`）。
   现改为同版本、同参数、同一批 2,499,996 条 reads，只换库：RVDB 0.800% vs PHROG 5.511% = **6.89×**。
   与 171→26 的收缩比 **6.60**、C1 下限抬升比 **6.62** 三者吻合——「库是主因」由此从推测变成定量结论。
3. **Results 与 Methods 的两组数字分母不同，已在两处加衔接句。** Results 的 0.84/4.17 是两套流程
   各自原样跑出的全量结果；Methods 的 0.800/5.511 是单端匹配对照。两者不可直接相减，只有比值有效。

**Discussion 里两处措辞是刻意的。** 一是「a database built for a different question」——把 RVDB 定性为
「为别的问题建的库」而非「坏库」，避免被读成贬损同行工具；二是「Reanalysability is not a luxury」——
这句把 171→26 的修订从「我们改错了」转为「我们保留了能定位错因的数据」，是全文唯一一处把方法学主张
与自身实践绑在一起的地方。

**仍待完成**：CIT-1 / CIT-2 / CIT-7 三条引用；`[repository to be assigned]` 需在投稿前替换为实际地址。

# 中英对照版 · Manuscript v0.4（全文）

**日期** 2026-11-19
**英文准据** `manuscript_v0.4_full_EN_2026-11-19.md`（投稿用这一版）
**中文来源** `manuscript_v0.2_front_中文_2026-11-13.md`（作者原文；本文件仅在其与英文稿不一致处做了标注与微调）
**用法** 同一编号下英文在上、中文在下，可逐段核对。凡带 **Δ** 标记的，是我对中文原文做了改动，理由见文末清单——不是翻译误差。

**两部分的中文性质不同，阅读时请注意**：`[T]`–`[R4-6]` 的中文是**作者原文**（取自 v0.2 中文稿），对照即等于核对英文有没有走味；`[D-1]`–`[D-8]` 与 `[M-1]`–`[M-7]` 是 **2026-11-19 新写的英文，中文由我回译**——它们没有作者中文底本，回译只用于核对英文是否说清，不能反过来当作中文原文引用。

---

## 标题

**[T]**
**Four reporting decisions, only one of which moves the number: a 26-fold range in the viral fraction of one gut metagenome dataset**

**Δ 四个报告决策，一个决定数字：同一批肠道宏基因组数据中"病毒占比"的 26 倍差异**

> 中文原题作"同一份肠道宏基因组中"。Δ 理由：26 倍是六样本 × 六定义的极值之比，单样本内只有 4.7–8.4 倍，标题若称"同一份"会被审稿人直接指出。

*备选 / Alternatives*
- One dataset, four decisions: how reporting choices set the viral fraction of vertebrate gut metagenomes
  一份数据，四个决策：报数方式如何决定脊椎动物肠道宏基因组的病毒占比
- Mind the denominator: how four reporting decisions shift a viral fraction by more than an order of magnitude
  当心分母：四个报告决策如何让病毒占比相差一个数量级以上（Δ 原文作"两个数量级"，现为 26 倍，不足两个数量级）

---

## 摘要

**[A-1]**
Viral reads typically account for less than one percent of a host-associated shotgun metagenome, yet the resulting percentages are quoted, compared across studies, and increasingly used to benchmark tools. How such a percentage is computed is rarely stated. Using six fecal metagenomes of the Chinese alligator (*Alligator sinensis*), we computed the viral fraction of reads under six reporting definitions that differ along four axes: the denominator, the reference space, the functional categories retained, and the counting unit. Across definitions and samples the fraction spanned 26-fold, from 0.59% to 15.2% — far less than the 171-fold we obtained when the same reads were screened against a general viral database, a difference traceable to that database's near-absence of phage proteins. More importantly, only one of the four decisions moves the number: the category filter changes the fraction 4.6-fold (2.6–5.2, n = 6), whereas the reference space, the counting unit and the denominator each change it by 1.0–1.1-fold. That fold change survived four independent checks: a different reference database (3.6–6.9-fold), a different read source (5.05 versus 5.17-fold), a stricter identity threshold of 90% (4.4-fold), and randomized decoy sequences (0 hits). Sample-to-sample variation was 1.6–7.1-fold, the same order of magnitude as the definition effect — which is why the definition has to be stated, not because definition overwhelms biology. We then calibrated the detection step with spike-ins of known abundance: recovery was 88.8% under the broad and 59.7% under the strict definition, and calibration returned estimates to within 1.2 percentage points of the known value. Spike-ins below about 1% could not be separated from background (a 0.1% spike raised the reading by 2.0% relative), and public datasets rarely carry the technical controls needed to trace absolute bias. We close with an eight-item minimum reporting checklist that makes each of these decisions explicit at no additional sequencing cost.

在宿主相关 shotgun 宏基因组中，病毒 reads 通常不足 1%，但这个百分比被反复引用、跨研究比较，近年还被用来评估工具性能。然而这个数字究竟怎么算出来的，论文里往往一句不写。我们以 6 份扬子鳄（*Alligator sinensis*）粪便宏基因组为例，沿四条轴——分母、参考空间、保留的功能类别、计数对象——构造六种报告定义并逐一计算。全部定义与全部样本合起来，占比跨度 26 倍（0.59%–15.2%），远小于我们最初用通用病毒库得到的 171 倍；差别的来源是那个库几乎不含噬菌体蛋白。更关键的是，四个决策里**只有一个真正移动数字**：类别筛选使占比变化 4.6 倍（2.6–5.2，n = 6），而参考空间、计数对象、分母各自只改变 1.0–1.1 倍。这一倍数的稳健性经四重检验：换参考库（3.6–6.9 倍）、换序列来源（5.05 对 5.17 倍）、提高判定阈值至 90% 一致度（4.4 倍）、随机化诱饵（0 命中）。与此同时，样本间变异为 1.6–7.1 倍，与定义效应**处于同一量级**——这正是必须把定义写清楚的理由，而不是"定义压倒生物学"。我们进一步用已知真值的掺入梯度标定检测环节：宽口径回收率 88.8%、严格口径 59.7%，校准后可将估计恢复到真值 1.2 个百分点以内；但低占比的掺入无法与本底区分（0.1% 的 spike 只贡献 2% 的相对增量），且公共数据普遍缺少技术对照，使绝对水平的偏差不可追溯。最后给出八项最低报告清单，在不增加测序成本的前提下把这些决策逐条显性化。

> Δ 中文原稿作"1.2% 以内"，英文按 percentage points 展开，故此处同步为"1.2 个百分点"。

---

## Introduction / 引言

**[I-1]**
Shotgun metagenomes of host-associated microbial communities yield a viral signal of at most a few percent of reads, and usually far less [CIT-1]. That number travels: it is used to argue that the virome is a minor or a major component of a system, to compare hosts and habitats, and increasingly as a reference point against which detection tools are tuned [CIT-2]. Its small magnitude is precisely what makes it fragile, because at this scale the difference between 0.1% and 0.01% can be produced by decisions taken long before any biological question is asked.

宿主相关微生物群落的 shotgun 宏基因组，其病毒信号最多只占 reads 的百分之几，多数情况下远低于此 [CIT-1]。这个数字却在流动：它被用来论证病毒组在一个系统中是次要还是主要组分，被用来比较不同宿主与生境，近年更被当作衡量检测工具性能的基准 [CIT-2]。正因为量级小，它才格外脆弱——在这个尺度上，0.1% 与 0.01% 之间的差别，可能在提出任何生物学问题之前就已经由一连串技术决策决定了。

**[I-2]**
Reporting conventions at the read level are, however, largely unstandardised. The MIUViG standard specifies what must accompany an uncultivated viral genome — its origin, quality, annotation, taxonomy, biogeographic distribution and predicted host — but it does not define how to compute a fraction of reads, nor which reads should count as viral [CIT-3]. As a consequence, two studies can both report "the viral fraction" while measuring different quantities, and a reader has no way to tell.

然而在 read 层面，报告规范基本是缺失的。MIUViG 标准规定了"一份未培养病毒基因组"必须附带什么——来源、质量、注释、分类、生物地理分布与宿主预测——但它没有规定"占比"该怎么算，也没有规定哪些 reads 才算病毒 [CIT-3]。后果是：两项研究都可以声称报告了"病毒占比"，实际测的却是不同的量，而读者无从分辨。

**[I-3]**
That tool choice matters is well established. A benchmark of eleven viral prediction tools on low-abundance metagenomes found precision ranging from 10% to 100%, and concluded that the best performance came not from any single tool but from specific two-tool combinations followed by taxonomic filtering [CIT-4]. Host read removal has likewise been benchmarked across methods and reference assemblies, with measurable consequences for the retained read composition and for downstream metrics such as average nucleotide identity and diversity [CIT-5]. These are tool-level effects, and they are increasingly well characterised.

工具会影响结果，这一点已有共识。一项针对低丰度宏基因组的基准测试比较了 11 种病毒识别工具，精确率从 10% 到 100% 不等，并指出最优表现并非来自任何单一工具，而是特定的两两组合再加分类学过滤 [CIT-4]。类似地，宿主 reads 去除方法也已被系统比较，不同方法与不同人类参考基因组会改变保留下来的 read 组成，并影响下游指标（如 ANI 与多样性）[CIT-5]。这些都是**工具层面**的效应，且正在被越来越清楚地刻画。

**[I-4]**
What has not been separated is the contribution of the reporting decision itself, with the tools held fixed. Four choices precede any reported fraction: what counts as the denominator; which reference space the reads are compared against; which functional categories of hits are retained; and what statistical unit is counted. If these choices alone move the number substantially, then cross-study comparison fails even when every laboratory uses the same assembler, the same database and the same alignment thresholds — a stricter and less forgiving claim than "tools differ".

尚未被单独剥离出来的，是**在工具固定的前提下，报数决策本身贡献了多少**。在任何占比被报出之前，至少要先做四个选择：什么算分母；reads 拿去和哪个参考空间比；哪些功能类别的命中予以保留；以及数的是什么统计单元。如果仅这四个选择就能显著移动这个数字，那么即便所有实验室用同一款组装器、同一个数据库、同一套比对阈值，跨研究比较依然不成立。**这比"工具之间存在差异"是一个更严苛、也更难回避的论断。**

**[I-5]**
Here we quantify that contribution on a single dataset, so that tools and data are constant by construction. Using six fecal metagenomes of the Chinese alligator, we computed the viral fraction of reads under six definitions that vary one axis at a time, and asked how much of the observed range is definition and how much is sample. We then applied the same logic to a second, threshold-driven quantity — the number of vOTUs shared across samples — and translated the results into a minimum reporting checklist. We do not claim an ecological result, we do not identify a correct definition, and we do not argue that any of the six is preferable. The claim is narrower, and we hope harder to dismiss: at this signal scale, the definition and the biology contribute variation of the same order.

本文就在一份数据上量化这一贡献，从而让工具与数据在构造上保持恒定。我们使用 6 份扬子鳄粪便宏基因组，沿四条轴逐次变动一个维度，构造六种定义，并追问：观测到的跨度里，多少来自定义、多少来自样本。随后我们把同一套逻辑应用到另一个由阈值驱动的量——跨样本共享 vOTU 数——并把结果整理成一份最低报告清单。我们不主张任何生态学结论，不认定哪一种定义"正确"，也不认为六者中有哪一个更可取。我们的主张更窄，也希望更难被驳回：在这一信号量级上，**定义与生物学贡献的变异处于同一量级**。

> Δ 中文原稿作"定义是比生物学更大的变异来源"。Δ 理由：新数据下定义效应（4.6×）与样本效应（1.6–7.1×）同量级，原句已不成立。

---

## Results / 结果

### 5.1 A fraction cannot be reported before four decisions are made
### 5.1 在报出任何占比之前，必须先做四个决策

**[R1-1]**
Every reported viral fraction is the outcome of four choices, whether or not they are stated (Fig. 1). The **denominator** decides what counts as 100%: all reads, or reads remaining after host removal. The **reference space** decides what the reads are compared against: a public protein database, a study-assembled catalogue, or values reported by an earlier study. The **category filter** decides which hits are admitted: any viral-like hit, or only those annotated to categories whose viral origin is unambiguous. The **counting unit** decides what is counted: reads, contigs, or abundance-weighted values.

每一个被报出的病毒占比，都是四个选择的结果，无论它们是否被写出来（图 1）。**分母**决定什么算 100%：全部 reads，还是去宿主之后剩下的 reads。**参考空间**决定 reads 拿去和什么比：公共蛋白库、本研究自组装的目录，还是前人报告的数值。**类别筛选**决定哪些命中被承认：任意病毒样命中，还是只保留那些病毒来源无争议的类别。**计数对象**决定数的是什么：reads、contig，还是丰度加权值。

**[R1-2]**
One methodological qualification is needed up front. As implemented here, the fourth axis changes the detection level as well — at the read level hits are called by protein alignment, at the contig level by gene-based genome assignment. It therefore returns an upper bound for that axis rather than a pure unit effect. We separated the two with a controlled comparison in 5.2.

需要先说明一个方法学上的限定：在本研究的实现中，第四轴（计数对象）**同时更换了检测层面**——read 层是蛋白比对，contig 层是基因组判定。因此它给出的是这一轴的**上界**，而不是纯粹的单位效应。我们在 5.2 用一组受控比较把二者拆开。

**[R1-3]**
We measured each choice with the other three held fixed, across six fecal metagenomes of *Alligator sinensis* (PRJNA539906; n = 6). Median fold changes were 4.6 for the category filter, 1.1 for the reference space, 1.0 for the counting unit and 1.01 for the denominator (Fig. 1). That is, of the four decisions that all have to be declared, **only one materially changes the number**; the other three are near-null in this dataset. These fold changes are neither multiplicative nor additive: a median ratio identifies which axis matters, and cannot be used to reconstruct the overall span, which is set by the extremes of four definitions across six samples (26-fold measured). The reference-space value deserves emphasis: it is **1.1-fold, not 5.6-fold**. An initial calculation with RVDB-prot gave 5.6-fold, but that database contains almost no phage proteins (see 5.2); with a phage-specific database the effect all but disappears.

我们固定其余三个维度、逐一测量每一个选择，样本为 6 份扬子鳄粪便宏基因组（PRJNA539906；n = 6）。四个维度的中位倍数分别为：类别筛选 **4.6 倍**、参考空间 1.1 倍、计数对象 1.0 倍、分母 1.01 倍（图 1）。也就是说，**四个都必须声明的决策里，只有一个真正改变数字**，其余三个在本批数据上接近无效应。这些倍数不可相乘，也不构成可加的总和：中位倍数只能说明哪一轴重要，不能用来复算总跨度（实测总跨度为 26 倍，由四个口径 × 六个样本的极值决定）。需要强调的是，参考空间那一轴的中位倍数是 **1.1 倍而非 5.6 倍**：初版用 RVDB-prot 计算时得到 5.6 倍，但那个库几乎不含噬菌体蛋白（详见 5.2），换用噬菌体专用库后该效应基本消失。

> Δ 英文将"初版用 RVDB-prot 计算"写作 "An initial calculation with RVDB-prot"，读作分析过程，而非稿件版本史。

**[R1-4]**
The near-unity denominator needs separate comment, because it is a null result and we report it as such. Host reads made up only 0.07–2.51% of these libraries, so removing them changed the fraction by at most 1.2% (Fig. 2A, Table 1, C2 versus C6). This is a property of fecal samples with low host content, not a general rule: in high-host or low-viral-biomass material the same axis can become the dominant source, and the choice of host-removal method is itself a variable that must be declared [CIT-5].

分母接近 1 这一点需要单独说明，因为它是阴性结果，我们按阴性结果来报告。本批文库中宿主 reads 仅占 0.07–2.51%，因此去不去宿主最多只让占比变动 1.2%（图 2A、表 1，C2 对 C6）。这是低宿主含量的粪便样本的特性，不是普适规律：在宿主占比高或病毒载量低的材料中，同一条轴可能反转为最主要的来源；而且**去宿主方法本身就是一个必须声明的变量** [CIT-5]。

---

### 5.2 Six definitions of one measurement span 26-fold
### 5.2 同一个测量的六种定义，跨度 26 倍

**[R2-1]**
Applying the six definitions to the same six samples produced fractions from **0.59% to 15.2%, a 26-fold range** (Fig. 2A; Table 1). The extremes are not one sample measured two ways but **two different samples under two different definitions** (0.59%: sample W2, strict category filter; 15.2%: sample S3, vOTU reference). The range therefore conflates two sources of variation, and we separated them.

把六种定义施用于同一批六个样本，得到的占比从 **0.59% 到 15.2%，跨度 26 倍**（图 2A；表 1）。端点并非"同一个样本用两种算法"，而是**两个不同样本、两种不同定义**（0.59% 为 W2、严格类别筛选；15.2% 为 S3、vOTU 参考）。因此这个跨度混合了两个来源，需要拆开。

**[R2-2]**
Within any single sample, the four definitions spanned **4.7–8.4-fold**. Conversely, holding a definition fixed and varying the sample spanned 1.6-fold (broad), 3.1-fold (strict) and 7.1-fold (vOTU reference). **Definition and sample effects are of the same order** — the opposite of our initial conclusion that definition exceeded sample by roughly ninety-fold, which was inflated by a reference database that lacked phage proteins. Being of the same order does not make the decision optional: precisely because the two are comparable, a value obtained under one definition cannot be told apart from a difference between samples.

在任意单个样本内，四个口径的极差为 **4.7–8.4 倍**；反过来，固定某一个口径、只更换样本，变异为 1.6 倍（宽口径）、3.1 倍（严格口径）到 7.1 倍（vOTU 口径）。**定义效应与样本效应处于同一量级**——这一点与初版结论（定义约为样本的 90 倍）相反，原因是初版的跨度被一个缺少噬菌体的参考库放大了。同量级并不意味着可以不报：恰恰因为二者相当，同一个样本在不同定义下的数字才会与不同样本之间的差异混在一起、无法区分。

**[R2-3]**
The six definitions behave as their construction predicts. The category filter produces the largest step, **4.6-fold**, from 0.59–1.82% (strict) to 2.89–4.71% (broad), because only **19.3%** of broad hits fall in the structural or replication/transcription categories: **55.2% have unknown function**, 10.4% are moron or auxiliary metabolic genes, 10.6% fall into other annotated categories, and 4.0% relate to integration and excision [CIT-6]. **This is a problem of attributability, not of how much evidence is demanded**: the excluded hits are proteins like any other, and no sequence-based rule can decide whether a given hit came from a virion, a prophage remnant, or a cellular homologue. It is worth noting that more than half of the hits carry no functional description at all — **in this field, half of what passes for "viral protein" is uncharacterised, and the definition forces us to adjudicate that half**.

六种定义的表现与它们的构造一致。类别筛选造成的落差最大，为 **4.6 倍**，从 0.59–1.82%（严格）升到 2.89–4.71%（宽），原因是宽口径命中中只有 **19.3%** 属于结构或复制/转录类别：**55.2% 功能未知**，10.4% 属 moron/辅助代谢基因，10.6% 归入 other，4.0% 与整合/切离相关 [CIT-6]。**这是可归属性问题，不是"要求多少证据"的问题**：被排除的命中同样是蛋白，但任何基于序列的规则都无法判定它来自病毒粒子、前噬菌体残留，还是细胞同源序列。值得注意的是，超过一半的命中根本没有功能描述——**在这个领域，"病毒蛋白"里有一半不知道是什么，而定义恰恰要求我们对这一半做出取舍**。

**[R2-4]**
The reference space retains only **1.1-fold** (0.63–3.23) once a phage-specific database is used. Our initial 5.6-fold was traced, after the fact, not to a general property of "switching databases" but to **a compositional defect of the database used**: the project's RVDB-prot v32 Unique contains 783,103 proteins, dominated by eukaryotic and RNA viruses (SARS-CoV-2, marine RNA viruses, insect viruses), with phage proteins severely underrepresented. Screening the same reads against PHROG (868,340 proteins) raised total hits from 0.84% to 4.17%, roughly six-fold; under matched search settings, in which only the library varies, the effect is **6.9-fold** (Materials and Methods). Randomized decoy sequences returned 0 hits, ruling out false positives. **The correct statement for this axis is therefore conditional: it moves the number only when the reference database systematically lacks the target group — and that kind of absence announces itself nowhere.**

参考空间在换用噬菌体专用库后只余 **1.1 倍**（0.63–3.23）。初版测得 5.6 倍，追查后确认那不是"换库"的普遍性质，而是**那个库的组成缺陷**：项目原用的 RVDB-prot v32 Unique 只有 783,103 条蛋白，以真核病毒与 RNA 病毒为主（SARS-CoV-2、海洋 RNA 病毒、昆虫病毒），噬菌体蛋白严重不足。同一批 reads 换库后总命中从 0.84% 升到 4.17%（PHROG，868,340 条），相差约 6 倍；在只更换参考库、其余条件全部对齐的对照下，该效应为 **6.9 倍**（见材料与方法）；随机化诱饵对照为 0 命中，排除了假阳性。**因此这一轴的正确表述是：只有当参考库系统性缺少目标类群时，它才会移动数字——而那种缺失不会给出任何提示。**

> Δ 英文把中文原 §5.2 第三段拆成 R2-3 与 R2-4 两段：前段讲类别构成，后段讲参考库缺陷。中文原文是一整段，此处仅分段，未改字句。

**[R2-5]**
The fourth axis was originally recorded as 5.4-fold (C4/C2), but that figure **cannot be read as a unit effect**, because it changes two things at once: the counting unit (reads versus contigs) and the detection level (read-level protein alignment versus contig-level genome assignment). To separate them we mapped each sample's reads back onto **its own** viral contig set, so that the reference set was identical and only the unit changed.

第四轴原先记为 5.4 倍（C4/C2），但这个数字**不能读作"单位效应"**，因为它同时换了两件事：计数单位（reads 对 contig），以及检测层面（read 层蛋白比对对 contig 层基因组判定）。为把二者拆开，我们把每个样本的 reads 比对回**它自己的**病毒 contig 集——参考集完全相同，只改变计数单位。

**[R2-6]**
Across the six samples the contig-to-read ratio was **0.485, 0.853, 1.606, 1.479, 1.129 and 0.896**, median **1.01**. Changing the unit therefore does not change the estimate on average, but the ratio scatters **3.3-fold** between samples (0.49–1.61); within the same samples, the read-based fraction itself spans 7.97-fold and the contig-based fraction 9.44-fold.

六个样本的结果是：contig 单位与 reads 单位之比为 **0.485、0.853、1.606、1.479、1.129、0.896**，中位 **1.01**。也就是说，换单位在平均水平上**不改变**估计值，但样本间的比值摆动达 **3.3 倍**（0.49–1.61）；在同一批样本里，reads 单位自身跨 7.97 倍、contig 单位跨 9.44 倍。

**[R2-7]**
The point of this control is not a different number but a different attribution: **almost all of the 5.4-fold came from the detection method and the reference set, while the counting unit itself has a median effect of 1.0-fold.** Calling that axis "statistical unit" would systematically overstate the role of the unit, and would invite the reading that switching from reads to contigs explains most of the disagreement. We therefore label the item "counting unit (including detection level)" in Table 2, and recommend that the two be reported separately.

这一对照的意义不在于换一个数字，而在于它改变了归因：**5.4 倍几乎全部来自检测方法与参考差异；计数单位本身的中位效应是 1.0 倍。**若把这一轴直接称作"统计单元"，会系统性高估单位的作用，也会让读者误以为换一种计数方式就能解释掉大部分分歧。我们在表 2 中据此把该项标为"计数对象（含检测层面）"，并建议后续研究把两者分开报告。

---

### 5.3 The number of shared vOTUs is a function of the detection threshold
### 5.3 共享 vOTU 数是检测阈值的函数

**[R3-1]**
The same dependence appears in a quantity that is not a fraction at all. Counting the vOTUs detected in all six samples gave **0** when presence was called at the contig level; **783** at RPKM > 0; 517 at RPKM ≥ 0.01; 63 at RPKM ≥ 0.1; **5** at RPKM ≥ 1; and **1** at RPKM ≥ 10 (Fig. 3A). The direction of change is monotonic, but its interpretation is not: "no vOTU is shared" and "783 vOTUs are shared" are both correct statements about the same six libraries.

同一种依赖性也出现在一个根本不是"占比"的量上。统计六个样本中均检出的 vOTU 数：contig 层面判定为 **0**；RPKM > 0 时为 **783**；RPKM ≥ 0.01 时为 517；≥ 0.1 时为 63；≥ 1 时为 **5**；≥ 10 时为 **1**（图 3A）。变化方向是单调的，但解释并不单调——"没有任何 vOTU 共享"与"有 783 个 vOTU 共享"，都是关于同一批六个文库的正确陈述。

**[R3-2]**
The proportion of vOTUs found in a single sample is likewise threshold-dependent, and its shape is informative (Fig. 3B). It is 84.5% when presence is called from contigs, falls to 6.0–10.8% at permissive read thresholds, and rises again to 49.4% and 55.2% at RPKM ≥ 1 and ≥ 10 — although the last two are computed over the 6,041 and 310 vOTUs that pass those thresholds, not over the full catalogue of 9,980. **The two ends of this U-shape have opposite causes.** At the contig end, the high value reflects assembly fragmentation: the same virus assembled into different fragments in different samples cannot be clustered into one vOTU. At the stringent end, it reflects genuine sample specificity of abundant viruses. A single reported value, without its threshold, cannot distinguish the two.

单样本特有比例同样依赖阈值，而它的形状本身携带信息（图 3B）。按 contig 判定时为 84.5%；放宽到 reads 阈值后降到 6.0–10.8%；到 RPKM ≥ 1 与 ≥ 10 又回升至 49.4% 与 55.2%——不过后两个数字的分母不是全部 9,980 个 vOTU，而是通过该阈值的 6,041 个与 310 个。**这条 U 型曲线的两端成因正好相反**：contig 端的高值反映组装碎片化——同一个病毒在不同样本里被组装成不同片段，无法归入同一个 vOTU；严格端的高值则反映高丰度病毒真实的样本特异性。只报一个数值而不说阈值，无法区分这两种情形。

**[R3-3]**
Sample-to-sample similarity shows the same ambiguity with less drama: median Jaccard similarity across the 15 sample pairs was 0.0065 when computed from contig presence and 0.0234 when computed from abundance-weighted reads at RPKM ≥ 1, a 3.6-fold difference in the same direction (Fig. 3C). Both absolute values are low, consistent with the individual specificity widely reported for viromes [CIT-7]; the point here is not that the communities are dissimilar, but that **the degree of dissimilarity is partly a property of the method used to measure it.**

样本间相似度呈现出同一种模糊性，只是不那么戏剧化：15 个样本对的 Jaccard 中位数，按 contig 存在计算为 0.0065，按 RPKM ≥ 1 的丰度加权 reads 计算为 0.0234，同方向相差 3.6 倍（图 3C）。这两个绝对值都很低，与文献中反复报告的"病毒组高度个体特异"一致 [CIT-7]；但本文要说的不是"群落彼此不同"，而是**"不同到什么程度"本身有一部分是测量方法的属性**。

---

### 5.4 Spike-in calibration against a known truth: what can and cannot be corrected
### 5.4 用已知真值的掺入标定：能校正的与校正不了的

**[R4-1]**
Every fold change above rests on the assumption that the measurement itself is accurate, and that assumption had not been tested. We spiked three pure-culture phages from three different families (T4, Lambda, T7) into a real fecal background at 0.1%, 1% and 5%, in triplicate at each level, with the true value known to four decimal places, and then measured them with the same rules.

上面所有倍数都建立在"测量本身是准的"这一假设上，而这个假设从未被检验。我们把三株纯培养噬菌体（T4、Lambda、T7，分属三个科）按 0.1%、1%、5% 三个水平掺入一份真实粪便背景，每个水平三次重复，真值精确到小数点后四位；然后用同一批规则测量。

**[R4-2]**
**The linearity of the model is exact.** Under a given rule, the reading is strictly linear in the spiked fraction (`est(f) = B(1−f) + rec·f`; R² = 1.000 for all four rules). The intercept of that regression is the background reading B and the slope is the recovery:

**模型的线性是精确的。** 同一规则下，读数对掺入比例严格线性（`est(f) = B(1−f) + rec·f`，四个规则的 R² 均为 1.000），线性回归的截距给出背景读数 B，斜率给出回收率：

| Rule / 规则 | Background B / 背景读数 | Recovery / 回收率 | Error after calibration / 校准后误差 |
|---|---|---|---|
| PHROG / broad 宽 | 4.156% | **88.75%** | ≤0.2 pp |
| PHROG / strict 严 | 0.799% | **59.74%** | ≤0.5 pp |
| RefSeq / broad 宽 | 1.267% | 89.28% | ≤0.5 pp |
| RefSeq / strict 严 | 0.335% | 55.07% | ≤1.2 pp |

**[R4-3]**
**First conclusion: the cost of a strict definition is sensitivity, not accuracy.** Its background reading is indeed lower (0.8% against 4.2%), but its recovery is only 59.7% — **four tenths of the true viruses are missed**, so calibration has to multiply by 1.67 and magnifies the noise accordingly; the broad definition multiplies by 1.13. Looking stricter is not the same as being closer to the truth. The criterion should be the residual uncertainty after calibration, which scales as 1/rec.

**第一个结论：严格口径的代价是灵敏度，不是准确度。** 它的背景读数确实更低（0.8% 对 4.2%），但回收率只有 59.7%——**漏掉四成真病毒**，校准时需放大 1.67 倍，噪声同比例放大。宽口径放大 1.13 倍。"看起来更严格"并不等于"更接近真相"；判据应是校准后的残余不确定度，而它正比于 1/rec。

**[R4-4]**
**Second conclusion: low fractions cannot be separated from background, and that is not a question of accuracy.** A 0.1% spike raised the reading by only 2.0% relative to background (+0.085 percentage points), whereas a 5% spike raised it by 102%. In a sample whose background is of order 4%, differences below roughly 1% therefore cannot be resolved at all — **what should be reported is a limit of detection, not a precise value.**

**第二个结论：低占比无法与本底区分，这不是准确度问题。** 0.1% 的掺入只让读数相对本底增加 2.0%（+0.085 个百分点），5% 的掺入才增加 102%。因此在本底为 4% 量级的样本里，低于约 1% 的差异根本无法分辨——**该报的是检出限，不是精确值。**

> Δ 中文原稿此处有一句括号注："（此处曾误写为'高估 42 倍'，那是对两个不同分母的读数相除，已撤回。）"——**英文稿已移除**，移入文末内部说明。理由：投稿文本不宜出现"上一版"，读者没有可比对象。

**[R4-5]**
**Third conclusion: the label "strict" hides another 3-fold of freedom.** Decomposing the combined definition, structural proteins alone give **14.9-fold** (5.4–21.0), replication/transcription genes alone **6.6-fold** (4.9–7.0), and only their combination 4.6-fold; structural proteins account for a median of just 31.3% of the strict category. **We criticise others for leaving the definition unstated, yet our own "strict" is equally a word that needs defining.**

**第三个结论："严格"这个标签内部还有 3 倍伸缩。** 把合并口径拆开：仅结构蛋白时倍数为 **14.9 倍**（5.4–21.0），仅复制类为 **6.6 倍**（4.9–7.0），合并后才是 4.6 倍。结构蛋白占严格类的中位仅 31.3%。**我们批评别人的定义不清，自己的"严格"同样是一个需要定义的词。**

**[R4-6]**
**Fourth conclusion: the dominant bias is procedural, not statistical, and it is not recoverable.** These data come from total-DNA metagenomics (direct column extraction, without viral-particle enrichment), so the 20–75% extraction recoveries reported for enrichment protocols do not apply; the full-chain recovery of this dataset is estimated at about **0.76** (0.85 × 0.89), corresponding to a calibration factor of about 1.3. But the original study **used no internal standard** (no ERCC, no phage spike), while viral sequences make up only 0.1–5% of total DNA and are therefore a very low-abundance template — **library amplification bias can be neither quantified nor reconstructed afterwards.** This is not a failing of one study; it is a failing of current data-sharing practice.

**第四个结论：真正的偏差不在统计，在流程，而且不可追溯。** 本文数据来自总 DNA 宏基因组（直接柱法提取，未做病毒颗粒富集），因此文献报道的 20–75% 提取回收率并不适用；本批的全链条回收率估计约 **0.76**（0.85 × 0.89），对应校准倍数约 1.3。但原始研究**未使用任何内标**（ERCC 或噬菌体 spike），而病毒序列仅占总 DNA 的 0.1–5%，属极低丰度模板——**建库扩增偏倚无法量化，也无法事后补**。这不是某一项研究的问题，是当前数据共享惯例的问题。

---

## Discussion / 讨论

> 本节英文为 2026-11-19 新写，**无作者中文底本**；中文为回译，仅供核对英文是否说清。

**[D-1]**
**Of the four decisions, only one moves the number.** Any viral-fraction estimate requires four choices: what counts as the denominator, which reference space is searched, which functional categories are retained, and whether reads or contigs are counted. Holding the data and the tools fixed, only the third one matters materially — excluding metabolic, housekeeping and functionally unannotated hits lowers the fraction 4.6-fold (2.6–5.2, n = 6). The other three each move it by 1.0–1.1-fold. This asymmetry is inconvenient for a field whose methods sections routinely specify the aligner and the e-value while leaving the counted categories unstated, even though that is the choice with the larger effect.

**四个决策里，只有一个真正移动数字。** 任何"病毒占比"的估计都要先做四个选择：什么算分母、比对哪个参考空间、保留哪些功能类别、数 reads 还是数 contigs。在数据与工具固定的前提下，只有第三个实质重要——剔除代谢类、持家类和功能未注释的命中，会使占比下降 4.6 倍（2.6–5.2，n = 6）；其余三个各只改变 1.0–1.1 倍。这种不对称对本领域颇为不利：方法学部分通常写明比对工具和 e-value，却把"数了哪些类别"留空，而那恰恰是影响更大的那个选择。

**[D-2]**
**The reference-space result is conditional, and the condition is invisible.** Within this study, moving between two phage-specific references — the PHROG protein database and the study's own 9,980 vOTUs — changes the fraction by only 1.1-fold. Moving from a general viral database to a phage-specific one changes it 6.9-fold. Both statements are correct, and the difference between them is the whole point: **a reference space matters only when it systematically lacks the target group, and that kind of absence announces itself nowhere.** RVDB-prot v32 Unique, with 783,103 proteins dominated by eukaryotic and RNA viruses, is not a defective database; it is a database built for a different question, and its construction explicitly excludes bacterial viruses [CIT-9]. That exclusion is stated in the original publication, but not in the name, the file header, or the size of the download. A user who screens a gut metagenome against it will obtain a number, and the number will be wrong by roughly sevenfold, with no error message.

**参考空间的结论是条件性的，而那个条件不可见。** 在本研究内部，在两个都是噬菌体特异的参考之间切换——PHROG 蛋白库与本研究的 9,980 个 vOTU——占比只改变 1.1 倍；而从通用病毒库换到噬菌体特异库，改变的是 6.9 倍。两句话都成立，它们的差别正是要点：**只有当参考空间系统性缺少目标类群时它才起作用，而这类缺失不会自我申报。** RVDB-prot v32 Unique 有 783,103 条蛋白，以真核病毒与 RNA 病毒为主——它不是坏库，而是为另一个问题建的库，其构建原则明确排除细菌病毒 [CIT-9]。这一排除写在原始文献里，但不在库名里、不在文件头里、也不在下载包的体积里。用它去筛肠道宏基因组的人会得到一个数字，而这个数字错约七倍，且没有任何报错。

**[D-3]**
**The revision of our own estimate can be located precisely, which is itself the argument.** Our initial analysis reported a 171-fold span; the present one reports 26-fold. The contraction ratio is 6.60, the increase in the strict-category floor is 6.62, and the library effect measured under identical search settings is 6.89 — three independent quantities that agree. The entire revision is therefore attributable to the reference space, not to a threshold change, not to a parameter change, and not to a software version. We report this because it is a rare case in which a published-style number can be traced back to a single cause; in most retractions of this kind the original intermediate files are gone, and the cause remains a conjecture. **The ability to locate the cause depended on the raw reads and the intermediate hit tables still existing.** Reanalysability is not a luxury.

**我们自己那个估计的修订过程可以被精确定位，这件事本身就是论据。** 初版分析报告 171 倍跨度，本版报告 26 倍。收缩比为 6.60，严格口径下限的抬升为 6.62，而在相同搜索条件下测得的库效应为 6.89——三个独立量相互吻合。因此整个修订可归因于参考空间，而不是阈值改动、不是参数改动、也不是软件版本。我们把它写出来，是因为"一个已发表量级的数字能被追到单一原因"是罕见情形；多数同类撤回里原始中间文件已经不在，原因只能停留在猜测。**能定位原因，前提是原始 reads 与中间命中表都还在。** 可重分析不是奢侈品。

**[D-4]**
**Definition and biology are of the same order, which is why the definition must be stated.** Sample-to-sample variation spans 1.6-fold (broad), 3.1-fold (strict) and 7.1-fold (vOTU reference), against a 4.6-fold definition effect. Our initial claim that definition exceeded biology by roughly ninetyfold was an artefact of the reference-space defect described above. The corrected claim is weaker and more useful: because the two contributions are comparable, **a value obtained under one definition cannot be distinguished from a difference between samples** — the ambiguity is not resolved by more sequencing, only by stating the definition.

**定义与生物学处于同一量级，所以定义必须写明。** 样本间变异跨度为 1.6 倍（宽口径）、3.1 倍（严格口径）、7.1 倍（vOTU 口径），而定义效应是 4.6 倍。初版称"定义超过生物学约九十倍"，那是上文所述参考空间缺陷造成的假象。修正后的主张更弱，也更有用：正因为两者的贡献相当，**一个定义下得到的数值无法与样本之间的差异相区分**——这种模糊不会因为多测序而消失，只能靠把定义写出来解决。

**[D-5]**
**Calibration corrects sensitivity, not composition.** Spike-ins of known abundance returned recoveries of 88.75% (broad) and 59.74% (strict), and applying them brought estimates to within 0.2 and 0.5 percentage points of truth. But the intercept of the same regression — the background reading B, 4.156% and 0.799% — cannot be decomposed by this design: it pools genuine viral signal with homology-driven misassignment, and treating it as false positives would drive the strict estimate negative. Two consequences follow. First, in a sample whose background is of order 4%, a 0.1% spike raises the reading by 2.0% relative and cannot be resolved; **what should be reported is a limit of detection, not a precise value.** Second, the largest bias in these data is procedural rather than statistical: the libraries were prepared without an internal standard, from a template in which viral DNA is a minor component, so amplification bias can be neither quantified nor reconstructed after the fact. Spike-in calibration, however well designed, cannot recover what was never measured.

**校准纠正的是灵敏度，不是构成。** 已知丰度的掺入给出回收率 88.75%（宽口径）与 59.74%（严格口径），据此校正后估计落在真值 0.2 与 0.5 个百分点以内。但同一条回归的截距——本底读数 B，4.156% 与 0.799%——无法用本设计拆解：它把真实的病毒信号与同源误判混在一起，若当作假阳性扣除，严格口径的估计会变成负值。由此有两个后果。其一，在本底约为 4% 的样本里，0.1% 的掺入只带来 2.0% 的相对增量，无法分辨；**应当报告的是检出限，不是一个精确值。** 其二，这批数据里最大的偏差是流程性的而非统计性的：建库时没有内标，模板中病毒 DNA 又只占少数，因此扩增偏差既无法定量、也无法事后重建。掺入校准设计得再好，也追不回从未被测量的东西。

**[D-6]**
**Two limits on generality.** First, all six libraries come from one host species, so the sample effect measured here is a within-species effect and is almost certainly an underestimate of the between-host variation that a cross-species comparison would encounter; the 26-fold span should be read as a lower bound on the definition-and-sample range, not as a property of gut metagenomes in general. Second, the counting-unit effect does not replicate in direction. Mapping reads back to each sample's own viral contigs, so that only the unit changes, gives a median contig-to-read ratio of 1.01 (0.49–1.61) in the alligator libraries but 0.554 (0.49–0.68) in an independently processed chicken gut dataset. A ratio near 1 means the two units agree on average; a ratio near 0.5 means contig counting loses half the signal. **That the direction differs between two datasets processed by the same rules is precisely why the unit should be reported separately rather than assumed to be interchangeable.**

**两条适用范围上的限制。** 其一，六个文库全部来自同一宿主物种，因此这里测得的样本效应是种内效应，几乎必然低于跨物种比较会遇到的宿主间变异；26 倍应读作"定义与样本合起来的范围"的下界，而不是肠道宏基因组的普遍性质。其二，计数对象效应在方向上无法重复。把 reads 比对回各样本自己的病毒 contigs、使只有计数单位改变时，扬子鳄文库的 contig/read 中位比为 1.01（0.49–1.61），而一个独立处理的鸡肠道数据集为 0.554（0.49–0.68）。比值接近 1 意味着两种单位平均而言一致；接近 0.5 意味着 contig 计数丢掉一半信号。**同规则处理的两个数据集在方向上相反，恰恰说明计数单位必须单独报告，而不能假定可互换。**

**[D-7]**
**What we are not claiming.** We do not identify a correct definition, we do not argue that any of the six is preferable, and we do not claim an ecological result. The claim is narrower: at this signal scale, the reporting decisions contribute variation of the same order as the biology, one of them dominates, and none of them is currently stated. The eight-item checklist in Table 2 makes each decision explicit at no additional sequencing cost; its value is that it converts an unstated choice into a recordable one.

**我们没有主张什么。** 我们不认定哪个定义正确，不主张六者之中有优劣，也不主张任何生态学结论。主张更窄：在这个信号尺度上，报数决策贡献的变异与生物学处于同一量级，其中一项占主导，而没有一项被写出来。表 2 的八项清单在不增加测序成本的前提下把每个决策显性化；它的价值在于把一次未声明的选择变成一条可记录的声明。

**[D-8]**
**Limitations.** The sample size is six, the host range is one species, and the spike-in experiment is in silico — it mixes reads by proportion and therefore bypasses extraction, library preparation and amplification, so extraction efficiency is assumed to be 100%, an assumption that real capsid lysis resistance can violate by orders of magnitude. The calibration therefore bounds the detection step, not the full chain. The decoy control rules out false positives from the search itself (0 hits in 2,499,996 reads against a shuffled database) but does not address misassignment between genuine viral and bacterial homologues, which is a property of the reference content rather than of the search.

**局限。** 样本量为 6，宿主只有 1 个物种，掺入实验是 in-silico 的——按比例混合 reads，因而绕过了提取、建库与扩增，等于假设提取效率为 100%；而真实噬菌体衣壳的抗裂解差异可以达到数量级。故本节校准界定的是检测环节，不是全链条。诱饵对照排除了搜索本身带来的假阳性（2,499,996 条 reads 对打乱库为 0 命中），但没有处理真实病毒与细菌同源序列之间的误判——那是参考内容的属性，不是搜索的属性。

---

## Materials and Methods / 材料与方法

> 本节英文为 2026-11-19 新写；中文为回译。**参数、命令、版本号一律保留英文原样**，不译、不改写。

**[M-1]**
**Metagenomes and host removal.** Six fecal metagenomes of the Chinese alligator (*Alligator sinensis*) were retrieved from PRJNA539906, comprising three hibernation-season libraries (W1–W3; SRR14300938, SRR14300939, SRR14300942) and three active-season libraries (S1–S3; SRR14300940, SRR14300941, SRR14300943). All were paired-end. Reads were quality-filtered with fastp 1.0.1 using `-q 20 -l 50`, with adapter detection, poly-G trimming and sliding-window quality cutting at default settings. Host reads were removed with bowtie2 2.5.5 against the *A. sinensis* reference GCA_000455745.1 (3.0 Gb; ENA AVPB01000001) using `--un-conc-gz --no-unal` and default sensitivity; the proportion of reads aligning to the host ranged from 0.07% to 2.51% across libraries, and 18.8–24.0 million read pairs per library were retained.

**宏基因组与去宿主。** 6 份扬子鳄（*Alligator sinensis*）粪便宏基因组取自 PRJNA539906，含三个冬眠期文库（W1–W3；SRR14300938、SRR14300939、SRR14300942）与三个活动期文库（S1–S3；SRR14300940、SRR14300941、SRR14300943），全部为双端。reads 用 fastp 1.0.1 质控，参数 `-q 20 -l 50`，接头识别、poly-G 修剪与滑窗质量剪切均为默认设置。宿主 reads 用 bowtie2 2.5.5 比对 *A. sinensis* 参考基因组 GCA_000455745.1（3.0 Gb；ENA AVPB01000001）去除，参数 `--un-conc-gz --no-unal`，灵敏度为默认；各文库比对到宿主的 reads 比例为 0.07%–2.51%，每个文库保留 1,880 万–2,400 万 read pairs。

**[M-2]**
**Assembly, viral contigs and vOTU catalogue.** Each library was assembled independently with MEGAHIT 1.2.9 using `--min-contig-len 1000`, yielding 15,076–38,043 contigs per library (N50 4.2–6.4 kb). Viral contigs were identified with geNomad 1.13.0 (`end-to-end --splits 4 --cleanup`, all thresholds at default) and quality-assessed with CheckV 1.1.1; 213–5,074 contigs per library were classified as viral, of which 202 were high-quality genomes. Viral contigs from all six libraries were pooled and clustered with CD-HIT-EST 4.8.1 at `-c 0.95 -aS 0.85 -g 1`, i.e. 95% average nucleotide identity over 85% of the shorter sequence, the vOTU definition used by IMG/VR, yielding 9,980 vOTUs. Reads were mapped to the representative vOTU set with bowtie2 (`--very-sensitive --no-unal`) and counted from alignments retaining primary hits only (`samtools view -F 2304`); multi-mapping reads were not deduplicated, so the vOTU count measures reads aligning to the catalogue rather than unique assignment, and is not equivalent to the single-best-hit counting used for the protein search.

**组装、病毒 contigs 与 vOTU 目录。** 每个文库用 MEGAHIT 1.2.9 独立组装，参数 `--min-contig-len 1000`，得到每文库 15,076–38,043 条 contigs（N50 4.2–6.4 kb）。病毒 contigs 用 geNomad 1.13.0 识别（`end-to-end --splits 4 --cleanup`，全部阈值为默认），用 CheckV 1.1.1 评估质量；每文库有 213–5,074 条 contigs 被判为病毒，其中 202 条为高质量基因组。六个文库的病毒 contigs 合并后用 CD-HIT-EST 4.8.1 聚类，参数 `-c 0.95 -aS 0.85 -g 1`，即较短序列 85% 覆盖下 95% 平均核苷酸一致度，这是 IMG/VR 采用的 vOTU 定义，共得 9,980 个 vOTU。reads 用 bowtie2（`--very-sensitive --no-unal`）比对到 vOTU 代表序列集，仅统计保留的 primary 比对（`samtools view -F 2304`）；多重比对的 reads 未去重，因此该计数衡量的是"比对到该目录的 reads"，而非唯一归属，与蛋白搜索所用的"每条 query 取最佳单一命中"不是同一类计数。

**[M-3]**
**Read-level protein homology search.** Reads were searched against PHROG v4 (868,340 proteins) with DIAMOND 2.0.4 `blastx` using `--evalue 1e-5 --max-target-seqs 1`, retaining the best hit per query. Hits were filtered to ≥40% amino acid identity and ≥30 aa alignment length, then deduplicated by read. Each read was assigned to one functional category through the PHROG annotation table: structural (head and packaging, tail, connector, virion, neck, baseplate), replication/transcription (DNA, RNA and nucleotide metabolism; transcription regulation), or other, the last pooling unannotated hits together with bacterial-homologous metabolic and housekeeping genes. The strict definition counts structural and replication/transcription hits; the broad definition counts all hits. Denominators are host-depleted reads with both mates counted; the host-retained control (C6) uses `total_reads × 2` from the host-removal step, so that numerator and denominator differ only in whether host reads were removed.

**read 层蛋白同源搜索。** reads 用 DIAMOND 2.0.4 的 `blastx` 比对 PHROG v4（868,340 条蛋白），参数 `--evalue 1e-5 --max-target-seqs 1`，每条 query 保留最佳命中。命中按 ≥40% 氨基酸一致度与 ≥30 aa 比对长度过滤，再按 read 去重。每条 read 经 PHROG 注释表归入一个功能类别：结构类（头部与包装、尾部、连接器、病毒粒子、颈部、基板）、复制/转录类（DNA、RNA 与核苷酸代谢；转录调控）、或 other——最后一类把未注释命中与细菌同源的代谢、持家基因合并在一起。严格口径统计结构类与复制/转录类命中，宽口径统计全部命中。分母为去宿主后的 reads，双端均计入；保留宿主的对照（C6）使用去宿主步骤的 `total_reads × 2`，使分子与分母的差别只在于是否扣除宿主 reads。

**[M-4]**
**The six definitions.** C1 (strict) and C2 (broad) use PHROG v4 with a category filter and no filter respectively; C3 is the range reported by Tang et al. (2019) for the same host species, obtained with nr + MEGAN4 lowest-common-ancestor assignment and therefore not recomputed here; C4 is the ratio of geNomad-classified viral contigs to all contigs; C5 is the ratio of vOTU-mapped reads to host-depleted reads; C6 is C2 with host reads retained in the denominator. Full definitions, per-sample values and denominators are given in Table 1.

**六种定义。** C1（严格）与 C2（宽）都用 PHROG v4，分别带类别筛选与不带筛选；C3 是 Tang 等（2019）对同一宿主物种报告的范围，用 nr + MEGAN4 最低共同祖先归属得到，故本文不重算；C4 是 geNomad 判定的病毒 contigs 占全部 contigs 的比例；C5 是比对到 vOTU 的 reads 占去宿主 reads 的比例；C6 是 C2 但分母保留宿主 reads。完整定义、逐样本数值与分母见表 1。

**[M-5]**
**Reference-space comparison and decoy control.** The initial analysis in this project screened reads against RVDB-prot v32 Unique (783,103 proteins) with DIAMOND 2.2.8 using `--fast -e 1e-5 -k 1 --query-cover 50`. That parameter set cannot be reproduced on DIAMOND 2.0.4, which no longer accepts `--fast`; the two pipelines therefore differ in library, parameters and software version at once, and the figures they produced as originally run (0.84% and 4.17% in Results) are not directly comparable. The causal attribution rests instead on a matched comparison in which only the library varies: a common query set of 2,499,996 reads (416,666 per library, sampled with a fixed seed), one DIAMOND version (2.0.4), one parameter set (`--evalue 1e-5 --max-target-seqs 1`, no sensitivity or coverage options), and the same post-filter. Under these conditions RVDB-prot v32 Unique returned 19,994 reads (0.800%) and PHROG v4 returned 137,770 reads (5.511%), a 6.89-fold difference attributable to the reference space alone. Because the matched comparison counts one mate only, its percentages are not comparable to the both-mates denominators used elsewhere; only the ratio is. A shuffled PHROG database returned 0 hits in the same 2,499,996 reads, while the unshuffled database returned 137,770, confirming that the search itself was functional.

**参考空间对照与诱饵控制。** 本项目初版分析用 DIAMOND 2.2.8 将 reads 比对 RVDB-prot v32 Unique（783,103 条蛋白），参数 `--fast -e 1e-5 -k 1 --query-cover 50`。该参数组在 DIAMOND 2.0.4 上无法复现，因为后者不再接受 `--fast`；两套流程因此在库、参数与软件版本上同时不同，各自原样跑出的数值（结果部分所述 0.84% 与 4.17%）不可直接比较。因果归因改用只更换参考库的匹配对照：同一组 2,499,996 条 query reads（每文库 416,666 条，固定种子抽样）、同一 DIAMOND 版本（2.0.4）、同一参数组（`--evalue 1e-5 --max-target-seqs 1`，不设灵敏度与覆盖度选项）、同一后处理过滤。在此条件下，RVDB-prot v32 Unique 返回 19,994 条 reads（0.800%），PHROG v4 返回 137,770 条（5.511%），相差 6.89 倍，可归因于参考空间本身。由于该匹配对照只计单端，其百分比与本文他处采用的双端分母不可比，可比的只有比值。打乱的 PHROG 库在同一批 2,499,996 条 reads 上返回 0 命中，而未打乱的同一库返回 137,770 条，说明搜索本身工作正常。

**[M-6]**
**Spike-in calibration.** Three pure-culture phages from different families (T4, Lambda, T7) were mixed in silico into 2 million read pairs of host-depleted W1 background at 0.1%, 1% and 5% (true fractions 0.1000%, 1.0000%, 5.0000%), in triplicate at each level, giving nine libraries. All nine were processed with the same search and filtering rules as the real data. For each rule the reading was modelled as `est(f) = B(1 − f) + rec·f`, where B is the background reading and rec the recovery; the model was fitted across the nine libraries and gave R² = 1.000 for all four rules. Recovery was 88.75% (broad) and 59.74% (strict), with background readings of 4.156% and 0.799%. Because the mixing is in silico, extraction, library preparation and amplification are bypassed; the calibration therefore characterises the detection step only.

**掺入校准。** 三个不同科的纯培养噬菌体（T4、Lambda、T7）以 in-silico 方式按 0.1%、1%、5% 混入 200 万对去宿主 W1 背景 reads（真值占比 0.1000%、1.0000%、5.0000%），每个水平三个重复，共九个文库。九个文库全部用与真实数据相同的搜索与过滤规则处理。对每种规则，读数建模为 `est(f) = B(1 − f) + rec·f`，其中 B 为本底读数、rec 为回收率；模型在九个文库上拟合，四种规则的 R² 均为 1.000。回收率为 88.75%（宽口径）与 59.74%（严格口径），本底读数分别为 4.156% 与 0.799%。由于混合是 in-silico 的，提取、建库与扩增均被绕过；因此该校准刻画的只是检测环节。

**[M-7]**
**Software and data availability.** fastp 1.0.1, bowtie2 2.5.5, samtools 1.25, MEGAHIT 1.2.9, geNomad 1.13.0, CheckV 1.1.1, CD-HIT 4.8.1, DIAMOND 2.0.4, PHROG v4 (868,340 proteins). All versions were read from the executables used, not from documentation. Analysis scripts and intermediate tables are available at [repository to be assigned]; raw reads are available under PRJNA539906.

**软件与数据可用性。** fastp 1.0.1、bowtie2 2.5.5、samtools 1.25、MEGAHIT 1.2.9、geNomad 1.13.0、CheckV 1.1.1、CD-HIT 4.8.1、DIAMOND 2.0.4、PHROG v4（868,340 条蛋白）。所有版本号均从实际使用的可执行文件读出，不是从文档转录。分析脚本与中间表见 [待指定仓库]；原始 reads 见 PRJNA539906。

---

---

## Δ 偏离清单（英文稿相对中文 v0.2 的全部改动）

| # | 位置 | 中文原文 | 英文稿 | 理由 |
|---|---|---|---|---|
| 1 | 标题 | "同一份肠道宏基因组中" | "one gut metagenome dataset" | 26 倍跨六样本，单样本内仅 4.7–8.4 倍；原文会被审稿人指出 |
| 2 | 标题备选 | "相差两个数量级" | "more than an order of magnitude" | 26 倍不足两个数量级，原表述夸大 |
| 3 | 引言末句 | "定义是比生物学更大的变异来源" | "the definition and the biology contribute variation of the same order" | 与 5.2 的"同量级"结论保持一致，原句已自相矛盾 |
| 4 | 5.1 | "初版用 RVDB-prot 计算时得到" | "An initial calculation with RVDB-prot gave" | 读作分析过程，不暴露稿件版本史 |
| 5 | 5.2 结构 | 一整段（类别 + 参考库） | 拆为 R2-3 / R2-4 | 两件事分属"可归属性"与"库缺陷"，分段更清楚；未改字句 |
| 6 | 5.4 | "≤1.2%"、"1.2 个百分点"混用 | 统一 percentage points | 避免与相对误差混淆 |
| 7 | 5.4 | 括号内"曾误写为高估 42 倍，已撤回" | 移入内部说明 | 投稿文本不宜出现版本史；记录不丢 |
| 8 | `[I-1]` | "well under one percent of reads" | "at most a few percent of reads, and usually far less" | 原表述找不到能直接兑现的单一出处；降强度后由 CIT-1（综述）与 CIT-8（实测 0.04–4.03%）共同支撑 |
| 9 | `[R2-5]` | 无此句 | 增 "under matched search settings … the effect is 6.9-fold" | 原句把库效应与参数、版本混在一起归因；补入匹配对照后 6.9 倍可单独成立（见 `[M-5]`） |
| 10 | `[D-2]` | 无此句 | 增 "its construction explicitly excludes bacterial viruses [CIT-9]" | Goodacre 2018 原文即 "excluding bacterial viruses"；把"缺噬菌体"从我们的观察变为该库的设计事实 |

## 曾留给 Discussion 的两条（2026-11-19 已写入 `[D-6]`）

1. 六样本同一宿主，样本效应被低估；跨宿主时该效应会更大。
2. 第二数据集（鸡肠道）同一受控对照中位比值为 **0.554**，与扬子鳄的 1.01 方向、量级都不同，说明**单位效应本身不稳定**、不能外推。这是 Table 2 第 4 项"建议分开报告"的直接理由，但两个数据集尚不足以当独立结论。

> 以上两条均已写入 `[D-6]`。**补充一句当时没有的数据**：鸡的比值范围是 0.49–0.68，六个样本方向一致；扬子鳄是 0.49–1.61，中位 1.01。也就是说鸡那边是稳定地低于 1，扬子鳄那边是围绕 1 散开——两种不同的失败形态。

# 图注正式稿（Fig 1–3）

**日期** 2026-11-17（v2）　|　**状态** 定稿（英文投稿版 + 中文对照）
**配套 Word**：`11_proposal/MS01/legends/output/Figure_legends.docx`（由本文件自动生成）
**对应图件**：`08_figures/fig_a0`、`08_figures/fig_a1`、`08_figures/fig_a2`

> 重新生成：`python 11_proposal/MS01/legends/code/make_legends_docx.py`
> **本文件是唯一来源**：脚本直接解析本文件生成 Word，不再另存一份硬编码文本。
> 英文为 canonical；中文仅供内部讨论，不入稿。

**v2 修订（2026-11-17）**：随 PHROG 换库，Fig 1/Fig 2 的数值全部更新——跨度 171× → **25.9×**，
样本内极差 22.2–124.8× → **4.7–8.4×**，样本效应 1.37× → **3.1×**，参考空间 5.6× → **1.1×**，
"7.1 × 5.6 ≈ 40" → **"4.6 × 1.1 ≈ 5"**。Fig 3 未受影响（vOTU 口径不依赖蛋白库）。

---

## 一、英文投稿版（canonical）

**Figure 1. Four reporting decisions, only one of which moves the number.**
Each row is a choice that has to be made before a viral fraction can be reported: denominator, reference space, category filter, and counting unit. Boxes list the alternatives available at each decision. Values on the right are median fold changes measured in this dataset with the other dimensions held fixed, from six fecal metagenomes of _Alligator sinensis_ (PRJNA539906; n = 6). Across all definitions and samples the observed span is 25.9× (0.589–15.23%). These fold changes are not multiplicative: 4.6 × 1.1 ≈ 5, whereas the measured span is 25.9×, because each ratio derives from a different sample and a different pair of definitions. Within a single sample, definitions alone span 4.7–8.4×, and the additional sample effect is 3.1× (Fig. 2). Only the category filter moves the number materially; the other three decisions change it by 1.00–1.14×. The denominator null reflects that host reads make up only 0.07–2.51% of these libraries, which is a property of feces rather than of metagenomes in general. The counting-unit null reflects that counting the same viral set as contigs rather than reads changes the estimate by a median factor of 1.01 (0.49–1.61). The near-unity reference space is not a general property either: it reflects the use of a phage-specific database here, and is discussed in Fig. 2.

**Figure 2. Six definitions of the same measurement span 26-fold.**
**(A)** Viral fraction of reads under six reporting definitions (C1, C2, C6, C3, C4 and C5; defined in Table 1) for six fecal metagenomes. Points are individual samples (W1–W3, hibernating; S1–S3, active); horizontal bars are medians across the six samples. The y axis is logarithmic. C3 is a literature-reported range (0.04–4.03%) with no per-sample values; it is drawn as a grey band for orientation only and is excluded from every fold-change calculation. C2 and C6 share the same numerator and differ only in whether host reads are retained in the denominator; the bracket marks their ≤1.2% difference. **(B)** Fold change between definitions, computed within each sample (n = 6) and summarised as boxplots; the dashed line marks no change and numbers above the boxes are medians. Definitions are not independent: 4.6 × 1.1 ≈ 5, well short of the observed 26-fold span. The reference-space ratio is near unity only because the database is phage-specific; with a general viral database that lacked phage proteins, the same comparison gave 5.6× (see Results), which is a property of that database, not of reference-space choices in general.

**Figure 3. The number of shared vOTUs is a function of the detection threshold.**
**(A)** Number of vOTUs detected in all six samples under six detection criteria: contig-level presence (0 vOTUs) and read-level abundance at RPKM > 0 (783), ≥0.01 (517), ≥0.1 (63), ≥1 (5) and ≥10 (1). The y axis is logarithmic. **(B)** Proportion of vOTUs detected in a single sample under the same criteria. The relationship is U-shaped, and the two ends have opposite causes: the high value at contig level (84.5%) reflects assembly fragmentation, whereas the high value at RPKM ≥ 10 (55.2%) reflects genuine sample specificity of abundant viruses. **(C)** Jaccard similarity for all 15 sample pairs, computed either from contig presence or from abundance-weighted reads (RPKM ≥ 1); horizontal bars are medians (0.0065 and 0.0234, a 3.6-fold difference). Throughout, n = 6 samples. The contig-level value of zero should not be read as an absence of shared viruses: the same virus can assemble into different fragments in different samples.

---

## 二、中文对照（内部讨论用）

**图 1. 四个报告决策中，只有一个真正移动数字。**
每一行都是报出"病毒占比"之前必须做出的选择：分母、参考空间、类别筛选、计数对象。方框列出该决策的可选项。右侧数值为固定其余维度时在本批数据上实测的中位倍数（6 份扬子鳄粪便宏基因组，PRJNA539906；n = 6）。全部定义与全部样本的实测跨度为 25.9×（0.589–15.23%）。这些倍数不可相乘：4.6 × 1.1 ≈ 5，而实测跨度是 25.9×，因为每个比值来自不同样本与不同定义组合。同一样本内仅定义本身即跨 4.7–8.4×，样本效应另贡献 3.1×（见图 2）。只有类别筛选实质性移动数字，其余三个决策的影响在 1.00–1.14× 之间。分母一行的阴性结果源于本批文库中宿主 reads 仅占 0.07–2.51%，这是粪便样本的特性，不是宏基因组的普遍性质。计数对象的阴性结果源于把同一病毒集按 contig 而非 reads 计数，中位倍数只有 1.01（0.49–1.61）。参考空间接近 1 也不是普遍性质：它反映的是此处使用了噬菌体专用库，详见第 2 图。

**图 2. 同一个测量的六种定义，跨度 26 倍。**
（A）六种报告定义（C1、C2、C6、C3、C4、C5，定义见表 1）下六个粪便宏基因组的病毒 reads 占比。点为单个样本（W1–W3 冬眠期；S1–S3 活动期），横线为六样本中位数；纵轴为对数。C3 为文献报告区间（0.04–4.03%），无逐样本数值，仅以灰带示意，不参与任何倍数计算。C2 与 C6 分子相同，只在分母是否保留宿主 reads 上不同，括号标出其 ≤1.2% 的差异。（B）逐样本计算的定义间倍数（n = 6），以箱线图汇总；虚线表示无变化，箱上方数字为中位数。各定义并不独立：4.6 × 1.1 ≈ 5，远小于实测的 26 倍跨度。参考空间比值接近 1，仅因为所用库是噬菌体专用库；换用缺少噬菌体蛋白的通用病毒库时，同一比较得到 5.6×（见结果），那是那个库的性质，不是"参考空间选择"的普遍性质。

**图 3. 共享 vOTU 的数量是检测阈值的函数。**
（A）六种检测标准下在全部六个样本中均检出的 vOTU 数：contig 层面存在（0 个）与 reads 层面 RPKM > 0（783）、≥0.01（517）、≥0.1（63）、≥1（5）、≥10（1）。纵轴为对数。（B）同一批标准下单样本特有的 vOTU 比例。呈 U 型，且两端成因相反：contig 层面的高值（84.5%）反映组装碎片化，而 RPKM ≥ 10 的高值（55.2%）反映高丰度病毒真实的样本特异性。（C）全部 15 个样本对的 Jaccard 相似度，分别按 contig 存在与丰度加权 reads（RPKM ≥ 1）计算；横线为中位数（0.0065 与 0.0234，相差 3.6 倍）。全图 n = 6 个样本。contig 层面的"零共享"不可读作"没有共同病毒"：同一病毒在不同样本中可能组装成不同片段。

---

## 三、写图注时的四条自律

| # | 规则 | 本文的执行 |
|---|---|---|
| 1 | 图注首句必须是**论断**，不是"这张图展示了……" | 三张图首句都是可证伪的陈述（"只有一个决策移动数字"/"六种定义跨度 26 倍"/"共享数是阈值的函数"） |
| 2 | n 与统计量必须写明 | 每个图注都写 n = 6；Fig 2B 说明箱线图与中位数；Fig 3C 说明 15 对与中位数 |
| 3 | 图上出现但正文没解释的元素，图注要解释 | C3 灰带、C2–C6 括号、对数轴、U 型两端成因 |
| 4 | **不可读作**的误读要主动堵 | Fig 3 明写"零共享 ≠ 没有共同病毒"；Fig 1 明写"分母接近 1 是粪便特性"、Fig 1/2 明写"参考空间接近 1 源于专用库" |

---

## 四、与表的分工

| 内容 | 放在哪里 |
|---|---|
| 六种定义的确切分子/分母/参考空间 | Table 1（不在图注重复） |
| 逐样本数值 | Table 1 |
| 定义之间"为什么会差" | 图注 + 正文 |
| 报数时必须写什么 | Table 2 |

图注里凡出现 "defined in Table 1" 都不再展开定义——避免同一内容两处维护。

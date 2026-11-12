# 图注正式稿（Fig 1–3）

**日期** 2026-11-13　|　**状态** 定稿（英文投稿版 + 中文对照）
**配套 Word**：`11_proposal/legends/output/Figure_legends.docx`
**对应图件**：`08_figures/fig_a0`、`08_figures/fig_a1`、`08_figures/fig_a2`

> 重新生成：`python 11_proposal/legends/code/make_legends_docx.py`
> 英文为 canonical；中文仅供内部讨论，不入稿。

---

## 一、英文投稿版（canonical）

**Figure 1. Four reporting decisions determine the viral fraction of a gut metagenome.**
Each row is a choice that has to be made before a viral fraction can be reported: denominator, reference space, category filter, and statistical unit. Boxes list the alternatives available at each decision. Values on the right are median fold changes measured in this dataset with the other dimensions held fixed, from six fecal metagenomes of *Alligator sinensis* (PRJNA539906; n = 6). Across all definitions and samples the observed span is 171× (0.089–15.2%). These fold changes are not multiplicative: 1.01 × 5.6 × 7.1 × 5.4 ≈ 217, whereas the measured span is 171×, because each ratio derives from a different sample and a different pair of definitions. Within a single sample, definitions alone span 22.2–124.8×, and the additional sample effect is 1.37× (Fig. 2). The denominator row shows a near-unity effect because host reads make up only 0.07–2.51% of these libraries; this reflects the low host content of fecal samples and is not a general property of metagenomes.

**Figure 2. Six definitions of the same measurement span 171-fold.**
(**A**) Viral fraction of reads under six reporting definitions (C1, C2, C6, C3, C4 and C5; defined in Table 1) for six fecal metagenomes. Points are individual samples (W1–W3, hibernating; S1–S3, active); horizontal bars are medians across the six samples. The y axis is logarithmic. C3 is a literature-reported range (0.04–4.03%) with no per-sample values; it is drawn as a grey band for orientation only and is excluded from every fold-change calculation. C2 and C6 share the same numerator and differ only in whether host reads are retained in the denominator; the bracket marks their ≤1.2% difference. (**B**) Fold change between definitions, computed within each sample (n = 6) and summarised as boxplots; the dashed line marks no change and numbers above the boxes are medians. Definitions are not independent: the product of the four median ratios (≈217) exceeds the observed 171-fold span.

**Figure 3. The number of shared vOTUs is a function of the detection threshold.**
(**A**) Number of vOTUs detected in all six samples under six detection criteria: contig-level presence (0 vOTUs) and read-level abundance at RPKM > 0 (783), ≥0.01 (517), ≥0.1 (63), ≥1 (5) and ≥10 (1). The y axis is logarithmic. (**B**) Proportion of vOTUs detected in a single sample under the same criteria. The relationship is U-shaped, and the two ends have opposite causes: the high value at contig level (84.5%) reflects assembly fragmentation, whereas the high value at RPKM ≥ 10 (55.2%) reflects genuine sample specificity of abundant viruses. (**C**) Jaccard similarity for all 15 sample pairs, computed either from contig presence or from abundance-weighted reads (RPKM ≥ 1); horizontal bars are medians (0.0065 and 0.0234, a 3.6-fold difference). Throughout, n = 6 samples. The contig-level value of zero should not be read as an absence of shared viruses: the same virus can assemble into different fragments in different samples.

---

## 二、中文对照（内部讨论用）

**图 1. 四个报告决策共同决定一份肠道宏基因组的病毒占比。**
每一行都是报出"病毒占比"之前必须做出的选择：分母、参考空间、类别筛选、统计单元。方框列出该决策的可选项。右侧数值为固定其余维度时在本批数据上实测的中位倍数（6 份扬子鳄粪便宏基因组，PRJNA539906；n = 6）。全部定义与全部样本的实测跨度为 171×（0.089–15.2%）。这些倍数不可相乘：1.01 × 5.6 × 7.1 × 5.4 ≈ 217，而实测跨度是 171×，因为每个比值来自不同样本与不同定义组合。同一样本内仅定义本身即跨 22.2–124.8×，样本效应另贡献 1.37×（见图 2）。分母一行接近 1，是因为本批文库中宿主 reads 仅占 0.07–2.51%——这是粪便样本低宿主含量的特性，不是宏基因组的普遍规律。

**图 2. 同一个测量的六种定义，跨度 171 倍。**
（A）六种报告定义（C1、C2、C6、C3、C4、C5，定义见表 1）下六个粪便宏基因组的病毒 reads 占比。点为单个样本（W1–W3 冬眠期；S1–S3 活动期），横线为六样本中位数；纵轴为对数。C3 为文献报告区间（0.04–4.03%），无逐样本数值，仅以灰带示意，不参与任何倍数计算。C2 与 C6 分子相同，只在分母是否保留宿主 reads 上不同，括号标出其 ≤1.2% 的差异。（B）逐样本计算的定义间倍数（n = 6），以箱线图汇总；虚线表示无变化，箱上方数字为中位数。各定义并不独立：四个中位比值之积（≈217）大于实测的 171×。

**图 3. 共享 vOTU 的数量是检测阈值的函数。**
（A）六种检测标准下在全部六个样本中均检出的 vOTU 数：contig 层面存在（0 个）与 reads 层面 RPKM > 0（783）、≥0.01（517）、≥0.1（63）、≥1（5）、≥10（1）。纵轴为对数。（B）同一批标准下单样本特有的 vOTU 比例。呈 U 型，且两端成因相反：contig 层面的高值（84.5%）反映组装碎片化，而 RPKM ≥ 10 的高值（55.2%）反映高丰度病毒真实的样本特异性。（C）全部 15 个样本对的 Jaccard 相似度，分别按 contig 存在与丰度加权 reads（RPKM ≥ 1）计算；横线为中位数（0.0065 与 0.0234，相差 3.6 倍）。全图 n = 6 个样本。contig 层面的"零共享"不可读作"没有共同病毒"：同一病毒在不同样本中可能组装成不同片段。

---

## 三、写图注时的四条自律

| # | 规则 | 本文的执行 |
|---|---|---|
| 1 | 图注首句必须是**论断**，不是"这张图展示了……" | 三张图首句都是可证伪的陈述（"四个决策决定占比"/"六种定义跨度 171 倍"/"共享数是阈值的函数"） |
| 2 | n 与统计量必须写明 | 每个图注都写 n = 6；Fig 2B 说明箱线图与中位数；Fig 3C 说明 15 对与中位数 |
| 3 | 图上出现但正文没解释的元素，图注要解释 | C3 灰带、C2–C6 括号、对数轴、U 型两端成因 |
| 4 | **不可读作**的误读要主动堵 | Fig 3 明写"零共享 ≠ 没有共同病毒"；Fig 1 明写"分母接近 1 是粪便样本特性" |

---

## 四、与表的分工

| 内容 | 放在哪里 |
|---|---|
| 六种定义的确切分子/分母/参考空间 | Table 1（不在图注重复） |
| 逐样本数值 | Table 1 |
| 定义之间"为什么会差" | 图注 + 正文 |
| 报数时必须写什么 | Table 2 |

图注里凡出现 "defined in Table 1" 都不再展开定义——避免同一内容两处维护。

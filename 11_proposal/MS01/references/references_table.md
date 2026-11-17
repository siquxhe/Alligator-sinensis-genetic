# 推荐文献表

> Zotero 导入请用同目录的 `refs.ris`（本文件为人读版）


## 一、核心（直接决定论文怎么写）

| 文献 | 出处 | DOI / PMID | 为什么读 |
|---|---|---|---|
| **Forbes et al. (2025)**<br>Benchmarking of Human Read Removal Strategies for Viral and Microbial Metagenomics | Cell Reports Methods | 10.1016/j.crmeth.2025.101218 | 分母轴最近邻。它评的是宿主 reads 去除的性能与下游影响，不是病毒占比——正文必须主动划清界限 |
| **bioRxiv 预印本 (2026)**<br>Benchmarking and integration of viral prediction tools to uncover viral dark matter across divergent low abundance metagenomes | bioRxiv | 10.64898/2026.10.14.759168 | 11 种病毒识别工具基准，结论是两两组合 + Kraken2X 过滤优于单工具；支持我们'无单一最佳流程'的论点 |
| **Kosmopoulos et al. (2026)**<br>CheckAMG: Accurate Identification of Auxiliary Viral Genes with Genome-Language Models | bioRxiv | 10.64898/2026.09.23.753886<br>PMID 42818345 | 明确承认'病毒 vs 细胞来源归属存在歧义'，是 47.4% 代谢基因那段最硬的背书；同时是 cargo 判定的压力来源 |
| **Roux et al. (2019)**<br>Minimum Information about an Uncultivated Virus Genome (MIUViG) | Nature Biotechnology 37(1): 29-37 | 10.1038/nbt.4306<br>PMID 30556814 | 唯一现成的病毒组报告标准，但只覆盖基因组、不覆盖 read 层占比——这正是我们的空位 |

## 二、决定 Table 2 站位（最易被忽略）

| 文献 | 出处 | DOI / PMID | 为什么读 |
|---|---|---|---|
| **Mirzayi et al. (2021)**<br>Reporting guidelines for human microbiome research: the STORMS checklist | Nature Medicine 27(11): 1885-1892 | 10.1038/s41591-021-01552-x<br>PMID 34789871 | 17 项清单、6 章节，是最成功的报告规范范式；其第 4.5 项已要求报告是否去除人源 DNA，Table 2 必须与之划界 |

## 三、方法可信度（被问到能答）

| 文献 | 出处 | DOI / PMID | 为什么读 |
|---|---|---|---|
| **Camargo et al. (2024)**<br>Identification of mobile genetic elements with geNomad | Nature Biotechnology 42(8): 1303-1312 | 10.1038/s41587-023-01953-y<br>PMID 37735266 | C4 的来源工具；审稿人会问其 MCC 95.3% 的适用范围 |
| **Nayfach et al. (2021)**<br>CheckV assesses the quality and completeness of metagenome-assembled viral genomes | Nature Biotechnology 39(5): 578-585 | 10.1038/s41587-020-00774-7 | 202 条基因组 Complete/High/Medium 分级的依据 |
| **Roux et al. (2023)**<br>iPHoP: An integrated machine learning framework to maximize host prediction for metagenome-derived viruses of archaea and bacteria | PLoS Biology 21(4): e3002083 | 10.1371/journal.pbio.3002083<br>PMID 37083735 | 宿主预测工具；我们属级只有 2/5 的那个结果出自它 |
| **Callanan et al. (2021)**<br>Biases in Viral Metagenomics-Based Detection, Cataloguing and Quantification of Bacteriophage Genomes in Human Faeces, a Review | Microorganisms 9(3): 524 | 10.3390/microorganisms9030524 | 逐环节偏差综述（采样、MDA、组装、数据库、注释），并指出 RVDB 排除噬菌体；直接支撑 Table 2 第 1–4 项 |

## 四、判断是否重复别人

| 文献 | 出处 | DOI / PMID | 为什么读 |
|---|---|---|---|
| **Sáenz et al. (2026)**<br>The chicken gut virome: spatial structuring and extensive diversity of 19,778 viral populations | mSystems 11(4): e00191-26 | 10.1128/msystems.00191-26<br>PMID 41910132 | 第二数据集来源。注意它的写法：1,514 样本、19,778 vOTU，病毒丰度只给'mapped reads 作为代理'（1.10–1.84%） |
| **Tang et al. (2019)**<br>Metagenomics Reveals Seasonal Functional Adaptation of the Gut Microbiome to Host Feeding and Fasting in the Chinese Alligator | Frontiers in Microbiology 10: 2409 | 10.3389/fmicb.2019.02409<br>PMID 31708889 | 扬子鳄原始数据来源；C3 那个 0.04–4.03% 出自它，且原文未说清怎么算的 |
| **Junier et al. (2019)**<br>Viral Metagenomics in the Clinical Realm: Lessons Learned from a Swiss-Wide Ring Trial | Genes 10(9): 655 | 10.3390/genes10090655 | 反证，必须主动处理：同一数据、同一共享库下性能主要由算法决定，库间无显著差异。区分点——他们比两个精选库，我们比'不含噬菌体的公共蛋白库 vs 含噬菌体的自组装目录' |
| **Choi et al. (2025)**<br>Benchmarking Read-Based Virome Profilers for Human Virus Detection and Community Discovery | Journal of Bacteriology and Virology 55(4) |  | 三种 read-based profiler 在同一数据上给出显著不同的病毒信号。⚠️ 未找到 DOI，导入 Zotero 后需手工补卷期页；补不到则改用 Callanan 2021 |

## 五、补充（备查）

| 文献 | 出处 | DOI / PMID | 为什么读 |
|---|---|---|---|
| **bioRxiv 预印本 (2025)**<br>LEMMIv2: Benchmarking Framework for Metagenomic and 16S Amplicon Profilers with a Catalogue of Evaluated Tools | bioRxiv | 10.1101/2025.03.06.641904 | 持续基准测试框架，支持'参考库/平台决定结论' |
| **Hegarty et al. (2024)**<br>Benchmarking informatics approaches for virus discovery: caution is needed when combining in silico identification methods | mSystems 9(3): e01105-23 | 10.1128/msystems.01105-23<br>PMID 38376167 | 组合工具并不必然更优；与'多口径并列'的论点呼应 |

## 六、RVDB 溯源与个体特异性

| 文献 | 出处 | DOI / PMID | 为什么读 |
|---|---|---|---|
| **Goodacre et al. (2018)**<br>A Reference Viral Database (RVDB) To Enhance Bioinformatics Analysis of High-Throughput Sequencing for Novel Virus Detection | mSphere 3(2): e00069-18 | 10.1128/mSphereDirect.00069-18<br>PMID 29564396 | RVDB 原始文献，明写收录范围 excluding bacterial viruses。Methods 声明库组成的第一出处；若 C1/C2 用 RVDB，必须引它 |
| **Chin et al. (2025)**<br>Refinement of the Reference Viral Database (RVDB) for improving bioinformatics analysis of virus detection by high-throughput sequencing (HTS) | mSphere 10: e00286-25 | 10.1128/msphere.00286-25 | RVDB 2025 精修版，再次确认 phages 被排除（to reduce false-positive hits）。与 Goodacre 2018 配对，构成'库不含噬菌体'的双证 |
| **Bigot et al. (2020)**<br>RVDB-prot, a reference viral protein database and its HMM profiles | F1000Research 8: 530 | 10.12688/f1000research.18776.2<br>PMID 32983411 | RVDB-prot 由 U-RVDB 核酸条目逐条转换而来，官方未逐字声明噬菌体范围——属推断继承。写进 Methods 前须用 workflow/check_rvdb_phage.sh 在本批库上验证 |
| **Garmaeva et al. (2021)**<br>Stability of the human gut virome and effect of gluten-free diet | Cell Reports 35(7): 109132 | 10.1016/j.celrep.2021.109132<br>PMID 34010651 | 11 人纵向，个体间高度分化；CIT-7 首选。其 Lifelines 工具比较（三种工具均 <1% 但彼此差异显著）可作 CIT-1 辅证——要写'估计随工具浮动'，不能写'病毒就是 <1%' |
| **Stockdale et al. (2023)**<br>Interpersonal variability of the human gut virome confounds disease signal detection in IBD | Communications Biology 6(1) | 10.1038/s42003-023-04592-w | 个体变异足以淹没疾病信号；比'个体差异大'更强的表述，适合解释 6 样本为何不能做组间比较 |
| **Minot et al. (2013)**<br>Rapid evolution of the human gut virome | Proceedings of the National Academy of Sciences 110(30): 12450-12455 | 10.1073/pnas.1300833110 | 单个体 2.5 年纵向，约 80% 病毒类型持续；用于'个体内稳定、个体间不同'这对表述 |
| **Reyes et al. (2010)**<br>Viruses in the faecal microbiota of monozygotic twins and their mothers | Nature 466: 334-338 | 10.1038/nature09199 | 同卵双生儿病毒组仍各自成组——经典对照，排除'遗传决定'这一解释 |

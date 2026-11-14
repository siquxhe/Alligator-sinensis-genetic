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

## 四、判断是否重复别人

| 文献 | 出处 | DOI / PMID | 为什么读 |
|---|---|---|---|
| **Sáenz et al. (2026)**<br>The chicken gut virome: spatial structuring and extensive diversity of 19,778 viral populations | mSystems 11(4): e00191-26 | 10.1128/msystems.00191-26<br>PMID 41910132 | 第二数据集来源。注意它的写法：1,514 样本、19,778 vOTU，病毒丰度只给'mapped reads 作为代理'（1.10–1.84%） |
| **Tang et al. (2019)**<br>Metagenomics Reveals Seasonal Functional Adaptation of the Gut Microbiome to Host Feeding and Fasting in the Chinese Alligator | Frontiers in Microbiology 10: 2409 | 10.3389/fmicb.2019.02409<br>PMID 31708889 | 扬子鳄原始数据来源；C3 那个 0.04–4.03% 出自它，且原文未说清怎么算的 |

## 五、补充（备查）

| 文献 | 出处 | DOI / PMID | 为什么读 |
|---|---|---|---|
| **bioRxiv 预印本 (2025)**<br>LEMMIv2: Benchmarking Framework for Metagenomic and 16S Amplicon Profilers with a Catalogue of Evaluated Tools | bioRxiv | 10.1101/2025.03.06.641904 | 持续基准测试框架，支持'参考库/平台决定结论' |
| **Hegarty et al. (2024)**<br>Benchmarking informatics approaches for virus discovery: caution is needed when combining in silico identification methods | mSystems 9(3): e01105-23 | 10.1128/msystems.01105-23<br>PMID 38376167 | 组合工具并不必然更优；与'多口径并列'的论点呼应 |

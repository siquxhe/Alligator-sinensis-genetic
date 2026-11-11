# Fig. M3 — 病毒基因组资源景观

> 首次出图：2026-11-08
> 定位：回答"这批数据能给出什么可用的病毒基因组资源"

## 1. 本图要支撑的论断

1. 六样本共产出 **202 条中高质量病毒基因组**（Complete 29 / High 48 / Medium 125），
   长度中位 32.5 kb，最长 201.8 kb。
2. 产量在样本间差异极大（10–72 条），与病毒丰度一致：S2/S3 贡献 130 条（64%），
   W2 最少（10 条）。
3. 完整性评估与 contig 长度强相关（Complete 中位 53.9 kb、High 38.8 kb、Medium 25.2 kb），
   这是 CheckV 的方法学特性，**不是"短基因组质量差"**——短 contig 缺少判定完整所需的末端信息。
4. 这些基因组携带足够的丰度信号（RPKM 中位 3.0，最高 313.8），可支持下游的宿主预测与生态分析。

## 2. 面板构成

| 面板 | 内容 | 支撑的论断 |
|---|---|---|
| A | 长度 × 完整性散点，点面积 = RPKM，颜色 = 季节 | 基因组质量画像；丰度与长度无强相关 |
| B | 各样本的基因组数（按 CheckV 分级堆叠） | 产量集中在 S2/S3 |
| C | 长度分布按质量分级（对数轴，横线为中位） | 完整度依赖长度，属方法学边界 |

配色：季节沿用 Okabe–Ito（冬 #0072B2 / 夏 #E69F00）；
质量分级用蓝色梯度（Complete 深 → Medium 浅）。

## 3. 关键数值

| 指标 | 数值 |
|---|---|
| 中高质量基因组总数 | 202 |
| Complete / High / Medium | 29 / 48 / 125 |
| 长度中位（全体） | 32,525 bp |
| 最长 | 201,842 bp（S3，Complete 100%） |
| 各质量长度中位 | Complete 53.9 kb / High 38.8 kb / Medium 25.2 kb |
| RPKM 中位 / 最大 | 3.0 / 313.8 |
| RPKM ≥ 1 的基因组 | 196 / 202 |

## 4. 方法

```
组装    MEGAHIT 1.2.9 --min-contig-len 1000
识别    geNomad 1.13.0 end-to-end（DB v1.9）
完整性  CheckV 1.1.1（Complete ≥90%、High ≥90% 且无污染、Medium ≥50%）
丰度    reads 比对到 9,980 个 vOTU 代表序列（bowtie2 --very-sensitive），RPKM 归一化
```

## 5. 局限

1. **完整性依赖长度**（C 面板）：短 contig 即使真实完整，也常被判为 Medium 或未确定。
   因此"202 条"是下限估计，实际存在的病毒基因组更多。
2. 分类分辨率不足：192/202 只能定到纲（Caudoviricetes），科属级信息缺失，
   需要额外的分类模块或比对才能细化。
3. RPKM 基于 contig 长度归一化，对部分基因组（provirus）可能低估。
4. 未做宿主预测（iPHoP），因此无法回答"这些病毒感染哪些肠道菌"。

## 6. 复现

```bash
cd 08_figures/fig_m3
python code/plot_m3.py
```
输入 `05_c_stage/hq_genomes_with_abundance.tsv`（由 `hq_genomes.tsv` + `votu_members.tsv`
+ `votu_abundance_rpkm.tsv` 合并得到）。
产出：`output/FigM3_viral_genome_landscape.pdf` + `.png`（300 dpi）。

## 7. 英文图注（投稿用草稿）

**Figure M3 | Landscape of assembled viral genomes.**
**(A)** Length, completeness and relative abundance of the 202 medium- and high-quality viral genomes.
Point area scales with RPKM; blue, genomes from winter (hibernating) samples; orange, from summer
(active) samples.
**(B)** Number of genomes recovered per sample, coloured by CheckV quality tier.
**(C)** Genome length by quality tier (log scale); horizontal bars denote medians.
Completeness calls are length-dependent — longer contigs carry the terminal information required for
complete-genome assignment — so the 202 genomes represent a lower bound on the true number of
recoverable viral genomes.

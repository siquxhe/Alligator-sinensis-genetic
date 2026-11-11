# Fig. M1 — 测序与病毒信号景观（第一版）

> 定位：两页纸材料/预实验报告用的基础图，不是投稿终稿。
> 首次出图：2026-11-08

## 1. 本图要支撑的科学论断

1. 6 个圈养扬子鳄粪便宏基因组样本测序质量合格，无样本需要剔除：
   Q30 由 84.8–95.3% 提升至 88.2–95.9%，reads 保留率 91.5–98.8%。
2. 去宿主后，带病毒蛋白相似性的 reads 占比稳定在 **0.675–0.702%**（26.1–33.1 万条/样本），
   远超进入组装阶段的门槛（0.01%），G1 闸门通过。
3. 冬季样本宿主比对率高于夏季（中位 0.60% vs 0.07%），但由 W1 单样本驱动，n=3，仅作描述。
4. **病毒信号是弥散的**：Top1 类群平均只占 5.4%，前 8 类群合计 27.4%，
   单个样本涉及 561–782 个"物种"。这意味着信号由大量低丰度、共享保守域的序列构成，
   而非某一优势病毒——这是判断"能否直接下病毒阳性结论"的关键证据。

## 2. 面板构成

| 面板 | 内容 | 可视化 | 数据层 |
|---|---|---|---|
| A | 质控前后 Q30 与 reads 保留率 | 哑铃图（open=原始，filled=质控后），箭头示方向；季节用刻度标签颜色编码 | `M1_summary.csv` 的 `q30_before_pct/q30_after_pct/pass_rate_pct` |
| B 左 | 宿主比对率 | 对数轴个体散点 + 组中位数短横线 | `host_aligned_pct` |
| B 右 | 病毒相似 reads 占比 | 线性紧轴个体散点 + 组中位数 | `viral_reads_pct` |
| C | 病毒类群构成 | 100% 堆叠条形（Top8 + Other） | `viral_top_taxa.tsv`、`viral_species_counts.tsv` |

配色：Okabe–Ito 色盲安全（冬 #0072B2 / 夏 #E69F00）。

## 3. 统计口径

- 每组 n=3，**不做显著性检验**（功效不足，任何 p 值都不可信）；
- 一律画个体点 + 中位数，不画箱线图（n=3 画箱线会暗示不存在的分布）；
- 病毒占比的"中位数"与"均值"差异 <0.005 个百分点，结论不受口径影响。

## 4. 数据与方法链条

```
00_raw → 01_qc (fastp 0.23.4, -q 20 -l 50)
       → 02_host_removed (bowtie2 2.5.4 --very-sensitive, 扬子鳄基因组)
       → 04_viral (DIAMOND 2.2.8 blastx vs RVDB-prot v32 Unique, 783,103 蛋白)
```

病毒命中筛选：`--fast -e 1e-5 -k 1 --query-cover 50`，后处理再筛比对长度 ≥30 aa、一致性 ≥40%。

## 5. 已知局限（写正文时必须交代）

> **2026-11-08 交叉验证后更新**：完成阈值阶梯、双零假设对照、双端一致性、功能归类四项验证。
> 结论是信号真实（对照零命中、双端富集 16–25 倍），但**远缘同源占绝对主导**，且 47.4% 的命中
> 落在巨型病毒携带的代谢管家酶上、仅 1.3% 落在结构蛋白上。
> 因此 0.69% 只能作上限口径，正文主指标改为**病毒特异 0.103%**。
> 完整证据见 `10_reports/viral_signal_validation_2026-11-08.md`。

1. **C 面板是 best-hit 层面的物种归属**，且已验证其中 47.4% 的命中指向代谢/管家酶（巨型病毒"偷"来的宿主基因）、
   仅 1.3% 指向结构蛋白。**该面板只能说明"与哪些参考蛋白最相似"，不能说明样本中存在哪些病毒**；
   下阳性结论必须等 C 阶段组装结果。
2. C 面板只展示 Top8 类群，其余 553–774 个类群合并为 Other。
3. 宿主基因组为参考基因组单拷贝比对，宿主率不含未收录的宿主序列，故为**下限**估计。
4. 未做去 rRNA（DNA 宏基因组按计划跳过），真核/细菌 RNA 残留会进入病毒筛查分母。
5. W3 与 S1 的重复率（9.6%、7.6%）明显高于其他样本，提示文库复杂度偏低。不过这两样本的病毒占比
   反而最高（0.692%、0.702%），**未观察到重复率高导致病毒检出下降**，故暂不认为影响本图结论；
   但该指标应在方法学中如实报告。

## 6. 复现

```bash
cd 08_figures/fig_m1
python code/plot_m1.py     # 读 ../../09_tables/，写 ../output/
```

产出：`output/FigM1_sequencing_landscape.pdf`（矢量）+ `.png`（300 dpi）。

## 7. 下一版待改

- [ ] 若能拿到基因组层面确认结果，C 面板改为"确认后的病毒科属构成"，可信度大幅提升；
- [ ] 补 rRNA 占比后，病毒占比改用"占非 rRNA reads"作为分母，更接近文献可比口径；
- [ ] 若能扩充到 n≥6/组，B 面板可改用带分布的箱线/小提琴并加检验。

## 8. 英文图注（投稿用草稿）

**Figure M1 | Sequencing landscape of captive Chinese alligator fecal metagenomes.**
**(A)** Q30 base percentage before (open circles) and after (filled circles) quality trimming,
annotated with read retention. Tick labels are coloured by season (blue, winter; orange, summer).
**(B)** Host-aligned read fraction (left, log scale) and viral-like read fraction (right) after
host depletion. Horizontal bars denote group medians. n = 3 per season; no statistical test was
applied owing to the small sample size. **(C)** Composition of viral-like reads at the best-hit
taxon level; the eight most abundant taxa across all samples are shown individually and remaining
taxa (553–774 per sample) are pooled as "Other". Viral-like reads were defined by DIAMOND blastx
against RVDB-prot v32 (Unique, 783,103 proteins) with E ≤ 1e-5, ≥50% query coverage, and
post-filtering at ≥30 aa alignment length and ≥40% identity. Taxon assignments reflect best-hit
similarity and should not be interpreted as confirmed viral presence.

---

# v2 版（2026-11-08）—— 按交叉验证后的新口径重画

## 改动理由

v1 把"病毒样 reads 0.69%"作为结论，并把 best-hit 物种构成画成主面板 C。
交叉验证表明：47.4% 的命中落在巨型病毒携带的管家酶上、结构蛋白仅 1.3%，
且信号在 60% 一致性处断崖（0.0001%）。原 C 面板会误导读者以为"样本里有这些病毒"，
故 v2 用两个验证面板替换它。

## 新面板构成

| 面板 | 内容 | 支撑的论断 |
|---|---|---|
| A | 质控前后 Q30 哑铃图 + 保留率 | 数据质量合格，无样本需剔除 |
| B | 宿主比对率（对数轴，组中位数） | 冬季 0.60% vs 夏季 0.07%，n=3 仅作描述 |
| **C** | **病毒样占比随比对严格度衰减（6 样本 + 均值，对数轴，G1 门槛虚线）** | **信号在 id≥60% 处断崖 → 无近缘已知病毒；三种口径数值同框** |
| **D** | **病毒样命中的功能构成（100% 堆叠）** | **47.4% 为宿主来源代谢基因，结构蛋白仅 1.3%** |

原 v1 的物种构成面板已移出主图（数据保留在 `09_tables/viral_top_taxa.tsv`，
如要用请放附图并注明"best-hit 相似性，非检出证据"）。

## 三种口径（图中 C 面板角标）

| 口径 | 均值 |
|---|---|
| viral-like | 0.692% |
| viral-specific（结构+复制） | 0.103% |
| structural only | 0.0089% |

## v2 英文图注（投稿用草稿）

**Figure M1 | Sequencing landscape and validation of viral signal in captive Chinese alligator
fecal metagenomes.**
**(A)** Q30 base percentage before (open circles) and after (filled circles) quality trimming,
annotated with read retention. Tick labels are coloured by season (blue, winter; orange, summer).
**(B)** Host-aligned read fraction after host depletion (log scale). Horizontal bars denote group
medians (n = 3 per season; no statistical test applied owing to sample size).
**(C)** Viral-like read fraction as a function of alignment stringency. Grey lines, individual
samples; black line, mean of six samples. The dashed line marks the 0.01% screening threshold.
Values inset give the three reporting definitions: viral-like (any hit, E ≤ 1e-5, ≥40% identity,
≥30 aa), viral-specific (structural and replication/transcription genes only) and structural-only.
Note the collapse above 60% identity, indicating that no reads derive from genomes closely related
to known viruses.
**(D)** Functional composition of viral-like reads. Nearly half map to metabolic/housekeeping
enzymes carried by giant viruses, whereas bona fide virion genes account for 1.3%.
Viral-like reads were defined by DIAMOND blastx against RVDB-prot v32 (Unique, 783,103 proteins).
Two null models (shuffled reads against the real database; real reads against a reversed database)
yielded zero hits, and paired-end concordance exceeded the independence expectation 16–25 fold,
indicating that the signal reflects genuine sequence homology rather than compositional bias.
Taxon assignments at the best-hit level are not evidence of viral presence.

## 复现

```bash
cd 08_figures/fig_m1
python code/plot_m1_v2.py
```
产出：`output/FigM1_v2_signal_validation.pdf` + `.png`（300 dpi）。

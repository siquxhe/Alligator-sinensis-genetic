# Fig. M2 — 肠道病毒组随宿主摄食状态变化，而非日历季节

> 首次出图：2026-11-08
> 定位：C 阶段（组装→病毒识别→丰度→群落比较）的核心结果图

## 1. 本图要支撑的论断

1. 六个圈养个体的肠道群落可分为**两类**：冬眠型（高 GC、病毒少）与活动型（低 GC、病毒丰富）。
2. 病毒组结构存在清晰的季节/状态结构（同季节 Bray-Curtis 0.660 vs 跨季节 0.912）。
3. **"夏季采样"不等于"活动期状态"**：个体 F5（样本 S1）在 7 月采样，但病毒组与菌群都是冬眠型。
4. 上述结论由**两类独立数据**支撑：病毒宏基因组的碱基组成与结构，以及细菌 16S 群落相似度。

## 2. 面板构成

| 面板 | 内容 | 支撑的论断 | 数据源 |
|---|---|---|---|
| A | 读段 GC 与病毒 reads 占比的散点（6 样本） | 群落分成两组；S1 落在冬眠型一侧 | `05_c_stage/sample_gc_viral.tsv` |
| B | 病毒组 Bray-Curtis 距离热图（vOTU 丰度加权） | 同季节相似、S1 离群 | `05_c_stage/votu_abundance_rpkm.tsv` 重算 |
| C | 细菌 16S 群落相似度热图（15-mer 余弦） | 独立验证：A.F5 与冬季组聚在一起 | `05_c_stage/16s_kmer_similarity.tsv` |

配色：季节用 Okabe–Ito（冬 #0072B2 / 夏 #E69F00）；离群个体用 #D55E00 红圈；
热图 B 用 YlOrRd（距离越大越红）、C 用 viridis（相似度越高越亮）。

## 3. 关键数值

| 指标 | 数值 |
|---|---|
| S1 与冬季样本的病毒距离 | 0.82 / 0.83 / 0.89 |
| S1 与夏季样本的病毒距离 | 0.94 / 0.95 |
| S1（A.F5）与冬季组 16S 相似度 | **0.801** |
| S1（A.F5）与夏季组 16S 相似度 | **0.415** |
| 夏季内部（AF3–AF4）16S 相似度 | 0.995 |
| 冬季内部 16S 相似度 | 0.915 |

## 4. 方法与口径

- **B 面板**：reads 比对到统一的 9,980 个 vOTU 代表序列（bowtie2 --very-sensitive），
  RPKM 归一化，按全矩阵计算 Bray-Curtis。距离 0 = 完全相同，1 = 完全不同。
- **C 面板**：每样本 3 万条 16S read，15-mer 频次（保留 ≥2 次），余弦相似度。
  无需参考数据库，不引入分类器偏差。
- **A 面板**：GC 由每样本 20 万条 read 抽样计算；病毒 reads 占比来自丰度比对结果。

## 5. 局限

1. n=3/组，不做统计检验；A 面板的两组分离是描述性的。
2. GC 是群落组成的间接指标（由优势菌门的 GC 偏好决定），不是直接分类结果。
3. C 面板为 k-mer 相似度，未做物种注释，因此只能回答"像谁"，不能回答"由哪些属组成"。
4. 季节与个体在设计上完全混淆（第 8 节），本图展示的是**状态关联**，不是因果。

## 6. 复现

```bash
cd 08_figures/fig_m2
python code/plot_m2.py
```
产出：`output/FigM2_host_state_viral_community.pdf`（矢量）+ `.png`（300 dpi）。

## 7. 英文图注（投稿用草稿）

**Figure M2 | Gut viral communities track host feeding state rather than calendar season.**
**(A)** Relationship between read GC content and the fraction of reads mapping to viral contigs.
Blue, winter (hibernating) samples; orange, summer (active) samples. The red ring marks sample S1
(individual F5), which was collected in summer but harbours a hibernating-type community.
**(B)** Bray-Curtis dissimilarity between viral communities, computed on vOTU-level RPKM after
mapping reads from all samples to a unified reference of 9,980 vOTUs. Values on the diagonal are zero
by definition and are shown in pale yellow.
**(C)** Bacterial 16S community similarity (15-mer cosine) for the six individuals; sample labels
follow the viral panels. A.F5 clusters with the winter animals (mean similarity 0.80 vs 0.41 to the
summer group), independently confirming the state assignment made from viral data.
Sample sizes are n = 3 per season; no statistical test was applied.

## 8. 2026-11-08 排版修订（出报告时发现）

| 问题 | 修法 |
|---|---|
| B 面板 colorbar 的 "Distance" 轴标题与 C 面板 y 轴样本标签相撞 | `wspace` 0.42 → 0.58；C 面板 `tick_params(axis="y", pad=1.5)` |
| B、C 两个热图行列顺序不同（B 为 W1–S3，C 为 AF3–HF6），读者需重新对号 | C 面板改用与 B 相同的顺序：`order16 = [HF2, HF1, HF6, AF5, AF4, AF3]`，标签格式改为 `W1/F2` 这类紧凑写法 |
| 打印件上 C 面板 x 轴标签拥挤 | 标签由 "S3 (F3)" 改为 "S3/F3"，字号 6.0 |

**注意**：改行序后，脚本里原先按行号硬编码的验证输出（`Cmat[2, …]`）会指错行，
已改为按名字定位（`order16.index("AF5")`）。修改后复核：AF5 对冬季组 0.801、对夏季组 0.415，与修订前一致。

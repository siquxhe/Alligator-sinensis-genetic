# Aligator-sinensis-genetic

扬子鳄（*Alligator sinensis*）肠道病毒组的预分析仓库，兼含由此衍生的方法学论文、两个立项文档与一次参考库标定。

数据集：PRJNA539906，6 个粪便宏基因组（3 冬 + 3 夏），参考基因组 `GCA_000455745.1`。原始文献见仓库根 `fmicb-10-02409.pdf`。

---

## 读数字之前先看这里

仓库里同时存在三代口径，这不是冗余，是研究过程本身。取用数字时按此优先级：

| 优先级 | 位置 | 状态 |
|---|---|---|
| **1（最高）** | `13_calibration/PHROG六样本_2026-11-16.md`、`13_calibration/参考库核查_2026-11-15.md` | 最新。参考库"RVDB"实测低估噬菌体 4.68 倍；换 PHROG 后总跨度 **171× → 25.9×**，类别筛选 **4.64×**（CI 2.59–5.24） |
| **2** | `09_tables/phrog_6samples.tsv`、`09_tables/consolidated/` | 结构化结果表，图与稿件的取数来源 |
| **3** | `10_reports/技术报告_病毒占比口径与7倍差异定位_2026-11-12.md` | **历史版**，仍是 171× / 7.07× 口径，只作过程记录，不可再引用其结论句 |
| **4** | `10_reports/` 中 2026-11-09 的简报与结论汇总 | 更早，仅作背景 |

**已作废的表述**：不要再用"定义效应比样本效应大约两个数量级"（原约 90 倍）。新库下两者同量级，比值约 2 倍。

**尚未收敛的**：绝对病毒占比的区间（宽口径 vs 严格口径）仍无独立数据裁决，现有表述只应给出区间，不应给出点值。

---

## 目录

| 目录 | 内容 |
|---|---|
| `05_c_stage/` | 组装、病毒识别、基因组质量的中间表 |
| `06_host/` | 宿主预测（iPHoP 全量结果在 `full_iphop/`） |
| `07_cargo/`、`07_mag/` | 前噬菌体 cargo、44 条 MAG 的质量/分类/宿主验证表 |
| `08_figures/` | `fig_a0`（四维框架）、`fig_a1`（六口径）、`fig_a2`（阈值 sweep）、`fig_m1/m2/m3`、`multiqc/`；每图自带 `code/`、`output/`、`figX_log.md` |
| `09_tables/` | 结果表与合并主表（`consolidated/master_*.tsv`） |
| `10_reports/` | 各阶段报告、评审意见、文献核查、可行性分析、打包说明（归档） |
| `11_proposal/` | 论文提纲与稿件、Reference 生成器、两个立项提纲 |
| `12_second_dataset/` | 鸡肠道公共数据的外部校验（可行性核查与结果） |
| `13_calibration/` | 参考库核查、PHROG 标定与六样本重算、研究设计 |
| `workflow/` | 主流程脚本、图脚本、汇总脚本、`versions.txt`（工具版本与 Windows 适配记录） |

顶层另有三份 2026-11 早期的任务/方向文档，作为项目起点保留。

---

## 复现入口

```bash
source workflow/env.sh                                  # 统一环境
python workflow/consolidate_results.py                  # 合并结果表
python 08_figures/fig_a1/code/01_compute_five_denominators.py
python 08_figures/fig_a1/code/02_plot_fig2.py
python 08_figures/fig_a0/code/05_plot_fig1_framework.py  # 数字运行时从 Table 1 读取
python 11_proposal/references/code/make_refs.py          # RIS + 文献表，唯一事实源
```

工具版本、替代方案与 Windows 下的坑（perl `LC_ALL=C`、bowtie2 wrapper、fastp cygwin 依赖等）见 `workflow/versions.txt`。

---

## 使用边界

- **内部文档，外发前需处理**：`11_proposal/科研计划_下一步_2026-11-11.md` 第 9.4、10.1 节含合作与竞争判断；`10_reports/可行性分析_论文方向_2026-11-14.md` 是内部决策分析。
- **历史快照**：`CRISPR_recording_package_2026-11-15.zip` 不入库（`.gitignore` 第 57 行 `*.zip`），其说明见 `10_reports/打包说明_CRISPR录制包_2026-11-15.md`。
- **数据未入库**：原始 FASTQ、组装产物、MAG FASTA、参考库均在服务器，仓库只保存文本结果与脚本。

---

## 当前状态

方法学主线处于重标定后的改写阶段：核心主张从"定义远大于样本（差两个数量级）"收缩为"单样本内定义仍跨 4.7–8.4 倍，与样本效应同量级"。第二数据集（鸡）只能校验部分轴，参考库已先去宿主，分母维度不可评估。

未完成的验证：绝对占比的独立裁决、44 MAGs 的 CRISPR 携带率（脚本 `workflow/crispr_carriage.py` 已就绪，待服务器运行）。

# Alligator-sinensis-genetic

扬子鳄（*Alligator sinensis*）肠道病毒组的预分析仓库，兼含由此衍生的方法学论文、一篇 Perspective 与两个立项文档。

数据集：PRJNA539906，6 个粪便宏基因组（3 冬 + 3 夏），参考基因组 `GCA_000455745.1`。原始文献 PDF 见 `11_proposal/MS01/references/pdf/fmicb-10-02409.pdf`。

> **先看工单**：仓库里有三条论文线并行，容易混。入口是 `15_tickets/README.md`（看板 + ID 规则）。
> 目录在 2026-11-17 按工单重排过，旧路径查 `PATH_MAP.md`。

---

## 读数字之前先看这里

仓库里同时存在三代口径，这不是冗余，是研究过程本身。取用数字时按此优先级：

| 优先级 | 位置 | 状态 |
|---|---|---|
| **1（最高）** | `13_calibration/PHROG六样本_2026-11-16.md`、`13_calibration/校准_2026-11-16.md`、`13_calibration/诱饵重跑_2026-11-18.md` | 最新。参考库"RVDB"实测低估噬菌体约 6 倍；换 PHROG 后总跨度 **171× → 25.9×**，类别筛选 **4.64×**（CI 2.59–5.24）。`诱饵重跑` 是假阳性对照**唯一有实物的版本**：0 / 2,499,996，同批 reads 正向对照 5.511% |
| **1（结论有效，对照未留存）** | `13_calibration/参考库核查_2026-11-15.md` | **4.68× 有效**（同批 reads、同参数的确定性比较，第二节）；但第三节目录诱饵对照的原始产物已缺失（该文 2026-11-18 附注），"假阳性可忽略"不能当可复查证据引用——要引双零对照，用 `诱饵重跑` |
| **2** | `09_tables/phrog_6samples.tsv`、`09_tables/consolidated/` | 结构化结果表，图与稿件的取数来源 |
| **3** | `10_reports/MS01/技术报告_病毒占比口径与7倍差异定位_2026-11-12.md` | **历史版**，仍是 171× / 7.07× 口径，只作过程记录，不可再引用其结论句 |
| **4** | `10_reports/_shared/` 中 2026-11-09 的简报与结论汇总 | 更早，仅作背景 |

**已作废的表述**：不要再用"定义效应比样本效应大约两个数量级"（原约 90 倍）。换库后两者同量级（定义 4.6×，样本 1.6–7.1×）。

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
| `10_reports/MS01/` | 方法学论文的技术报告、评审意见、文献扫描、PHROG 建库报告 |
| `10_reports/CR01/` | Perspective 的文献地图、结案报告、核心论证、CRISPR 携带率 |
| `10_reports/_shared/` | 跨线：测序技术简报、结论汇总、可行性分析、文献核查 |
| `11_proposal/MS01/` | 方法学论文：`manuscript/`（v0.1–v0.3）、`tables/`、`legends/`、`references/`、`plans/` |
| `11_proposal/CR01/` | Perspective：`plans/`（提纲、骨架 v2）、`evidence/`（五层证据表、§2支撑） |
| `11_proposal/AR01/` | 幼鳄死因归因立项提纲（暂停） |
| `11_proposal/_shared/` | 科研总计划、系统迁移清单、早期任务表与方向备忘 |
| `12_second_dataset/` | 鸡肠道公共数据的外部校验（G-A1） |
| `13_calibration/` | 参考库核查、PHROG 标定、六样本重算、掺入校准 |
| `14_library/` | **统一文献库**：`Microbiomics.ris`（128 条）+ 核查记录；Zotero 为主库，RIS 为快照。v1 服务器文库计划已作废，留档 |
| `15_tickets/` | **工单**：看板与三条线的身份登记（新会话先读这里） |
| `workflow/` | 主流程脚本、图脚本、汇总脚本、`versions.txt`（工具版本与 Windows 适配记录） |

---

## 复现入口

```bash
source workflow/env.sh                                  # 统一环境
python workflow/consolidate_results.py                  # 合并结果表
python 08_figures/fig_a1/code/01_compute_five_denominators.py
python 08_figures/fig_a1/code/02_plot_fig2.py
python 08_figures/fig_a0/code/05_plot_fig1_framework.py  # 数字运行时从 Table 1 读取
python 11_proposal/MS01/references/code/make_refs.py      # RIS + 文献表
python 11_proposal/MS01/tables/table1/code/make_table1_docx.py
python 11_proposal/MS01/tables/table2/code/make_table2_docx.py
python 11_proposal/MS01/legends/code/make_legends_docx.py  # 解析 md 生成图注 Word，含过期数字断言
```

工具版本、替代方案与 Windows 下的坑（perl `LC_ALL=C`、bowtie2 wrapper、fastp cygwin 依赖等）见 `workflow/versions.txt`。

> 三个文档生成脚本均按 `.git` 定位仓库根，目录再搬也不会静默读错文件。

---

## 使用边界

- **内部文档，外发前需处理**：`11_proposal/_shared/科研计划_下一步_2026-11-11.md` 第 9.4、10.1 节含合作与竞争判断；`10_reports/_shared/可行性分析_论文方向_2026-11-14.md` 是内部决策分析。
- **历史快照**：`CRISPR_recording_package_2026-11-15.zip` 不入库（`.gitignore` 第 57 行 `*.zip`），其说明见 `10_reports/CR01/打包说明_CRISPR录制包_2026-11-15.md`。
- **数据未入库**：原始 FASTQ、组装产物、MAG FASTA、参考库均在服务器，仓库只保存文本结果与脚本。

---

## 当前状态（2026-11-17）

- **MS-01 方法学**：S3 正文。英文 v0.3 前半（摘要 279 词 + 引言与结果 5.1–5.4）完成，Methods/Discussion 未写；图、表、图注已按 PHROG 全长一致。
- **CR-01 Perspective**：S1 计划。提纲与骨架 v2（三条界线）完成，正文未起。
- **AR-01 幼鳄死因**：暂停。
- 已完成但曾列为"未完成"的两项：44 MAGs 的 CRISPR 携带率已实测为 **9/44 = 20.5%**（Wilson 95% CI 11.2–34.5%，`10_reports/CR01/CRISPR携带率_44MAGs_2026-11-15.md`）；掺入校准已完成（回收率 88.75% / 59.74%，校准后误差 ≤1.2 pp）。

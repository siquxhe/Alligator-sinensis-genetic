# 路径映射表（2026-11-17 目录重分类）

**为什么有这个文件**：目录按工单归属重排后，历史文档里的大量旧路径不会自动更新。
查文件时以本表为准，**不要**再去旧路径找。

**迁移原则**

1. 分析流水线（`00_db`–`13_calibration`）**一律不动**——数据按阶段编号流转，按论文拆会破坏流程与脚本。
2. 只重排"面向论文"的文档层：`11_proposal/`、`10_reports/` 与根目录散落文件。
3. 全部用 `git mv`，历史可追、可整体回滚。
4. 生成脚本的路径解析已从 `parents[N]` 改为按 `.git` 定位仓库根，**层次再变也不会静默读错**；
   迁移后 Table 1、Table 2、图注三个 Word 生成器均已复跑通过。

---

## 一、目录级

| 旧路径 | 新路径 |
|---|---|
| `11_proposal/manuscript/` | `11_proposal/MS01/manuscript/` |
| `11_proposal/table1/` | `11_proposal/MS01/tables/table1/` |
| `11_proposal/table2/` | `11_proposal/MS01/tables/table2/` |
| `11_proposal/legends/` | `11_proposal/MS01/legends/` |
| `11_proposal/references/` | `11_proposal/MS01/references/` |
| `10_reports/`（MS-01 相关） | `10_reports/MS01/` |
| `10_reports/`（CR-01 相关） | `10_reports/CR01/` |
| `10_reports/`（跨线） | `10_reports/_shared/` |

**保持不动的目录**：`00_db`、`03_assembly`、`04_viral`、`05_c_stage`、`05_mag`、`06_crispr`、`06_host`、
`07_cargo`、`07_mag`、`07_network`、`08_figures`、`09_tables`、`12_second_dataset`、`13_calibration`、
`14_library`、`workflow`。

## 二、单文件（共 57 条，按新路径排序）

| # | 旧路径 | 新路径 |
|---|---|---|
| 1 | `10_reports/CRISPR携带率_44MAGs_2026-11-15.md` | `10_reports/CR01/CRISPR携带率_44MAGs_2026-11-15.md` |
| 2 | `10_reports/为什么不大行_核心论证_2026-11-16.md` | `10_reports/CR01/为什么不大行_核心论证_2026-11-16.md` |
| 3 | `10_reports/打包说明_CRISPR录制包_2026-11-15.md` | `10_reports/CR01/打包说明_CRISPR录制包_2026-11-15.md` |
| 4 | `10_reports/文献地图_CRISPR记录与病毒发现_2026-11-14.md` | `10_reports/CR01/文献地图_CRISPR记录与病毒发现_2026-11-14.md` |
| 5 | `10_reports/结案报告_工程菌诱饵方案_2026-11-14.md` | `10_reports/CR01/结案报告_工程菌诱饵方案_2026-11-14.md` |
| 6 | `10_reports/评审意见_CRISPR录制包_2026-11-16.md` | `10_reports/CR01/评审意见_CRISPR录制包_2026-11-16.md` |
| 7 | `phrog_library_report.md` | `10_reports/MS01/phrog_library_report.md` |
| 8 | `10_reports/五口径定义对齐与修正_2026-11-12.md` | `10_reports/MS01/五口径定义对齐与修正_2026-11-12.md` |
| 9 | `10_reports/修改意见_FigA0与五口径修正_2026-11-12.md` | `10_reports/MS01/修改意见_FigA0与五口径修正_2026-11-12.md` |
| 10 | `10_reports/技术报告_病毒占比口径与7倍差异定位_2026-11-12.md` | `10_reports/MS01/技术报告_病毒占比口径与7倍差异定位_2026-11-12.md` |
| 11 | `10_reports/文献扫描_预印本_2026-11-12.md` | `10_reports/MS01/文献扫描_预印本_2026-11-12.md` |
| 12 | `10_reports/评审意见_spike校准42倍归因_2026-11-16.md` | `10_reports/MS01/评审意见_spike校准42倍归因_2026-11-16.md` |
| 13 | `10_reports/评审意见_五口径定义对齐_2026-11-12.md` | `10_reports/MS01/评审意见_五口径定义对齐_2026-11-12.md` |
| 14 | `10_reports/c_stage_summary_2026-11-08.md` | `10_reports/_shared/c_stage_summary_2026-11-08.md` |
| 15 | `10_reports/literature_check_2026-11-10.md` | `10_reports/_shared/literature_check_2026-11-10.md` |
| 16 | `10_reports/mag_2026-11-09.md` | `10_reports/_shared/mag_2026-11-09.md` |
| 17 | `10_reports/prophage_cargo_2026-11-09.md` | `10_reports/_shared/prophage_cargo_2026-11-09.md` |
| 18 | `10_reports/viral_signal_validation_2026-11-08.md` | `10_reports/_shared/viral_signal_validation_2026-11-08.md` |
| 19 | `10_reports/可行性分析_论文方向_2026-11-14.md` | `10_reports/_shared/可行性分析_论文方向_2026-11-14.md` |
| 20 | `10_reports/技术简报_扬子鳄肠道病毒组_2026-11-09.docx` | `10_reports/_shared/技术简报_扬子鳄肠道病毒组_2026-11-09.docx` |
| 21 | `10_reports/技术简报_扬子鳄肠道病毒组_2026-11-09.md` | `10_reports/_shared/技术简报_扬子鳄肠道病毒组_2026-11-09.md` |
| 22 | `10_reports/技术简报_扬子鳄肠道病毒组_2026-11-09.pdf` | `10_reports/_shared/技术简报_扬子鳄肠道病毒组_2026-11-09.pdf` |
| 23 | `10_reports/文献核查记录_2026-11-14.md` | `10_reports/_shared/文献核查记录_2026-11-14.md` |
| 24 | `10_reports/结论汇总_2026-11-09.md` | `10_reports/_shared/结论汇总_2026-11-09.md` |
| 25 | `11_proposal/项目启动提纲_幼鳄死因归因_2026-11-10.md` | `11_proposal/AR01/项目启动提纲_幼鳄死因归因_2026-11-10.md` |
| 26 | `11_proposal/transcript2.txt` | `11_proposal/CR01/evidence/transcript2.txt` |
| 27 | `11_proposal/§2支撑_分辨力核查_2026-11-16.md` | `11_proposal/CR01/evidence/§2支撑_分辨力核查_2026-11-16.md` |
| 28 | `11_proposal/五层证据表_W1_2026-11-16.md` | `11_proposal/CR01/evidence/五层证据表_W1_2026-11-16.md` |
| 29 | `11_proposal/Perspective_outline_Recording_is_not_discovery_2026-11-15.md` | `11_proposal/CR01/plans/Perspective_outline_Recording_is_not_discovery_2026-11-15.md` |
| 30 | `11_proposal/生物学原理版论证框架_2026-11-16.md` | `11_proposal/CR01/plans/生物学原理版论证框架_2026-11-16.md` |
| 31 | `11_proposal/论文骨架_v2_2026-11-16.md` | `11_proposal/CR01/plans/论文骨架_v2_2026-11-16.md` |
| 32 | `11_proposal/legends/Figure_legends_2026-11-13.md` | `11_proposal/MS01/legends/Figure_legends_2026-11-13.md` |
| 33 | `11_proposal/legends/output/Figure_legends.docx` | `11_proposal/MS01/legends/output/Figure_legends.docx` |
| 34 | `11_proposal/manuscript/manuscript_v0.1_front_2026-11-13.md` | `11_proposal/MS01/manuscript/manuscript_v0.1_front_2026-11-13.md` |
| 35 | `11_proposal/manuscript/manuscript_v0.2_front_中文_2026-11-13.md` | `11_proposal/MS01/manuscript/manuscript_v0.2_front_中文_2026-11-13.md` |
| 36 | `11_proposal/改稿方案_v1_2026-11-16.md` | `11_proposal/MS01/plans/改稿方案_v1_2026-11-16.md` |
| 37 | `11_proposal/论文提纲_方法学_2026-11-10.md` | `11_proposal/MS01/plans/论文提纲_方法学_2026-11-10.md` |
| 38 | `11_proposal/论文提纲_方法学_v2_2026-11-12.md` | `11_proposal/MS01/plans/论文提纲_方法学_v2_2026-11-12.md` |
| 39 | `11_proposal/references/Microbiome_Reptile_Immune.ris` | `11_proposal/MS01/references/Microbiome_Reptile_Immune.ris` |
| 40 | `11_proposal/references/code/make_refs.py` | `11_proposal/MS01/references/code/make_refs.py` |
| 41 | `fmicb-10-02409.pdf` | `11_proposal/MS01/references/pdf/fmicb-10-02409.pdf` |
| 42 | `11_proposal/references/references_table.docx` | `11_proposal/MS01/references/references_table.docx` |
| 43 | `11_proposal/references/references_table.md` | `11_proposal/MS01/references/references_table.md` |
| 44 | `11_proposal/references/refs.ris` | `11_proposal/MS01/references/refs.ris` |
| 45 | `11_proposal/references/文献集核查_Microbiome_Reptile_Immune_2026-11-17.md` | `11_proposal/MS01/references/文献集核查_Microbiome_Reptile_Immune_2026-11-17.md` |
| 46 | `11_proposal/table1/Table1_正式稿_2026-11-13.md` | `11_proposal/MS01/tables/table1/Table1_正式稿_2026-11-13.md` |
| 47 | `11_proposal/table1/code/make_table1_docx.py` | `11_proposal/MS01/tables/table1/code/make_table1_docx.py` |
| 48 | `11_proposal/table1/output/Table1_six_definitions.docx` | `11_proposal/MS01/tables/table1/output/Table1_six_definitions.docx` |
| 49 | `11_proposal/table2/Table2_正式稿_2026-11-13.md` | `11_proposal/MS01/tables/table2/Table2_正式稿_2026-11-13.md` |
| 50 | `11_proposal/table2/code/make_table2_docx.py` | `11_proposal/MS01/tables/table2/code/make_table2_docx.py` |
| 51 | `11_proposal/table2/output/Table2_reporting_checklist.docx` | `11_proposal/MS01/tables/table2/output/Table2_reporting_checklist.docx` |
| 52 | `当前工作任务表_2026-11-05.md` | `11_proposal/_shared/当前工作任务表_2026-11-05.md` |
| 53 | `扬子鳄病毒组_PriorArt与Novelty_2026-11-07.md` | `11_proposal/_shared/扬子鳄病毒组_PriorArt与Novelty_2026-11-07.md` |
| 54 | `扬子鳄病毒组_方向备忘_2026-11-07.md` | `11_proposal/_shared/扬子鳄病毒组_方向备忘_2026-11-07.md` |
| 55 | `11_proposal/科研计划_下一步_2026-11-11.md` | `11_proposal/_shared/科研计划_下一步_2026-11-11.md` |
| 56 | `11_proposal/系统迁移操作清单_2026-11-10.md` | `11_proposal/_shared/系统迁移操作清单_2026-11-10.md` |
| 57 | `ntp_probe.py` | `workflow/ntp_probe.py` |

## 三、当前骨架

```
261105/
├── 00_db/ 03_assembly/ 04_viral/ ... 13_calibration/   分析流水线（未动）
├── 08_figures/   Fig 1–3 源码与产物
├── 09_tables/    数据表（TSV，数源）
├── 10_reports/
│   ├── MS01/     MS-01 的技术报告与评审意见
│   ├── CR01/     CR-01 的文献地图、结案报告、论证
│   ├── _shared/  跨线：测序描述、结论汇总、可行性分析
│   └── _archive/
├── 11_proposal/
│   ├── MS01/
│   │   ├── manuscript/   v0.1 / v0.2 / v0.3 EN / v0.3 中英对照
│   │   ├── tables/       table1/ table2/
│   │   ├── legends/      图注（md 单一来源 + docx）
│   │   ├── references/   RIS、参考文献表、pdf/
│   │   └── plans/        提纲 v1/v2、改稿方案
│   ├── CR01/
│   │   ├── plans/        outline、骨架 v2、生物学原理版框架
│   │   └── evidence/     五层证据表、§2支撑、transcript2
│   ├── AR01/             项目启动提纲
│   └── _shared/          科研计划、系统迁移、任务表、方向备忘、PriorArt
├── 12_second_dataset/   鸡肠道（G-A1）
├── 13_calibration/      掺入校准
├── 14_library/          旧文献库目录（仅存作废 v1）
├── 15_tickets/          工单（本机制入口）
├── workflow/            流水线脚本与工具
├── README.md
├── DATA_LOCATIONS.md
└── PATH_MAP.md          ← 本文件
```

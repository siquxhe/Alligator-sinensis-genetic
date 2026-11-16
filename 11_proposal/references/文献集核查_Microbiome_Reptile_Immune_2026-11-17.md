# 文献集核查：Microbiome_Reptile_Immune.ris

**文件** `11_proposal/references/Microbiome_Reptile_Immune.ris`
**来源** Web of Science 导出（全库记录均带 `AN  - WOS:` 编号）
**核查日期** 2026-11-17
**结论** 可用。结构完整、无重复、DOI 可解析；三处 WoS 导出习惯需知道，不影响入库。

## 一、结构核验

| 项 | 结果 |
|---|---|
| 大小 / 编码 | 338,311 B，UTF-8 无 BOM |
| 记录数 | **128**（`TY` 128 / `ER` 128 闭合） |
| 文献类型 | 全部 `JOUR`（期刊论文），无会议摘要、无书籍章节 |
| 必需字段 | `TI` `AU` `PY` `T2` `DO` **128/128 齐全**，无缺失 |
| DOI | 128 条，**128 个互不相同**，无组内重复 |
| 标题重复 | 0 |
| 年份跨度 | 2011–2026，重心在近两年（2025: 25 篇，2026: 18 篇） |
| 补充字段 | 摘要 125 篇、关键词 127 篇、WoS 编号 128 篇、全文链接 `L1` 105 篇 |
| 与 `refs.ris`（22 条）重叠 | **0** —— 与本项目既有引用库无交集，是净增 |

DOI 抽样 6 条经 Crossref 解析，全部命中且刊名、标题与条目一致：

```
10.1002/ece3.7373        Ecology and Evolution
10.1002/ece3.8904        Ecology and Evolution
10.1016/j.dci.2023.104690 Developmental & Comparative Immunology
10.1002/njz2.70015       New Zealand Journal of Zoology
10.1002/ece3.71068       Ecology and Evolution
10.1128/spectrum.00294-25 Microbiology Spectrum
```

## 二、三处 WoS 导出习惯（知悉即可，不必修）

1. **15 条摘要在源文件里跨行。** WoS 把结构化摘要（`Background:` / `Results:` / `Conclusions:`）按段落折行，折行后的文字没有 `XX  - ` 前缀，成了"无标签行"。影响范围仅限 `AB` 字段：严格按"一字段一行"解析的工具会只保留第一段。**书目信息（标题、作者、刊名、年、DOI）全部完好**，检索与引用不受影响。Zotero 这类会把无标签行并回上一字段的解析器可完整读入；若用别的工具批量处理，需按"无前缀行并入上一字段"处理。
2. **46 条 `DA` 字段尾缀 `//undefined`**（形如 `2026/08//undefined`）。这是 WoS 在缺日/期时的占位写法，`PY`（年份）字段 128 条全部规范为四位数字，因此不影响排序与引用年份。
3. **刊名全大写**（`FRONTIERS IN MICROBIOLOGY`、`ECOLOGY AND EVOLUTION`）。导入 Zotero 后会被条目样式表覆盖显示，源文件层面不必改。

## 三、内容画像

按标题+摘要的**提及**统计（一条可命中多类，非互斥分区）：

| 类群 | 提及条数 |
|---|---:|
| 哺乳类/人 | 113 |
| 爬行类 | 84 |
| 两栖类 | 26 |
| 鱼类 | 22 |
| 鸟类 | 16 |
| **鳄类**（crocodilian/alligator/caiman/gharial） | **10** |

高频关键词：diversity 46、evolution 42、gut microbiota 39、microbiome 33、conservation 17、reptile(s) 27。

刊源 67 种，前五：Frontiers in Microbiology 11、Ecology and Evolution 7、Molecular Ecology 7、PLOS ONE 6、Microbiome 6。

**含免疫相关表述（immun/innate/TLR/cytokine/inflammation/MHC/AMP）46 篇。**

## 四、这套文献能支撑什么、不能支撑什么

**能支撑**：宿主—菌群—免疫这一层的背景论述，尤其是"菌群随宿主生理状态变化""个体差异""爬行类菌群研究稀缺"三条；鳄类那 10 篇可直接用于引言的地域性/物种性铺垫。对 `11_proposal/Perspective_outline_Recording_is_not_discovery_2026-11-15.md` 的引言段够用。

**不能支撑**：**病毒组层面的任何论断**。128 条里标题含 virus/virome/phage 的只有 **2 篇**。若把这份集合当作病毒组文献基础，会在审稿时被直接指出"只引了细菌组"。病毒组那一路仍须用 `refs.ris`（22 条，含 RVDB 溯源、基准、个体特异性）。

## 五、下一步

- **导入 Zotero 请走图形界面**（文件 → 导入 → 从文件），不要用本地 API 批量写入：`IMPORTED.md` 已记录该通道条目创建会 30 秒超时。GUI 导入不经过本地 API，不受此影响。
- 导入前注意：库中已有 **43 组重复（103 条）** 未合并。这 128 条与既有库按 DOI 是否重复尚未核对（本次只核了与 `refs.ris` 的关系），建议先合并旧重复再导入，否则新重复会叠在旧重复上、更难分辨。
- 若这批文献要进「微生物组学」知识库，需要的是 PDF 而非 RIS；本文件只解决"引哪些"，不解决"有全文"。

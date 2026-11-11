# 试跑结果对应的文献核查（增量）

**日期** 2026-11-10　|　**范围** 针对本项目试跑得到的具体发现做定向检索
**配套** `扬子鳄病毒组_PriorArt与Novelty_2026-11-07.md`（面向旧方向，本文只做增量，不重复）

> **检索边界**：基于英文公开文献与摘要级检索。CNKI 全文、学位论文、会议摘要、企业内部报告未覆盖。**"未检索到"不等于"没人做"**。

---

## 0. 一句话

**"噬菌体携带抗氧化基因"这件事本身不新**（已有 196 个噬菌体基因组被报道携带锰过氧化氢酶，sodCI 更是沙门氏菌 Gifsy-2 的教科书案例）；**新的是"在鳄类肠道条件致病菌的前噬菌体上、katA 与 sodCI 共定位、且与疾病状态挂钩"这一具体组合**——而这一层，公开检索未见。

---

## 1. 按我们的四条发现逐条核查

### 发现 A｜*Aeromonas* 前噬菌体携带 katA + sodCI

| 核查项 | 结论 |
|---|---|
| 噬菌体能否携带过氧化氢酶 | **能，且不罕见**。Nature Microbiome 2021 报道 196 个噬菌体基因组携带**锰过氧化氢酶**、36 个携带 DPS 类蛋白，并明确指出"锰过氧化氢酶此前未在噬菌体基因组中被记录" |
| 噬菌体能否携带 sodCI | **能，经典案例**。沙门氏菌 Gifsy-2 前噬菌体携带 sodCI（Cu-Zn SOD），是溶源转换增强毒力的旗舰证据；sodCI 突变体在小鼠中显著减毒 |
| *Aeromonas* 的 katA/SOD 是否为毒力因子 | **是，证据很强**。*A. schubertii* 的 catalase 缺失株（Δcat）在蛇头鱼中 14 天累积死亡率从 100% 降到 **0%**；*A. salmonicida* 的 catalase 诱导后可抵抗虹鳟活化巨噬细胞杀伤 |
| *Aeromonas* 前噬菌体是否已知携带毒力基因 | **有推测，未落到具体基因**。2016 年 *A. hydrophila* 毒力因子综述引述 Hossain 等（2013）：高毒力株中前噬菌体携带的顺/反式元件高度保守，**推测溶源转换可能调控毒力差异**——但未指名 katA/sodCI，也未做功能验证 |
| **katA 与 sodCI 在同一前噬菌体上共定位** | **公开检索未见** |

**必须注意的技术点**：我们的 katA 注释最佳命中是 ***Neisseria gonorrhoeae*** 的 KatA（VFG037029），identity **43.9%**、coverage 93.7%。这属于同一蛋白家族（单功能血红素过氧化氢酶）的远缘同源，**可以写"同源/类似"，不能写"就是 katA"**。sodCI 命中沙门氏菌 Gifsy-2（54.3%/85.3%），指向性更强。

### 发现 B｜*Hafnia* 前噬菌体携带 ParE 类毒素（TA 系统）

| 核查项 | 结论 |
|---|---|
| 噬菌体携带 TA 系统 | **已知且常见**。综述明确指出前噬菌体常编码 TA 系统作为 moron，功能包括稳定溶源、抗超感染、流产感染 |
| TA 系统与溶源稳定性 | **机制清楚**：TA 使前噬菌体在宿主群体中"赖着不走"，稳定溶源是后续被诱导的前提 |
| 鳄类来源 *Hafnia* 的前噬菌体 TA | **公开检索未见** |

→ 这一条的**机制不新，物种背景新**。单例价值有限，宜作为"分布特征"的一条，而非独立卖点。

### 发现 C｜前噬菌体 cargo 中零获得性抗性基因（三重检验）

| 核查项 | 结论 |
|---|---|
| 是否与主流印象冲突 | **是**。"噬菌体是 ARG 仓库"是流行印象，但本批数据三重检验一致为 0 |
| 有无类似报道 | 有零散的"噬菌体 ARG 携带率低"报道，但**鳄类中无** |
| 价值 | 阴性结论本身稳（三重独立检验），可作为**"选择压力来自宿主免疫而非抗生素"**这一推理的支点 |

### 发现 D｜鳄类肠道病毒组本身

| 研究 | 做了什么 | 与我们的关系 |
|---|---|---|
| Tang et al. 2019（*Front Microbiol*，PRJNA539906） | 我们的数据源。16S + shotgun，比较冬眠 vs 活动期；病毒只报了一个占比（0.04 → 4.03%），全文无 phage/prophage/contig/vOTU | **测过但未刻画** |
| Harding et al. 2022（*ISME Commun*） | 两栖爬行动物病毒组，含扬子鳄**肾脏**数据集中狂犬病毒样序列 | 组织病毒组，非肠道 |
| Castelli et al. 2025（*Front Microbiol*） | 奥里诺科鳄口腔/泄殖腔菌群，**16S**，关注 *Helicobacter* | 细菌层，非病毒组 |
| Marsh crocodile（*C. palustris*）粪便 | One Codex 群落描述，含病毒但仅到门/属计数 | 描述性，无病毒基因组 |
| Keenan 2013；Perez-Marron 2022 | 美洲短吻鳄肠道/口腔细菌 microbiome、ARG 储库 | 细菌层 |

→ **鳄类肠道 shotgun 病毒组（vOTU、病毒基因组、宿主、前噬菌体 cargo）在公开检索中仍是空白。**

---

## 2. 三层判断

| 层级 | 内容 | 可否写入材料 |
|---|---|---|
| **已被做过** | 噬菌体携带 Mn-过氧化氢酶（196 例）；Gifsy-2 sodCI；*Aeromonas* catalase 是毒力因子；噬菌体编码 TA 系统 | 只能作为**背景与机制先例**引用 |
| **被推测但未做实** | *A. hydrophila* 高毒力株前噬菌体保守 → 溶源转换或调控毒力（Hossain 2013） | 可作为**"前人指出了方向但没落地"**的缺口陈述 |
| **公开检索未见** | ① 鳄类肠道病毒组系统刻画；② *Aeromonas* 前噬菌体携带 katA+sodCI 共定位；③ 鳄类病原前噬菌体与疾病状态的关联；④ 鳄类前噬菌体 cargo 的 ARG 阴性结论 | **novelty 的落点** |

---

## 3. 对表述的三条约束

1. **不能写"首次发现噬菌体携带抗氧化基因"**——锰过氧化氢酶已有 196 例、sodCI 是教科书案例。正确写法是"**首次在鳄类肠道条件致病菌的前噬菌体中观察到 katA 与 sodCI 共定位**"。
2. **不能把 katA 写成确证**——43.9% identity 属远缘同源，须标注 identity/coverage，并用"同源"而非"即"。
3. **不能把"噬菌体携带毒力基因"当新概念**——*Aeromonas* 领域 2013 年就有人提出溶源转换调控毒力的推测，我们的增量是**具体基因 + 鳄类背景 + 疾病关联**，不是概念本身。

---

## 4. 检索式（便于更新）

```
crocodilian gut virome / crocodile phageome
Alligator sinensis virome prophage
Aeromonas prophage catalase / superoxide dismutase
phage encoded catalase KatA moron
Gifsy-2 sodCI lysogenic conversion
prophage toxin-antitoxin ParE lysogeny stabilization
Aeromonas hydrophila prophage virulence lysogenic conversion
reptile gut virome metagenome
```

---

## 5. 参考文献（均可核验）

1. Nayfach S, et al. Metagenomic compendium of 189,680 DNA viruses from the human gut microbiome. *Nat Microbiol* 2021. （含 196 个噬菌体基因组携带锰过氧化氢酶的报道）https://microbiomejournal.biomedcentral.com/articles/10.1186/s40168-021-01017-w
2. Figueroa-Bossi N, Bossi L. Inducible prophages of *Salmonella*. *Mol Microbiol* 1999；Ho TD, Slauch JM. 相关后续工作。
3. "Virulent *Salmonella typhimurium* has two periplasmic Cu,Zn-superoxide dismutases"（sodCI 由前噬菌体携带）https://pmc.ncbi.nlm.nih.gov/articles/pmid/10377444/
4. Jiang M, et al. Catalase is a critical virulence factor in *Aeromonas schubertii* infection of snakehead fish. （Δcat 死亡率 100% → 0%）
5. "Peroxide-inducible catalase in *Aeromonas salmonicida* protects against killing by activated rainbow trout macrophages" https://www.sciencedirect.com/science/article/pii/S0882401098902601
6. "Virulence Factors of *Aeromonas hydrophila*: In the Wake of Reclassification". *Front Microbiol* 2016.（引述 Hossain 2013 关于前噬菌体与溶源转换的推测）https://pmc.ncbi.nlm.nih.gov/articles/PMC4997093/
7. Wang Y, et al. Biologic and genomic characterization of a novel virulent *Aeromonas hydrophila* phage phiA051, with high homology to prophages. *Front Vet Sci* 2024. https://pubmed.ncbi.nlm.nih.gov/39091387/
8. Tang K-Y, et al. Metagenomics Reveals Seasonal Functional Adaptation of the Gut Microbiome to Host Feeding and Fasting in the Chinese Alligator. *Front Microbiol* 2019;10:2409. https://doi.org/10.3389/fmicb.2019.02409
9. Harding EF, et al. Revealing the uncharacterised diversity of amphibian and reptile viruses. *ISME Commun* 2022;2:95. https://pmc.ncbi.nlm.nih.gov/articles/PMC9723728/
10. Castelli L, et al. Microbial diversity in the critically endangered Orinoco crocodile: influence of body site and *Helicobacter* spp. *Front Microbiol* 2025;16:1697111. https://europepmc.org/articles/PMC12679878
11. "Microbial Arsenal of Antiviral Defenses. Part II"（前噬菌体编码 TA 系统作为 moron）https://link.springer.com/10.1134/S0006297921040064
12. Keenan SW, et al. The alligator gut microbiome and implications for archosaur symbioses. *Sci Rep* 2013;3:2877.

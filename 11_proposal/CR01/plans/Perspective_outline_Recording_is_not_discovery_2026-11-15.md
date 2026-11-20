# Perspective 起草包：*Recording is not discovery*

**日期** 2026-11-15
**类型** Perspective / Opinion（目标 4,000 词，4 图，1 表，~60 refs）
**目标期刊** *Trends in Microbiology* (Opinion) → *CRISPR Journal* (Perspective) → *mSystems* (Perspective) → *BioEssays* (Prospects) → *Frontiers in Microbiology* (Perspective)
**核心文献底图** `10_reports/CR01/文献地图_CRISPR记录与病毒发现_2026-11-14.md`

> **2026-11-20 准据指针（取代 11-16 的旧指针）**
>
> 论证主线以 **`论文骨架_v2_2026-11-16.md`** 为准，三条界线：
> ①spacer 是索引不是证据 ②产出形态不可回溯 ③检出下限是三项乘积（`n × v × i·s·q`）。
>
> `生物学原理版论证框架_2026-11-16.md` 已**降级为支撑层**——五层只作机制解释，不得当骨架用
> （理由见工单 §五风险表第一条：五层每一层都能被"我优化一下"回应，退回五层等于重开这个口子）。
>
> 本 outline 的 §2（检测模型）对应骨架 §4；§3（七条偏差）已被骨架 §5 取代。
> §1（问题错位）、§4（窄场景）、§5（报告标准）、文献底图与投稿策略仍然有效。

---

## 0. 一句话论点

**CRISPR spacer recording 能记录“某个已知受体介导的注入事件”，但不能无偏地发现环境病毒；把两者混为一谈，是当前领域一个未经验证的假设。**

---

## 1. 200 词 presubmission（可直接发编辑）

> **Proposed Perspective: Recording is not discovery — bounding the use of CRISPR spacer recorders for virus surveillance**
>
> CRISPR spacer acquisition has been engineered into a molecular recorder, and engineered bacteria expressing heterologous phage receptors have been proposed as “bait” to detect viruses by sequencing the spacers acquired after infection. We argue that this proposal conflates molecular recording with virus discovery. Using a simple detection model parameterized with published data, we show that the probability of recording a virus is the product of receptor coverage, injection efficiency, survival/spacer acquisition, and database matching. Under optimistic assumptions, the detection floor is ~10⁵ particles/mL; under realistic assumptions for unknown viruses, it exceeds 10⁸ particles/mL, above the abundance of most environmental targets. We do not claim that receptor baiting or spacer-based virus detection is new—both have precedent. We provide, to our knowledge, the first systematic boundary analysis of their combination, a decision framework that distinguishes targeted recording from unbiased discovery, and a reporting checklist for future recording studies. The perspective will interest virologists, microbiome researchers, synthetic biologists, and environmental surveillance programs, and will help prevent overinterpretation of recording signals.

**字数** 约 190 词。**卖点** 不是“新方法”，是“边界 + 决策框架 + 报告标准”。

---

## 2. 一页 outline

### Title

**Recording is not discovery: a boundary analysis of CRISPR spacer recording for virus surveillance**

备选：
- *What CRISPR spacer recorders can and cannot tell us about viruses*
- *Beyond the bait: a decision framework for virus discovery and targeted recording*

### Abstract（150–200 词，投稿时再压缩）

> **⚠ 以下为 2026-11-15 旧版草稿**：写于三条界线与 Fig 2 之前，落点是"bias structure（受体特异性、裂解/温和选择、anti-CRISPR…）"，与现行骨架不是同一篇文章。
> **仅供语感参考，不可直接使用**。现行摘要口径见骨架 §六与 `CR01_系统检索记录`。

CRISPR spacer acquisition is a natural memory of viral infection and has been engineered into a molecular recorder. A recent proposal combines engineered bacteria expressing heterologous phage receptors (“bait”) with spacer sequencing to identify viruses in environmental samples. We show that this application conflates recording with discovery. We develop a simple detection model in which the per-phage recording probability is the product of receptor coverage, injection efficiency, survival/spacer acquisition, and database matching. Parameterized with published data, the model predicts that the detection floor ranges from ~10⁵ particles/mL under optimistic assumptions to >10⁸ particles/mL for unknown viruses under realistic assumptions—above the abundance of most environmental targets. We identify the bias structure (receptor specificity, lytic/temperate selection, anti-CRISPR, spacer length, database completeness) and propose a decision framework that separates targeted recording from unbiased discovery. We also provide a reporting checklist (LOD, spike-in, controls, Acr status, bias, database version). Our analysis does not argue that recording is useless; it defines when recording is the right tool and when metagenomics, viral tagging, or receptor biosensors are better.

### 1. The proposal and the conflation（~600 词）

- **1.1 What was proposed**：工程菌表面表达异源受体 → 噬菌体注入 → Cas1-Cas2 记录 spacer → 测序读出“哪些病毒来过”。
- **1.2 Two different questions**：
  - Discovery：环境里有哪些病毒？（无偏、未知、定量）
  - Targeted recording：某受体是否介导了注入？（靶向、已知、定性）
  - 原设想把两者混为一谈。
- **1.3 Three assertions**：
  - A. 工程：异源受体可让噬菌体吸附/注入（部分成立，依受体类型）。
  - B. 记录：注入 DNA 可被记成 spacer（成立，但依系统/感染结局）。
  - C. 应用：因此可用于环境病毒发现（不成立）。
- **1.4 Prior art（必须引用，避免 novelty 碰撞）**：
  - Zeng & Salmond 2020：异源受体诱饵已用于环境噬菌体富集（培养/噬菌斑读出）。
  - Snyder et al. 2010：环境 spacer 微阵列已用于病毒检测，且已报告低丰度/不可定量/需已知库等限制。
  - Munck et al. 2020（EcRec）：CRISPR 记录 HGT，1 donor/10⁶。
  - Olivenza et al. 2020：opvAB 生物传感器检测噬菌体并区分受体。
- **1.5 The gap**：组合 + 边界 + 决策框架，三件事都没人做。

### 2. A detection model（~900 词）

- **2.1 Definitions**：
  - \(V\)：噬菌体浓度（particles/mL）
  - \(v\)：处理体积（mL）
  - \(r\)：受体覆盖（使用该受体的噬菌体比例）
  - \(i\)：结合后注入概率
  - \(s\)：感染后存活并获取可检出 spacer 的概率
  - \(q\)：spacer 能匹配数据库/组装的概率
- **2.2 Equations**：
  - 每噬菌体记录概率 \(P = r \times i \times s \times q\)
  - 期望事件数 \(E = V \times v \times P\)（当 \(V \times v \ll N_c\)）
  - 检出下限 \(V_{min} = 1/(v \times P)\)（E=1）
  - 更一般：\(E = N_c \times M \times P\)，\(M\) = MOI
- **2.3 Parameter table**：见第 3 节。
- **2.4 Sensitivity**：Panel A 画 \(V_{min}\) 对受体数 \(n\)（\(r = n \times 0.09\%\)）在固定 \(v=1\) mL、基线 \(i,s,q\) 下；known 与 unknown 各一条（q=0.1 / 0.01）。Panel B 画 \(n \times s\) 热图（known），说明获取效率如何整体平移包络。合取关系（\(n \times v \times i·s·q\)）由 Supplementary 表承担。现成图：`08_figures/fig_c2/`。
- **2.5 Sanity checks**：
  - EcRec 1/10⁶ 是供体细胞锚点，不是噬菌体 LOD。
  - Modell 2017 / Keith 2025：记录偏向早期注入区/温和噬菌体。
  - Snyder 2010：环境 spacer 检测的低丰度/不可定量限制。
- **2.6 Result**：乐观 ~10⁵ particles/mL；现实 unknown >10⁸ particles/mL；多数环境目标低于检出下限。结论不是“绝对不行”，是“只在很窄的参数区间可行”。

### 3. The bias structure（~800 词）

- **3.1 Receptor coverage**：只看到使用表达受体的噬菌体；未知受体是鸡生蛋问题。
- **3.2 Injection/permissive state**：结合 ≠ 注入；TonB、膜电位、共受体、许可状态。
- **3.3 Survival/temperate bias**：烈性噬菌体裂解记录细胞；Keith 2025 证明溶原提高获取；记录高估温和/休眠噬菌体、低估烈性噬菌体。
- **3.4 Anti-CRISPR**：抗获取 Acr（如截短 AcrIIA6、AcrVA5）系统性漏检。
- **3.5 Spacer length/database**：30–40 bp；可匹配少数派；Snyder 2010 ~28%；Shang 2025 预测率 <5%。
- **3.6 Array capacity/competition**：阵列有限；多次感染竞争；不是定量。
- **3.7 GMO/containment**：体外 BSL-2；不向保护动物释放；原位监测受限。

### 4. When recording is the right tool（~700 词）

- **4.1 Decision tree**：
  1. 需要无偏发现未知病毒？→ 宏基因组/宏病毒组。
  2. 已知受体–噬菌体组合，只需证明注入？→ recording / viral tagging。
  3. 宿主不可培养？→ recording / Hi-C。
  4. 只需受体分型？→ opvAB 类生物传感器（更简单）。
  5. 需要时间维度？→ recording（但仍是群体水平）。
  6. 需要定量/感染性？→ 噬菌斑/qPCR。
- **4.2 Four narrow use cases**：
  - 受体分型（已知受体库）。
  - 不可培养宿主的功能宿主。
  - 非裂解/温和噬菌体的注入检测。
  - 受控体系内的时序记录。
- **4.3 What would change the conclusion**：
  - 获取效率/灵敏度提高 2–3 个数量级；
  - 广谱受体库（r 提高到 0.1）；
  - 数据库/组装覆盖提高（q 提高到 0.9）；
  - 非 GMO 记录系统；
  - 单细胞/单颗粒读出。

### 5. Reporting standards（~500 词）

Checklist：
1. 受体身份与覆盖（r 的估计）。
2. LOD：spike-in 已知噬菌体，报告 particles/mL。
3. 对照：Δcas1/Δcas2、热灭活、DNase、无受体、非诱导。
4. Acr 状态：目标噬菌体是否携带抗获取 Acr。
5. 幸存者/温和偏倚：报告裂解 vs 溶原、采样时间。
6. 阵列容量/竞争：报告阵列长度、扩展比例。
7. 数据库版本/匹配阈值：报告 spacer 匹配的参数。
8. 原始数据/代码：公开阵列与模型代码。

### Boxes

- **Box 1**：Three assertions（A/B/C）。
- **Box 2**：What would change our mind。

### Figures / Table

- **Fig 1**：Recording vs discovery 概念图（两个问题、两个读出）。
- **Fig 2**：Detection envelope 热图（\(V_{min}\) vs \(r\)、\(s\)；known vs unknown）。
- **Fig 3**：Bias decomposition 漏斗（受体不匹配 → 不注入 → 裂解/Acr → 数据库不匹配）。
- **Fig 4**：Decision tree。
- **Table 1**：Method comparison（metagenomics / viral tagging / phageFISH / Hi-C / epicPCR / receptor biosensor / engineered recording）。

---

## 3. 模型参数表（order-of-magnitude，非实测）

> **重要**：下表是**情景参数**，不是测量值；论文必须做敏感性分析，不能把某一组数字写成“事实”。所有参数都要在 Methods/Supplementary 里给出处与假设。

| 符号 | 含义 | 乐观（known） | 现实（known） | 现实（unknown） | 悲观（unknown） | 出处/备注 |
|---|---|---|---|---|---|---|
| \(r\) | 使用表达受体的噬菌体比例 | 0.01（1%） | 0.001（0.1%） | 0.001（0.1%） | 0.0001（0.01%） | **分解**：`r ≈ n × 0.09%`（Zeng & Salmond 2020，1100 个噬菌体中 1 个）。1% 需 11 个功能受体，3% 需 33 个 |
| \(i\) | 结合后成功注入概率 | 0.5 | 0.1 | 0.1 | 0.01 | 噬菌体生物学；FhuA/TonB 依赖因噬菌体而异 |
| \(s\) | 感染后存活并获取可检出 spacer 的概率 | 10⁻³ | 10⁻⁴ | 10⁻⁴ | 10⁻⁶ | EcRec 1/10⁶ 作为悲观锚点（供体细胞，非噬菌体）；Keith 2025 溶原提高获取 |
| \(q\) | spacer 能匹配数据库/组装的概率 | 0.5 | 0.1 | 0.01 | 0.01 | Snyder 2010 ~28% 探针；Shang 2025 预测率 <5% |
| \(P\) | 每噬菌体记录概率 \(r \times i \times s \times q\) | 2.5×10⁻⁶ | 1×10⁻⁹ | 1×10⁻¹⁰ | 1×10⁻¹⁴ | 计算值 |
| \(V_{min}\) | 1 mL 样本、E=1 的检出下限（particles/mL） | 4×10⁵ | 1×10⁹ | 1×10¹⁰ | 1×10¹⁴ | \(1/P\) |

**说明**：
- \(s=10^{-6}\) 来自 EcRec 的“1 donor/10⁶ recording cells”，但这是**供体细胞**锚点，不是噬菌体感染；只用作悲观下界。
- \(q\) 对 known vs unknown 差别很大：unknown 病毒的 30–40 bp spacer 可能无法组装/分类，\(q\) 取 0.01 或更低。
- \(V\) 的典型环境范围：10⁴–10¹⁰ particles/mL（按样本类型变化）；论文的 x 轴应覆盖这个范围。
- \(v\) 可取 1–100 mL；\(V_{min}\) 随 \(v\) 反比下降。

### 3.1 计算示例

- 乐观（known）：\(P = 0.01 \times 0.5 \times 10^{-3} \times 0.5 = 2.5 \times 10^{-6}\)；1 mL 的 \(V_{min} = 4 \times 10^5\) particles/mL。
- 现实（known）：\(P = 0.001 \times 0.1 \times 10^{-4} \times 0.1 = 1 \times 10^{-9}\)；\(V_{min} = 1 \times 10^9\) particles/mL。
- 现实（unknown）：\(P = 0.001 \times 0.1 \times 10^{-4} \times 0.01 = 1 \times 10^{-10}\)；\(V_{min} = 1 \times 10^{10}\) particles/mL。
- 悲观（unknown）：\(P = 10^{-4} \times 10^{-2} \times 10^{-6} \times 10^{-2} = 10^{-14}\)；\(V_{min} = 10^{14}\) particles/mL。

**论文的结论句式**：

> **The detection floor is the product of three terms that cannot substitute for one another**: receptor coverage (`r = n × 0.09%`), sample volume (`v`), and infection-to-detectable-spacer efficiency (`i·s·q`). At the realistic engineered corner (n = 30, v = 1 mL, baseline `i·s·q`), the floor is 3.7 × 10⁷ particles/mL (known) and 3.7 × 10⁸ (unknown). Each term must move about 3.7 × 10³-fold on its own to reach the low-abundance end; only when all three are pushed to their optimistic ends does the floor fall to 10³. **Any one term reverting to baseline returns the floor above 10⁵.** The method is therefore usable in the high-abundance tail of environmental samples, and in targeted, known-receptor questions—not for unbiased discovery.

**三项分解（2026-11-20 补，替换原"上界被工程钉住"的说法）**

| 可调项 | 锚点 | 独自达标所需 | 现实性 |
|---|---|---|---|
| 受体数 `n` | 30 | 1.1×10⁵ 个 | 无此可能 |
| 处理体积 `v` | 1 mL | 3.7 L | 水样勉强，肠道/组织不可能 |
| `i·s·q` | 10⁻⁶ | 3.7×10⁻³（3700×） | 三项全乐观也只有 2.5×10⁻⁴ |

**`n = 33` 是覆盖率等值点，不是检出边界。** 33 个受体让 `r` 追平宏基因组的 3%，但那一行的 `V_min` 仍是 3.7×10⁷——只覆盖环境丰度带的高端。把"33 个受体 = 工程边界"当主要论据，等于承认"再努力一点可能做到"；真正的边界在 10⁵ 个受体与 3.7 L 样本。计算与合取表见 `08_figures/fig_c2/`。

### 3.2 模型假设（必须写进 Methods/Supplementary）

1. 噬菌体与记录细胞充分混合；\(V \times v \ll N_c\)。
2. 每个噬菌体最多感染一个细胞；多次感染不改变数量级。
3. \(r, i, s, q\) 相互独立；实际可能有相关性（如受体覆盖高的噬菌体也更容易培养）。
4. 记录事件可被测序检出；阵列容量/竞争未单独建模。
5. 参数是 order-of-magnitude，不是精确测量。

---

## 4. 论文的“新意”边界（写作时必须守住）

### 可以写

- 首次**系统分析**“异源受体诱饵 + CRISPR spacer 读出”的组合边界。
- 首次给出**定量检测包络**（\(r \times i \times s \times q\)）和**决策框架**。
- 首次提出针对 recording-for-discovery 的**报告标准**。

### 不能写

- “首次提出工程菌诱饵”（Zeng & Salmond 2020 已做）。
- “首次用 spacer 检测环境病毒”（Snyder 2010 已做）。
- “国内外空白”（未做系统检索）。
- “spacer 获取需要活跃细胞分裂”（过度概括；系统依赖）。
- “EcRec 灵敏度是 1/10”（错误；是 1/10⁶）。
- “温和噬菌体也能记录，所以没有幸存者偏差”（正好相反：记录偏向温和噬菌体）。

---

## 5. 目标期刊与投稿策略

| 顺序 | 期刊 | 栏目 | 字数 | 备注 |
|---|---|---|---|---|
| 1 | *Trends in Microbiology* | Opinion | 3,000–4,000 | 先发 presubmission inquiry；竞争高 |
| 2 | *CRISPR Journal* | Perspective | 4,000–6,000 | 最匹配；订阅制，无强制 APC |
| 3 | *mSystems* | Perspective | ~5,000 | ASM；开放获取，有 APC |
| 4 | *BioEssays* | Prospects | 3,000–5,000 | 概念型 |
| 5 | *Frontiers in Microbiology* | Perspective | ~4,000 | 保底；APC 先问 |

**Presubmission 策略**：先发 *Trends* 的 200 词 inquiry + Fig 1 草图；若 2 周无正面回复，转 *CRISPR Journal*。不要同时投多家。

---

## 6. 4 周写作计划

| 周 | 任务 | 产出 |
|---|---|---|
| W1 | 系统检索 + 引文追踪；确认无同类 Perspective；核对 B 级数字 | PRISMA 表 + 证据表 v2 |
| W2 | 模型 + 敏感性分析 + Fig 2/3 | 模型代码 + 图 |
| W3 | 写正文 1–5 节；Fig 1/4 + Table 1 | 初稿 |
| W4 | 内部评审、润色、presubmission/投稿 | 投稿版 |

---

## 7. 下一步（今天就能做）

1. 把这份 outline 发给潘老师/合作者，确认“gap 是否值得写”。
2. 跑 44 MAGs 的 CRISPR 携带率：脚本已写好 `workflow/crispr_carriage.py`；在服务器上按 `10_reports/CR01/CRISPR携带率_44MAGs_2026-11-15.md` 的命令运行。
3. 确认目标期刊的 presubmission 要求（字数、图数、参考文献格式）。
4. 决定是否把“模型代码”放 Zenodo/GitHub。

---

## 8. 一句话

**论文不是“我们试了不行”，而是“这个组合的检测包络有多窄、什么时候值得用”。** 这句话决定了标题、摘要、图和审稿人的第一印象。

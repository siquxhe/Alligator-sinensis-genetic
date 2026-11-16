# PHROG 带注释蛋白库重建与类别筛选轴标定 — 执行结果

服务器：192.168.71.177（wuyanching）｜执行时间：2026-11-16 07:00–07:10
查询集：`/mnt/work/chicken/refcheck/sub.fq`（2,500,000 条 R1，125 bp）
工具：diamond 2.0.4 / seqkit / python3（`$HOME/biotools/envs/virome/bin`）

---

## 1. 下载结果

| 项目 | 状态 | 大小 | MD5 |
|---|---|---|---|
| `FAA_phrog.tar.gz` | 源 1（Zenodo）成功 | 55,485,003 B | `dd90a0d1…2bb5` ✔ 与官方一致 |
| `phrog_annot_v4.tsv` | 重下成功 | 3,831,481 B | `3f078c58…9a44` ✔ 与官方一致 |

**重要发现（与原认知不同）**

1. 昨晚的 55,485,003 B 并非"未下完"，而是**尺寸已达全文、内容已损坏**。Zenodo 返回的 `content-length`
   恰为 55,485,003，服务器未声明 `Accept-Ranges`，`curl -C -` 的续传写入发生重叠，
   导致本地 MD5 `5a5ae665…d607` ≠ 官方值。`tar tzf` 报 `invalid compressed data--format violated`，
   仅能读出 10,286 / 38,880 个 .faa。**结论：该源不能续传，只能整包重下。**本机已保留 `FAA_phrog.tar.gz.corrupt`。
2. 注释表 `phrog_annot_v4.tsv` 同样是截断文件：本地 2,303,496 B / 64,811 行，末行为 `64811\t#c9c9`（断在半途）；
   官方为 3,831,481 B / **109,404 行**（phrog 1…109,404）。MD5 不符。已重下修复。
   **原"64,811 行已完整"的判断不成立。**
3. 该 Zenodo 记录（Achilles Database v1.0）只有 4 个文件，无其他更完整的 FAA 版本：
   `FAA_phrog.tar.gz` / `HMM_phrog.tar.gz`（131 MB）/ `phrog_annot_v4.tsv` / `MSA_phrogs.tar.gz`。

**实际库内容（与预期的 >60,000 个文件不符）**

- `FAA_phrog/` 共 **38,880** 个 .faa，合计 **868,340** 条蛋白序列（253 MB），序列头形如 `>phrog_1 ## p428256 VI_04636`。
- 38,880 个 phrog ID 在注释表中 **100% 有对应行**；但其中 **33,747（86.8%）为 `unknown function`**，
  仅 **5,133（13.2%）** 具备功能类别。这是本次结果解读的核心约束。

## 2. 建库与比对

| 步骤 | 结果 |
|---|---|
| 合并 | `phrog_all.faa`，868,340 条序列，253 MB |
| 建库 | `diamond makedb -d phrog`，868,340 seqs / 193,422,455 letters，267 MB，1.5 s |
| 比对 | `diamond blastx --evalue 1e-5 --outfmt 6 qseqid stitle pident length --max-target-seqs 1 --threads 8` |
| 原始命中 | 146,873 行 |
| 过滤后（pident≥40 且 length≥30，reads 级去重） | **144,750** reads |

**流程可信性校验**

- 同参数复算两个既有基线：RVDB 旧库 `0.839%`（20,974 reads）、自建无注释库 `3.929%`（98,222 reads）——与记录值**完全一致**。
- 子集一致性：前 200,000 reads 单独重跑得 5.761%，全量结果在该子集内为 5.760%，重叠 11,519/11,521
  （2 条差异来自多线程并列打分的择优抖动）。

## 3. 类别统计（reads 级，分母 2,500,000）

| 类别 | reads | 占全部 reads | 占命中 |
|---|---|---|---|
| **总病毒样** | 144,750 | **5.790%** | 100% |
| structural | 7,461 | **0.298%** | 5.15% |
| replication | 20,540 | **0.822%** | 14.19% |
| other | 116,749 | **4.670%** | 80.66% |
| strict（structural+replication） | 28,001 | **1.120%** | 19.34% |

structural = head and packaging + tail + connector + virion；replication = DNA, RNA and nucleotide metabolism + transcription regulation。

类别明细（占命中比）：unknown function 55.22%、DNA/RNA/核苷酸代谢 12.87%、other 10.57%、
moron/AMG 10.37%、integration and excision 4.03%、head and packaging 2.89%、tail 2.04%、
transcription regulation 1.32%、lysis 0.47%、connector 0.23%。

## 4. 与基线对比

| 库 | 占比 | 相对 RVDB 旧库 | 相对自建无注释库 |
|---|---|---|---|
| RVDB v32（旧） | 0.839% | 1.00× | — |
| 自建 vOTU 无注释 | 3.929% | 4.68× | 1.00× |
| **PHROG v4 带注释** | **5.790%** | **6.90×** | **1.47×** |

## 5. 对 C1/C2 = 7.1× 的回答

**严格类别筛选占比仍显著低于总占比 —— 方向成立，但倍数不是 7.1×，而是 5.17×。**

- 总占比 5.790% ÷ strict 1.120% = **5.17×**
- 倍数对"严格"的定义高度敏感：
  - 仅 replication 单轴：5.790 / 0.822 = **7.05×**（≈ 原 7.1）
  - structural + replication 双轴：**5.17×**
  - 仅 structural 单轴：5.790 / 0.298 = **19.40×**

即：原 7.1× 只有在"严格 = 仅复制/转录类"的口径下才复现；若按 structural+replication 双轴口径，
应修正为 **5.17×**。无论哪种口径，"严格筛选后的占比远低于总病毒样占比"这一结论都稳健成立。

## 6. 需要带进结论的两个限制

1. **注释稀疏主导一切**：库中 86.8% 的蛋白无功能注释，命中里 55.22% 落在 unknown function，
   80.66% 被判入 other。所谓"严格类别筛选"实际是在 13.2% 有注释的子集上做判断，
   它度量的是**功能可归属比例**，不能当作病毒真实丰度使用。
2. **库规模小于预期**：38,880 个 phrog（868,340 序列）覆盖注释表 109,404 个 ID 的 35.5%。
   若后续需要全库，只能另寻 HMM/MSA 文件或与其他版本合并，单纯重下不会得到更多 .faa。

## 7. 产物路径

- `db/phrog/phrog_all.faa`、`db/phrog/phrog.dmnd`（267 MB）
- `db/phrog/FAA_phrog/`（38,880 个 .faa）
- `refcheck/phrog.hits.tsv`（9.3 MB）、`refcheck/phrog_check.sh`、`refcheck/phrog_classify.py`
- `refcheck/phrog_summary.tsv`（本报告全部数值的机器可读版）
- 损坏原件备份：`db/phrog/FAA_phrog.tar.gz.corrupt`、`db/phrog/phrog_annot_v4.tsv.corrupt`

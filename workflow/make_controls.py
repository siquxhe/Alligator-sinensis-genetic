#!/usr/bin/env python3
"""为病毒信号交叉验证准备对照数据集

生成三样东西：
  1) q_real.fa          —— 从 S1 去宿主 R1 抽取的真实 reads（固定 400 万条）
  2) q_shuf.fa          —— 同一条 reads 的随机重排版本（碱基组成不变、序列顺序破坏）
  3) RVDBv32_rev.fasta  —— 参考库逐条氨基酸序列反转（组成不变、结构域破坏）

用途：真实 reads × 真实库 为基线；真实 reads × 反转库、重排 reads × 真实库
      为两个零假设。若零假设命中率接近基线，说明信号由组成/低复杂度驱动而非真实同源。
"""
import random
import sys
from pathlib import Path

import gzip

PROJ = Path(__file__).resolve().parent.parent
CTL = PROJ / "04_viral" / "controls"
DB = PROJ / "00_db"
N_READS = 4_000_000

CTL.mkdir(parents=True, exist_ok=True)

# ---- 1) 抽取真实 reads（fastq → fasta，header 截短）------------------------
src = PROJ / "02_host_removed" / "SRR14300940.host_rm.1.fq.gz"
real_fa = CTL / "q_real.fa"
shuf_fa = CTL / "q_shuf.fa"

random.seed(20261108)
n = 0
with gzip.open(src, "rt", errors="replace") as fi, \
        open(real_fa, "w") as fr, open(shuf_fa, "w") as fs:
    while n < N_READS:
        head = fi.readline()
        if not head:
            break
        seq = fi.readline().strip()
        fi.readline()
        fi.readline()
        rid = head[1:].split()[0]
        fr.write(f">{rid}\n{seq}\n")
        lst = list(seq)
        random.shuffle(lst)
        fs.write(f">{rid}\n{''.join(lst)}\n")
        n += 1
print(f"真实 reads: {n:,} 条 → {real_fa.name} / {shuf_fa.name}")

# ---- 2) 反转参考库 -------------------------------------------------------
src_db = DB / "RVDBv32_unique.fasta"
rev_db = DB / "RVDBv32_rev.fasta"
nprot = 0
with open(src_db, encoding="utf-8", errors="replace") as fi, \
        open(rev_db, "w") as fo:
    buf = []
    for line in fi:
        if line.startswith(">"):
            if buf:
                fo.write("".join(buf)[::-1] + "\n")
                buf = []
            fo.write(line)
            nprot += 1
        else:
            buf.append(line.rstrip())
    if buf:
        fo.write("".join(buf)[::-1] + "\n")
print(f"反转库: {nprot:,} 条蛋白 → {rev_db.name}")

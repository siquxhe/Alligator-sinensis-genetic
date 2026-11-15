#!/usr/bin/env python3
"""
B1: 生成 in-silico spike 文库

背景 reads = W1 去宿主后的 reads（子采样到 N 对）
掺入 reads = T4 / Lambda / T7 三个噬菌体基因组等比例混合，150 bp 双端，插入片段 ~300 bp
每个 spike 水平 3 个重复，随机种子固定

真值 = spike 对数 / (背景对数 + spike 对数)，逐文库精确记录
spike reads 的 read ID 带 SPIKE_ 前缀，便于事后算灵敏度

用法：python3 make_spike_libs.py
输出：libs/<level>_<rep>_1.fq.gz / _2.fq.gz、truth.tsv
"""
import gzip
import random
from pathlib import Path

BASE = Path("/mnt/work/chicken/b1")
BG1 = Path("/home/wuyanching/virome/data/SRR14300938.host_rm.1.fq.gz")
BG2 = Path("/home/wuyanching/virome/data/SRR14300938.host_rm.2.fq.gz")
GENOMES = ["NC_000866.4", "NC_001416.1", "NC_001604.1"]

N_BG = 2_000_000          # 每文库背景对数
LEVELS = [0.001, 0.01, 0.05]   # 0.1% / 1% / 5%
REPS = 3
RL = 150                  # 读长
INS = 300                 # 插入片段
SEED0 = 20261115

COMP = str.maketrans("ACGTNacgtn", "TGCANtgcan")


def rc(s: str) -> str:
    return s.translate(COMP)[::-1]


def load_genomes():
    seqs = {}
    for g in GENOMES:
        txt = (BASE / f"{g}.fa").read_text()
        seq = "".join(l.strip() for l in txt.splitlines() if not l.startswith(">"))
        seqs[g] = seq.upper()
    return seqs


def make_spike_reads(seqs, n, rng):
    """等比例从三个基因组抽 n 条片段，返回 [(name, r1, r2)]"""
    out = []
    names = list(seqs)
    for i in range(n):
        g = names[i % len(names)]
        s = seqs[g]
        L = len(s)
        if L <= INS:
            pos = 0
            frag = (s * ((INS // L) + 2))[:INS]
        else:
            pos = rng.randrange(0, L - INS)
            frag = s[pos:pos + INS]
        r1 = frag[:RL]
        r2 = rc(frag)[:RL]
        out.append((f"SPIKE_{g}_{i:07d}", r1, r2))
    return out


def write_lib(idx, level, rep, seqs, truth_rows):
    rng = random.Random(SEED0 + idx)
    n_spike = int(round(N_BG * level / (1 - level)))
    spike = make_spike_reads(seqs, n_spike, rng)

    tag = f"L{str(level).replace('.','p')}_R{rep}"
    f1 = gzip.open(BASE / "libs" / f"{tag}_1.fq.gz", "wt", compresslevel=6)
    f2 = gzip.open(BASE / "libs" / f"{tag}_2.fq.gz", "wt", compresslevel=6)

    # 背景
    with gzip.open(BG1, "rt") as a, gzip.open(BG2, "rt") as b:
        for i in range(N_BG):
            h1 = a.readline().rstrip("\n"); s1 = a.readline().rstrip("\n")
            a.readline(); a.readline()
            h2 = b.readline().rstrip("\n"); s2 = b.readline().rstrip("\n")
            b.readline(); b.readline()
            if not s1:
                break
            f1.write(f"{h1}\n{s1}\n+\n{'I'*len(s1)}\n")
            f2.write(f"{h2}\n{s2}\n+\n{'I'*len(s2)}\n")

    # spike
    for name, r1, r2 in spike:
        f1.write(f"@{name}/1\n{r1}\n+\n{'I'*len(r1)}\n")
        f2.write(f"@{name}/2\n{r2}\n+\n{'I'*len(r2)}\n")
    f1.close(); f2.close()

    true_frac = len(spike) / (N_BG + len(spike))
    truth_rows.append((tag, level, rep, N_BG, len(spike), f"{true_frac:.8f}"))
    print(f"  {tag}: 背景 {N_BG} + spike {len(spike)} -> 真值 {true_frac*100:.4f}%")


def main():
    (BASE / "libs").mkdir(parents=True, exist_ok=True)
    seqs = load_genomes()
    print("基因组:", {k: len(v) for k, v in seqs.items()})

    rows = []
    idx = 0
    for level in LEVELS:
        for rep in range(1, REPS + 1):
            write_lib(idx, level, rep, seqs, rows)
            idx += 1

    out = BASE / "truth.tsv"
    with open(out, "w") as f:
        f.write("lib\tlevel\trep\tn_bg\tn_spike\ttrue_frac\n")
        for r in rows:
            f.write("\t".join(map(str, r)) + "\n")
    print("真值表:", out)
    print(f"共 {len(rows)} 个文库")
    print("谨慎提示: 未加入测序错误模型，本研究度量的是'可比对性'偏倚，不是碱基质量偏倚")


if __name__ == "__main__":
    main()

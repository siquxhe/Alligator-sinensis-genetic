#!/usr/bin/env python3
"""用已知真值的 spike 梯度反解：背景基线 + 回收率 + 校准后的估计

模型（同一规则、同一背景、spike 只稀释背景）：
    est(f) = B*(1-f) + rec*f  =  B + (rec - B)*f
线性回归 est ~ f：
    截距 = B          背景基线（该规则测到的非 spike 病毒占比）
    斜率 = rec - B    =>  rec = 截距 + 斜率
校准：
    f_cal = (est - B) / rec

每个 (库, 口径) 都跑一遍，比较哪个规则校准后最接近真值。
"""
import re
import sys
from collections import Counter, defaultdict

BASE = "/mnt/work/chicken/refcheck/spike"
TRUE_F = {"L0p001": 0.001, "L0p01": 0.01, "L0p05": 0.05}
LEVELS = ["L0p001", "L0p01", "L0p05"]
REPS = ["R1", "R2", "R3"]

STRUCT = {"head and packaging", "tail", "connector", "virion", "neck", "baseplate"}
REPL = {"DNA, RNA and nucleotide metabolism", "transcription regulation"}
KW_STRUCT = ["capsid", "coat protein", "major head", "minor head", "tail", "portal",
             "terminase", "baseplate", "spike", "fiber", "virion", "envelope",
             "glycoprotein", "neck", "tape measure", "sheath", "prohead"]
KW_REPL = ["polymerase", "replicase", "helicase", "primase", "integrase", "transposase",
           "nuclease", "ligase", "single-strand", "ssdna", "replication", "transcription",
           "rna-dependent", "rdrp", "polyprotein"]


def load_phrog_ann():
    import csv
    ann = {}
    with open("/mnt/work/chicken/db/phrog/phrog_annot_v4.tsv") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            ann[r["phrog"]] = r["category"]
    return ann


def cls_phrog(ann, desc):
    m = re.search(r"(\d+)", desc)
    cat = ann.get(m.group(1)) if m else None
    if cat in STRUCT:
        return "structural"
    if cat in REPL:
        return "replication"
    return "other"


def cls_kw(desc):
    d = desc.lower()
    if any(k in d for k in KW_STRUCT):
        return "structural"
    if any(k in d for k in KW_REPL):
        return "replication"
    return "other"


def parse(tag, lib, n_reads, ann, use_phrog):
    """返回 (total_hit, strict_hit, spike_hit)"""
    f = f"{BASE}/{tag}.{lib}.hits"
    seen = {}
    for line in open(f):
        p = line.rstrip("\n").split("\t")
        if len(p) < 4:
            continue
        try:
            if float(p[2]) < 40 or int(p[3]) < 30:
                continue
        except ValueError:
            continue
        if p[0] in seen:
            continue
        seen[p[0]] = cls_phrog(ann, p[1]) if use_phrog else cls_kw(p[1])
    c = Counter(seen.values())
    tot = len(seen)
    strict = c["structural"] + c["replication"]
    spike_hit = sum(1 for r in seen if r.startswith("SPIKE_"))
    return tot, strict, spike_hit


def linfit(xs, ys):
    n = len(xs)
    mx = sum(xs) / n
    my = sum(ys) / n
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sxx = sum((x - mx) ** 2 for x in xs)
    b = sxy / sxx
    a = my - b * mx
    ss_res = sum((y - (a + b * x)) ** 2 for x, y in zip(xs, ys))
    ss_tot = sum((y - my) ** 2 for y in ys)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else float("nan")
    return a, b, r2


def main():
    ann = load_phrog_ann()
    truth = {}
    for line in open("/mnt/work/chicken/b1/truth.tsv"):
        p = line.rstrip("\n").split("\t")
        if p[0] == "lib":
            continue
        truth[p[0]] = (int(p[4]), float(p[5]))  # n_spike, true_frac

    results = defaultdict(dict)
    for lib, use_phrog in [("phrog", True), ("refseq", False)]:
        for tag in [f"{lv}_{r}" for lv in LEVELS for r in REPS]:
            n_spike, tf = truth[tag]
            n_reads_file = f"{BASE}/{tag}.nreads"
            n_reads = int(open(n_reads_file).read().strip())
            tot, strict, sp = parse(tag, lib, n_reads, ann, use_phrog)
            for kname, val in [("wide", tot), ("strict", strict)]:
                results[(lib, kname)][tag] = dict(
                    n=n_reads, hit=val, est=val / n_reads,
                    spike_hit=sp, spike_total=n_spike * 2,  # R1+R2
                    rec=sp / (n_spike * 2),
                )

    print(f"{'规则':<16}{'水平':>8}{'真值%':>8}{'估计%':>9}{'回收率%':>9}{'背景基线%':>10}{'R2':>7}")
    print("-" * 72)
    summary = []
    for key in [("phrog", "wide"), ("phrog", "strict"), ("refseq", "wide"), ("refseq", "strict")]:
        lib, kj = key
        xs, ys, recs = [], [], []
        for lv in LEVELS:
            vals = [results[key][f"{lv}_{r}"] for r in REPS]
            est = sorted(v["est"] for v in vals)[1]  # 中位
            rec = sorted(v["rec"] for v in vals)[1]
            xs.append(TRUE_F[lv])
            ys.append(est)
            recs.append(rec)
            print(f"{lib+'/'+kj:<16}{lv:>8}{TRUE_F[lv]*100:>8.3f}{est*100:>9.3f}{rec*100:>9.2f}")
        a, b, r2 = linfit(xs, ys)
        B = a
        rec_fit = a + b   # rec = B + slope
        print(f"{'':16}{'回归':>8}{'':>8}{'':>9}{rec_fit*100:>9.2f}{B*100:>10.3f}{r2:>7.3f}")
        summary.append((lib, kj, B, rec_fit, r2, recs))
        print()

    print("=" * 72)
    print("校准效果：f_cal = (est - B) / (rec - B)   [由 est = B(1-f)+rec*f 解出]")
    print(f"{'规则':<16}{'真值%':>8}{'原始估计%':>11}{'校准后%':>10}{'相对误差':>10}")
    print("-" * 72)
    for lib, kj, B, rec, r2, _ in summary:
        key = (lib, kj)
        for lv in LEVELS:
            vals = [results[key][f"{lv}_{r}"]["est"] for r in REPS]
            est = sorted(vals)[1]
            fcal = (est - B) / (rec - B) if (rec - B) != 0 else float("nan")
            tf = TRUE_F[lv]
            err = (fcal - tf) / tf * 100 if tf else float("nan")
            print(f"{lib+'/'+kj:<16}{tf*100:>8.3f}{est*100:>11.3f}{fcal*100:>10.3f}{err:>9.1f}%")
        print()


if __name__ == "__main__":
    main()

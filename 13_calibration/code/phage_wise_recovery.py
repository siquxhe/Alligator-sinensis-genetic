#!/usr/bin/env python3
"""三个 spike 噬菌体的分别回收率

T4    NC_000866.4  Myoviridae  168 kb  GC 35%
Lambda NC_001416.1 Siphoviridae 48 kb  GC 50%
T7    NC_001604.1  Podoviridae  40 kb  GC 48%

若三者回收率一致 -> in-silico 检测层面对这三个科无偏
若不同           -> 检测层面本身有偏好，89% 是平均值
注意：in-silico spike 未经过提取，此差异不反映衣壳抗裂解能力
"""
import gzip
import re
import sys
from collections import Counter

BASE = "/mnt/work/chicken/refcheck/spike"
PHAGES = {"NC_000866": "T4_Myoviridae", "NC_001416": "Lambda_Siphoviridae",
          "NC_001604": "T7_Podoviridae"}
LEVELS = ["L0p001", "L0p01", "L0p05"]
REPS = ["R1", "R2", "R3"]


def count_total(tag):
    """从 R1 数每个噬菌体的 reads 数（R2 相同，故 x2）"""
    c = Counter()
    with gzip.open(f"/mnt/work/chicken/b1/libs/{tag}_1.fq.gz", "rt") as f:
        for i, line in enumerate(f):
            if i % 4 == 0 and line.startswith("@SPIKE_"):
                m = re.match(r"@SPIKE_(NC_\d+)\.", line)
                if m:
                    c[m.group(1)] += 1
    return {k: v * 2 for k, v in c.items()}


def count_hit(tag, lib):
    c = Counter()
    seen = set()
    try:
        fh = open(f"{BASE}/{tag}.{lib}.hits")
    except FileNotFoundError:
        return c
    for line in fh:
        p = line.rstrip("\n").split("\t")
        if len(p) < 4:
            continue
        try:
            if float(p[2]) < 40 or int(p[3]) < 30:
                continue
        except ValueError:
            continue
        rid = p[0]
        if rid in seen or not rid.startswith("SPIKE_"):
            continue
        seen.add(rid)
        m = re.match(r"SPIKE_(NC_\d+)\.", rid)
        if m:
            c[m.group(1)] += 1
    return c


def main():
    print(f"{'水平':>8}{'噬菌体':>22}{'总数':>9}{'检出':>8}{'回收率':>9}")
    print("-" * 58)
    for lv in LEVELS:
        rows = {}
        for pacc, pname in PHAGES.items():
            tot_n = 0
            hit_n = 0
            for rep in REPS:
                tag = f"{lv}_{rep}"
                tot_n += count_total(tag).get(pacc, 0)
                hit_n += count_hit(tag, "phrog").get(pacc, 0)
            rows[pname] = (tot_n, hit_n)
        for pname, (t, h) in rows.items():
            r = h / t * 100 if t else 0
            print(f"{lv:>8}{pname:>22}{t:>9,}{h:>8,}{r:>8.2f}%")
        vals = [h / t for t, h in rows.values() if t]
        if vals:
            print(f"{'':>8}{'三噬菌体差异':>22}{'':>9}{'':>8}{max(vals)/min(vals):>8.3f}x")
        print()


if __name__ == "__main__":
    main()

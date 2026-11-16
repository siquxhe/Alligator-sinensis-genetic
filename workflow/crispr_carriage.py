#!/usr/bin/env python3
"""
CRISPR carriage rate for MAGs (MinCED + HMMER Cas1/Cas2).

Purpose
-------
Compute, per MAG:
  - number of CRISPR arrays and spacers (MinCED)
  - Cas1 / Cas2 presence (hmmsearch vs PF01867 / PF09827 HMMs)
  - any-array, any-Cas, both-Cas, array+Cas
and summarize carriage rates with Wilson 95% CI, overall and by phylum.

This is the "main metric" from 当前工作任务表 D5/F3:
  cas1/cas2 carriage = MAGs with cas1 or cas2 / total MAGs
  decision: >20% feasible; <10% downgrade the spacer route.

Usage
-----
  python3 workflow/crispr_carriage.py \
    --mag-dir  $HOME/virome/work/mag_all_bins \
    --meta     07_mag/mag_final_annotated.tsv \
    --cas1-hmm $HOME/biotools/hmm/Cas1.hmm \
    --cas2-hmm $HOME/biotools/hmm/Cas2.hmm \
    --out      $HOME/virome/work/crispr_carriage \
    --threads  8

If HMMs are not available, the script still computes arrays with MinCED and
marks Cas columns as missing. If MinCED is not available, it still computes
Cas with HMMER.

Requirements
------------
  - minced     (https://github.com/ctSkennerton/minced)
  - hmmsearch  (HMMER 3.x)
  - Cas1 HMM   PF01867 (or lab equivalent)
  - Cas2 HMM   PF09827 (or lab equivalent)
  - Python 3.6+ (standard library only)

Notes
-----
  - Short-read MAGs often miss complete arrays; cas1/cas2 is the robust metric.
  - A MAG is "Cas+" if either Cas1 or Cas2 has a hit passing i-Evalue and
    coverage thresholds. "both" requires both.
  - HMMER hit: i-Evalue < --min-evalue AND alignment coverage >= --min-coverage.
  - The script is idempotent and overwrites outputs in --out.
"""

from __future__ import annotations

import argparse
import csv
import gzip
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Dict, List, Optional, Tuple


# ----------------------------- helpers ------------------------------------

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def which_or_none(name: str) -> Optional[str]:
    return shutil.which(name)


def find_mags(mag_dir: Path) -> List[Path]:
    patterns = ["*.fa", "*.fna", "*.fasta", "*.fa.gz", "*.fna.gz", "*.fasta.gz"]
    files: List[Path] = []
    for pat in patterns:
        files.extend(mag_dir.glob(pat))
    # de-duplicate and sort
    return sorted(set(files))


def mag_id(path: Path) -> str:
    name = path.name
    for suffix in [".fa.gz", ".fna.gz", ".fasta.gz", ".fa", ".fna", ".fasta"]:
        if name.endswith(suffix):
            return name[: -len(suffix)]
    return path.stem


def materialize(path: Path, tmpdir: Path) -> Path:
    """Return a plain FASTA path; decompress .gz into tmpdir if needed."""
    if not path.name.endswith(".gz"):
        return path
    out = tmpdir / (mag_id(path) + ".fa")
    if out.exists():
        return out
    with gzip.open(path, "rt") as fh_in, open(out, "w") as fh_out:
        shutil.copyfileobj(fh_in, fh_out)
    return out


def run_cmd(cmd: List[str], log_fh, timeout: int = 3600) -> Tuple[int, str, str]:
    log_fh.write("$ " + " ".join(cmd) + "\n")
    log_fh.flush()
    try:
        p = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout,
        )
        if p.stdout:
            log_fh.write(p.stdout[-2000:])
        if p.stderr:
            log_fh.write("[stderr]\n" + p.stderr[-2000:])
        log_fh.flush()
        return p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired:
        log_fh.write(f"[timeout] {' '.join(cmd)}\n")
        log_fh.flush()
        return 124, "", "timeout"
    except FileNotFoundError as exc:
        log_fh.write(f"[missing] {exc}\n")
        log_fh.flush()
        return 127, "", str(exc)


# ----------------------------- parsers ------------------------------------

MINCED_RE = re.compile(
    r"CRISPR\s+\d+\s+Range:\s*(\d+)\s*-\s*(\d+).*?Repeats:\s*(\d+).*?Spacers:\s*(\d+)",
    re.IGNORECASE,
)


def parse_minced(text: str) -> Tuple[int, int]:
    """Return (n_arrays, n_spacers) from MinCED stdout."""
    n_arrays = 0
    n_spacers = 0
    for line in text.splitlines():
        m = MINCED_RE.search(line)
        if m:
            n_arrays += 1
            n_spacers += int(m.group(4))
    return n_arrays, n_spacers


def parse_domtbl(path: Path, min_evalue: float, min_cov: float) -> int:
    """Count HMMER domain hits passing i-Evalue and coverage thresholds."""
    if not path.exists():
        return 0
    n = 0
    with open(path) as fh:
        for line in fh:
            if not line.strip() or line.startswith("#"):
                continue
            cols = line.split()
            if len(cols) < 19:
                continue
            try:
                qlen = int(cols[5])
                i_evalue = float(cols[12])
                ali_from = int(cols[17])
                ali_to = int(cols[18])
            except (ValueError, IndexError):
                continue
            cov = (ali_to - ali_from + 1) / qlen if qlen > 0 else 0.0
            if i_evalue <= min_evalue and cov >= min_cov:
                n += 1
    return n


# ----------------------------- stats --------------------------------------

def wilson(k: int, n: int, z: float = 1.96) -> Tuple[float, float, float]:
    """Return (pct, ci_low_pct, ci_high_pct)."""
    if n <= 0:
        return (float("nan"), float("nan"), float("nan"))
    p = k / n
    denom = 1.0 + z * z / n
    center = (p + z * z / (2.0 * n)) / denom
    half = z * math.sqrt(p * (1.0 - p) / n + z * z / (4.0 * n * n)) / denom
    return (100.0 * p, 100.0 * max(0.0, center - half), 100.0 * min(1.0, center + half))


# ----------------------------- metadata -----------------------------------

META_COLS = ["bin", "sample_id", "quality", "completeness", "contamination", "phylum", "genus"]


def read_meta(path: Optional[Path]) -> Dict[str, Dict[str, str]]:
    if path is None or not path.exists():
        return {}
    meta: Dict[str, Dict[str, str]] = {}
    with open(path, newline="") as fh:
        reader = csv.DictReader(fh, delimiter="\t")
        for row in reader:
            key = row.get("bin", "")
            if key:
                meta[key] = row
    return meta


# ----------------------------- main ---------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description="CRISPR carriage rate for MAGs")
    ap.add_argument("--mag-dir", required=True, help="directory with MAG FASTA files")
    ap.add_argument("--meta", default=None, help="mag_final_annotated.tsv (optional)")
    ap.add_argument("--out", required=True, help="output directory")
    ap.add_argument("--minced", default=None, help="path to minced (default: PATH)")
    ap.add_argument("--hmmsearch", default=None, help="path to hmmsearch (default: PATH)")
    ap.add_argument("--cas1-hmm", default=None, help="Cas1 HMM (PF01867)")
    ap.add_argument("--cas2-hmm", default=None, help="Cas2 HMM (PF09827)")
    ap.add_argument("--threads", type=int, default=4, help="hmmsearch CPUs")
    ap.add_argument("--min-evalue", type=float, default=1e-5, help="HMMER i-Evalue cutoff")
    ap.add_argument("--min-coverage", type=float, default=0.5, help="HMMER alignment coverage cutoff")
    ap.add_argument("--limit", type=int, default=0, help="only first N MAGs (0 = all)")
    args = ap.parse_args()

    mag_dir = Path(args.mag_dir).expanduser()
    out_dir = Path(args.out).expanduser()
    out_dir.mkdir(parents=True, exist_ok=True)
    meta = read_meta(Path(args.meta).expanduser() if args.meta else None)

    mags = find_mags(mag_dir)
    if args.limit and args.limit > 0:
        mags = mags[: args.limit]
    if not mags:
        eprint(f"[error] no MAG FASTA found in {mag_dir}")
        return 2

    minced = args.minced or which_or_none("minced")
    hmmsearch = args.hmmsearch or which_or_none("hmmsearch")
    cas1_hmm = Path(args.cas1_hmm).expanduser() if args.cas1_hmm else None
    cas2_hmm = Path(args.cas2_hmm).expanduser() if args.cas2_hmm else None

    if not minced:
        eprint("[warn] minced not found; arrays will be marked missing")
    if not hmmsearch:
        eprint("[warn] hmmsearch not found; Cas will be marked missing")
    if hmmsearch and (not cas1_hmm or not cas1_hmm.exists()):
        eprint("[warn] Cas1 HMM missing; Cas1 will be marked missing")
        cas1_hmm = None
    if hmmsearch and (not cas2_hmm or not cas2_hmm.exists()):
        eprint("[warn] Cas2 HMM missing; Cas2 will be marked missing")
        cas2_hmm = None

    tmpdir = Path(tempfile.mkdtemp(prefix="crispr_carriage_", dir=str(out_dir)))
    per_mag_path = out_dir / "per_mag.tsv"
    summary_path = out_dir / "summary.tsv"
    by_phylum_path = out_dir / "by_phylum.tsv"
    log_path = out_dir / "run.log"

    rows: List[Dict[str, object]] = []

    with open(log_path, "w") as log_fh:
        log_fh.write(f"mag_dir={mag_dir}\n")
        log_fh.write(f"n_mags={len(mags)}\n")
        log_fh.write(f"minced={minced}\n")
        log_fh.write(f"hmmsearch={hmmsearch}\n")
        log_fh.write(f"cas1_hmm={cas1_hmm}\n")
        log_fh.write(f"cas2_hmm={cas2_hmm}\n\n")

        for i, mag_path in enumerate(mags, 1):
            mid = mag_id(mag_path)
            fasta = materialize(mag_path, tmpdir)
            eprint(f"[{i}/{len(mags)}] {mid}")

            # ---- MinCED
            n_arrays = 0
            n_spacers = 0
            array_status = "missing"
            if minced:
                rc, stdout, stderr = run_cmd(
                    [minced, "-minNR", "2", "-minRL", "18", "-spacers", str(fasta)],
                    log_fh,
                )
                if rc == 0:
                    n_arrays, n_spacers = parse_minced(stdout)
                    array_status = "ok"
                else:
                    array_status = f"error:{rc}"

            # ---- HMMER Cas1
            cas1_hits = 0
            cas1_status = "missing"
            if hmmsearch and cas1_hmm:
                domtbl = out_dir / f"{mid}.cas1.domtbl"
                rc, _, _ = run_cmd(
                    [
                        hmmsearch,
                        "--domtblout", str(domtbl),
                        "--cpu", str(args.threads),
                        "--noali",
                        str(cas1_hmm),
                        str(fasta),
                    ],
                    log_fh,
                )
                if rc == 0:
                    cas1_hits = parse_domtbl(domtbl, args.min_evalue, args.min_coverage)
                    cas1_status = "ok"
                else:
                    cas1_status = f"error:{rc}"

            # ---- HMMER Cas2
            cas2_hits = 0
            cas2_status = "missing"
            if hmmsearch and cas2_hmm:
                domtbl = out_dir / f"{mid}.cas2.domtbl"
                rc, _, _ = run_cmd(
                    [
                        hmmsearch,
                        "--domtblout", str(domtbl),
                        "--cpu", str(args.threads),
                        "--noali",
                        str(cas2_hmm),
                        str(fasta),
                    ],
                    log_fh,
                )
                if rc == 0:
                    cas2_hits = parse_domtbl(domtbl, args.min_evalue, args.min_coverage)
                    cas2_status = "ok"
                else:
                    cas2_status = f"error:{rc}"

            m = meta.get(mid, {})
            rows.append(
                {
                    "bin": mid,
                    "sample_id": m.get("sample_id", ""),
                    "quality": m.get("quality", ""),
                    "completeness": m.get("completeness", ""),
                    "contamination": m.get("contamination", ""),
                    "phylum": m.get("phylum", ""),
                    "genus": m.get("genus", ""),
                    "n_crispr_arrays": n_arrays,
                    "n_spacers": n_spacers,
                    "array_status": array_status,
                    "cas1_hits": cas1_hits,
                    "cas2_hits": cas2_hits,
                    "cas1_status": cas1_status,
                    "cas2_status": cas2_status,
                    "cas1": int(cas1_hits > 0) if cas1_status == "ok" else "",
                    "cas2": int(cas2_hits > 0) if cas2_status == "ok" else "",
                    "cas_any": (
                        int(cas1_hits > 0 or cas2_hits > 0)
                        if (cas1_status == "ok" and cas2_status == "ok")
                        else ""
                    ),
                    "both_cas": (
                        int(cas1_hits > 0 and cas2_hits > 0)
                        if (cas1_status == "ok" and cas2_status == "ok")
                        else ""
                    ),
                    "array_any": int(n_arrays > 0) if array_status == "ok" else "",
                    "array_and_cas": (
                        int(n_arrays > 0 and (cas1_hits > 0 or cas2_hits > 0))
                        if (array_status == "ok" and cas1_status == "ok" and cas2_status == "ok")
                        else ""
                    ),
                }
            )

    # ---- per-MAG table
    cols = [
        "bin", "sample_id", "quality", "completeness", "contamination",
        "phylum", "genus", "n_crispr_arrays", "n_spacers", "array_status",
        "cas1_hits", "cas2_hits", "cas1_status", "cas2_status",
        "cas1", "cas2", "cas_any", "both_cas", "array_any", "array_and_cas",
    ]
    with open(per_mag_path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, delimiter="\t")
        w.writeheader()
        for row in rows:
            w.writerow(row)

    # ---- summary
    def count_metric(key: str) -> Tuple[int, int]:
        vals = [r[key] for r in rows if r[key] != ""]
        return sum(int(v) for v in vals), len(vals)

    metrics = [
        ("any_crispr_array", "array_any"),
        ("cas1", "cas1"),
        ("cas2", "cas2"),
        ("cas_any", "cas_any"),
        ("cas1_and_cas2", "both_cas"),
        ("array_and_cas", "array_and_cas"),
    ]
    summary_rows = []
    for label, key in metrics:
        k, n = count_metric(key)
        pct, lo, hi = wilson(k, n)
        summary_rows.append(
            {
                "metric": label,
                "n_positive": k,
                "n_evaluable": n,
                # n==0 时不得输出 0.00（会被读成"阳性率为 0"）；写 NA 并提示分母缺失
                "pct": f"{pct:.2f}" if n else "NA",
                "ci95_low": f"{lo:.2f}" if n else "NA",
                "ci95_high": f"{hi:.2f}" if n else "NA",
            }
        )
    with open(summary_path, "w", newline="") as fh:
        w = csv.DictWriter(
            fh,
            fieldnames=["metric", "n_positive", "n_evaluable", "pct", "ci95_low", "ci95_high"],
            delimiter="\t",
        )
        w.writeheader()
        for row in summary_rows:
            w.writerow(row)

    # ---- by phylum
    phyla: Dict[str, List[Dict[str, object]]] = {}
    for r in rows:
        phyla.setdefault(str(r.get("phylum") or "unclassified"), []).append(r)

    by_rows = []
    for phylum, rs in sorted(phyla.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        arr = [r["array_any"] for r in rs if r["array_any"] != ""]
        cas = [r["cas_any"] for r in rs if r["cas_any"] != ""]
        n = len(rs)
        by_rows.append(
            {
                "phylum": phylum,
                "n_mags": n,
                "n_array_evaluable": len(arr),
                "n_array_positive": sum(int(v) for v in arr),
                "pct_array": f"{100.0 * sum(int(v) for v in arr) / len(arr):.2f}" if arr else "",
                "n_cas_evaluable": len(cas),
                "n_cas_positive": sum(int(v) for v in cas),
                "pct_cas": f"{100.0 * sum(int(v) for v in cas) / len(cas):.2f}" if cas else "",
            }
        )
    with open(by_phylum_path, "w", newline="") as fh:
        w = csv.DictWriter(
            fh,
            fieldnames=[
                "phylum", "n_mags", "n_array_evaluable", "n_array_positive",
                "pct_array", "n_cas_evaluable", "n_cas_positive", "pct_cas",
            ],
            delimiter="\t",
        )
        w.writeheader()
        for row in by_rows:
            w.writerow(row)

    # ---- console summary
    print(f"\nWrote:\n  {per_mag_path}\n  {summary_path}\n  {by_phylum_path}\n  {log_path}")
    print("\nSummary:")
    for row in summary_rows:
        print(
            f"  {row['metric']:<18} {row['n_positive']}/{row['n_evaluable']}"
            + (f"  {row['pct']}%  (95% CI {row['ci95_low']}–{row['ci95_high']})"
               if row["pct"] != "NA"
               else "  NA (n_evaluable = 0, 结果不可解释)")
        )
    if any(r["array_status"] != "ok" for r in rows):
        eprint("\n[warn] some MAGs have missing/error array calls; see run.log")
    _tot = len(rows)
    _bad = sum(1 for r in rows if r.get("cas1_status") != "ok" or r.get("cas2_status") != "ok")
    if _bad:
        eprint(f"\n[WARN] {_bad}/{_tot} MAGs 的 Cas 调用失败。"
               f"失败样本可能是信息性缺失（本项目中失败的 10 个里有 6 个为阳性），"
               f"据此得到的百分比不可外推；请先补测再解读。")
    if any(r["cas1_status"] != "ok" or r["cas2_status"] != "ok" for r in rows):
        eprint("[warn] some MAGs have missing/error Cas calls; see run.log")

    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""bioRxiv 全量扫描（OpenAlex 侧）：2024-01 起按月分窗，标题+摘要关键词过滤。

按月分窗 + 页号翻页，不依赖 cursor（带摘要查询时 next_cursor 不稳定）。
断点续跑：done_months_oa.txt；命中追加 hits_oa.tsv。
"""
import calendar
import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

UA = {"User-Agent": "mailto:research@example.org"}
SID = "S4306402567"
BASE = Path.home() / "virome" / "preprint_scan"
BASE.mkdir(parents=True, exist_ok=True)
HITS, DONE, LOG = BASE / "hits_oa.tsv", BASE / "done_months_oa.txt", BASE / "scan_oa.log"

TARGET = ("phage", "bacteriophage", "virome", "metagenom", "environment", "wastewater",
          "sewage", "soil", "marine", "gut", "fecal", "faecal")

PAT = {
    # 论点撞车
    "A_argument": re.compile(
        r"recording is not|record is not|records? (?:are|is) not (?:a )?discover|"
        r"not a discovery tool|discovery (?:versus|vs\.?) record|detection is not discover", re.I),
    # spacer/CRISPR × 检测/发现/监测 × 环境病毒（要求环境词，排除慢病毒载体）
    "B_spacer_detect": re.compile(
        r"(?=.*(?:crispr|spacer))(?=.*(?:detect|discover|surveil|monitor))"
        r"(?=.*(?:phage|bacteriophage|virome|metagenom))", re.I | re.S),
    # 记录器 × 病毒组（要求记录 + CRISPR + 病毒组/噬菌体，不认泛 virus）
    "C_recorder_virus": re.compile(
        r"(?=.*(?:recorder|recording|record(?:ed|ing)?))(?=.*(?:crispr|spacer))"
        r"(?=.*(?:phage|bacteriophage|virome))", re.I | re.S),
    # 受体/诱饵 × 噬菌体 × 工程/检测
    "D_receptor_bait": re.compile(
        r"(?=.*(?:bait|receptor|host range))(?=.*(?:phage|bacteriophage))"
        r"(?=.*(?:engineer|synthetic|platform|detect|surveil))", re.I | re.S),
    # 检出限 × CRISPR × 环境
    "E_lod_crispr": re.compile(
        r"(?=.*(?:limit of detection|detection limit|sensitivity))(?=.*(?:crispr|spacer))"
        r"(?=.*(?:environment|metagenom|virome|wastewater|water|soil))", re.I | re.S),
}


def abstract_from_inv(inv):
    if not inv:
        return ""
    pos = [(i, w) for w, idxs in inv.items() for i in idxs]
    pos.sort()
    return " ".join(w for _, w in pos)


def get(url, tries=3):
    for k in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=45) as r:
                return json.load(r)
        except Exception as e:  # noqa: BLE001
            if k == tries - 1:
                LOG.open("a", encoding="utf-8").write(f"ERR {type(e).__name__}\n")
                return None
            time.sleep(3 * (k + 1))
    return None


def months():
    out = []
    for y in (2024, 2025, 2026):
        for m in range(1, 13):
            if y == 2026 and m > 11:
                break
            out.append((y, m))
    return out


def run_month(y, m):
    start = f"{y}-{m:02d}-01"
    end = f"{y}-{m:02d}-{calendar.monthrange(y, m)[1]:02d}"
    base_filter = (f"primary_location.source.id:{SID},from_publication_date:{start},"
                   f"to_publication_date:{end}")
    seen = hits = page = 0
    total = None
    while True:
        page += 1
        url = "https://api.openalex.org/works?" + urllib.parse.urlencode({
            "filter": base_filter, "per-page": 200, "page": page,
            "select": "doi,title,publication_date",
        })
        d = get(url)
        if not d or not d.get("results"):
            break
        if total is None:
            total = d["meta"].get("count") or 0
        rows = []
        for w in d["results"]:
            seen += 1
            title = w.get("title") or ""
            ab = ""   # 仅扫标题；命中项另抓摘要复核
            text = title + " . " + ab
            tags = [k for k, p in PAT.items() if p.search(text)]
            if tags:
                hits += 1
                rows.append((w.get("publication_date", ""),
                             (w.get("doi") or "").replace("https://doi.org/", ""),
                             ",".join(tags), title.replace("\t", " "), ab[:400].replace("\t", " ")))
        if rows:
            with HITS.open("a", encoding="utf-8") as f:
                for row in rows:
                    f.write("\t".join(row) + "\n")
        if len(d["results"]) < 200:
            break
        if total and page * 200 >= total:
            break
        if page >= 60:          # 兜底
            break
    with DONE.open("a", encoding="utf-8") as f:
        f.write(f"{y}-{m:02d}\n")
    print(f"    {y}-{m:02d}: {seen}/{total} 条, {page} 页, 命中 {hits}", flush=True)
    return seen, hits


def main():
    if not HITS.exists():
        HITS.write_text("date\tdoi\tcategories\ttitle\tabstract\n", encoding="utf-8")
    done = set(DONE.read_text(encoding="utf-8").split()) if DONE.exists() else set()
    t0 = time.time()
    tot = th = 0
    for (y, m) in months():
        key = f"{y}-{m:02d}"
        if key in done:
            continue
        seen, hits = run_month(y, m)
        tot += seen
        th += hits
        msg = f"[{time.strftime('%H:%M:%S')}] {key}: {seen} 条, 命中 {hits} | 累计 {tot}, {th} | {(time.time()-t0)/60:.1f} min"
        print(msg, flush=True)
        LOG.open("a", encoding="utf-8").write(msg + "\n")
    print(f"DONE 共 {tot} 条，命中 {th}，{(time.time()-t0)/60:.1f} min", flush=True)


if __name__ == "__main__":
    main()

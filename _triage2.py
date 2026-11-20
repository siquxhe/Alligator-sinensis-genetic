import collections
import csv
import re

PATH = "/home/wuyanching/virome/preprint_scan/hits.tsv"
rows = []
with open(PATH, encoding="utf-8") as f:
    for x in csv.DictReader(f, delimiter="\t"):
        rows.append(x)

seen = {}
for x in rows:
    seen[x["doi"]] = x
u = list(seen.values())
print("原始 %d 行，去重后 %d 条" % (len(rows), len(u)))
print("类别:", dict(collections.Counter(c for x in u for c in (x["categories"] or "").split(",") if c)))
print("年份:", dict(collections.Counter(x["date"][:4] for x in u)))

# 严格筛：必须真的在讲"用 spacer 做检测/发现"，且不是 Cas 工程
SP = re.compile(r"\bspacer", re.I)
DISC = re.compile(r"discover|detection limit|limit of detection|unknown virus|uncharted|blind spot|undocumented|only known|cannot detect", re.I)
BAD = re.compile(r"base edit|prime edit|knock-?in|knockout|screen(ing)? of|macrophage|tumou?r|cancer|therap|vaccine|antibod|cytokine|immunotherapy|editing efficiency|off-target", re.I)

core = []
for x in u:
    t = (x["title"] or "") + " " + (x["abstract"] or "")
    if SP.search(t) and DISC.search(t) and not BAD.search(x["title"]):
        core.append(x)

print("\n严格筛后 %d 条:" % len(core))
for x in sorted(core, key=lambda y: y["date"]):
    print("  %s %s" % (x["date"], x["title"][:96]))

# 单独看：明确讨论"记录≠发现"或"只检已知"的句子
SENT = re.compile(r"(only|solely)[^.]{0,60}known|not (?:a )?(?:tool|method) for discovery|recording[^.]{0,40}not", re.I)
hits2 = [(x, SENT.search(x["abstract"] or "")) for x in u]
hits2 = [(x, m) for x, m in hits2 if m]
print("\n摘要含'只检已知/不是发现工具'类句子 %d 条:" % len(hits2))
for x, m in hits2[:12]:
    print("  %s %s" % (x["date"], x["title"][:80]))
    print("      …%s…" % m.group(0)[:90])

#!/usr/bin/env python3
"""
生成图注正式稿（Fig 1–3）的 Word 版本。

**单一来源**：本脚本解析 `Figure_legends_2026-11-13.md` 的英文段落，不再另存一份硬编码文本。
这样图注改了 md 就是改了稿，不会再出现"图重出了、图注还是旧数"的漂移。

输出：11_proposal/MS01/legends/output/Figure_legends.docx
格式：A4 纵向、页边距 2.5 cm、Times New Roman 11 pt、1.5 倍行距、两端对齐
文本标记：**加粗**、_斜体_（仅用于物种名）

用法：python 11_proposal/MS01/legends/code/make_legends_docx.py
"""

import re
import sys
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "output"
SRC = HERE.parent / "Figure_legends_2026-11-13.md"
OUT.mkdir(parents=True, exist_ok=True)

# 旧数字黑名单：换库前的值不得回流到投稿文本里
STALE = ["171×", "171-fold", "0.089", "7.1 × 5.6", "22.2–124.8", "1.37×", "5.6× 的普遍"]
# 新数字必须在场，防止改漏
REQUIRED = ["25.9×", "4.7–8.4×", "3.1×", "4.6 × 1.1 ≈ 5", "26-fold"]

HEADING = re.compile(r"^\*\*(Figure\s+(\d)\.\s*(.+?))\*\*\s*$")


def parse_md(path: Path) -> list[tuple[str, str, str]]:
    """抽出英文投稿段的 (label, title, body)。"""
    text = path.read_text(encoding="utf-8")
    marker = "## 一、英文投稿版"
    if marker not in text:
        sys.exit(f"找不到章节：{marker}")
    block = text.split(marker, 1)[1].split("\n---", 1)[0]

    legends: list[tuple[str, str, str]] = []
    cur: tuple[str, str, list[str]] | None = None
    for raw in block.splitlines():
        line = raw.strip()
        m = HEADING.match(line)
        if m:
            if cur:
                legends.append((cur[0], cur[1], " ".join(cur[2]).strip()))
            label = f"Figure {m.group(2)}. "
            cur = (label, m.group(3).strip(), [])
        elif cur is not None and line:
            cur[2].append(line)
    if cur:
        legends.append((cur[0], cur[1], " ".join(cur[2]).strip()))

    if len(legends) != 3:
        sys.exit(f"期望 3 条图注，实际解析到 {len(legends)} 条")
    return legends


def guard(legends: list[tuple[str, str, str]]) -> None:
    joined = " ".join(t + " " + b for _, t, b in legends)
    hits = [s for s in STALE if s in joined]
    if hits:
        sys.exit(f"发现过期数字：{hits}。请改 {SRC.name} 后重跑。")
    missing = [s for s in REQUIRED if s not in joined]
    if missing:
        sys.exit(f"缺少应有数字：{missing}。检查是否改漏。")


TOKEN = re.compile(r"(\*\*.+?\*\*|_[^_]+?_)")


def add_rich(paragraph, text: str, size: float = 11.0) -> None:
    """按 **粗体** / _斜体_ 标记写入 run。"""
    for chunk in TOKEN.split(text):
        if not chunk:
            continue
        bold = chunk.startswith("**") and chunk.endswith("**")
        italic = chunk.startswith("_") and chunk.endswith("_") and not bold
        content = chunk[2:-2] if bold else (chunk[1:-1] if italic else chunk)
        run = paragraph.add_run(content)
        run.font.name = "Times New Roman"
        run.font.size = Pt(size)
        run.font.bold = bold
        run.font.italic = italic
        run._element.rPr.rFonts.set(qn("w:eastAsia"), "SimSun")


def main() -> None:
    legends = parse_md(SRC)
    guard(legends)

    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Cm(21.0), Cm(29.7)
    for attr in ("left_margin", "right_margin", "top_margin", "bottom_margin"):
        setattr(sec, attr, Cm(2.5))

    normal = doc.styles["Normal"]
    normal.font.name = "Times New Roman"
    normal.font.size = Pt(11)
    normal.element.rPr.rFonts.set(qn("w:eastAsia"), "SimSun")

    head = doc.add_paragraph()
    head.paragraph_format.space_after = Pt(14)
    hr = head.add_run("Figure legends")
    hr.font.name = "Times New Roman"
    hr.font.size = Pt(12)
    hr.font.bold = True
    hr._element.rPr.rFonts.set(qn("w:eastAsia"), "SimSun")

    for label, title, body in legends:
        p = doc.add_paragraph()
        pf = p.paragraph_format
        pf.space_after = Pt(12)
        pf.line_spacing = 1.5
        pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

        r1 = p.add_run(label)
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(11)
        r1.font.bold = True
        r1._element.rPr.rFonts.set(qn("w:eastAsia"), "SimSun")

        r2 = p.add_run(title + " ")
        r2.font.name = "Times New Roman"
        r2.font.size = Pt(11)
        r2.font.bold = True
        r2._element.rPr.rFonts.set(qn("w:eastAsia"), "SimSun")

        add_rich(p, body)

    out = OUT / "Figure_legends.docx"
    doc.save(out)
    print(f"已输出: {out}")
    print(f"  来源: {SRC.name}")
    print(f"  图注数: {len(legends)}  过期数字检查: 通过")
    for _, title, body in legends:
        print(f"  {len(title) + len(body):4d} 字符 | {title[:56]}...")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
生成 Table 2 正式稿（Word）

输入：09_tables/Table2_reporting_checklist.tsv
输出：11_proposal/table2/output/Table2_reporting_checklist.docx

格式约定（投稿常见三线表）
- A4，页边距 2.5 cm
- Times New Roman 9 pt；标题 10.5 pt 加粗
- 仅保留顶线、表头下线、底线；无竖线、无行间线
- 表注置于表下，8 pt

用法：python 11_proposal/table2/code/make_table2_docx.py
"""

from pathlib import Path

import pandas as pd
from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SRC = ROOT / "09_tables" / "Table2_reporting_checklist.tsv"
OUT = HERE.parent / "output"
OUT.mkdir(parents=True, exist_ok=True)

TITLE = ("Table 2. Minimum reporting checklist for viral-fraction estimates "
         "from host-associated metagenomes.")

NOTES = [
    ("Values in the last column are the median (range) fold change across the six samples, "
     "computed with the other dimensions held fixed. They are not multiplicative: "
     "1.01 × 5.6 × 7.1 × 5.4 ≈ 217, whereas the observed overall span is 171×."),
    ("Items 1–4 correspond to the four dimensions in Fig. 1; items 5–8 concern reliability "
     "rather than definition."),
    ("The denominator effect was measured in fecal samples with low host content (0.07–2.51%). "
     "Host-removal method choice can dominate in high-host or low-viral-biomass samples "
     "(Forbes et al., Cell Reports Methods 2025, doi:10.1016/j.crmeth.2025.101218)."),
    ("Host-prediction agreement was assessed against 19 prophages with MAG-confirmed hosts; "
     "iPHoP returned a prediction for 5 of these (phylum 5/5, genus 2/5)."),
    ("Zero acquired ARGs: geNomad AMR annotation returned 0 of 2,678 genes; CARD searches "
     "returned 66 hits (22 unique genes), of which only gyrA fluoroquinolone mutation models "
     "exceeded 60% identity; none was an acquired resistance gene."),
    ("Items 1–8 complement MIUViG (Roux et al., Nat Biotechnol 2019, doi:10.1038/nbt.4306), "
     "which specifies reporting of uncultivated viral genomes rather than read-level fractions."),
    ("Item 4 combines the counting unit with the detection level: in this study C2 counts "
     "read-level protein hits while C4 counts geNomad-assigned contigs. Mapping reads back to "
     "each sample's own viral contig set, so that only the unit changes, yields a contig-to-read "
     "ratio of ≈0.6 — the opposite direction. The 5.4× is therefore an upper bound on the unit "
     "effect; most of it arises from the detection level and the reference set."),
]

COLS = ["No.", "Item", "What must be reported", "Consequence if omitted",
        "Effect measured in this study"]
WIDTHS_CM = [0.9, 2.7, 6.1, 3.3, 3.0]   # 合计 16.0 cm = A4 21 − 2×2.5


def set_fixed_layout(table, widths_cm) -> None:
    """固定表格布局：python-docx 只设 cell.width 不足以生效，必须写 tblLayout + gridCol。"""
    tbl = table._tbl
    tblPr = tbl.tblPr

    for old in tblPr.findall(qn("w:tblLayout")):
        tblPr.remove(old)
    layout = OxmlElement("w:tblLayout")
    layout.set(qn("w:type"), "fixed")
    tblPr.append(layout)

    for old in tblPr.findall(qn("w:tblW")):
        tblPr.remove(old)
    tbl_w = OxmlElement("w:tblW")
    tbl_w.set(qn("w:type"), "dxa")
    tbl_w.set(qn("w:w"), str(int(sum(widths_cm) * 567)))
    tblPr.append(tbl_w)

    grid = tbl.find(qn("w:tblGrid"))
    if grid is not None:
        for gc, w in zip(grid.findall(qn("w:gridCol")), widths_cm):
            gc.set(qn("w:w"), str(int(w * 567)))

    for row in table.rows:
        for cell, w in zip(row.cells, widths_cm):
            cell.width = Cm(w)


def set_cell_text(cell, text: str, bold: bool = False, size: float = 9.0) -> None:
    cell.text = ""
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(1)
    p.paragraph_format.line_spacing = 1.0
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(size)
    run.font.bold = bold
    run._element.rPr.rFonts.set(qn("w:eastAsia"), "SimSun")


def set_table_borders(table) -> None:
    """三线表：顶线 1.5 pt、表头下线 0.75 pt、底线 1.5 pt，其余无。"""
    tbl = table._tbl
    tblPr = tbl.tblPr
    for old in tblPr.findall(qn("w:tblBorders")):
        tblPr.remove(old)
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement(f"w:{edge}")
        if edge == "top":
            el.set(qn("w:val"), "single"); el.set(qn("w:sz"), "12")
        elif edge == "bottom":
            el.set(qn("w:val"), "single"); el.set(qn("w:sz"), "12")
        else:
            el.set(qn("w:val"), "none"); el.set(qn("w:sz"), "0")
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), "000000")
        borders.append(el)
    tblPr.append(borders)

    # 表头行下边框单独加
    for cell in table.rows[0].cells:
        tcPr = cell._tc.get_or_add_tcPr()
        tcBorders = OxmlElement("w:tcBorders")
        bottom = OxmlElement("w:bottom")
        bottom.set(qn("w:val"), "single")
        bottom.set(qn("w:sz"), "6")
        bottom.set(qn("w:space"), "0")
        bottom.set(qn("w:color"), "000000")
        tcBorders.append(bottom)
        tcPr.append(tcBorders)


def repeat_header(row) -> None:
    trPr = row._tr.get_or_add_trPr()
    el = OxmlElement("w:tblHeader")
    el.set(qn("w:val"), "true")
    trPr.append(el)


def main() -> None:
    df = pd.read_csv(SRC, sep="\t", dtype=str).fillna("")

    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Cm(21.0), Cm(29.7)
    for attr in ("left_margin", "right_margin", "top_margin", "bottom_margin"):
        setattr(sec, attr, Cm(2.5))

    normal = doc.styles["Normal"]
    normal.font.name = "Times New Roman"
    normal.font.size = Pt(9)
    normal.element.rPr.rFonts.set(qn("w:eastAsia"), "SimSun")

    # 标题
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(6)
    r = p.add_run(TITLE)
    r.font.name = "Times New Roman"
    r.font.size = Pt(10.5)
    r.font.bold = True
    r._element.rPr.rFonts.set(qn("w:eastAsia"), "SimSun")

    # 表格
    table = doc.add_table(rows=1, cols=len(COLS))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    hdr = table.rows[0]
    for i, name in enumerate(COLS):
        set_cell_text(hdr.cells[i], name, bold=True)
    repeat_header(hdr)

    for _, row in df.iterrows():
        cells = table.add_row().cells
        for i, col in enumerate(COLS):
            set_cell_text(cells[i], str(row[col]))

    set_fixed_layout(table, WIDTHS_CM)
    set_table_borders(table)

    # 表注
    pn = doc.add_paragraph()
    pn.paragraph_format.space_before = Pt(6)
    pn.paragraph_format.space_after = Pt(0)
    lead = pn.add_run("Notes. ")
    lead.font.name = "Times New Roman"
    lead.font.size = Pt(8)
    lead.font.bold = True
    lead._element.rPr.rFonts.set(qn("w:eastAsia"), "SimSun")

    sup = "abcdefgh"
    for i, note in enumerate(NOTES):
        run = pn.add_run(f"({sup[i]}) {note} ")
        run.font.name = "Times New Roman"
        run.font.size = Pt(8)
        run._element.rPr.rFonts.set(qn("w:eastAsia"), "SimSun")

    out = OUT / "Table2_reporting_checklist.docx"
    doc.save(out)
    print(f"已输出: {out}")
    print(f"  行数: {len(df)}  列数: {len(COLS)}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
生成 Table 1 正式稿（Word，横向）

输入：09_tables/Table1_six_definitions.tsv
输出：11_proposal/table1/output/Table1_six_definitions.docx

格式与 Table 2 保持一致（A4、页边距 2.5 cm、Times New Roman、三线表），
因本表 12 列，改用横向页面（文本宽 24.7 cm）。

用法：python 11_proposal/table1/code/make_table1_docx.py
"""

from pathlib import Path

import pandas as pd
from docx import Document
from docx.enum.section import WD_ORIENT
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SRC = ROOT / "09_tables" / "Table1_six_definitions.tsv"
OUT = HERE.parent / "output"
OUT.mkdir(parents=True, exist_ok=True)

TITLE = ("Table 1. Viral fraction of reads under six reporting definitions in six "
         "Chinese alligator gut metagenomes.")

COLS = ["Code", "Definition", "Denominator", "Reference space", "Assignment",
        "W1", "W2", "W3", "S1", "S2", "S3", "Range (%)"]
WIDTHS_CM = [1.1, 4.4, 2.8, 3.0, 2.4] + [1.25] * 6 + [3.5]   # 合计 24.7 cm

NOTES = [
    "Values are percentages: of reads for C1, C2, C5 and C6, and of contigs for C4. "
    "Samples are six fecal shotgun metagenomes of Alligator sinensis (PRJNA539906; "
    "Tang et al., Front Microbiol 2019, doi:10.3389/fmicb.2019.02409).",
    "Clean reads are reads after host removal, i.e. the input to viral screening. "
    "C6 uses the pre-depletion QC read count (host_removal_summary.total_reads × 2) and "
    "shares its numerator with C2; the two rows therefore differ only in the denominator, "
    "by ≤1.2%.",
    "C3 gives the range reported by the original study (0.04% during hibernation to 4.03% "
    "during the active phase; their Supplementary Table S19). That study does not specify "
    "how viral sequences were defined beyond referring to that table, and the value could "
    "not be recomputed here because the original ORF alignments were not retained. C3 is "
    "shown for orientation only and is excluded from every fold-change calculation.",
    "Viral-like hits were identified with DIAMOND blastx against RVDB-prot v32 Unique "
    "(alignment length ≥30 aa, identity ≥40%, E ≤ 1e-5). C1 retains only hits annotated to "
    "structural or replication/transcription categories; C2 applies no category filter.",
    "Contigs were assembled with MEGAHIT and classified with geNomad; vOTUs were clustered "
    "with CD-HIT-EST at 95% identity and 85% coverage of the shorter sequence (n = 9,980).",
    "Values are given at the precision produced by the analysis pipeline; fold changes "
    "between definitions are shown in Fig. 2B and are not multiplicative.",
]


def set_cell_text(cell, text: str, bold: bool = False, size: float = 8.5) -> None:
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


def set_fixed_layout(table, widths_cm) -> None:
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


def set_table_borders(table) -> None:
    tbl = table._tbl
    tblPr = tbl.tblPr
    for old in tblPr.findall(qn("w:tblBorders")):
        tblPr.remove(old)
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement(f"w:{edge}")
        if edge in ("top", "bottom"):
            el.set(qn("w:val"), "single")
            el.set(qn("w:sz"), "12")
        else:
            el.set(qn("w:val"), "none")
            el.set(qn("w:sz"), "0")
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), "000000")
        borders.append(el)
    tblPr.append(borders)

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


def verify_against_fig_source(df: pd.DataFrame) -> None:
    """与 Fig 2 的输入表比对，防止两份表静默漂移。

    本表（09_tables/）供投稿，Fig 2 读的是 08_figures/fig_a1/output/ 下的表；
    两者同源但文件分离，上游重算后若只更新一处，就会出现图与表对不上。
    """
    fig_src = ROOT / "08_figures" / "fig_a1" / "output" / "Table1_five_denominators.tsv"
    if not fig_src.exists():
        print(f"  [跳过一致性校验] 未找到 {fig_src}")
        return

    ref = pd.read_csv(fig_src, sep="\t").set_index("口径")
    samples = ["W1", "W2", "W3", "S1", "S2", "S3"]
    problems = []
    for _, row in df.iterrows():
        code = row["Code"]
        if code not in ref.index:
            continue
        for s in samples:
            mine, theirs = str(row[s]), ref.loc[code, s]
            if mine in ("n.a.", "") or pd.isna(theirs):
                continue
            a, b = float(mine), float(theirs)
            if abs(a - b) > max(0.01, 0.01 * abs(b)):
                problems.append(f"{code}/{s}: 本表 {a} vs 上游 {b}")

    if problems:
        raise SystemExit("一致性校验失败：\n  " + "\n  ".join(problems))
    print("  一致性校验通过（与 fig_a1 输出同源）")


def main() -> None:
    df = pd.read_csv(SRC, sep="\t", dtype=str).fillna("")
    verify_against_fig_source(df)

    doc = Document()
    sec = doc.sections[0]
    sec.orientation = WD_ORIENT.LANDSCAPE
    sec.page_width, sec.page_height = Cm(29.7), Cm(21.0)
    for attr in ("left_margin", "right_margin", "top_margin", "bottom_margin"):
        setattr(sec, attr, Cm(2.5))

    normal = doc.styles["Normal"]
    normal.font.name = "Times New Roman"
    normal.font.size = Pt(8.5)
    normal.element.rPr.rFonts.set(qn("w:eastAsia"), "SimSun")

    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(6)
    r = p.add_run(TITLE)
    r.font.name = "Times New Roman"
    r.font.size = Pt(10.5)
    r.font.bold = True
    r._element.rPr.rFonts.set(qn("w:eastAsia"), "SimSun")

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
            bold = col == "Code"
            set_cell_text(cells[i], str(row[col]), bold=bold)

    set_fixed_layout(table, WIDTHS_CM)
    set_table_borders(table)

    pn = doc.add_paragraph()
    pn.paragraph_format.space_before = Pt(6)
    pn.paragraph_format.space_after = Pt(0)
    lead = pn.add_run("Notes. ")
    lead.font.name = "Times New Roman"
    lead.font.size = Pt(8)
    lead.font.bold = True
    lead._element.rPr.rFonts.set(qn("w:eastAsia"), "SimSun")

    sup = "abcdef"
    for i, note in enumerate(NOTES):
        run = pn.add_run(f"({sup[i]}) {note} ")
        run.font.name = "Times New Roman"
        run.font.size = Pt(8)
        run._element.rPr.rFonts.set(qn("w:eastAsia"), "SimSun")

    out = OUT / "Table1_six_definitions.docx"
    doc.save(out)
    print(f"已输出: {out}")
    print(f"  行数: {len(df)}  列数: {len(COLS)}")


if __name__ == "__main__":
    main()

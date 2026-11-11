"""把两页纸报告 Markdown 渲染为排好版的 DOCX。
A4；正文两页 + 附图两页（第 3 页 Fig M1/M2，第 4 页 Fig M3 + 附表 S1）。
"""
import re
import sys
from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

ROOT = Path(__file__).resolve().parents[1]
MD = ROOT / "10_reports" / "技术简报_扬子鳄肠道病毒组_2026-11-09.md"
# 可选版本后缀：原文件被占用时用 `python build_docx.py v2`
SUFFIX = sys.argv[1] if len(sys.argv) > 1 else ""
OUT = ROOT / "10_reports" / f"技术简报_扬子鳄肠道病毒组_2026-11-09{('_' + SUFFIX) if SUFFIX else ''}.docx"
FIG = ROOT / "08_figures"

FIGS = [
    (FIG / "fig_m1/output/FigM1_v2_signal_validation.png", Cm(13.4),
     "Figure M1 | Sequencing landscape and validation of viral signal. ",
     "**(A)** Q30 bases before (open) and after (filled) trimming, with read retention. "
     "**(B)** Host-aligned fraction after host depletion (log scale); bars, group medians. "
     "**(C)** Viral-like read fraction versus alignment stringency (grey, individual samples; "
     "black, mean of six). The signal collapses above 60% identity, indicating that no reads derive "
     "from genomes closely related to known viruses; dashed line, 0.01% screening threshold. "
     "**(D)** Functional composition of viral-like reads: 47.4% map to metabolic/housekeeping "
     "enzymes carried by giant viruses, only 1.3% to virion structural genes. n = 3 per season; "
     "no statistical test applied."),
    (FIG / "fig_m2/output/FigM2_host_state_viral_community.png", Cm(16.4),
     "Figure M2 | Gut viral communities track host physiological state rather than calendar season. ",
     "**(A)** Read GC content versus fraction of reads mapping to viral contigs. Blue, winter "
     "(hibernating); orange, summer (active). The red ring marks S1 (individual F5), collected in "
     "summer but harbouring a hibernating-type community. **(B)** Bray-Curtis dissimilarity between "
     "viral communities, computed on vOTU-level RPKM after mapping all samples to a unified "
     "reference of 9,980 vOTUs. **(C)** Bacterial 16S community similarity (15-mer cosine); A.F5 "
     "clusters with the winter animals (0.80 vs 0.41 to the summer group), independently confirming "
     "the state assignment derived from viral data. n = 3 per season."),
    (FIG / "fig_m3/output/FigM3_viral_genome_landscape.png", Cm(16.4),
     "Figure M3 | Landscape of assembled viral genomes. ",
     "**(A)** Length, completeness and abundance of the 202 medium- and high-quality viral genomes "
     "(point area scales with RPKM; blue, winter; orange, summer). **(B)** Genomes recovered per "
     "sample, coloured by CheckV quality tier. **(C)** Genome length by quality tier (log scale); "
     "bars, medians. Completeness calls are length-dependent, so the 202 genomes represent a lower "
     "bound on the true number of recoverable viral genomes."),
]

TABLE_S1 = [
    ["样本", "采样期 / 个体", "病毒 contigs", "病毒占比", "读段 GC", "病毒 reads", "中高质量基因组"],
    ["W1", "2016-01 / F2", "549", "1.87%", "50.3%", "2.62%", "19"],
    ["W2", "2016-01 / F1", "213", "1.41%", "45.9%", "3.72%", "10"],
    ["W3", "2016-01 / F6", "926", "4.92%", "45.3%", "3.91%", "26"],
    ["S1", "2015-07 / F5", "739", "2.63%", "46.6%", "2.14%", "17"],
    ["S2", "2015-07 / F4", "5,074", "13.34%", "39.0%", "12.81%", "72"],
    ["S3", "2015-07 / F3", "4,515", "12.70%", "39.7%", "15.23%", "58"],
    ["合计", "6 只个体", "12,016", "7.30%", "—", "—", "202"],
]

BODY_EA, BODY_LATIN = "宋体", "Times New Roman"
HEAD_EA, HEAD_LATIN = "黑体", "Arial"

C_DARK = RGBColor(0x1A, 0x1A, 0x1A)
C_GREY = RGBColor(0x59, 0x59, 0x59)
C_ACCENT = RGBColor(0x0B, 0x4F, 0x6C)


# ---------------------------------------------------------------- 基础工具
def set_font(run, *, ea=BODY_EA, latin=BODY_LATIN, size=9.5, bold=False,
             italic=False, color=C_DARK):
    run.font.name = latin
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.append(rFonts)
    rFonts.set(qn("w:eastAsia"), ea)
    rFonts.set(qn("w:ascii"), latin)
    rFonts.set(qn("w:hAnsi"), latin)


TOKEN = re.compile(r"\*\*\*(.+?)\*\*\*|\*\*(.+?)\*\*|\*(?!\*)([^*]+?)\*")


def add_rich(par, text, *, ea=BODY_EA, latin=BODY_LATIN, size=9.5,
             color=C_DARK, bold_color=None):
    """按 **粗体** / *斜体* 切分写入 run；反引号去掉。"""
    text = text.replace("`", "")
    pos = 0

    def emit(seg, bold=False, italic=False):
        if not seg:
            return
        run = par.add_run(seg)
        set_font(run, ea=ea, latin=latin, size=size, bold=bold, italic=italic,
                 color=(bold_color or color) if bold else color)

    for m in TOKEN.finditer(text):
        emit(text[pos:m.start()])
        if m.group(1) is not None:          # ***粗斜体***
            emit(m.group(1), bold=True, italic=True)
        elif m.group(2) is not None:        # **粗体**
            emit(m.group(2), bold=True)
        else:                                # *斜体*
            emit(m.group(3), italic=True)
        pos = m.end()
    emit(text[pos:])


def para(doc, *, space_before=0, space_after=3, line=14.3, indent=None,
         align=WD_ALIGN_PARAGRAPH.JUSTIFY, keep_next=False):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(space_before)
    pf.space_after = Pt(space_after)
    pf.line_spacing = Pt(line)
    if indent is not None:
        pf.first_line_indent = Cm(indent)
    p.alignment = align
    pf.keep_with_next = keep_next
    pf.widow_control = True
    return p


def shade(el, hexcolor):
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hexcolor)
    el.append(shd)


def bottom_border(par, color="0B4F6C", size="8"):
    pPr = par._p.get_or_add_pPr()
    borders = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), size)
    bottom.set(qn("w:space"), "2")
    bottom.set(qn("w:color"), color)
    borders.append(bottom)
    pPr.append(borders)


def cell_shade(cell, hexcolor):
    shade(cell._tc.get_or_add_tcPr(), hexcolor)


def table_borders(table, color="BFBFBF"):
    tblPr = table._tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement(f"w:{edge}")
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), "4")
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), color)
        borders.append(el)
    tblPr.append(borders)


def add_table(doc, rows, widths, *, size=8.4, center_all=False, line=12):
    ncol = len(rows[0])
    # 3 列表：带 "#" 编号列的用窄首列，其余用常规首列
    if ncol == 3 and str(rows[0][0]).strip() != "#":
        widths = [Cm(3.0), Cm(8.4), Cm(5.4)]
    # 列宽不足时按列数自适应（正文宽 16.8 cm）
    if len(widths) != ncol:
        hdr = [str(c) for c in rows[0]]
        if ncol == 4 and any("属" in h for h in hdr):
            # 含属名的表：第二列留给长属名列表
            widths = [Cm(2.9), Cm(6.6), Cm(3.7), Cm(3.6)]
        elif ncol == 4:
            widths = [Cm(4.2)] * 4
        else:
            widths = [Cm(16.8 / ncol)] * ncol
    t = doc.add_table(rows=len(rows), cols=ncol)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    table_borders(t)
    for ci, w in enumerate(widths):
        t.columns[ci].width = w
    for ri, cells in enumerate(rows):
        for ci in range(ncol):
            cell = t.cell(ri, ci)
            cell.width = widths[ci]
            cp = cell.paragraphs[0]
            cp.text = ""
            cp.paragraph_format.space_before = Pt(1.5)
            cp.paragraph_format.space_after = Pt(1.5)
            cp.paragraph_format.line_spacing = Pt(line)
            centred = center_all or ci == 0 or ri == 0
            cp.alignment = (WD_ALIGN_PARAGRAPH.CENTER if centred
                            else WD_ALIGN_PARAGRAPH.LEFT)
            add_rich(cp, cells[ci] if ci < len(cells) else "", size=size,
                     bold_color=C_ACCENT)
            if ri == 0:
                for r_ in cp.runs:
                    r_.font.bold = True
                cell_shade(cell, "E8F0F4")
    return t


def add_page_number(par):
    run = par.add_run()
    for kind, text in (("begin", None), (None, "PAGE"), ("end", None)):
        if kind:
            fc = OxmlElement("w:fldChar")
            fc.set(qn("w:fldCharType"), kind)
            run._r.append(fc)
        else:
            it = OxmlElement("w:instrText")
            it.set(qn("xml:space"), "preserve")
            it.text = text
            run._r.append(it)
    set_font(run, size=8, color=C_GREY)


# ---------------------------------------------------------------- 解析 Markdown
def parse(md_text):
    blocks, buf, tbl = [], [], []

    def flush_par():
        if buf:
            blocks.append(("p", " ".join(buf).strip()))
            buf.clear()

    def flush_tbl():
        if tbl:
            blocks.append(("table", list(tbl)))
            tbl.clear()

    for raw in md_text.splitlines():
        line = raw.rstrip()
        if line.startswith("|"):
            flush_par()
            if re.fullmatch(r"\|[\s:|-]+\|", line):
                continue
            tbl.append([c.strip() for c in line.strip("|").split("|")])
            continue
        flush_tbl()
        if not line.strip():
            flush_par()
            continue
        if line.startswith("# "):
            flush_par(); blocks.append(("h1", line[2:].strip()))
        elif line.startswith("## "):
            flush_par(); blocks.append(("h2", line[3:].strip()))
        elif line.startswith("### "):
            flush_par(); blocks.append(("h3", line[4:].strip()))
        elif line.startswith("#### "):
            flush_par(); blocks.append(("h4", line[5:].strip()))
        elif line.strip() == "---":
            flush_par()
        elif line.startswith("> "):
            flush_par(); blocks.append(("note", line[2:].strip()))
        elif line.startswith("- "):
            flush_par(); blocks.append(("bullet", line[2:].strip()))
        elif re.match(r"^\d+\.\s", line):
            flush_par(); blocks.append(("num", line.strip()))
        else:
            buf.append(line.strip())
    flush_par()
    flush_tbl()
    return blocks


# ---------------------------------------------------------------- 生成
def render_fig(doc, spec):
    path, width, head, body = spec
    pic = doc.add_paragraph()
    pic.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pic.paragraph_format.space_before = Pt(3)
    pic.paragraph_format.space_after = Pt(2)
    pic.paragraph_format.keep_with_next = True
    pic.add_run().add_picture(str(path), width=width)

    cap = para(doc, space_before=0, space_after=6, line=10.8)
    r = cap.add_run(head)
    set_font(r, size=7.5, bold=True, color=C_DARK)
    add_rich(cap, body, size=7.5, color=C_GREY)


def section_head(doc, text, *, page_break=False):
    p = para(doc, space_after=5, align=WD_ALIGN_PARAGRAPH.LEFT, line=14, keep_next=True)
    if page_break:
        p.paragraph_format.page_break_before = True
    set_font(p.add_run(text), ea=HEAD_EA, latin=HEAD_LATIN, size=11,
             bold=True, color=C_ACCENT)
    bottom_border(p, color="D6E4EA")


def build():
    doc = Document()

    sec = doc.sections[0]
    sec.page_height, sec.page_width = Cm(29.7), Cm(21.0)
    sec.top_margin, sec.bottom_margin = Cm(1.8), Cm(1.7)
    sec.left_margin, sec.right_margin = Cm(2.1), Cm(2.1)
    sec.header_distance, sec.footer_distance = Cm(1.0), Cm(0.9)

    normal = doc.styles["Normal"]
    normal.font.name = BODY_LATIN
    normal.font.size = Pt(9.5)
    normal.element.rPr.rFonts.set(qn("w:eastAsia"), BODY_EA)

    for kind, payload in parse(MD.read_text(encoding="utf-8")):
        if kind == "h1":
            p = para(doc, space_after=2, align=WD_ALIGN_PARAGRAPH.CENTER,
                     line=22, keep_next=True)
            set_font(p.add_run(payload), ea="微软雅黑", latin="Arial",
                     size=17, bold=True, color=C_ACCENT)
        elif kind == "h2":
            p = para(doc, space_after=8, align=WD_ALIGN_PARAGRAPH.CENTER,
                     line=13, keep_next=True)
            set_font(p.add_run(payload), ea=HEAD_EA, latin=HEAD_LATIN,
                     size=9, color=C_GREY)
        elif kind == "h3":
            p = para(doc, space_before=8, space_after=3, line=14,
                     align=WD_ALIGN_PARAGRAPH.LEFT, keep_next=True)
            set_font(p.add_run(payload), ea=HEAD_EA, latin=HEAD_LATIN,
                     size=11, bold=True, color=C_ACCENT)
            bottom_border(p, color="D6E4EA", size="6")
        elif kind == "h4":
            p = para(doc, space_before=6, space_after=2, line=13.5, keep_next=True)
            add_rich(p, payload, ea=HEAD_EA, latin=HEAD_LATIN, size=9.8,
                     color=C_ACCENT, bold_color=C_ACCENT)
        elif kind == "p":
            add_rich(para(doc, indent=0.68), payload, size=9.5)
        elif kind == "bullet":
            p = para(doc, space_after=1.5, line=13.6)
            p.paragraph_format.left_indent = Cm(0.55)
            p.paragraph_format.first_line_indent = Cm(-0.32)
            set_font(p.add_run("· "), size=9.5, color=C_GREY)
            add_rich(p, payload, size=9.3)
        elif kind == "num":
            m = re.match(r"^(\d+)\.\s+(.*)$", payload)
            p = para(doc, space_after=1.5, line=13.6)
            p.paragraph_format.left_indent = Cm(0.55)
            p.paragraph_format.first_line_indent = Cm(-0.55)
            set_font(p.add_run(f"{m.group(1)}. "), size=9.3, bold=True, color=C_ACCENT)
            add_rich(p, m.group(2), size=9.3)
        elif kind == "note":
            p = para(doc, space_before=2, space_after=4, line=13.2)
            p.paragraph_format.left_indent = Cm(0.35)
            shade(p._p.get_or_add_pPr(), "EDF4F7")
            add_rich(p, payload, size=8.8, color=RGBColor(0x24, 0x4A, 0x5A))
        elif kind == "table":
            add_table(doc, payload, [Cm(0.9), Cm(7.0), Cm(8.6)])
            para(doc, space_after=2, line=6)

    # ---- 第 3 页：附图 M1 + M2
    section_head(doc, "附图 / Supplementary figures", page_break=True)
    render_fig(doc, FIGS[0])
    render_fig(doc, FIGS[1])

    # ---- 第 4 页：附图 M3 + 附表 S1
    section_head(doc, "附图（续）与附表 / Supplementary figures (cont.) and table",
                 page_break=True)
    render_fig(doc, FIGS[2])

    th = para(doc, space_before=4, space_after=4, line=13, keep_next=True,
              align=WD_ALIGN_PARAGRAPH.LEFT)
    set_font(th.add_run("附表 S1 ｜ 六样本关键指标 / Supplementary table S1. Sample-level metrics."),
             ea=HEAD_EA, latin=HEAD_LATIN, size=9, bold=True, color=C_ACCENT)

    add_table(doc, TABLE_S1,
              [Cm(1.3), Cm(2.6), Cm(2.5), Cm(2.1), Cm(2.0), Cm(2.3), Cm(3.1)],
              size=8.2, center_all=True, line=11.5)

    note = para(doc, space_before=3, space_after=0, line=11)
    add_rich(note,
             "病毒占比 = 病毒 contigs / 该样本 contigs 总数；中高质量 = CheckV Complete + High + "
             "Medium（完整性 ≥50%）；病毒 reads = 比对到统一 vOTU 参考的 reads 占比。"
             "W / S 前缀分别为 2016-01 与 2015-07 采样，六样本来自六只不同个体、无配对。",
             size=7.5, color=C_GREY)

    # ---- 口径与可复现说明
    ph3 = para(doc, space_before=14, space_after=4, line=13, keep_next=True,
               align=WD_ALIGN_PARAGRAPH.LEFT)
    set_font(ph3.add_run("口径与可复现说明 / Definitions and reproducibility"),
             ea=HEAD_EA, latin=HEAD_LATIN, size=9.5, bold=True, color=C_ACCENT)
    bottom_border(ph3, color="D6E4EA", size="6")

    NOTES = [
        ("病毒样（viral-like）",
         "DIAMOND blastx 比对 RVDB-prot v32（Unique, 783,103 蛋白），E ≤ 1e-5、一致性 ≥40%、"
         "比对长度 ≥30 aa；六样本均值 0.693%，仅作**上限**参考。"),
        ("病毒特异（viral-specific）",
         "仅计结构蛋白与复制/转录基因，均值 0.103%，为**本报告主指标**。"),
        ("中高质量基因组",
         "CheckV 分级：Complete（完整性 ≥90%）、High（≥90% 且无污染）、Medium（≥50%）。"),
        ("G1 闸门",
         "判据为病毒 reads ≥0.01% 且 ≥10⁴ 条。按病毒特异口径达标（约超阈值 10 倍）；"
         "按仅结构蛋白口径（0.0089%）则不达标——故主指标的选择直接决定闸门结论。"),
        ("数据与代码",
         "原始数据 PRJNA539906 与 SRP315843（16S）；作图脚本见 08_figures/fig_m1–m3/code/，"
         "结果表见 05_c_stage/，服务器端流程见 workflow/server_run_c.sh。"
         "全部数值由真实计算生成，无占位数据。"),
    ]
    for label, text in NOTES:
        p = para(doc, space_after=2.2, line=12.4, align=WD_ALIGN_PARAGRAPH.LEFT)
        p.paragraph_format.left_indent = Cm(0.55)
        p.paragraph_format.first_line_indent = Cm(-0.55)
        set_font(p.add_run("· "), size=8.2, color=C_GREY)
        set_font(p.add_run(f"{label}："), size=8.2, bold=True, color=C_ACCENT)
        add_rich(p, text, size=8.2, color=RGBColor(0x33, 0x33, 0x33))

    footer = doc.sections[0].footer
    fp = footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_page_number(fp)

    doc.save(OUT)
    print(f"已生成 {OUT}")


if __name__ == "__main__":
    build()

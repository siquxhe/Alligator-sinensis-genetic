#!/usr/bin/env python3
"""
生成 Zotero 可识别的文献表

输出：
  11_proposal/references/refs.ris                      RIS 格式，直接拖入 Zotero
  11_proposal/references/references_table.docx         人读表格（同内容）
  11_proposal/references/references_table.md           纯文本版

用法：python 11_proposal/references/code/make_refs.py
"""

from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

HERE = Path(__file__).resolve().parent
OUT = HERE.parent

# ---------------------------------------------------------------- 文献数据
# type: JOUR=期刊论文, UNPB=预印本（Zotero 会建为 Unpublished/Preprint 条目）
REFS = [
    dict(
        group="一、核心（直接决定论文怎么写）",
        ty="JOUR",
        authors=[("Forbes", "Matthew"), ("Ng", "Duncan Y. K."), ("Boggan", "Róisín M."),
                 ("Frick-Kretschmer", "Andrea"), ("Durham", "Jillian"), ("Lorenz", "Oliver")],
        title="Benchmarking of Human Read Removal Strategies for Viral and Microbial Metagenomics",
        journal="Cell Reports Methods", year="2025", volume="", issue="", pages="",
        doi="10.1016/j.crmeth.2025.101218", pmid="",
        why="分母轴最近邻。它评的是宿主 reads 去除的性能与下游影响，不是病毒占比——正文必须主动划清界限",
    ),
    dict(
        group="一、核心（直接决定论文怎么写）",
        ty="UNPB",
        authors=[],
        title="Benchmarking and integration of viral prediction tools to uncover viral dark matter across divergent low abundance metagenomes",
        journal="bioRxiv", year="2026", volume="", issue="", pages="",
        doi="10.64898/2026.10.14.759168", pmid="",
        why="11 种病毒识别工具基准，结论是两两组合 + Kraken2X 过滤优于单工具；支持我们'无单一最佳流程'的论点",
    ),
    dict(
        group="一、核心（直接决定论文怎么写）",
        ty="UNPB",
        authors=[("Kosmopoulos", "James C."), ("Martin", "Cody"), ("Wainaina", "James M."),
                 ("Bolduc", "Benjamin"), ("Urvoy", "Marion"), ("Sullivan", "Matthew B."),
                 ("Anantharaman", "Karthik")],
        title="CheckAMG: Accurate Identification of Auxiliary Viral Genes with Genome-Language Models",
        journal="bioRxiv", year="2026", volume="", issue="", pages="",
        doi="10.64898/2026.09.23.753886", pmid="42818345",
        why="明确承认'病毒 vs 细胞来源归属存在歧义'，是 47.4% 代谢基因那段最硬的背书；同时是 cargo 判定的压力来源",
    ),
    dict(
        group="一、核心（直接决定论文怎么写）",
        ty="JOUR",
        authors=[("Roux", "Simon"), ("Adriaenssens", "Evelien M."), ("Dutilh", "Bas E."),
                 ("Koonin", "Eugene V."), ("Kropinski", "Andrew M."), ("Krupovic", "Mart"),
                 ("Kuhn", "Jens H."), ("Lavigne", "Rob"), ("Brister", "J. Rodney"), ("Varsani", "Arvind")],
        title="Minimum Information about an Uncultivated Virus Genome (MIUViG)",
        journal="Nature Biotechnology", year="2019", volume="37", issue="1", pages="29-37",
        doi="10.1038/nbt.4306", pmid="30556814",
        why="唯一现成的病毒组报告标准，但只覆盖基因组、不覆盖 read 层占比——这正是我们的空位",
    ),
    dict(
        group="二、决定 Table 2 站位（最易被忽略）",
        ty="JOUR",
        authors=[("Mirzayi", "Chloe"), ("Renson", "Audrey"), ("Zohra", "Fatima"),
                 ("Elsafoury", "Shaimaa"), ("Geistlinger", "Ludwig"), ("Kasselman", "Lora J."),
                 ("Eckenrode", "Kelly"), ("van de Wijgert", "Janneke"), ("Loughman", "Amy"),
                 ("Marques", "Francine Z.")],
        title="Reporting guidelines for human microbiome research: the STORMS checklist",
        journal="Nature Medicine", year="2021", volume="27", issue="11", pages="1885-1892",
        doi="10.1038/s41591-021-01552-x", pmid="34789871",
        why="17 项清单、6 章节，是最成功的报告规范范式；其第 4.5 项已要求报告是否去除人源 DNA，Table 2 必须与之划界",
    ),
    dict(
        group="三、方法可信度（被问到能答）",
        ty="JOUR",
        authors=[("Camargo", "Antonio Pedro"), ("Roux", "Simon"), ("Schulz", "Frederik"),
                 ("Babinski", "Michal"), ("Xu", "Yan"), ("Hu", "Bin"), ("Chain", "Patrick S. G."),
                 ("Nayfach", "Stephen"), ("Kyrpides", "Nikos C.")],
        title="Identification of mobile genetic elements with geNomad",
        journal="Nature Biotechnology", year="2024", volume="42", issue="8", pages="1303-1312",
        doi="10.1038/s41587-023-01953-y", pmid="37735266",
        why="C4 的来源工具；审稿人会问其 MCC 95.3% 的适用范围",
    ),
    dict(
        group="三、方法可信度（被问到能答）",
        ty="JOUR",
        authors=[("Nayfach", "Stephen"), ("Camargo", "Antonio Pedro"), ("Schulz", "Frederik"),
                 ("Eloe-Fadrosh", "Emiley"), ("Roux", "Simon"), ("Kyrpides", "Nikos C.")],
        title="CheckV assesses the quality and completeness of metagenome-assembled viral genomes",
        journal="Nature Biotechnology", year="2021", volume="39", issue="5", pages="578-585",
        doi="10.1038/s41587-020-00774-7", pmid="",
        why="202 条基因组 Complete/High/Medium 分级的依据",
    ),
    dict(
        group="三、方法可信度（被问到能答）",
        ty="JOUR",
        authors=[("Roux", "Simon"), ("Camargo", "Antonio Pedro"), ("Coutinho", "Felipe H."),
                 ("Dabdoub", "Shareef M."), ("Dutilh", "Bas E."), ("Nayfach", "Stephen"),
                 ("Tritt", "Andrew")],
        title="iPHoP: An integrated machine learning framework to maximize host prediction for metagenome-derived viruses of archaea and bacteria",
        journal="PLoS Biology", year="2023", volume="21", issue="4", pages="e3002083",
        doi="10.1371/journal.pbio.3002083", pmid="37083735",
        why="宿主预测工具；我们属级只有 2/5 的那个结果出自它",
    ),
    dict(
        group="四、判断是否重复别人",
        ty="JOUR",
        authors=[("Sáenz", "Johan S."), ("Yergaliyev", "Timur"), ("Rios-Galicia", "Bibiana"),
                 ("Seifert", "Jana"), ("Camarinha-Silva", "Amélia")],
        title="The chicken gut virome: spatial structuring and extensive diversity of 19,778 viral populations",
        journal="mSystems", year="2026", volume="11", issue="4", pages="e00191-26",
        doi="10.1128/msystems.00191-26", pmid="41910132",
        why="第二数据集来源。注意它的写法：1,514 样本、19,778 vOTU，病毒丰度只给'mapped reads 作为代理'（1.10–1.84%）",
    ),
    dict(
        group="四、判断是否重复别人",
        ty="JOUR",
        authors=[("Tang", "Ke-Yi"), ("Wang", "Zhen-Wei"), ("Wan", "Qiu-Hong"), ("Fang", "Sheng-Guo")],
        title="Metagenomics Reveals Seasonal Functional Adaptation of the Gut Microbiome to Host Feeding and Fasting in the Chinese Alligator",
        journal="Frontiers in Microbiology", year="2019", volume="10", issue="", pages="2409",
        doi="10.3389/fmicb.2019.02409", pmid="31708889",
        why="扬子鳄原始数据来源；C3 那个 0.04–4.03% 出自它，且原文未说清怎么算的",
    ),
    dict(
        group="五、补充（备查）",
        ty="UNPB",
        authors=[],
        title="LEMMIv2: Benchmarking Framework for Metagenomic and 16S Amplicon Profilers with a Catalogue of Evaluated Tools",
        journal="bioRxiv", year="2025", volume="", issue="", pages="",
        doi="10.1101/2025.03.06.641904", pmid="",
        why="持续基准测试框架，支持'参考库/平台决定结论'",
    ),
    dict(
        group="五、补充（备查）",
        ty="JOUR",
        authors=[("Hegarty", "Bridget"), ("Riddell", "James V."), ("Bastien", "Eric"),
                 ("Langenfeld", "Kathryn"), ("Lindback", "Morgan"), ("Saini", "Jaspreet S."),
                 ("Wing", "Anthony"), ("Zhang", "Jessica"), ("Duhaime", "Melissa")],
        title="Benchmarking informatics approaches for virus discovery: caution is needed when combining in silico identification methods",
        journal="mSystems", year="2024", volume="9", issue="3", pages="e01105-23",
        doi="10.1128/msystems.01105-23", pmid="38376167",
        why="组合工具并不必然更优；与'多口径并列'的论点呼应",
    ),
]


def ris_text(refs) -> str:
    out = []
    for r in refs:
        out.append(f"TY  - {r['ty']}")
        for last, first in r["authors"]:
            out.append(f"AU  - {last}, {first}")
        out.append(f"TI  - {r['title']}")
        if r["journal"]:
            out.append(f"T2  - {r['journal']}")
        out.append(f"PY  - {r['year']}")
        if r["volume"]:
            out.append(f"VL  - {r['volume']}")
        if r["issue"]:
            out.append(f"IS  - {r['issue']}")
        if r["pages"]:
            if "-" in r["pages"] and not r["pages"].startswith("e"):
                sp, ep = r["pages"].split("-", 1)
                out.append(f"SP  - {sp}")
                out.append(f"EP  - {ep}")
            else:
                out.append(f"SP  - {r['pages']}")
        if r["doi"]:
            out.append(f"DO  - {r['doi']}")
            out.append(f"UR  - https://doi.org/{r['doi']}")
        if r["pmid"]:
            out.append(f"AN  - PMID:{r['pmid']}")
        out.append(f"KW  - {r['group'].split('（')[0]}")
        if r["ty"] == "UNPB":
            out.append("KW  - preprint")
        out.append(f"N1  - {r['why']}")
        out.append("ER  - ")
        out.append("")
    return "\n".join(out)


def set_cell(cell, text, bold=False, size=8.5):
    cell.text = ""
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(1)
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(size)
    r.font.bold = bold
    r._element.rPr.rFonts.set(qn("w:eastAsia"), "SimSun")


def fixed_layout(table, widths):
    tbl = table._tbl
    tblPr = tbl.tblPr
    for old in tblPr.findall(qn("w:tblLayout")):
        tblPr.remove(old)
    lay = OxmlElement("w:tblLayout")
    lay.set(qn("w:type"), "fixed")
    tblPr.append(lay)
    grid = tbl.find(qn("w:tblGrid"))
    if grid is not None:
        for gc, w in zip(grid.findall(qn("w:gridCol")), widths):
            gc.set(qn("w:w"), str(int(w * 567)))
    for row in table.rows:
        for cell, w in zip(row.cells, widths):
            cell.width = Cm(w)


def borders(table):
    tbl = table._tbl
    tblPr = tbl.tblPr
    for old in tblPr.findall(qn("w:tblBorders")):
        tblPr.remove(old)
    b = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement(f"w:{edge}")
        if edge in ("top", "bottom"):
            el.set(qn("w:val"), "single"); el.set(qn("w:sz"), "12")
        elif edge == "insideH":
            el.set(qn("w:val"), "single"); el.set(qn("w:sz"), "4")
        else:
            el.set(qn("w:val"), "none"); el.set(qn("w:sz"), "0")
        el.set(qn("w:space"), "0"); el.set(qn("w:color"), "000000")
        b.append(el)
    tblPr.append(b)


GROUP_SHORT = {
    "一、核心（直接决定论文怎么写）": "一\n核心",
    "二、决定 Table 2 站位（最易被忽略）": "二\n表格定位",
    "三、方法可信度（被问到能答）": "三\n方法依据",
    "四、判断是否重复别人": "四\n背景对照",
    "五、补充（备查）": "五\n补充",
}


def short_authors(r):
    if not r["authors"]:
        return "bioRxiv 预印本"
    first = r["authors"][0][0]
    return f"{first} et al." if len(r["authors"]) > 1 else first


def build_docx(refs, path):
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Cm(29.7), Cm(21.0)   # 横向
    for attr in ("left_margin", "right_margin", "top_margin", "bottom_margin"):
        setattr(sec, attr, Cm(2.0))

    normal = doc.styles["Normal"]
    normal.font.name = "Times New Roman"
    normal.font.size = Pt(9)
    normal.element.rPr.rFonts.set(qn("w:eastAsia"), "SimSun")

    t = doc.add_paragraph()
    t.paragraph_format.space_after = Pt(4)
    r = t.add_run("推荐文献表（可与 refs.ris 配套导入 Zotero）")
    r.font.name = "Times New Roman"; r.font.size = Pt(11); r.font.bold = True
    r._element.rPr.rFonts.set(qn("w:eastAsia"), "SimSun")

    sub = doc.add_paragraph()
    sub.paragraph_format.space_after = Pt(8)
    rs = sub.add_run("导入方式：Zotero → 文件 → 导入 → 选择 refs.ris（或直接把 refs.ris 拖进 Zotero 窗口）。"
                     "预印本会建为 Unpublished/Preprint 条目，可按需改类型。")
    rs.font.name = "Times New Roman"; rs.font.size = Pt(8)
    rs._element.rPr.rFonts.set(qn("w:eastAsia"), "SimSun")

    cols = ["分组", "文献", "出处", "DOI / PMID", "为什么读"]
    widths = [3.4, 4.6, 5.2, 5.0, 7.5]
    table = doc.add_table(rows=1, cols=len(cols))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    for i, c in enumerate(cols):
        set_cell(table.rows[0].cells[i], c, bold=True)

    for ref in refs:
        cells = table.add_row().cells
        cite = f"{short_authors(ref)} ({ref['year']})"
        src = ref["journal"] + (f" {ref['volume']}" if ref["volume"] else "")
        if ref["pages"]:
            src += f": {ref['pages']}"
        ids = ref["doi"]
        if ref["pmid"]:
            ids += f"\nPMID {ref['pmid']}"
        set_cell(cells[0], GROUP_SHORT.get(ref["group"], ref["group"]))
        set_cell(cells[1], cite + "\n" + ref["title"])
        set_cell(cells[2], src)
        set_cell(cells[3], ids)
        set_cell(cells[4], ref["why"])

    fixed_layout(table, widths)
    borders(table)
    doc.save(path)


def build_md(refs, path):
    lines = ["# 推荐文献表", "", "> Zotero 导入请用同目录的 `refs.ris`（本文件为人读版）", ""]
    cur = None
    for r in refs:
        if r["group"] != cur:
            cur = r["group"]
            lines += ["", f"## {cur}", "",
                      "| 文献 | 出处 | DOI / PMID | 为什么读 |", "|---|---|---|---|"]
        src = r["journal"] + (f" {r['volume']}" if r["volume"] else "")
        if r["issue"]:
            src += f"({r['issue']})"
        if r["pages"]:
            src += f": {r['pages']}"
        ids = r["doi"] + (f"<br>PMID {r['pmid']}" if r["pmid"] else "")
        lines.append(f"| **{short_authors(r)} ({r['year']})**<br>{r['title']} | {src} | {ids} | {r['why']} |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    ris = OUT / "refs.ris"
    ris.write_text(ris_text(REFS), encoding="utf-8")
    build_docx(REFS, OUT / "references_table.docx")
    build_md(REFS, OUT / "references_table.md")
    print(f"ris  : {ris}  ({len(REFS)} 条)")
    print(f"docx : {OUT / 'references_table.docx'}")
    print(f"md   : {OUT / 'references_table.md'}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
生成图注正式稿（Fig 1–3）

输出：11_proposal/legends/output/Figure_legends.docx
格式：A4 纵向、页边距 2.5 cm、Times New Roman 11 pt、1.5 倍行距、两端对齐

文本标记：**加粗**、_斜体_（仅用于物种名），其余按正文处理。
改文字请改本文件 LEGENDS，再重跑。

用法：python 11_proposal/legends/code/make_legends_docx.py
"""

import re
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "output"
OUT.mkdir(parents=True, exist_ok=True)

LEGENDS = [
    (
        "Figure 1. ",
        "Four reporting decisions determine the viral fraction of a gut metagenome.",
        "Each row is a choice that has to be made before a viral fraction can be reported: "
        "denominator, reference space, category filter, and statistical unit. Boxes list the "
        "alternatives available at each decision. Values on the right are median fold changes "
        "measured in this dataset with the other dimensions held fixed, from six fecal "
        "metagenomes of _Alligator sinensis_ (PRJNA539906; n = 6). Across all definitions and "
        "samples the observed span is 171× (0.089–15.2%). These fold changes are not "
        "multiplicative: 1.01 × 5.6 × 7.1 × 5.4 ≈ 217, whereas the measured span is 171×, "
        "because each ratio derives from a different sample and a different pair of "
        "definitions. Within a single sample, definitions alone span 22.2–124.8×, and the "
        "additional sample effect is 1.37× (Fig. 2). The denominator row shows a near-unity "
        "effect because host reads make up only 0.07–2.51% of these libraries; this reflects "
        "the low host content of fecal samples and is not a general property of metagenomes.",
    ),
    (
        "Figure 2. ",
        "Six definitions of the same measurement span 171-fold.",
        "**(A)** Viral fraction of reads under six reporting definitions (C1, C2, C6, C3, C4 "
        "and C5; defined in Table 1) for six fecal metagenomes. Points are individual samples "
        "(W1–W3, hibernating; S1–S3, active); horizontal bars are medians across the six "
        "samples. The y axis is logarithmic. C3 is a literature-reported range (0.04–4.03%) "
        "with no per-sample values; it is drawn as a grey band for orientation only and is "
        "excluded from every fold-change calculation. C2 and C6 share the same numerator and "
        "differ only in whether host reads are retained in the denominator; the bracket marks "
        "their ≤1.2% difference. **(B)** Fold change between definitions, computed within each "
        "sample (n = 6) and summarised as boxplots; the dashed line marks no change and numbers "
        "above the boxes are medians. Definitions are not independent: the product of the four "
        "median ratios (≈217) exceeds the observed 171-fold span.",
    ),
    (
        "Figure 3. ",
        "The number of shared vOTUs is a function of the detection threshold.",
        "**(A)** Number of vOTUs detected in all six samples under six detection criteria: "
        "contig-level presence (0 vOTUs) and read-level abundance at RPKM > 0 (783), ≥0.01 "
        "(517), ≥0.1 (63), ≥1 (5) and ≥10 (1). The y axis is logarithmic. **(B)** Proportion of "
        "vOTUs detected in a single sample under the same criteria. The relationship is "
        "U-shaped, and the two ends have opposite causes: the high value at contig level "
        "(84.5%) reflects assembly fragmentation, whereas the high value at RPKM ≥ 10 (55.2%) "
        "reflects genuine sample specificity of abundant viruses. **(C)** Jaccard similarity for "
        "all 15 sample pairs, computed either from contig presence or from abundance-weighted "
        "reads (RPKM ≥ 1); horizontal bars are medians (0.0065 and 0.0234, a 3.6-fold "
        "difference). Throughout, n = 6 samples. The contig-level value of zero should not be "
        "read as an absence of shared viruses: the same virus can assemble into different "
        "fragments in different samples.",
    ),
]

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

    for label, title, body in LEGENDS:
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
    print(f"  图注数: {len(LEGENDS)}")
    for _, title, body in LEGENDS:
        print(f"  {len(title) + len(body)} 字符 | {title[:52]}...")


if __name__ == "__main__":
    main()

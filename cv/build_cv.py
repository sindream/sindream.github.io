#!/usr/bin/env python3
"""Build Woojae Shin's paper-led public research CV."""

from __future__ import annotations

import html
import json
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = Path(__file__).with_name("cv_data.json")
OUTPUT_PATH = ROOT / "assets" / "cv" / "woojae-shin-cv.pdf"

BLACK = colors.HexColor("#050607")
INK = colors.HexColor("#111416")
WHITE = colors.HexColor("#F4F6F6")
MUTED = colors.HexColor("#626B6D")
MUTED_LIGHT = colors.HexColor("#A6AFB1")
ACCENT = colors.HexColor("#2B8F8A")
ACCENT_LIGHT = colors.HexColor("#63D7D1")
LINE = colors.HexColor("#CCD0CE")
PAPER = colors.HexColor("#F2F2ED")


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def emphasize_name(authors: str, name: str) -> str:
    safe_authors = esc(authors)
    safe_name = esc(name)
    return safe_authors.replace(safe_name, f"<b>{safe_name}</b>")


def page_decoration(canvas, document):
    canvas.saveState()
    width, _ = A4
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.45)
    canvas.line(document.leftMargin, 12 * mm, width - document.rightMargin, 12 * mm)
    canvas.setFont("Helvetica", 6.8)
    canvas.setFillColor(MUTED)
    canvas.drawString(document.leftMargin, 8.3 * mm, "Woojae Shin - Research CV")
    canvas.drawRightString(width - document.rightMargin, 8.3 * mm, f"Page {document.page}")
    canvas.restoreState()


def section_header(title: str, styles: dict[str, ParagraphStyle]) -> Table:
    table = Table(
        [[Paragraph(esc(title.upper()), styles["section"]), Paragraph("RESEARCH PROFILE", styles["section_meta"])]],
        colWidths=[81 * mm, 81 * mm],
    )
    table.setStyle(
        TableStyle(
            [
                ("LINEABOVE", (0, 0), (-1, 0), 0.8, INK),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return table


def build() -> Path:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    document = SimpleDocTemplate(
        str(OUTPUT_PATH),
        pagesize=A4,
        rightMargin=16 * mm,
        leftMargin=16 * mm,
        topMargin=14 * mm,
        bottomMargin=17 * mm,
        title=f"{data['name']} - Research CV",
        author=data["name"],
        subject="Paper-led public research curriculum vitae",
        creator="ReportLab",
    )

    base = getSampleStyleSheet()
    styles = {
        "name": ParagraphStyle(
            "Name",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=27,
            leading=28,
            textColor=WHITE,
            spaceAfter=2.2 * mm,
        ),
        "role": ParagraphStyle(
            "Role",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=9.4,
            leading=12.3,
            textColor=ACCENT_LIGHT,
            spaceAfter=1 * mm,
        ),
        "affiliation": ParagraphStyle(
            "Affiliation",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=7.6,
            leading=10.5,
            textColor=MUTED_LIGHT,
        ),
        "links": ParagraphStyle(
            "Links",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=7.4,
            leading=11.5,
            alignment=TA_RIGHT,
            textColor=MUTED_LIGHT,
        ),
        "body": ParagraphStyle(
            "Body",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=8.35,
            leading=11.6,
            textColor=INK,
            spaceAfter=0,
        ),
        "small": ParagraphStyle(
            "Small",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=7.1,
            leading=9.6,
            textColor=MUTED,
            spaceAfter=0,
        ),
        "section": ParagraphStyle(
            "Section",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=8.2,
            leading=10,
            textColor=INK,
            spaceAfter=0,
        ),
        "section_meta": ParagraphStyle(
            "SectionMeta",
            parent=base["Normal"],
            fontName="Courier",
            fontSize=6.7,
            leading=10,
            alignment=TA_RIGHT,
            textColor=MUTED,
        ),
        "label": ParagraphStyle(
            "Label",
            parent=base["Normal"],
            fontName="Courier-Bold",
            fontSize=6.5,
            leading=8.5,
            textColor=ACCENT,
        ),
        "value": ParagraphStyle(
            "Value",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=8.2,
            leading=10.5,
            textColor=INK,
        ),
        "period": ParagraphStyle(
            "Period",
            parent=base["Normal"],
            fontName="Courier-Bold",
            fontSize=7.2,
            leading=9.5,
            textColor=ACCENT,
        ),
        "entry_title": ParagraphStyle(
            "EntryTitle",
            parent=base["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=8.8,
            leading=10.8,
            textColor=INK,
            spaceAfter=0.8 * mm,
        ),
        "entry_text": ParagraphStyle(
            "EntryText",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=7.05,
            leading=9.2,
            textColor=MUTED,
            spaceAfter=0.4 * mm,
        ),
        "footer_note": ParagraphStyle(
            "FooterNote",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=6.6,
            leading=8.8,
            textColor=MUTED,
        ),
    }

    links = (
        f'<link href="{esc(data["website"])}" color="#63D7D1">sindream.github.io</link><br/>'
        f'<link href="{esc(data["orcid"])}" color="#63D7D1">ORCID 0000-0002-6155-3712</link>'
    )
    header = Table(
        [[
            [
                Paragraph(esc(data["name"]), styles["name"]),
                Paragraph(esc(data["role"]), styles["role"]),
                Paragraph(esc(data["affiliation"]), styles["affiliation"]),
            ],
            Paragraph(links, styles["links"]),
        ]],
        colWidths=[116 * mm, 46 * mm],
    )
    header.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), BLACK),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (0, 0), 12),
                ("RIGHTPADDING", (0, 0), (0, 0), 8),
                ("LEFTPADDING", (1, 0), (1, 0), 8),
                ("RIGHTPADDING", (1, 0), (1, 0), 12),
                ("TOPPADDING", (0, 0), (-1, -1), 11),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 11),
            ]
        )
    )

    identity = Table(
        [[
            [Paragraph("FULL NAME", styles["label"]), Paragraph(esc(data["name"]), styles["value"])],
            [Paragraph("DATE OF BIRTH", styles["label"]), Paragraph(esc(data["date_of_birth"]), styles["value"])],
            [Paragraph("AGE", styles["label"]), Paragraph(f'{esc(data["age"])} <font color="#626B6D">as of {esc(data["age_as_of"])}</font>', styles["value"])],
        ]],
        colWidths=[54 * mm, 54 * mm, 54 * mm],
    )
    identity.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), PAPER),
                ("BOX", (0, 0), (-1, -1), 0.5, LINE),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )

    story = [header, Spacer(1, 3 * mm), identity, Spacer(1, 3.2 * mm)]
    story.extend(
        [
            section_header("Profile", styles),
            Paragraph(esc(data["profile"]), styles["body"]),
            Spacer(1, 3.2 * mm),
            section_header("Education", styles),
        ]
    )

    for item in data["education"]:
        education_row = Table(
            [[
                Paragraph(esc(item["period"]), styles["period"]),
                [
                    Paragraph(esc(item["degree"]), styles["entry_title"]),
                    Paragraph(esc(item["institution"]), styles["entry_text"]),
                ],
            ]],
            colWidths=[31 * mm, 131 * mm],
        )
        education_row.setStyle(
            TableStyle(
                [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 0),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                    ("TOPPADDING", (0, 0), (-1, -1), 1.5),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5),
                ]
            )
        )
        story.append(KeepTogether([education_row]))

    story.extend([Spacer(1, 1.2 * mm), section_header("Selected Publications", styles)])
    for publication in data["publications"]:
        title = (
            f'<link href="{esc(publication["doi"])}" color="#111416">'
            f'{esc(publication["title"])} <font color="#2B8F8A">[DOI]</font></link>'
        )
        details = (
            f'{emphasize_name(publication["authors"], data["name"])}<br/>'
            f'<font color="#2B8F8A">{esc(publication["venue"])}</font>'
        )
        publication_row = Table(
            [[
                Paragraph(esc(publication["year"]), styles["period"]),
                [Paragraph(title, styles["entry_title"]), Paragraph(details, styles["entry_text"])],
            ]],
            colWidths=[18 * mm, 144 * mm],
        )
        publication_row.setStyle(
            TableStyle(
                [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 0),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                    ("TOPPADDING", (0, 0), (-1, -1), 1),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ]
            )
        )
        story.append(KeepTogether([publication_row]))

    story.extend(
        [
            Spacer(1, 1.2 * mm),
            section_header("Research Interests", styles),
            Paragraph(" <font color='#2B8F8A'>/</font> ".join(esc(item) for item in data["research_interests"]), styles["body"]),
            Spacer(1, 3 * mm),
            Paragraph(
                f'Last updated {esc(data["updated"])}. Publication metadata verified through the public ORCID and DOI records.',
                styles["footer_note"],
            ),
        ]
    )

    document.build(story, onFirstPage=page_decoration, onLaterPages=page_decoration)
    return OUTPUT_PATH


if __name__ == "__main__":
    print(build())

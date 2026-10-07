#!/usr/bin/env python3
"""Build Woojae Shin's public academic CV."""

from __future__ import annotations

import html
import json
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import CondPageBreak, KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = Path(__file__).with_name("cv_data.json")
OUTPUT_PATH = ROOT / "assets" / "cv" / "woojae-shin-cv.pdf"
FONT_DIR = ROOT / "assets" / "fonts"

INK = colors.HexColor("#18201D")
MUTED = colors.HexColor("#68716D")
ACCENT = colors.HexColor("#287E73")
LINE = colors.HexColor("#CDD4D0")
SOFT = colors.HexColor("#EEF2EF")
CONTENT_WIDTH = 178 * mm


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def emphasize_name(authors: str, name: str) -> str:
    safe_authors = esc(authors)
    safe_name = esc(name)
    return safe_authors.replace(safe_name, f"<b>{safe_name}</b>")


def register_fonts() -> None:
    pdfmetrics.registerFont(TTFont("Nunito", FONT_DIR / "nunito-sans-regular.ttf"))
    pdfmetrics.registerFont(TTFont("Nunito-Semibold", FONT_DIR / "nunito-sans-semibold.ttf"))
    pdfmetrics.registerFont(TTFont("Nunito-Bold", FONT_DIR / "nunito-sans-bold.ttf"))
    pdfmetrics.registerFontFamily(
        "Nunito",
        normal="Nunito",
        bold="Nunito-Bold",
        italic="Nunito",
        boldItalic="Nunito-Bold",
    )


def page_decoration(canvas, document) -> None:
    canvas.saveState()
    width, _ = A4
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.45)
    canvas.line(document.leftMargin, 12 * mm, width - document.rightMargin, 12 * mm)
    canvas.setFont("Nunito", 7.2)
    canvas.setFillColor(MUTED)
    canvas.drawString(document.leftMargin, 8.3 * mm, "Woojae Shin - Curriculum Vitae")
    canvas.drawRightString(width - document.rightMargin, 8.3 * mm, f"Page {document.page}")
    canvas.restoreState()


def section_header(title: str, styles: dict[str, ParagraphStyle]) -> Table:
    table = Table(
        [[Paragraph(esc(title), styles["section"])]],
        colWidths=[CONTENT_WIDTH],
        hAlign="LEFT",
    )
    table.setStyle(
        TableStyle(
            [
                ("LINEBELOW", (0, 0), (-1, -1), 0.7, LINE),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    return table


def publication_row(
    publication: dict[str, str],
    name: str,
    styles: dict[str, ParagraphStyle],
) -> Table:
    link_label = publication.get("link_label", "Link")
    title = esc(publication["title"])
    if publication.get("url"):
        title = (
            f'<link href="{esc(publication["url"])}" color="#18201D">'
            f'{title} <font color="#287E73">[{esc(link_label)}]</font></link>'
        )
    if publication.get("project_url"):
        title += (
            f' <link href="{esc(publication["project_url"])}" color="#287E73">'
            "[Project]</link>"
        )

    details = (
        f'{emphasize_name(publication["authors"], name)}<br/>'
        f'<font color="#287E73">{esc(publication["venue"])}</font>'
    )
    row = Table(
        [[
            Paragraph(esc(publication["year"]), styles["period"]),
            [Paragraph(title, styles["publication_title"]), Paragraph(details, styles["publication_text"])],
        ]],
        colWidths=[18 * mm, 144 * mm],
    )
    row.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 1.5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5.5),
            ]
        )
    )
    return row


def award_row(
    award: dict[str, str],
    styles: dict[str, ParagraphStyle],
) -> Table:
    title = esc(award["title"])
    link_parts = []
    if award.get("virtual_url"):
        link_parts.append(
            f'<link href="{esc(award["virtual_url"])}" color="#287E73">'
            f'[{esc(award.get("virtual_link_label", "Virtual result"))}]</link>'
        )
    if award.get("url"):
        link_parts.append(
            f'<link href="{esc(award["url"])}" color="#287E73">'
            f'[{esc(award.get("link_label", "Official recap"))}]</link>'
        )
    if link_parts:
        title += " " + " ".join(link_parts)

    details = (
        f'<font color="#287E73"><b>{esc(award["distinction"])}</b></font><br/>'
        f'{esc(award["organization"])}<br/>'
        f'{esc(award["note"])}'
    )
    row = Table(
        [[
            Paragraph(esc(award["year"]), styles["period"]),
            [Paragraph(title, styles["entry_title"]), Paragraph(details, styles["entry_text"])],
        ]],
        colWidths=[31 * mm, 131 * mm],
    )
    row.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5.5),
            ]
        )
    )
    return row


def build() -> Path:
    register_fonts()
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    document = SimpleDocTemplate(
        str(OUTPUT_PATH),
        pagesize=A4,
        rightMargin=16 * mm,
        leftMargin=16 * mm,
        topMargin=14 * mm,
        bottomMargin=17 * mm,
        title=f"{data['name']} - Curriculum Vitae",
        author=data["name"],
        subject="Academic curriculum vitae",
        creator="ReportLab",
    )

    base = getSampleStyleSheet()
    styles = {
        "name": ParagraphStyle(
            "Name",
            parent=base["Title"],
            fontName="Nunito-Bold",
            fontSize=29,
            leading=31,
            alignment=TA_LEFT,
            textColor=INK,
            spaceAfter=2.3 * mm,
        ),
        "role": ParagraphStyle(
            "Role",
            parent=base["Normal"],
            fontName="Nunito-Semibold",
            fontSize=10.8,
            leading=13.8,
            textColor=ACCENT,
            spaceAfter=0.6 * mm,
        ),
        "affiliation": ParagraphStyle(
            "Affiliation",
            parent=base["Normal"],
            fontName="Nunito",
            fontSize=9.2,
            leading=12.2,
            textColor=MUTED,
        ),
        "meta": ParagraphStyle(
            "Meta",
            parent=base["Normal"],
            fontName="Nunito",
            fontSize=8.7,
            leading=12.8,
            alignment=TA_RIGHT,
            textColor=MUTED,
        ),
        "body": ParagraphStyle(
            "Body",
            parent=base["BodyText"],
            fontName="Nunito",
            fontSize=10,
            leading=14,
            textColor=INK,
            spaceAfter=0,
        ),
        "section": ParagraphStyle(
            "Section",
            parent=base["Heading2"],
            fontName="Nunito-Bold",
            fontSize=12,
            leading=14.5,
            textColor=INK,
            spaceAfter=0,
        ),
        "period": ParagraphStyle(
            "Period",
            parent=base["Normal"],
            fontName="Nunito-Semibold",
            fontSize=9,
            leading=11.4,
            textColor=ACCENT,
        ),
        "entry_title": ParagraphStyle(
            "EntryTitle",
            parent=base["BodyText"],
            fontName="Nunito-Semibold",
            fontSize=10.5,
            leading=12.8,
            textColor=INK,
            spaceAfter=0.7 * mm,
        ),
        "entry_text": ParagraphStyle(
            "EntryText",
            parent=base["BodyText"],
            fontName="Nunito",
            fontSize=8.8,
            leading=11.4,
            textColor=MUTED,
            spaceAfter=0,
        ),
        "entry_lab": ParagraphStyle(
            "EntryLab",
            parent=base["BodyText"],
            fontName="Nunito-Semibold",
            fontSize=8.8,
            leading=11.4,
            textColor=ACCENT,
            spaceBefore=0.7 * mm,
            spaceAfter=0,
        ),
        "publication_title": ParagraphStyle(
            "PublicationTitle",
            parent=base["BodyText"],
            fontName="Nunito-Semibold",
            fontSize=10.2,
            leading=12.6,
            textColor=INK,
            spaceAfter=0.7 * mm,
        ),
        "publication_group": ParagraphStyle(
            "PublicationGroup",
            parent=base["Heading3"],
            fontName="Nunito-Bold",
            fontSize=10.4,
            leading=12.8,
            textColor=ACCENT,
            spaceAfter=1.1 * mm,
        ),
        "publication_text": ParagraphStyle(
            "PublicationText",
            parent=base["BodyText"],
            fontName="Nunito",
            fontSize=8.7,
            leading=11,
            textColor=MUTED,
            spaceAfter=0,
        ),
        "interests": ParagraphStyle(
            "Interests",
            parent=base["BodyText"],
            fontName="Nunito",
            fontSize=9.8,
            leading=13,
            textColor=INK,
        ),
    }

    links = (
        f'<link href="{esc(data["website"])}" color="#287E73">sindream.github.io</link><br/>'
        f'<link href="{esc(data["orcid"])}" color="#287E73">ORCID 0000-0002-6155-3712</link><br/>'
        f'<link href="{esc(data["linkedin"])}" color="#287E73">LinkedIn</link><br/>'
        f'Born {esc(data["date_of_birth"])}<br/>'
        f'Updated {esc(data["updated"])}'
    )
    header = Table(
        [[
            [
                Paragraph(esc(data["name"]), styles["name"]),
                Paragraph(esc(data["role"]), styles["role"]),
                Paragraph(esc(data["affiliation"]), styles["affiliation"]),
            ],
            Paragraph(links, styles["meta"]),
        ]],
        colWidths=[132 * mm, 46 * mm],
        hAlign="LEFT",
    )
    header.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
                ("LINEBELOW", (0, 0), (-1, -1), 1.4, ACCENT),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
            ]
        )
    )

    story = [header, Spacer(1, 4.2 * mm)]
    story.extend(
        [
            section_header("Profile", styles),
            Spacer(1, 1.8 * mm),
            Paragraph(esc(data["profile"]), styles["body"]),
            Spacer(1, 4.1 * mm),
            section_header("Education", styles),
            Spacer(1, 1.2 * mm),
        ]
    )

    for item in data["education"]:
        education_details = [
            Paragraph(esc(item["degree"]), styles["entry_title"]),
            Paragraph(esc(item["institution"]), styles["entry_text"]),
        ]
        if item.get("laboratory"):
            laboratory = esc(item["laboratory"])
            if item.get("laboratory_url"):
                laboratory = (
                    f'<link href="{esc(item["laboratory_url"])}" color="#287E73">'
                    f'{laboratory}</link>'
                )
            education_details.append(
                Paragraph(f"Laboratory: {laboratory}", styles["entry_lab"])
            )

        education_row = Table(
            [[
                Paragraph(esc(item["period"]), styles["period"]),
                education_details,
            ]],
            colWidths=[31 * mm, 131 * mm],
        )
        education_row.setStyle(
            TableStyle(
                [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 0),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                    ("TOPPADDING", (0, 0), (-1, -1), 2),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ]
            )
        )
        story.append(KeepTogether([education_row]))

    story.extend(
        [
            Spacer(1, 1.2 * mm),
            section_header("Awards and competitions", styles),
            Spacer(1, 1.2 * mm),
        ]
    )

    for award in data["awards_competitions"]:
        story.append(KeepTogether([award_row(award, styles)]))

    story.extend(
        [
            Spacer(1, 1.2 * mm),
            section_header("Research interests", styles),
            Spacer(1, 1.8 * mm),
            Paragraph(
                " <font color='#287E73'>/</font> ".join(esc(item) for item in data["research_interests"]),
                styles["interests"],
            ),
            Spacer(1, 4.1 * mm),
            section_header("Publications and presentations", styles),
            Spacer(1, 1.2 * mm),
        ]
    )

    for section in data["publication_sections"]:
        items = section["items"]
        story.extend(
            [
                CondPageBreak(28 * mm),
                Paragraph(f'{esc(section["title"])} ({len(items)})', styles["publication_group"]),
            ]
        )
        for publication in items:
            story.append(KeepTogether([publication_row(publication, data["name"], styles)]))
        story.append(Spacer(1, 1.3 * mm))

    document.build(story, onFirstPage=page_decoration, onLaterPages=page_decoration)
    return OUTPUT_PATH


if __name__ == "__main__":
    print(build())

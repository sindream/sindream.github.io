#!/usr/bin/env python3
"""Build the public research CV from structured JSON data."""

from __future__ import annotations

import html
import json
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = Path(__file__).with_name("cv_data.json")
OUTPUT_PATH = ROOT / "assets" / "cv" / "woojae-shin-cv.pdf"

INK = colors.HexColor("#17221E")
MUTED = colors.HexColor("#5D6963")
GREEN = colors.HexColor("#245F55")
ORANGE = colors.HexColor("#C85E33")
LINE = colors.HexColor("#D1D2CB")
PAPER = colors.HexColor("#FBFAF6")


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def emphasize_name(authors: str, name: str) -> str:
    safe_authors = esc(authors)
    safe_name = esc(name)
    return safe_authors.replace(safe_name, f"<b>{safe_name}</b>")


def section_header(title: str, styles: dict[str, ParagraphStyle]):
    return KeepTogether(
        [
            Spacer(1, 4 * mm),
            Paragraph(esc(title.upper()), styles["section"]),
            HRFlowable(width="100%", thickness=0.65, color=LINE, spaceBefore=1.5 * mm, spaceAfter=2.3 * mm),
        ]
    )


def page_decoration(canvas, document):
    canvas.saveState()
    width, height = A4
    canvas.setFillColor(GREEN)
    canvas.rect(document.leftMargin, height - 13 * mm, 34 * mm, 1.6 * mm, fill=1, stroke=0)
    canvas.setFillColor(ORANGE)
    canvas.circle(width - document.rightMargin - 2 * mm, height - 12.2 * mm, 1.5 * mm, fill=1, stroke=0)
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.45)
    canvas.line(document.leftMargin, 12 * mm, width - document.rightMargin, 12 * mm)
    canvas.setFont("Helvetica", 6.8)
    canvas.setFillColor(MUTED)
    canvas.drawString(document.leftMargin, 8.3 * mm, "Woojae Shin - Research CV")
    canvas.drawRightString(width - document.rightMargin, 8.3 * mm, f"Page {document.page}")
    canvas.restoreState()


def build() -> Path:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    document = SimpleDocTemplate(
        str(OUTPUT_PATH),
        pagesize=A4,
        rightMargin=16 * mm,
        leftMargin=16 * mm,
        topMargin=17 * mm,
        bottomMargin=17 * mm,
        title=f"{data['name']} - Research CV",
        author=data["name"],
        subject="Public research curriculum vitae",
        creator="ReportLab",
    )

    base = getSampleStyleSheet()
    styles = {
        "name": ParagraphStyle(
            "Name",
            parent=base["Title"],
            fontName="Times-Bold",
            fontSize=28,
            leading=29,
            textColor=INK,
            spaceAfter=1.5 * mm,
        ),
        "affiliation": ParagraphStyle(
            "Affiliation",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=9.5,
            leading=12,
            textColor=GREEN,
        ),
        "links": ParagraphStyle(
            "Links",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=8,
            leading=12,
            alignment=TA_RIGHT,
            textColor=MUTED,
        ),
        "body": ParagraphStyle(
            "Body",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=8.8,
            leading=12.2,
            textColor=INK,
            spaceAfter=0,
        ),
        "small": ParagraphStyle(
            "Small",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=7.5,
            leading=10.2,
            textColor=MUTED,
            spaceAfter=0,
        ),
        "section": ParagraphStyle(
            "Section",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=8.1,
            leading=10,
            textColor=GREEN,
            spaceAfter=0,
        ),
        "year": ParagraphStyle(
            "Year",
            parent=base["Normal"],
            fontName="Times-Italic",
            fontSize=9.5,
            leading=11,
            textColor=ORANGE,
        ),
        "entry_title": ParagraphStyle(
            "EntryTitle",
            parent=base["BodyText"],
            fontName="Times-Bold",
            fontSize=9.5,
            leading=11.4,
            textColor=INK,
            spaceAfter=1.2 * mm,
        ),
        "entry_text": ParagraphStyle(
            "EntryText",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=7.35,
            leading=9.7,
            textColor=MUTED,
            spaceAfter=0.6 * mm,
        ),
        "footer_note": ParagraphStyle(
            "FooterNote",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=6.8,
            leading=9,
            textColor=MUTED,
        ),
    }

    links = (
        f'<link href="{esc(data["website"])}" color="#245F55">sindream.github.io</link><br/>'
        f'<link href="{esc(data["github"])}" color="#245F55">github.com/sindream</link><br/>'
        f'<link href="{esc(data["orcid"])}" color="#245F55">ORCID 0000-0002-6155-3712</link>'
    )
    header = Table(
        [
            [
                [Paragraph(esc(data["name"]), styles["name"]), Paragraph(esc(data["affiliation"]), styles["affiliation"])],
                Paragraph(links, styles["links"]),
            ]
        ],
        colWidths=[118 * mm, 44 * mm],
    )
    header.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )

    story = [header, Spacer(1, 4 * mm)]
    profile_box = Table(
        [[Paragraph(esc(data["profile"]), styles["body"])]],
        colWidths=[162 * mm],
    )
    profile_box.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), PAPER),
                ("BOX", (0, 0), (-1, -1), 0.6, LINE),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    story.extend(
        [
            profile_box,
            Spacer(1, 2.5 * mm),
            Paragraph(" <font color='#C85E33'>/</font> ".join(esc(item) for item in data["interests"]), styles["small"]),
            section_header("Publications", styles),
        ]
    )

    for publication in data["publications"]:
        title = (
            f'<link href="{esc(publication["doi"])}" color="#17221E">'
            f'{esc(publication["title"])} <font color="#245F55">[DOI]</font></link>'
        )
        details = (
            f'{emphasize_name(publication["authors"], data["name"])}<br/>'
            f'<font color="#245F55">{esc(publication["venue"])}</font>'
        )
        row = Table(
            [[Paragraph(esc(publication["year"]), styles["year"]), [Paragraph(title, styles["entry_title"]), Paragraph(details, styles["entry_text"])]]],
            colWidths=[14 * mm, 148 * mm],
        )
        row.setStyle(
            TableStyle(
                [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 0),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                    ("TOPPADDING", (0, 0), (-1, -1), 0),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 2.2 * mm),
                ]
            )
        )
        story.append(KeepTogether([row]))

    story.append(section_header("Selected Projects", styles))
    for project in data["projects"]:
        project_title = (
            f'<link href="{esc(project["url"])}" color="#17221E">'
            f'{esc(project["name"])} <font color="#245F55">[GitHub]</font></link>'
        )
        body = f'{esc(project["description"])}<br/><font color="#245F55">{esc(project["keywords"])}</font>'
        project_row = Table(
            [[Paragraph(project_title, styles["entry_title"]), Paragraph(body, styles["entry_text"])]],
            colWidths=[40 * mm, 122 * mm],
        )
        project_row.setStyle(
            TableStyle(
                [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 0),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                    ("TOPPADDING", (0, 0), (-1, -1), 0),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 2.2 * mm),
                ]
            )
        )
        story.append(KeepTogether([project_row]))

    story.extend(
        [
            section_header("Technical Scope", styles),
            Paragraph(" <font color='#C85E33'>/</font> ".join(esc(item) for item in data["technical_scope"]), styles["body"]),
            Spacer(1, 4 * mm),
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

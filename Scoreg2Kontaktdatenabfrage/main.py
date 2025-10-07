# importing modules
from reportlab.lib.pagesizes import A5
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_RIGHT
import pandas as pd
from enum import Enum
from typing import List
from dataclasses import dataclass
import argparse
from reportlab.lib import colors
from commons import MemberInfo, parse_df_to_member_info, scoreg_excel_to_df
styles = getSampleStyleSheet()

class Stufe(str, Enum):
    BIEBER = 'BI'
    WICHTEL = 'WI'
    WOELFLINGE = 'WOE'
    GUIDES = 'GU'
    SPAEHER = 'SP'
    CAVELIERS = 'CA'
    EXPLORERS = 'EX'
    RANGER = 'RA'
    ROVER = 'RO'

@dataclass
class ParsedArgs():
    stufen: List[Stufe]
    input_file_path: str
    output_file_path: str

def parse_args() -> ParsedArgs:
    parser = argparse.ArgumentParser(
        prog='Scoreg2Kontakdatenabfrage',
        description='Program to create an A5 page for each member containing parent information, used to check if the data is still valid.'
    )
    parser.add_argument('-i', '--input-file', required=True)
    parser.add_argument('-o', '--output-file', required=True)
    parser.add_argument('-s', '--stufen', default="")
    args = parser.parse_args()
    stufen = []
    for s in str(args.stufen).split(","):
        if (s == ''):
            continue
        stufen.append(Stufe[s])
    return ParsedArgs(stufen, args.input_file, args.output_file)

def filter_by_stufen(df: pd.DataFrame, selected_stufen: List[Stufe]) -> pd.DataFrame:
    if (len(selected_stufen) == 0):
        return df
    return df[df['Stufe'].isin(selected_stufen)]

def create_pdf(filename: str, data: List[MemberInfo]):
    doc = SimpleDocTemplate(filename, pagesize=A5)
    styles = getSampleStyleSheet()
    normal_style = styles["Normal"]
    right_align = ParagraphStyle(
        name="RightAlign",
        parent=normal_style,  # inherit base font, size, etc.
        alignment=TA_RIGHT
    )

    story = []

    for item in data:
        # --- Basisdaten ---
        basis_data = [
            ["Name:", Paragraph(f"{item.firstname} {item.lastname}", normal_style)],
            ["Geburtsdatum:", Paragraph(f"{item.birthday}", normal_style)],
            ["Anschrift:", Paragraph(f"{item.street}, {item.plz} {item.city}, {item.state} {item.country}", normal_style)],
        ]
        if getattr(item, "handy", None):
            basis_data.append(["Handy:", Paragraph(f"{item.handy}", normal_style)])
        if getattr(item, "festnetz", None):
            basis_data.append(["Telefon:", Paragraph(f"{item.festnetz}", normal_style)])

        basis_table = Table([["BASISDATEN", ""]] + basis_data, colWidths=[100, 230])
        basis_table.setStyle(
            TableStyle(
                [
                    ("SPAN", (0, 0), (-1, 0)),
                    ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("ALIGN", (0, 0), (0, -1), "RIGHT"),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),  # keeps text aligned at top
                    ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                    ("FONTSIZE", (0, 0), (-1, -1), 9),
                    ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
                ]
            )
        )
        story.append(basis_table)
        story.append(Spacer(1, 10))

        # --- Kontakt 1 ---
        kontakt1_data = [
            #["Art:", Paragraph(f"{item.contact_1_kind}", normal_style)],
            ["Name:", Paragraph(f"{item.contact_1_name}", normal_style)],
            ["Email:", Paragraph(f"{item.contact_1_email}", normal_style)],
            ["Telefon:", Paragraph(f"{item.contact_1_phone}", normal_style)],
        ]
        kontakt1_table = Table([["KONTAKT 1", ""]] + kontakt1_data, colWidths=[100, 230])
        kontakt1_table.setStyle(
            TableStyle(
                [
                    ("SPAN", (0, 0), (-1, 0)),
                    ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("ALIGN", (0, 0), (0, -1), "RIGHT"),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                    ("FONTSIZE", (0, 0), (-1, -1), 9),
                    ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
                ]
            )
        )
        story.append(kontakt1_table)
        story.append(Spacer(1, 10))

        # --- Kontakt 2 ---
        kontakt2_data = [
            #["Art:", Paragraph(f"{item.contact_2_kind}", normal_style)],
            ["Name:", Paragraph(f"{item.contact_2_name}", normal_style)],
            ["Email:", Paragraph(f"{item.contact_2_email}", normal_style)],
            ["Telefon:", Paragraph(f"{item.contact_2_phone}", normal_style)],
        ]
        kontakt2_table = Table([["KONTAKT 2", ""]] + kontakt2_data, colWidths=[100, 230])
        kontakt2_table.setStyle(
            TableStyle(
                [
                    ("SPAN", (0, 0), (-1, 0)),
                    ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("ALIGN", (0, 0), (0, -1), "RIGHT"),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                    ("FONTSIZE", (0, 0), (-1, -1), 9),
                    ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
                ]
            )
        )
        story.append(kontakt2_table)
        story.append(Spacer(1, 10))

        # -- medical data --
        med_data = [
            #["Art:", Paragraph(f"{item.contact_2_kind}", normal_style)],
            ["Allergien:", Paragraph(f"", normal_style)],
            ["Medikamente:", Paragraph("", normal_style)],
            ["Unverträglichkeiten:", Paragraph("", normal_style)],
            [Paragraph("physische oder chronische Krankheiten:", right_align), Paragraph("", normal_style)],
            [Paragraph("psychische Krankheiten:", right_align), Paragraph("", normal_style)],
        ]
        med_table = Table([["MEDIZINISCHES", ""]] + med_data, colWidths=[100, 230])
        med_table.setStyle(
            TableStyle(
                [
                    ("SPAN", (0, 0), (-1, 0)),
                    ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("ALIGN", (0, 0), (0, -1), "RIGHT"),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                    ("FONTSIZE", (0, 0), (-1, -1), 9),
                    ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
                ]
            )
        )
        story.append(med_table)

        # Force page break
        story.append(PageBreak())

    doc.build(story)

a = parse_args()
d = scoreg_excel_to_df(a.input_file_path)
fd = filter_by_stufen(d, a.stufen)
pi = parse_df_to_member_info(fd)
create_pdf(a.output_file_path, pi)

print(fd)

# https://www.geeksforgeeks.org/python/creating-pdf-documents-with-python/

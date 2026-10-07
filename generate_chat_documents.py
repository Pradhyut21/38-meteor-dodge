import os
import re
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Preformatted, Table, TableStyle, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor('#64748B'))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(40, 755, "Lab 4: VibeCoding — Meteor Dodge (Antigravity & Pradhyut)")
            self.setStrokeColor(colors.HexColor('#E2E8F0'))
            self.setLineWidth(0.6)
            self.line(40, 747, 572, 747)

        # Footer (all pages)
        self.setStrokeColor(colors.HexColor('#E2E8F0'))
        self.setLineWidth(0.6)
        self.line(40, 36, 572, 36)
        
        self.drawString(40, 24, "Student: Pradhyut | Repository: github.com/Pradhyut21/38-meteor-dodge")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(572, 24, page_str)
        self.restoreState()


def format_markdown_text(text):
    """Convert common inline markdown (bold, italic, code) to ReportLab XML tags."""
    # Escape ampersands and angle brackets that aren't tags
    text = text.replace("&", "&amp;")
    # Protect any actual tags if existing
    text = text.replace("<", "&lt;").replace(">", "&gt;")
    
    # Inline code `foo` -> <font name="Courier" color="#b91c1c">foo</font>
    text = re.sub(r'`([^`]+)`', r'<font name="Courier" color="#991b1b"><b>\1</b></font>', text)
    # Bold **foo** -> <b>foo</b>
    text = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', text)
    # Italic *foo* -> <i>foo</i>
    text = re.sub(r'\*([^*]+)\*', r'<i>\1</i>', text)
    return text


def build_pdf_from_markdown(md_path, pdf_path, main_title="Lab 4: VibeCoding"):
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=10
    )

    meta_box_style = ParagraphStyle(
        'MetaBox',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor('#334155')
    )

    h2_style = ParagraphStyle(
        'H2Style',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor('#1E3A8A'),
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    h3_student_style = ParagraphStyle(
        'H3Student',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=15,
        textColor=colors.HexColor('#047857'),
        spaceBefore=12,
        spaceAfter=4,
        keepWithNext=True
    )

    h3_ai_style = ParagraphStyle(
        'H3AI',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=15,
        textColor=colors.HexColor('#1D4ED8'),
        spaceBefore=12,
        spaceAfter=4,
        keepWithNext=True
    )

    h4_style = ParagraphStyle(
        'H4Style',
        parent=styles['Heading4'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor('#334155'),
        spaceBefore=8,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#1E293B'),
        spaceAfter=5
    )

    quote_style = ParagraphStyle(
        'StudentQuote',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=13.5,
        textColor=colors.HexColor('#065F46'),
        leftIndent=14,
        rightIndent=14,
        spaceBefore=3,
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'BulletStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#1E293B'),
        leftIndent=15,
        spaceAfter=3
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Code'],
        fontName='Courier',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor('#0F172A'),
        spaceBefore=2,
        spaceAfter=2
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#1E293B')
    )

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=42,
        bottomMargin=45
    )

    with open(md_path, "r", encoding="utf-8") as f:
        raw_lines = f.readlines()

    story = []
    
    in_code = False
    code_lines = []
    in_table = False
    table_rows = []

    def flush_table():
        nonlocal in_table, table_rows
        if not table_rows:
            in_table = False
            return
        
        # Build platypus table
        formatted_table_data = []
        is_first = True
        for row in table_rows:
            row_paras = []
            for col in row:
                st = table_header_style if is_first else table_cell_style
                fmt_col = format_markdown_text(col)
                row_paras.append(Paragraph(fmt_col, st))
            formatted_table_data.append(row_paras)
            is_first = False

        num_cols = len(table_rows[0])
        avail_width = 532
        if num_cols == 3:
            col_widths = [110, 150, 272]
        elif num_cols == 2:
            col_widths = [150, 382]
        elif num_cols == 4:
            col_widths = [100, 110, 120, 202]
        else:
            col_widths = [avail_width / num_cols] * num_cols

        t = Table(formatted_table_data, colWidths=col_widths)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E293B')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('LEFTPADDING', (0, 0), (-1, -1), 5),
            ('RIGHTPADDING', (0, 0), (-1, -1), 5),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#F8FAFC'), colors.HexColor('#FFFFFF')]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ]))
        story.append(Spacer(1, 4))
        story.append(t)
        story.append(Spacer(1, 6))
        table_rows = []
        in_table = False

    for line in raw_lines:
        stripped = line.rstrip()

        # Handle Code Blocks
        if stripped.startswith("```"):
            if in_code:
                in_code = False
                snippet_text = "\n".join(code_lines)
                
                # Render code inside a styled box table
                code_p = Preformatted(snippet_text, code_style)
                code_table = Table([[code_p]], colWidths=[532])
                code_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F1F5F9')),
                    ('BOX', (0, 0), (-1, -1), 0.7, colors.HexColor('#CBD5E1')),
                    ('LEFTPADDING', (0, 0), (-1, -1), 8),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                    ('TOPPADDING', (0, 0), (-1, -1), 4),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                ]))
                story.append(Spacer(1, 2))
                story.append(code_table)
                story.append(Spacer(1, 5))
                code_lines = []
            else:
                if in_table:
                    flush_table()
                in_code = True
                code_lines = []
            continue

        if in_code:
            code_lines.append(stripped)
            continue

        # Handle Tables
        if stripped.startswith("|") and stripped.endswith("|"):
            raw_cells = [c.strip() for c in stripped.split("|")[1:-1]]
            # check if it's a delimiter row like | :--- | :--- |
            if all(set(c).issubset({'-', ':', ' '}) for c in raw_cells):
                continue
            if not in_table:
                in_table = True
                table_rows = []
            table_rows.append(raw_cells)
            continue
        elif in_table:
            flush_table()

        # Title
        if stripped.startswith("# "):
            title_text = stripped[2:].strip()
            story.append(Paragraph(format_markdown_text(title_text), title_style))
            story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#1E3A8A'), spaceBefore=2, spaceAfter=8))
            continue

        # Headings
        if stripped.startswith("## "):
            h2_text = stripped[3:].strip()
            story.append(Spacer(1, 4))
            story.append(Paragraph(format_markdown_text(h2_text), h2_style))
            story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor('#94A3B8'), spaceBefore=1, spaceAfter=5))
            continue

        if stripped.startswith("### "):
            h3_text = stripped[4:].strip()
            if "Student" in h3_text:
                story.append(Spacer(1, 4))
                story.append(Paragraph(f"&#9654; {format_markdown_text(h3_text)}", h3_student_style))
            elif "Antigravity" in h3_text:
                story.append(Spacer(1, 4))
                story.append(Paragraph(f"&#9670; {format_markdown_text(h3_text)}", h3_ai_style))
            else:
                story.append(Spacer(1, 4))
                story.append(Paragraph(format_markdown_text(h3_text), h2_style))
            continue

        if stripped.startswith("#### "):
            h4_text = stripped[5:].strip()
            story.append(Paragraph(format_markdown_text(h4_text), h4_style))
            continue

        # Quotes (Student inquiry)
        if stripped.startswith("> "):
            q_text = stripped[2:].strip()
            story.append(Paragraph(format_markdown_text(q_text), quote_style))
            continue
        elif stripped == ">":
            story.append(Spacer(1, 2))
            continue

        # Divider
        if stripped == "---":
            story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#E2E8F0'), spaceBefore=5, spaceAfter=5))
            continue

        # List items
        if stripped.startswith("- ") or stripped.startswith("* "):
            item_text = stripped[2:].strip()
            story.append(Paragraph(f"&bull;&nbsp;&nbsp;{format_markdown_text(item_text)}", bullet_style))
            continue

        # Numbered list
        num_match = re.match(r'^(\d+)\.\s+(.*)$', stripped)
        if num_match:
            num, item_text = num_match.groups()
            story.append(Paragraph(f"<b>{num}.</b>&nbsp;&nbsp;{format_markdown_text(item_text)}", bullet_style))
            continue

        # Regular non-empty text
        if stripped:
            story.append(Paragraph(format_markdown_text(stripped), body_style))
        else:
            story.append(Spacer(1, 2))

    if in_table:
        flush_table()

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated PDF: {pdf_path} ({os.path.getsize(pdf_path)} bytes)")


def build_docx_from_markdown(md_path, docx_path, doc_title="Lab 4: VibeCoding — Chat History"):
    doc = Document()
    
    # Custom Margins
    for section in doc.sections:
        section.top_margin = Inches(0.7)
        section.bottom_margin = Inches(0.7)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)

    title_p = doc.add_paragraph()
    title_run = title_p.add_run(doc_title)
    title_run.font.name = "Calibri"
    title_run.font.size = Pt(20)
    title_run.font.bold = True
    title_run.font.color.rgb = RGBColor(15, 23, 42)
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER

    meta_p = doc.add_paragraph()
    meta_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = meta_p.add_run("Student: Pradhyut | Repository: https://github.com/Pradhyut21/38-meteor-dodge | AI: Antigravity")
    r.font.name = "Calibri"
    r.font.size = Pt(10)
    r.font.color.rgb = RGBColor(100, 116, 139)

    doc.add_paragraph("―" * 60)

    with open(md_path, "r", encoding="utf-8") as f:
        raw_lines = f.readlines()

    in_code = False
    code_lines = []

    for line in raw_lines:
        stripped = line.rstrip()

        if stripped.startswith("# "):
            continue

        if stripped.startswith("```"):
            if in_code:
                in_code = False
                cp = doc.add_paragraph()
                crun = cp.add_run("\n".join(code_lines))
                crun.font.name = "Consolas"
                crun.font.size = Pt(8.5)
                crun.font.color.rgb = RGBColor(30, 41, 59)
                code_lines = []
            else:
                in_code = True
                code_lines = []
            continue

        if in_code:
            code_lines.append(stripped)
            continue

        if stripped.startswith("## "):
            h = doc.add_heading(stripped[3:].strip(), level=1)
            for run in h.runs:
                run.font.name = "Calibri"
                run.font.color.rgb = RGBColor(30, 58, 138)
            continue

        if stripped.startswith("### "):
            h = doc.add_heading(stripped[4:].replace("**", "").strip(), level=2)
            for run in h.runs:
                run.font.name = "Calibri"
                if "Student" in stripped:
                    run.font.color.rgb = RGBColor(4, 120, 87)
                else:
                    run.font.color.rgb = RGBColor(29, 78, 216)
            continue

        if stripped.startswith("#### "):
            h = doc.add_heading(stripped[5:].strip(), level=3)
            for run in h.runs:
                run.font.name = "Calibri"
                run.font.color.rgb = RGBColor(51, 65, 85)
            continue

        if stripped.startswith("> "):
            qp = doc.add_paragraph()
            qrun = qp.add_run(stripped[2:].replace("`", ""))
            qrun.italic = True
            qrun.font.name = "Calibri"
            qrun.font.color.rgb = RGBColor(6, 95, 70)
            continue

        if stripped == "---":
            doc.add_paragraph("―" * 55)
            continue

        if stripped.startswith("- ") or stripped.startswith("* "):
            bp = doc.add_paragraph(stripped[2:], style='List Bullet')
            for run in bp.runs:
                run.font.name = "Calibri"
            continue

        if stripped.startswith("|") and stripped.endswith("|"):
            cells = [c.strip() for c in stripped.split("|")[1:-1]]
            if all(set(c).issubset({'-', ':', ' '}) for c in cells):
                continue
            tp = doc.add_paragraph(" | ".join(cells))
            for run in tp.runs:
                run.font.name = "Calibri"
                run.font.size = Pt(9)
            continue

        if stripped:
            clean = stripped.replace("`", "").replace("**", "")
            p = doc.add_paragraph(clean)
            for run in p.runs:
                run.font.name = "Calibri"
                run.font.size = Pt(10)

    doc.save(docx_path)
    print(f"Successfully generated DOCX: {docx_path} ({os.path.getsize(docx_path)} bytes)")


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    lab4_dir = os.path.join(base_dir, "Lab-4")
    
    # 1. Export Chat_History_Lab4
    chat_md = os.path.join(lab4_dir, "Chat_History_Lab4.md")
    chat_pdf = os.path.join(lab4_dir, "Chat_History_Lab4.pdf")
    chat_docx = os.path.join(lab4_dir, "Chat_History_Lab4.docx")
    
    if os.path.exists(chat_md):
        print(f"Processing {chat_md}...")
        build_pdf_from_markdown(chat_md, chat_pdf, main_title="Lab 4: VibeCoding — Pair Programming Chat History")
        build_docx_from_markdown(chat_md, chat_docx, doc_title="Lab 4: VibeCoding — Pair Programming Chat History")

    # 2. Export VibeCoding_Chat_History_Lab4 (Report)
    report_md = os.path.join(lab4_dir, "VibeCoding_Chat_History_Lab4.md")
    report_pdf = os.path.join(lab4_dir, "VibeCoding_Chat_History_Lab4.pdf")
    report_docx = os.path.join(lab4_dir, "VibeCoding_Chat_History_Lab4.docx")
    
    if os.path.exists(report_md):
        print(f"Processing {report_md}...")
        build_pdf_from_markdown(report_md, report_pdf, main_title="Lab 4: VibeCoding — Meteor Dodge Report")
        build_docx_from_markdown(report_md, report_docx, doc_title="Lab 4: VibeCoding — Meteor Dodge Report")

"""Generate a professionally styled PDF cover letter with soft forest green theme."""

import io
import re
from fpdf import FPDF


def _strip_markdown(text: str) -> str:
    """Remove common markdown formatting from text."""
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"__(.*?)__", r"\1", text)
    text = re.sub(r"\*(.*?)\*", r"\1", text)
    text = re.sub(r"_(.*?)_", r"\1", text)
    text = re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"^---+$", "", text, flags=re.MULTILINE)
    return text.strip()


# ── Color palette ──────────────────────────────────────────────────
PAGE_BG = (234, 245, 234)        # soft mint background for entire page
BETREFF_BG = (200, 228, 200)     # slightly deeper green for subject highlight
DARK_GREEN = (30, 80, 50)        # primary text color
ACCENT_GREEN = (45, 110, 65)     # headings / greeting / closing
FOOTER_GREEN = (120, 175, 130)   # footer text


class CoverLetterPDF(FPDF):
    """Custom PDF with soft green background and dark green text."""

    def header(self):
        # Full-page mint background
        self.set_fill_color(*PAGE_BG)
        self.rect(0, 0, 210, 297, "F")

    def footer(self):
        # Thin accent line
        self.set_draw_color(*FOOTER_GREEN)
        self.set_line_width(0.3)
        self.line(20, 282, 190, 282)

        # Page number
        self.set_y(-12)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(*FOOTER_GREEN)
        self.cell(0, 10, f"- {self.page_no()} -", align="C",
                  new_x="LMARGIN", new_y="NEXT")


def generate_cover_letter_pdf(cover_letter_text: str) -> bytes:
    """Create a styled PDF from cover letter text.

    Returns the PDF content as bytes.
    """
    text = _strip_markdown(cover_letter_text)

    pdf = CoverLetterPDF("P", "mm", "A4")
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    # Start content with normal top margin
    pdf.set_y(20)

    lines = text.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Skip empty lines - add small spacing
        if not line:
            pdf.ln(3)
            i += 1
            continue

        # ── Subject line (Betreff) ─────────────────────────────
        if line.lower().startswith("betreff"):
            pdf.ln(2)
            pdf.set_font("Helvetica", "B", 11)
            pdf.set_text_color(*DARK_GREEN)
            pdf.set_fill_color(*BETREFF_BG)
            # fill=True makes the cell background cover the full width
            pdf.cell(0, 8, f"  {line}", fill=True,
                     new_x="LMARGIN", new_y="NEXT")
            pdf.ln(3)
            i += 1
            continue

        # ── Greeting line ──────────────────────────────────────
        is_greeting = any(
            line.lower().startswith(g)
            for g in ["sehr geehrte", "liebe ", "lieber ",
                       "hallo ", "guten tag"]
        )
        if is_greeting:
            pdf.ln(1)
            pdf.set_font("Helvetica", "B", 10.5)
            pdf.set_text_color(*ACCENT_GREEN)
            pdf.cell(0, 6, line, new_x="LMARGIN", new_y="NEXT")
            pdf.ln(2)
            i += 1
            continue

        # ── Closing line ───────────────────────────────────────
        is_closing = any(
            line.lower().startswith(c)
            for c in [
                "mit freundlichen",
                "herzliche",
                "viele gr",
                "beste gr",
                "freundliche gr",
                "hochachtungsvoll",
            ]
        )
        if is_closing:
            pdf.ln(3)
            pdf.set_font("Helvetica", "B", 10.5)
            pdf.set_text_color(*ACCENT_GREEN)
            pdf.cell(0, 6, line, new_x="LMARGIN", new_y="NEXT")
            pdf.ln(6)
            i += 1
            continue

        # ── Regular body text ──────────────────────────────────
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(*DARK_GREEN)
        pdf.multi_cell(0, 5.5, line, new_x="LMARGIN", new_y="NEXT")
        i += 1

    buf = io.BytesIO()
    pdf.output(buf)
    return buf.getvalue()

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from pathlib import Path
import datetime

def export_to_pdf(company, question, answer, filename=None):
    styles = getSampleStyleSheet()
    now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    Path("outputs/pdf_summaries").mkdir(parents=True, exist_ok=True)
    filename = filename or f"outputs/pdf_summaries/{company}_{now}.pdf"
    doc = SimpleDocTemplate(filename)
    elements = [
        Paragraph(f"<b>Company:</b> {company}", styles["Normal"]),
        Spacer(1, 12),
        Paragraph(f"<b>Question:</b> {question}", styles["Normal"]),
        Spacer(1, 12),
        Paragraph(f"<b>Answer:</b>", styles["Normal"]),
        Paragraph(answer, styles["Normal"])
    ]
    doc.build(elements)
    return filename

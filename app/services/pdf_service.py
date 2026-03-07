from weasyprint import HTML
from io import BytesIO

def generate_pdf(rendered_html: str) -> BytesIO:
    pdf_bytes = BytesIO()
    HTML(string=rendered_html).write_pdf(pdf_bytes)
    pdf_bytes.seek(0)
    return pdf_bytes

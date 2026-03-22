# app/services/docx_service.py
from docxtpl import DocxTemplate
from flask_babel import _
from io import BytesIO
import os

TEMPLATE_PATH = os.path.join("templates", "export", "template.docx")

def generate_docx(context: dict) -> BytesIO:
    """
    Render ein DocxTemplate mit dem gegebenen Context.
    context muss für Zertifikate:
    {
        "certs_table": {
            "col_labels": ["Image", "Info"],
            "tbl_contents": [
                {"label":"", "cols": [image, info]},
                ...
            ]
        },
        "config": {...}
    }
    enthalten.
    """
    tpl = DocxTemplate(TEMPLATE_PATH)
    
    # docxtpl erwartet die Schleife als 'c' in template
    certs_flat = []
    for row in context.get("certs_table", {}).get("tbl_contents", []):
        certs_flat.append({"cols": row["cols"]})
    context["certificates"] = certs_flat  # im Template: {% for c in certificates %}
    context.update({
        "_": _,
        "certs": certs
    })
    docx_bytes = BytesIO()
    tpl.render(context)
    tpl.save(docx_bytes)
    docx_bytes.seek(0)
    return docx_bytes

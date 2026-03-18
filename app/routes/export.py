from flask import Blueprint, render_template, request, send_file, current_app
from io import BytesIO
from datetime import datetime
import os
import yaml

from ..utils import load_json, DATA_FILES, DATA_DIR
from ..services.export_service import prepare_export_data
from ..services.pdf_service import generate_pdf
from app.services.docx_service import generate_docx
from ..render.html_renderer import render_export_html

export_bp = Blueprint("export_bp", __name__, template_folder="../templates")

CONFIG_FILE = os.path.join(DATA_DIR, "config.yaml")


@export_bp.route("/", methods=["GET", "POST"])
def export_view():
    HTML_PREVIEW_PATH = os.path.join(current_app.static_folder, "export_preview.html")

    skills = load_json(DATA_FILES["skills"])
    projects = load_json(DATA_FILES["projects"])
    certificates = load_json(DATA_FILES["certificates"])
    categories = load_json(DATA_FILES["categories"])

    # Config laden
    config_data = {}
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            config_data = yaml.safe_load(f) or {}

    if request.method == "POST":
        selected_skills = request.form.getlist("skills")
        language = request.form.get("language", "EN").upper()
        export_type = request.form.get("export_type", "html").lower()

        # Daten vorbereiten
        context = prepare_export_data(
            skills, projects, certificates, categories, selected_skills
        )

        context.update({
            "config": config_data,
            "lang": language
        })

        # Template wählen
        template = "export/docx.html" if export_type == "docx" else "export/pdf.html"

        # HTML rendern
        rendered_html = render_export_html(template, context)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        # Export-Typen
        if export_type == "pdf":
            pdf_bytes = generate_pdf(rendered_html)
            return send_file(
                pdf_bytes,
                as_attachment=True,
                download_name=f"skills_export_{timestamp}.pdf",
                mimetype="application/pdf"
            )

        elif export_type == "docx":

            docx_bytes = generate_docx(context)

            return send_file(
                docx_bytes,
                as_attachment=True,
                download_name=f"skills_export_{timestamp}.docx",
                mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

        else:
            return rendered_html


    return render_template("export/export_form.html", skills=skills)

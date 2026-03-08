from flask import Flask, render_template, request, send_file, redirect, url_for
import os, json
from io import BytesIO
from weasyprint import HTML
from html4docx import HtmlToDocx
from datetime import datetime
from docx import Document

app = Flask(__name__)
DATA_DIR = os.environ.get("DATA_DIR", "data")

DATA_FILES = {
    "skills": os.path.join(DATA_DIR, "skills.json"),
    "jobtitles": os.path.join(DATA_DIR, "jobtitles.json"),
    "projects": os.path.join(DATA_DIR, "projects.json"),
    "certificates": os.path.join(DATA_DIR, "certificates.json"),
    "index":  os.path.join(DATA_DIR, "index.json")
}

# --- Helferfunktionen ---
def ensure_json(path):
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        with open(path, "w", encoding="utf-8") as f:
            json.dump([], f)

def load_json(path):
    ensure_json(path)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path, data, generate_index_flag=True):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    if generate_index_flag:
        generate_index()

# --- JSON-Dateien initialisieren ---
os.makedirs(DATA_DIR, exist_ok=True)
for file_path in DATA_FILES.values():
    ensure_json(file_path)

# --- Routes ---
@app.route("/")
def home():
    skills = load_json(DATA_FILES["skills"])
    projects = load_json(DATA_FILES["projects"])
    certificates = load_json(DATA_FILES["certificates"])
    return render_template("home.html", skills=skills, projects=projects, certificates=certificates)

# Skills anzeigen / hinzufügen
@app.route("/skills", methods=["GET", "POST"])
def skills():
    skills = load_json(DATA_FILES["skills"])
    if request.method == "POST":
        # Neues Skill hinzufügen
        name = request.form.get("name")
        name_de = request.form.get("name_de") or ""
        skills.append({"name": name, "name_de": name_de})
        save_json(DATA_FILES["skills"], skills)
        return redirect(url_for("skills"))
    return render_template("skills.html", skills=skills)

# Skill bearbeiten (in-place)
@app.route("/skills/edit", methods=["POST"])
def edit_skill():
    data = request.get_json()
    index = int(data["index"])
    skills = load_json(DATA_FILES["skills"])
    skills[index]["name"] = data["name"]
    skills[index]["name_de"] = data.get("name_de", "")
    save_json(DATA_FILES["skills"], skills)
    return '', 204

# Skill löschen
@app.route("/skills/delete", methods=["POST"])
def delete_skill():
    data = request.get_json()
    index = int(data["index"])
    skills = load_json(DATA_FILES["skills"])
    skills.pop(index)
    save_json(DATA_FILES["skills"], skills)
    return '', 204

# Job Titles anzeigen / hinzufügen
@app.route("/jobtitles", methods=["GET", "POST"])
def jobtitles():
    jobtitles = load_json(DATA_FILES["jobtitles"])
    if request.method == "POST":
        # Neues Job Title hinzufügen
        name = request.form.get("name")
        name_de = request.form.get("name_de") or ""
        jobtitles.append({"name": name, "name_de": name_de})
        save_json(DATA_FILES["jobtitles"], jobtitles)
        return redirect(url_for("jobtitles"))
    return render_template("jobtitles.html", jobtitles=jobtitles)

# Job Title bearbeiten (in-place)
@app.route("/jobtitles/edit", methods=["POST"])
def edit_jobtitle():
    data = request.get_json()
    index = int(data["index"])
    jobtitles = load_json(DATA_FILES["jobtitles"])
    jobtitles[index]["name"] = data["name"]
    jobtitles[index]["name_de"] = data.get("name_de", "")
    save_json(DATA_FILES["jobtitles"], jobtitles)
    return '', 204

# Job Title löschen
@app.route("/jobtitles/delete", methods=["POST"])
def delete_jobtitle():
    data = request.get_json()
    index = int(data["index"])
    jobtitles = load_json(DATA_FILES["jobtitles"])
    jobtitles.pop(index)
    save_json(DATA_FILES["jobtitles"], jobtitles)
    return '', 204

# Projekte anzeigen / hinzufügen
@app.route("/projects", methods=["GET", "POST"])
def projects():
    projects = load_json(DATA_FILES["projects"])
    jobtitles = load_json(DATA_FILES["jobtitles"])
    skills = load_json(DATA_FILES["skills"])

    if request.method == "POST":
        edit_index = request.form.get("edit_index")
        title = request.form.get("title")
        title_de = request.form.get("title_de") or title
        jobtitle = request.form.get("jobtitle")
        from_date = request.form.get("from")
        until_date = request.form.get("until")

        # Tasks dynamisch
        tasks = []
        task_count = int(request.form.get("task_count", 0))
        for i in range(task_count):
            desc = request.form.get(f"task_{i}_desc")
            desc_de = request.form.get(f"task_{i}_desc_de") or desc
            task_skills = request.form.getlist(f"task_{i}_skills")
            if desc:
                tasks.append({"description": desc, "description_de": desc_de, "skills": task_skills})

        project_data = {
            "title": title,
            "title_de": title_de,
            "jobtitle": jobtitle,
            "from": from_date,
            "until": until_date,
            "tasks": tasks
        }

        if edit_index != "":
            projects[int(edit_index)] = project_data
        else:
            projects.append(project_data)

        save_json(DATA_FILES["projects"], projects)
        return redirect(url_for("projects"))

    return render_template("projects.html", projects=projects, jobtitles=jobtitles, skills=skills)

# Projekt löschen
@app.route("/projects/delete", methods=["POST"])
def delete_project():
    data = request.get_json()
    index = int(data["index"])
    projects = load_json(DATA_FILES["projects"])
    projects.pop(index)
    save_json(DATA_FILES["projects"], projects)
    return '', 204

# Übersicht + Add
@app.route("/certificates", methods=["GET", "POST"])
def certificates_view():
    certificates = load_json(DATA_FILES["certificates"])
    skills = [s["name"] for s in load_json(DATA_FILES["skills"])]

    if request.method == "POST":
        code = request.form.get("code")
        if any(c["code"] == code for c in certificates):
            flash("Zertifikat mit diesem Code existiert bereits.")
            return redirect("/certificates")

        new_cert = {
            "code": code,
            "issuer": request.form.get("issuer"),
            "badge": request.form.get("badge"),
            "badge_img": request.form.get("badge_img"),
            "url": request.form.get("url"),
            "from": request.form.get("from"),
            "until": request.form.get("until"),
            "skills": request.form.getlist("skills")
        }
        certificates.append(new_cert)
        save_json(DATA_FILES["certificates"], certificates)
        return redirect("/certificates")

    return render_template("certificates.html", certificates=certificates, skills=skills)

# Edit
@app.route("/certificates/edit", methods=["POST"])
def edit_certificate():
    certificates = load_json(DATA_FILES["certificates"])
    skills = [s["name"] for s in load_json(DATA_FILES["skills"])]
    code = request.form.get("code")
    cert = next((c for c in certificates if c["code"] == code), None)
    if not cert:
        flash("Zertifikat nicht gefunden")
        return redirect("/certificates")

    # Editieren, wenn POST neue Daten gesendet hat
    if "issuer" in request.form:
        cert["issuer"] = request.form.get("issuer")
        cert["badge"] = request.form.get("badge")
        cert["badge_img"] = request.form.get("badge_img")
        cert["url"] = request.form.get("url")
        cert["from"] = request.form.get("from")
        cert["until"] = request.form.get("until")
        cert["skills"] = request.form.getlist("skills")
        save_json(DATA_FILES["certificates"], certificates)
        return redirect("/certificates")

    # GET nicht nötig, Formular wird über POST aufgerufen
    return render_template("certificates.html", certificates=certificates, skills=skills, edit_cert=cert)

# Delete
@app.route("/certificates/delete", methods=["POST"])
def delete_certificate():
    certificates = load_json(DATA_FILES["certificates"])
    code = request.form.get("code")
    certificates = [c for c in certificates if c["code"] != code]
    save_json(DATA_FILES["certificates"], certificates)
    return redirect("/certificates")

@app.route("/generate_index", methods=["GET"])
def generate_index():
    skills = load_json(DATA_FILES["skills"])
    projects = load_json(DATA_FILES["projects"])
    certificates = load_json(DATA_FILES["certificates"])

    index = {}

    for skill in skills:
        name = skill["name"]

        index[name] = {
            "projects": [],
            "certificates": []
        }

        # --- Projekte / Tasks scannen ---
        for p_i, project in enumerate(projects):
            task_indices = []

            for t_i, task in enumerate(project.get("tasks", [])):
                if name in task.get("skills", []):
                    task_indices.append(t_i)

            if task_indices:
                index[name]["projects"].append({
                    "id": p_i,
                    "tasks": task_indices
                })

        # --- Zertifikate scannen ---
        cert_indices = [c_i for c_i, cert in enumerate(certificates) if name in cert.get("skills", [])]
        index[name]["certificates"] = cert_indices

    save_json(DATA_FILES["index"], index, False)
    return "OK"

@app.route("/export", methods=["GET", "POST"])
def export():
    skills = load_json(DATA_FILES["skills"])
    projects = load_json(DATA_FILES["projects"])
    certificates = load_json(DATA_FILES["certificates"])

    if request.method == "POST":
        selected_skills = request.form.getlist("skills")

        # --- Projekte filtern (antichronologisch) ---
        filtered_projects = []
        for proj in projects:
            if any(skill in task.get("skills", []) for task in proj.get("tasks", []) for skill in selected_skills):
                filtered_projects.append(proj)
        filtered_projects.sort(key=lambda p: p.get("from",""), reverse=True)

        # --- Zertifikate filtern ---
        filtered_certificates = [cert for cert in certificates if any(skill in cert.get("skills", []) for skill in selected_skills)]

        # --- HTML rendern ---
        rendered_html = render_template(
            "export_template.html",
            projects=filtered_projects,
            certificates=filtered_certificates,
            skills=skills,
            selected_skills=selected_skills
        )

        with open("/tmp/rendered.html", "w", encoding="utf-8") as f:
          f.write(rendered_html)
        # --- Exporttyp ---
        export_type = request.form.get("export_type", "pdf")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")

        if export_type == "pdf":
            pdf_bytes = BytesIO()
            HTML(string=rendered_html).write_pdf(pdf_bytes)
            pdf_bytes.seek(0)
            return send_file(
                pdf_bytes,
                as_attachment=True,
                download_name=f"skills_export_{timestamp}.pdf",
                mimetype="application/pdf"
            )
        elif export_type == "docx":
            parser = HtmlToDocx()
            docx_bytes = BytesIO()
            document = Document()
            parser.add_html_to_document(rendered_html, document)
            parser.save(docx_bytes)
            docx_bytes.seek(0)
            return send_file(
                docx_bytes,
                as_attachment=True,
                download_name=f"skills_export_{timestamp}.docx",
                mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

    # GET: Formular anzeigen
    return render_template("export_form.html", skills=skills)

# --- Start App ---
if __name__ == "__main__":
    schedule_index()
    app.run(host="0.0.0.0", port=5000, debug=True)

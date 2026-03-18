from flask import Blueprint, render_template, request, redirect, url_for
from ..utils import load_json, save_json, DATA_FILES

certificates_bp = Blueprint("certificates_bp", __name__)

@certificates_bp.route("/", methods=["GET","POST"])
def certificates_view():
    certificates = load_json(DATA_FILES["certificates"])
    skills = [s["name"] for s in load_json(DATA_FILES["skills"])]
    if request.method == "POST":
        code = request.form.get("code")
        if any(c["code"]==code for c in certificates):
            return redirect(url_for("certificates_bp.certificates_view"))
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
        return redirect(url_for("certificates_bp.certificates_view"))
    return render_template("certificates.html", certificates=certificates, skills=skills)

@certificates_bp.route("/edit", methods=["POST"])
def edit_certificate():
    certificates = load_json(DATA_FILES["certificates"])
    code = request.form.get("code")
    cert = next((c for c in certificates if c["code"]==code), None)
    if not cert:
        return redirect(url_for("certificates_bp.certificates_view"))
    if "issuer" in request.form:
        cert["issuer"] = request.form.get("issuer")
        cert["badge"] = request.form.get("badge")
        cert["badge_img"] = request.form.get("badge_img")
        cert["url"] = request.form.get("url")
        cert["from"] = request.form.get("from")
        cert["until"] = request.form.get("until")
        cert["skills"] = request.form.getlist("skills")
        save_json(DATA_FILES["certificates"], certificates)
        return redirect(url_for("certificates_bp.certificates_view"))
    skills = [s["name"] for s in load_json(DATA_FILES["skills"])]
    return render_template("certificates.html", certificates=certificates, skills=skills, edit_cert=cert)

@certificates_bp.route("/delete", methods=["POST"])
def delete_certificate():
    certificates = load_json(DATA_FILES["certificates"])
    code = request.form.get("code")
    certificates = [c for c in certificates if c["code"] != code]
    save_json(DATA_FILES["certificates"], certificates)
    return redirect(url_for("certificates_bp.certificates_view"))

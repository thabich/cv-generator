from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from ..utils import load_json, save_json, DATA_FILES

skills_bp = Blueprint("skills_bp", __name__)
def sort_skills(skills):
    return sorted(skills, key=lambda k: k['name'], reverse=False)

@skills_bp.route("/", methods=["GET","POST"])
def skills_view():
    skills = load_json(DATA_FILES["skills"])
    skills_sorted = sort_skills(skills)
    categories = load_json(DATA_FILES["categories"])
    if request.method == "POST":
        name = request.form.get("name")
        name_de = request.form.get("name_de") or ""
        category = request.form.get("category") or ""
        skills.append({"name": name, "name_de": name_de, "category": category})
        save_json(DATA_FILES["skills"], sort_skills(skills))
        return redirect(url_for("skills_bp.skills_view"))
    return render_template("skills.html", skills=sort_skills(skills), categories=categories)

@skills_bp.route("/edit", methods=["POST"])
def edit_skill():
    data = request.get_json()
    index = int(data["index"])
    skills = load_json(DATA_FILES["skills"])
    skills[index]["name"] = data["name"]
    skills[index]["name_de"] = data.get("name_de","")
    skills[index]["category"] = data.get("category","")
    save_json(DATA_FILES["skills"], sort_skills(skills))
    return '', 204

@skills_bp.route("/delete", methods=["POST"])
def delete_skill():
    data = request.get_json()
    index = int(data["index"])
    skills = load_json(DATA_FILES["skills"])
    skills.pop(index)
    save_json(DATA_FILES["skills"], sort_skills(skills))
    return '', 204

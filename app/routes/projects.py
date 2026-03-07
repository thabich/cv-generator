from flask import Blueprint, render_template, request, redirect, url_for
from ..utils import load_json, save_json, DATA_FILES

projects_bp = Blueprint("projects_bp", __name__)

@projects_bp.route("/", methods=["GET","POST"])
def projects_view():
    projects = load_json(DATA_FILES["projects"])
    skills = load_json(DATA_FILES["skills"])
    jobtitles = load_json(DATA_FILES["jobtitles"])
    if request.method == "POST":
        edit_index = request.form.get("edit_index")
        title = request.form.get("title")
        title_de = request.form.get("title_de") or title
        jobtitle = request.form.get("jobtitle")
        from_date = request.form.get("from")
        until_date = request.form.get("until")
        tasks = []
        task_count = int(request.form.get("task_count",0))
        for i in range(task_count):
            desc = request.form.get(f"task_{i}_desc")
            desc_de = request.form.get(f"task_{i}_desc_de") or desc
            task_skills = request.form.getlist(f"task_{i}_skills")
            if desc:
                tasks.append({"description": desc, "description_de": desc_de, "skills": task_skills})
        pdata = {"title":title,"title_de":title_de,"jobtitle":jobtitle,"from":from_date,"until":until_date,"tasks":tasks}
        if edit_index != "":
            projects[int(edit_index)] = pdata
        else:
            projects.append(pdata)
        save_json(DATA_FILES["projects"], projects)
        return redirect(url_for("projects_bp.projects_view"))
    return render_template("projects.html", projects=projects, skills=skills, jobtitles=jobtitles)

@projects_bp.route("/delete", methods=["POST"])
def delete_project():
    data = request.get_json()
    index = int(data["index"])
    projects = load_json(DATA_FILES["projects"])
    projects.pop(index)
    save_json(DATA_FILES["projects"], projects)
    return '', 204

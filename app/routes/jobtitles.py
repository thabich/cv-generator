from flask import Blueprint, render_template, request, redirect, url_for
from ..utils import load_json, save_json, DATA_FILES

jobtitles_bp = Blueprint("jobtitles_bp", __name__)

@jobtitles_bp.route("/", methods=["GET","POST"])
def jobtitles_view():
    jobtitles = load_json(DATA_FILES["jobtitles"])
    if request.method == "POST":
        name = request.form.get("name")
        name_de = request.form.get("name_de") or ""
        jobtitles.append({"name": name, "name_de": name_de})
        save_json(DATA_FILES["jobtitles"], jobtitles)
        return redirect(url_for("jobtitles_bp.jobtitles_view"))
    return render_template("jobtitles.html", jobtitles=jobtitles)

@jobtitles_bp.route("/edit", methods=["POST"])
def edit_jobtitle():
    data = request.get_json()
    index = int(data["index"])
    jobtitles = load_json(DATA_FILES["jobtitles"])
    jobtitles[index]["name"] = data["name"]
    jobtitles[index]["name_de"] = data.get("name_de","")
    save_json(DATA_FILES["jobtitles"], jobtitles)
    return '', 204

@jobtitles_bp.route("/delete", methods=["POST"])
def delete_jobtitle():
    data = request.get_json()
    index = int(data["index"])
    jobtitles = load_json(DATA_FILES["jobtitles"])
    jobtitles.pop(index)
    save_json(DATA_FILES["jobtitles"], jobtitles)
    return '', 204

from flask import Blueprint, render_template, request, redirect, url_for
from ..utils import load_json, save_json, DATA_FILES

categories_bp = Blueprint("categories_bp", __name__)

@categories_bp.route("/", methods=["GET","POST"])
def categories_view():
    categories = load_json(DATA_FILES["categories"])
    if request.method == "POST":
        name = request.form.get("name")
        name_de = request.form.get("name_de")
        color = request.form.get("color")
        categories.append({"name": name, "name_de": name_de, "color": color})
        save_json(DATA_FILES["categories"], categories)
        return redirect(url_for("categories_bp.categories_view"))
    return render_template("categories.html", categories=categories)

@categories_bp.route("/delete", methods=["POST"])
def delete_category():
    data = request.get_json()
    index = int(data["index"])
    categories = load_json(DATA_FILES["categories"])
    categories.pop(index)
    save_json(DATA_FILES["categories"], categories)
    return '', 204

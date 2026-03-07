from flask import Blueprint, render_template
from ..utils import load_json, DATA_FILES

home_bp = Blueprint("home_bp", __name__)

@home_bp.route("/")
def home():
    skills = load_json(DATA_FILES["skills"])
    projects = load_json(DATA_FILES["projects"])
    certificates = load_json(DATA_FILES["certificates"])
    return render_template("home.html", skills=skills, projects=projects, certificates=certificates)

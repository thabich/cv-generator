from flask import Blueprint, render_template, request, redirect, url_for
import yaml
import os
from ..utils import DATA_DIR

config_bp = Blueprint("config_bp", __name__, template_folder="../templates")
CONFIG_FILE = os.path.join(DATA_DIR, "config.yaml")

@config_bp.route("/", methods=["GET","POST"])
def config_view():
    config_data = {}
    # YAML laden, falls vorhanden
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            config_data = yaml.safe_load(f) or {}

    saved = False
    if request.method == "POST":
        # Daten aus Formular holen
        config_data = {
            "first_name": request.form.get("first_name",""),
            "last_name": request.form.get("last_name",""),
            "email": request.form.get("email",""),
            "website": request.form.get("website",""),
            "phone": request.form.get("phone",""),
            "custom_params": request.form.get("custom_params","")
        }
        # YAML speichern
        os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            yaml.dump(config_data, f, allow_unicode=True)
        saved = True

    return render_template("config.html", config=config_data, saved=saved)

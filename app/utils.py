import os, json
from datetime import datetime
from io import BytesIO

DATA_DIR = os.environ.get("DATA_DIR", "data")
DATA_FILES = {
    "skills": os.path.join(DATA_DIR, "skills.json"),
    "categories": os.path.join(DATA_DIR, "categories.json"),
    "jobtitles": os.path.join(DATA_DIR, "jobtitles.json"),
    "projects": os.path.join(DATA_DIR, "projects.json"),
    "certificates": os.path.join(DATA_DIR, "certificates.json"),
    "index": os.path.join(DATA_DIR, "index.json")
}

def ensure_json(path):
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        with open(path, "w", encoding="utf-8") as f:
            json.dump([], f)

def load_json(path):
    ensure_json(path)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path, data, generate_index_flag=True):
    from .utils import generate_index  # um Kreisabhängigkeiten zu vermeiden
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    if generate_index_flag:
        generate_index()

def generate_index():
    skills = load_json(DATA_FILES["skills"])
    projects = load_json(DATA_FILES["projects"])
    certificates = load_json(DATA_FILES["certificates"])
    index = {}
    for skill in skills:
        name = skill["name"]
        index[name] = {"projects": [], "certificates": []}
        for p_i, project in enumerate(projects):
            task_indices = [t_i for t_i, task in enumerate(project.get("tasks", [])) if name in task.get("skills", [])]
            if task_indices:
                index[name]["projects"].append({"id": p_i, "tasks": task_indices})
        cert_indices = [c_i for c_i, cert in enumerate(certificates) if name in cert.get("skills", [])]
        index[name]["certificates"] = cert_indices
    save_json(DATA_FILES["index"], index, False)

def prepare_export_data(skills, projects, certificates, categories, selected_skills):
    if selected_skills:
        filtered_projects = [
            proj for proj in projects
            if any(skill in task.get("skills", [])
                   for task in proj.get("tasks", [])
                   for skill in selected_skills)
        ]
        filtered_certificates = [
            c for c in certificates
            if any(skill in c.get("skills", []) for skill in selected_skills)
        ]
    else:
        filtered_projects = projects.copy()
        filtered_certificates = certificates.copy()

    filtered_projects.sort(key=lambda p: p.get("from", ""), reverse=True)

    # Task-Skills-Zusammenfassung
    for proj in filtered_projects:
        task_skills = set()
        for t in proj.get("tasks", []):
            if selected_skills:
                task_skills.update([s for s in t.get("skills", []) if s in selected_skills])
            else:
                task_skills.update(t.get("skills", []))
        proj["task_skills_summary"] = sorted(task_skills)

    return {
        "projects": filtered_projects,
        "certificates": filtered_certificates,
        "skills": skills,
        "categories": {c['name']: c for c in categories},
        "selected_skills": selected_skills
    }

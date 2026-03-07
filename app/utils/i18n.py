# app/utils/i18n.py
translations = {
    "DE": {
        "Projects": "Projekte",
        "Certificates": "Zertifikate",
        "Skills": "Skills",
        "Project": "Projekt",
        "Role": "Rolle",
        "Period": "Zeitraum",
        "Tasks": "Aufgaben",
        "Image": "Bild",
        "Info": "Info",
        "Email": "E-Mail",
        "Phone": "Telefon",
        "Website": "Website"
    },
    "EN": {
        "Projects": "Projects",
        "Certificates": "Certificates",
        "Skills": "Skills",
        "Project": "Project",
        "Role": "Role",
        "Period": "Period",
        "Tasks": "Tasks",
        "Image": "Image",
        "Info": "Info",
        "Email": "Email",
        "Phone": "Phone",
        "Website": "Website"
    }
}

def trans(key: str, lang: str = "EN") -> str:
    return translations.get(lang, {}).get(key, key)

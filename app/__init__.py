from flask import Flask
from flask_babel import Babel
import os
from .utils import ensure_json, DATA_FILES

def create_app():
    app = Flask(__name__,         template_folder="../templates",
        static_folder="../static")
    app.config['BABEL_DEFAULT_LOCALE'] = 'en'
    babel = Babel(app)    
    # --- JSON Dateien sicherstellen ---
    os.makedirs(os.environ.get("DATA_DIR", "data"), exist_ok=True)
    for file_path in DATA_FILES.values():
        ensure_json(file_path)

    # --- Blueprints importieren ---
    from .routes.skills import skills_bp
    from .routes.categories import categories_bp
    from .routes.jobtitles import jobtitles_bp
    from .routes.projects import projects_bp
    from .routes.certificates import certificates_bp
    from .routes.export import export_bp
    from .routes.config import config_bp
    from .routes.home import home_bp

    # --- Blueprints registrieren ---
    app.register_blueprint(home_bp)
    app.register_blueprint(skills_bp, url_prefix="/skills")
    app.register_blueprint(categories_bp, url_prefix="/categories")
    app.register_blueprint(jobtitles_bp, url_prefix="/jobtitles")
    app.register_blueprint(projects_bp, url_prefix="/projects")
    app.register_blueprint(certificates_bp, url_prefix="/certificates")
    app.register_blueprint(config_bp, url_prefix="/config")
    app.register_blueprint(export_bp, url_prefix="/export")

    return app

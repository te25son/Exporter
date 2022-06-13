from typing import Any, Dict
from flask import Flask
from flask_wtf.csrf import CSRFProtect  # type: ignore
from .main import main as main_blueprint
from .auth import auth as auth_blueprint
from .db import create_db_and_tables, create_dummy_admin

csrf = CSRFProtect()


def create_app(override_settings: Dict[str, Any] = None) -> Flask:
    app = Flask(__name__)
    app.config.from_object("exporter.settings")

    if override_settings:
        app.config.update(override_settings)

    csrf.init_app(app)

    create_db_and_tables()
    create_dummy_admin()

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)

    return app

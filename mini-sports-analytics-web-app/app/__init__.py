"""
app/__init__.py
Flask Application Factory.

This project intentionally avoids a single monolithic run script.
create_app() builds and configures the Flask app, ensures required
directories exist, and registers the blueprint that holds all routes.
"""

import os
from flask import Flask

# Project root (one level up from the app/ package)
_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def create_app():
    """Flask application factory."""
    app = Flask(
        __name__,
        template_folder=os.path.join(_PROJECT_ROOT, "templates"),
        static_folder=os.path.join(_PROJECT_ROOT, "static"),
    )
    app.config.from_object("config.Config")

    # Create required directories (idempotent)
    os.makedirs(app.config["RAW_DATA_DIR"], exist_ok=True)
    os.makedirs(app.config["PROCESSED_DATA_DIR"], exist_ok=True)
    os.makedirs(app.config["PLOTS_DIR"], exist_ok=True)

    # Register blueprints
    from app.routes import main_bp
    app.register_blueprint(main_bp)

    return app

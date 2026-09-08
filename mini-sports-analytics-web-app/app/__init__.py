"""
app/__init__.py
Flask Application Factory.

Registers all blueprints:
  - dashboard_bp  → / (Home)
  - matches_bp    → /matches
  - teams_bp      → /teams
  - players_bp    → /players
  - standings_bp  → /standings
  - analytics_bp  → /analytics
  - compare_bp    → /compare
  - records_bp    → /records
  - datalab_bp    → /data-lab + legacy routes
  - api_bp        → /api/*
  - main_bp       → legacy routes (backward compatibility)
"""

import os
from flask import Flask, render_template

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

    # Register new modular blueprints
    from app.routes.dashboard import dashboard_bp
    from app.routes.matches import matches_bp
    from app.routes.teams import teams_bp
    from app.routes.players import players_bp
    from app.routes.standings import standings_bp
    from app.routes.analytics import analytics_bp
    from app.routes.compare import compare_bp
    from app.routes.records import records_bp
    from app.routes.datalab import datalab_bp
    from app.routes.predict import predict_bp
    from app.routes.hypothesis import hypothesis_bp
    from app.routes.api import api_bp

    app.register_blueprint(dashboard_bp)
    app.register_blueprint(matches_bp)
    app.register_blueprint(teams_bp)
    app.register_blueprint(players_bp)
    app.register_blueprint(standings_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(compare_bp)
    app.register_blueprint(records_bp)
    app.register_blueprint(predict_bp)
    app.register_blueprint(hypothesis_bp)
    app.register_blueprint(datalab_bp)
    app.register_blueprint(api_bp)

    # Custom error handlers
    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html", page_title="Page Not Found"), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template("500.html", page_title="Server Error"), 500

    return app

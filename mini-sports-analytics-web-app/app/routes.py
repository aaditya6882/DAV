"""
app/routes.py
Presentation Layer — Software Developer role.

Routes are kept intentionally thin: they call service-layer functions
and pass results into templates. No heavy computation happens here.
"""

import os

from flask import Blueprint, render_template, current_app, send_from_directory

from app.services.data_loader import load_raw_data, load_processed_data
from app.services.preprocessing import clean_data, save_processed_data
from app.services import eda, statistics as stats_service
from app.services.visualizations.generate import generate_all_plots

main_bp = Blueprint("main", __name__)


def _get_clean_dataframe():
    """Helper: load raw data, clean it, and persist the processed copy."""
    raw_df = load_raw_data()
    clean_df = clean_data(raw_df)
    save_processed_data(clean_df)
    return clean_df


@main_bp.route("/")
def index():
    """Render main dashboard."""
    df = _get_clean_dataframe()

    summary = eda.generate_summary(df)
    context = {
        "summary": summary,
    }
    return render_template("index.html", **context)


@main_bp.route("/visualizations")
def visualizations():
    """Render the generated data visualizations."""
    df = _get_clean_dataframe()
    return render_template("visualizations.html", plots=generate_all_plots(df))


@main_bp.route("/eda")
def eda_page():
    """Render exploratory data analysis metrics and unusual matches."""
    df = _get_clean_dataframe()
    return render_template(
        "eda.html",
        summary=eda.generate_summary(df),
        outliers=eda.detect_outliers(df).to_dict(orient="records"),
    )


@main_bp.route("/preprocessing")
def preprocessing_page():
    """Show the transformations applied before analysis."""
    raw_df = load_raw_data()
    clean_df = clean_data(raw_df)
    save_processed_data(clean_df)
    return render_template(
        "preprocessing.html",
        raw_rows=len(raw_df),
        cleaned_rows=len(clean_df),
        raw_columns=list(raw_df.columns),
        cleaned_columns=list(clean_df.columns),
    )


@main_bp.route("/statistics")
def statistics_page():
    """Render team standings and year-level match statistics."""
    df = _get_clean_dataframe()
    return render_template(
        "statistics.html",
        team_stats=stats_service.compute_team_stats(df).to_dict(orient="records"),
        year_stats=stats_service.compute_year_stats(df).to_dict(orient="records"),
    )


@main_bp.route("/about")
def about():
    """Render project information."""
    return render_template("about.html")


@main_bp.route("/css/<path:filename>")
def template_css(filename):
    """Serve styles stored alongside the templates."""
    return send_from_directory(os.path.join(current_app.template_folder, "css"), filename)


@main_bp.route("/teams")
def teams():
    """Render full team standings table."""
    df = _get_clean_dataframe()
    team_stats = stats_service.compute_team_stats(df)
    return render_template("teams.html", team_stats=team_stats.to_dict(orient="records"))


@main_bp.route("/outliers")
def outliers():
    """Render detected outlier matches (unusually high/low scoring)."""
    df = _get_clean_dataframe()
    outlier_matches = eda.detect_outliers(df, column="total_goals")
    return render_template(
        "outliers.html", outliers=outlier_matches.to_dict(orient="records")
    )

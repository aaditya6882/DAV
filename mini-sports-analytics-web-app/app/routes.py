"""
app/routes.py
Presentation Layer — Software Developer role.

Routes are kept intentionally thin: they call service-layer functions
and pass results into templates. No heavy computation happens here.
"""

import os
import pandas as pd

from flask import Blueprint, render_template, current_app, send_from_directory, redirect, url_for

from app.services.data_loader import (
    load_raw_data,
    load_processed_data,
    load_groups_data,
    load_stats_data,
    load_achievements_data,
)
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
    return render_template("index.html", summary=summary)


@main_bp.route("/visualizations")
def visualizations():
    """Render the generated data visualizations and interactive Chart.js charts."""
    df = _get_clean_dataframe()
    stats_df = load_stats_data()
    groups_df = load_groups_data()
    achievements_df = load_achievements_data()
    
    # 1. Goals per match distribution
    goals_dist_raw = df["total_goals"].value_counts().sort_index().to_dict()
    goals_distribution = {str(k): int(v) for k, v in goals_dist_raw.items()}

    # 2. Goals per team
    goals_home = df.groupby("home_team")["home_score"].sum()
    goals_away = df.groupby("away_team")["away_score"].sum()
    goals_per_team = goals_home.add(goals_away, fill_value=0).sort_values(ascending=False).to_dict()

    # 3. Result breakdown
    results_raw = df["result"].value_counts().to_dict()
    results_data = {
        "Home Wins": results_raw.get("home_win", 0),
        "Draws": results_raw.get("draw", 0),
        "Away Wins": results_raw.get("away_win", 0)
    }

    # 4. Top player scorers
    top_scorers = stats_df[stats_df["goals"] > 0].sort_values("goals", ascending=False).to_dict(orient="records")

    # 5. Group standings
    group_data = {}
    for g, rows in groups_df.groupby("group"):
        group_data[g] = rows.sort_values("position")[["team", "points", "goals_for", "goals_against", "goal_difference"]].to_dict(orient="records")

    # 6. Tournament awards
    awards_data = achievements_df.to_dict(orient="records")

    # 7. Stadium distribution
    stadium_counts = df["stadium"].value_counts().to_dict()

    # 8. City distribution
    city_counts = df["city"].value_counts().to_dict()

    # 9. Team Performance Matrix (Goals For vs Goals Against)
    team_gf = df.groupby("home_team")["home_score"].sum().add(df.groupby("away_team")["away_score"].sum(), fill_value=0)
    team_ga = df.groupby("home_team")["away_score"].sum().add(df.groupby("away_team")["home_score"].sum(), fill_value=0)
    matrix_df = pd.DataFrame({"goals_for": team_gf, "goals_against": team_ga}).reset_index()
    matrix_df.columns = ["team", "goals_for", "goals_against"]
    team_matrix = matrix_df.to_dict(orient="records")

    return render_template(
        "visualizations.html",
        plots=generate_all_plots(df),
        goals_distribution=goals_distribution,
        goals_per_team=goals_per_team,
        results_data=results_data,
        top_scorers=top_scorers,
        group_data=group_data,
        awards_data=awards_data,
        stadium_counts=stadium_counts,
        city_counts=city_counts,
        team_matrix=team_matrix
    )


@main_bp.route("/eda")
def eda_page():
    """Render exploratory data analysis metrics, unusual matches, and top scorers."""
    df = _get_clean_dataframe()
    stats_df = load_stats_data()
    if "rank" in stats_df.columns:
        stats_df = stats_df.sort_values("rank")
    return render_template(
        "eda.html",
        summary=eda.generate_summary(df),
        outliers=eda.detect_outliers(df).to_dict(orient="records"),
        players=stats_df.to_dict(orient="records"),
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
    """Render 8-group standings and year-level match statistics."""
    df = _get_clean_dataframe()
    groups_df = load_groups_data()
    grouped = {
        group_name: group_rows.sort_values("position").to_dict(orient="records")
        for group_name, group_rows in groups_df.groupby("group")
    }
    return render_template(
        "statistics.html",
        groups=grouped,
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
    return redirect(url_for("main.statistics_page"))


@main_bp.route("/outliers")
def outliers():
    """Render detected outlier matches (unusually high/low scoring)."""
    return redirect(url_for("main.eda_page"))


@main_bp.route("/groups")
def groups():
    """Redirect deprecated /groups route to /statistics."""
    from flask import redirect, url_for
    return redirect(url_for("main.statistics_page"))


@main_bp.route("/player-stats")
def player_stats():
    """Redirect deprecated /player-stats route to /eda."""
    from flask import redirect, url_for
    return redirect(url_for("main.eda_page"))


@main_bp.route("/awards")
def awards():
    """Render tournament awards (team and individual)."""
    achievements_df = load_achievements_data()
    team_awards = achievements_df[achievements_df["category"] == "Team"].to_dict(orient="records")
    individual_awards = achievements_df[achievements_df["category"] == "Individual"].to_dict(orient="records")
    return render_template(
        "awards.html", team_awards=team_awards, individual_awards=individual_awards
    )


@main_bp.route("/achievements")
def achievements():
    """Redirect legacy /achievements to /awards."""
    from flask import redirect, url_for
    return redirect(url_for("main.awards"))


"""
app/routes/datalab.py
Data Lab blueprint — preserves all original academic/data-science functionality.
"""

import os
from flask import Blueprint, render_template, current_app, send_from_directory, redirect, url_for

from app.services.data_loader import load_raw_data, load_processed_data, load_stats_data, load_achievements_data, load_groups_data
from app.services.preprocessing import clean_data, save_processed_data
from app.services import eda, statistics as stats_service
from app.services.visualizations.generate import generate_all_plots
from app.services.insight_service import get_data_quality

datalab_bp = Blueprint("datalab", __name__)


@datalab_bp.route("/data-lab")
def data_lab():
    quality = get_data_quality()
    raw_df = load_raw_data()
    clean_df = load_processed_data()
    return render_template(
        "datalab.html",
        active_tab="datalab",
        quality=quality,
        raw_rows=len(raw_df),
        cleaned_rows=len(clean_df),
        raw_columns=list(raw_df.columns),
        cleaned_columns=list(clean_df.columns),
        page_title="Data Lab",
        meta_description="Data science and academic analysis section for the FIFA World Cup 2022 dataset.",
    )


# --- Preserved original routes (legacy) ---

@datalab_bp.route("/eda")
def eda_page():
    df = load_processed_data()
    clean_data(load_raw_data())
    stats_df = load_stats_data()
    if "rank" in stats_df.columns:
        stats_df = stats_df.sort_values("rank")
    return render_template(
        "eda.html",
        active_tab="datalab",
        summary=eda.generate_summary(df),
        outliers=eda.detect_outliers(df).to_dict(orient="records"),
        players=stats_df.to_dict(orient="records"),
    )


@datalab_bp.route("/preprocessing")
def preprocessing_page():
    raw_df = load_raw_data()
    clean_df = clean_data(raw_df)
    save_processed_data(clean_df)
    return render_template(
        "preprocessing.html",
        active_tab="datalab",
        raw_rows=len(raw_df),
        cleaned_rows=len(clean_df),
        raw_columns=list(raw_df.columns),
        cleaned_columns=list(clean_df.columns),
    )


@datalab_bp.route("/statistics-lab")
def statistics_page():
    df = load_processed_data()
    groups_df = load_groups_data()
    grouped = {
        gname: grow.sort_values("position").to_dict(orient="records")
        for gname, grow in groups_df.groupby("group")
    }
    return render_template(
        "statistics.html",
        active_tab="datalab",
        groups=grouped,
        year_stats=stats_service.compute_year_stats(df).to_dict(orient="records"),
    )


@datalab_bp.route("/visualizations-lab")
def visualizations_page():
    df = load_processed_data()
    stats_df = load_stats_data()
    groups_df = load_groups_data()
    achievements_df = load_achievements_data()

    goals_dist_raw = df["total_goals"].value_counts().sort_index().to_dict()
    goals_distribution = {str(k): int(v) for k, v in goals_dist_raw.items()}

    import pandas as pd
    goals_home = df.groupby("home_team")["home_score"].sum()
    goals_away = df.groupby("away_team")["away_score"].sum()
    goals_per_team = goals_home.add(goals_away, fill_value=0).sort_values(ascending=False).to_dict()

    results_raw = df["result"].value_counts().to_dict()
    results_data = {
        "Home Wins": results_raw.get("home_win", 0),
        "Draws": results_raw.get("draw", 0),
        "Away Wins": results_raw.get("away_win", 0),
    }

    top_scorers = stats_df[stats_df["goals"] > 0].sort_values("goals", ascending=False).to_dict(orient="records")
    group_data = {
        g: rows.sort_values("position")[["team", "points", "goals_for", "goals_against", "goal_difference"]].to_dict(orient="records")
        for g, rows in groups_df.groupby("group")
    }
    awards_data = achievements_df.to_dict(orient="records")
    stadium_counts = df["stadium"].value_counts().to_dict()
    city_counts = df["city"].value_counts().to_dict()

    team_gf = df.groupby("home_team")["home_score"].sum().add(df.groupby("away_team")["away_score"].sum(), fill_value=0)
    team_ga = df.groupby("home_team")["away_score"].sum().add(df.groupby("away_team")["home_score"].sum(), fill_value=0)
    matrix_df = pd.DataFrame({"goals_for": team_gf, "goals_against": team_ga}).reset_index()
    matrix_df.columns = ["team", "goals_for", "goals_against"]
    team_matrix = matrix_df.to_dict(orient="records")

    return render_template(
        "visualizations.html",
        active_tab="datalab",
        plots=generate_all_plots(df),
        goals_distribution=goals_distribution,
        goals_per_team=goals_per_team,
        results_data=results_data,
        top_scorers=top_scorers,
        group_data=group_data,
        awards_data=awards_data,
        stadium_counts=stadium_counts,
        city_counts=city_counts,
        team_matrix=team_matrix,
    )


@datalab_bp.route("/awards")
def awards():
    achievements_df = load_achievements_data()
    team_awards = achievements_df[achievements_df["category"] == "Team"].to_dict(orient="records")
    individual_awards = achievements_df[achievements_df["category"] == "Individual"].to_dict(orient="records")
    return render_template(
        "awards.html",
        active_tab="datalab",
        team_awards=team_awards,
        individual_awards=individual_awards,
    )


@datalab_bp.route("/about")
def about():
    return render_template("about.html", active_tab="datalab")


@datalab_bp.route("/achievements")
def achievements():
    return redirect(url_for("datalab.awards"))


@datalab_bp.route("/outliers")
def outliers():
    return redirect(url_for("datalab.eda_page"))


# Serve CSS from templates/css (legacy)
@datalab_bp.route("/css/<path:filename>")
def template_css(filename):
    return send_from_directory(os.path.join(current_app.template_folder, "css"), filename)

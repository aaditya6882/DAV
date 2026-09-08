"""
app/routes/records.py
Records blueprint — dynamically computed tournament records.
"""

from flask import Blueprint, render_template
from app.services.insight_service import get_tournament_records
from app.services.data_loader import load_processed_data, load_stats_data
from app.services.analytics_service import get_team_analytics

records_bp = Blueprint("records", __name__)


@records_bp.route("/records")
def records():
    main_records = get_tournament_records()
    df = load_processed_data()
    stats_df = load_stats_data().copy()
    for col in ["goals", "assists", "matches_played"]:
        if col in stats_df.columns:
            stats_df[col] = stats_df[col].fillna(0).astype(int)

    team_data = get_team_analytics()

    # Top 5 scorers
    top_scorers = stats_df.sort_values("goals", ascending=False).head(5).to_dict(orient="records")

    # Top 5 assist providers
    top_assists = stats_df.sort_values("assists", ascending=False).head(5).to_dict(orient="records")

    # Highest scoring matches (top 5)
    top_matches = df.sort_values("total_goals", ascending=False).head(5).to_dict(orient="records")

    # Biggest victories (top 5)
    df["abs_diff"] = df["goal_difference"].abs()
    biggest_wins = df.sort_values("abs_diff", ascending=False).head(5).to_dict(orient="records")

    # Most goals by team
    team_goals = sorted(team_data, key=lambda x: x["goals_for"], reverse=True)[:10]

    # Best defensive teams (fewest goals against with >= 3 matches)
    best_defense = sorted([t for t in team_data if t["played"] >= 3], key=lambda x: x["goals_against"])[:10]

    # Most matches played (teams with >= 6 matches)
    most_matches = sorted(team_data, key=lambda x: x["played"], reverse=True)[:5]

    # Venue usage
    venue_counts = df["stadium"].value_counts().reset_index()
    venue_counts.columns = ["stadium", "matches"]
    venues = venue_counts.head(5).to_dict(orient="records")

    return render_template(
        "records.html",
        active_tab="records",
        records=main_records,
        top_scorers=top_scorers,
        top_assists=top_assists,
        top_matches=top_matches,
        biggest_wins=biggest_wins,
        team_goals=team_goals,
        best_defense=best_defense,
        most_matches=most_matches,
        venues=venues,
        page_title="Records",
        meta_description="FIFA World Cup 2022 tournament records — top scorers, highest-scoring matches, biggest victories, and more.",
    )

"""
app/routes/dashboard.py
Dashboard / Home blueprint.
"""

from flask import Blueprint, render_template
from app.services.data_loader import load_processed_data, load_stats_data
from app.services.insight_service import get_tournament_records, get_did_you_know_facts
from app.services.match_service import get_all_matches

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
def index():
    df = load_processed_data()
    stats_df = load_stats_data().copy()
    for col in ["goals", "assists", "matches_played"]:
        if col in stats_df.columns:
            stats_df[col] = stats_df[col].fillna(0).astype(int)

    matches = get_all_matches()

    kpi = {
        "total_matches": len(df),
        "total_goals": int(df["total_goals"].sum()),
        "total_teams": len(set(df["home_team"]) | set(df["away_team"])),
        "total_players": len(stats_df),
        "total_stadiums": df["stadium"].nunique(),
        "avg_goals": round(float(df["total_goals"].mean()), 2),
    }

    records = get_tournament_records()
    facts = get_did_you_know_facts()

    # Featured match — the Final
    final_matches = df[df["stage"].str.lower() == "final"]
    featured = None
    if not final_matches.empty:
        row = final_matches.iloc[-1]
        featured = {
            "match_id": int(row.get("match_id", 1)),
            "home_team": row["home_team"],
            "away_team": row["away_team"],
            "home_score": int(row["home_score"]),
            "away_score": int(row["away_score"]),
            "stage": row["stage"],
            "date": str(row["date"])[:10],
            "venue": row["stadium"],
            "city": row["city"],
        }

    return render_template(
        "index.html",
        active_tab="home",
        kpi=kpi,
        records=records,
        facts=facts,
        featured=featured,
        page_title="Home",
        meta_description="QFIFA - FIFA World Cup 2022 Football Intelligence Platform. Explore match results, team stats, player rankings, and analytics.",
    )

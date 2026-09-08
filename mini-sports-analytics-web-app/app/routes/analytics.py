"""
app/routes/analytics.py
Analytics blueprint.
"""

from flask import Blueprint, render_template
from app.services.analytics_service import (
    get_goal_analytics,
    get_team_analytics,
    get_venue_analytics,
    get_player_analytics,
    get_tournament_analytics,
)

analytics_bp = Blueprint("analytics", __name__)


@analytics_bp.route("/analytics")
def analytics():
    goal_data = get_goal_analytics()
    team_data = get_team_analytics()
    venue_data = get_venue_analytics()
    player_data = get_player_analytics()
    tournament_data = get_tournament_analytics()

    return render_template(
        "analytics.html",
        active_tab="analytics",
        goal_data=goal_data,
        team_data=team_data,
        venue_data=venue_data,
        player_data=player_data,
        tournament_data=tournament_data,
        page_title="Analytics",
        meta_description="Interactive football analytics charts for the FIFA World Cup 2022 — goals, teams, players, and venues.",
    )

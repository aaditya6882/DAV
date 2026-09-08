"""
app/routes/compare.py
Compare blueprint — team vs team and player vs player.
"""

from flask import Blueprint, render_template, request
from app.services.team_service import get_all_teams, get_team_detail
from app.services.player_service import get_player_teams, get_player_by_id, filter_players

compare_bp = Blueprint("compare", __name__)


@compare_bp.route("/compare")
def compare():
    mode = request.args.get("mode", "team")  # 'team' or 'player'

    # Team comparison
    team_a = request.args.get("team_a", "")
    team_b = request.args.get("team_b", "")
    team_detail_a = get_team_detail(team_a) if team_a else None
    team_detail_b = get_team_detail(team_b) if team_b else None

    # Player comparison
    player_a_id = request.args.get("player_a", "")
    player_b_id = request.args.get("player_b", "")
    player_a = get_player_by_id(player_a_id) if player_a_id else None
    player_b = get_player_by_id(player_b_id) if player_b_id else None

    all_teams = get_all_teams()
    all_players = filter_players(sort_by="goals_desc")

    return render_template(
        "compare.html",
        active_tab="compare",
        mode=mode,
        all_teams=all_teams,
        all_players=all_players,
        team_a=team_detail_a,
        team_b=team_detail_b,
        team_a_name=team_a,
        team_b_name=team_b,
        player_a=player_a,
        player_b=player_b,
        player_a_id=player_a_id,
        player_b_id=player_b_id,
        page_title="Compare",
        meta_description="Compare FIFA World Cup 2022 teams or players side-by-side.",
    )

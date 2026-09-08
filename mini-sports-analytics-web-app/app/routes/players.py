"""
app/routes/players.py
Players blueprint.
"""

from flask import Blueprint, render_template, request, abort
from app.services.player_service import (
    filter_players,
    get_player_by_id,
    get_player_teams,
    get_player_positions,
    get_rankings,
)

players_bp = Blueprint("players", __name__)


@players_bp.route("/players")
def players():
    q = request.args.get("q", "")
    team = request.args.get("team", "all")
    position = request.args.get("position", "all")
    sort_by = request.args.get("sort", "goals_desc")
    tab = request.args.get("tab", "all")

    player_list = filter_players(query=q, team=team, position=position, sort_by=sort_by)
    teams = get_player_teams()
    positions = get_player_positions()
    rankings = get_rankings()

    return render_template(
        "players.html",
        active_tab="players",
        players=player_list,
        teams=teams,
        positions=positions,
        rankings=rankings,
        filters={"q": q, "team": team, "position": position, "sort": sort_by, "tab": tab},
        total=len(player_list),
        page_title="Players",
        meta_description="Explore all 832 FIFA World Cup 2022 players — goals, assists, appearances, and rankings.",
    )


@players_bp.route("/players/<player_id>")
def player_detail(player_id):
    player = get_player_by_id(player_id)
    if not player:
        abort(404)

    return render_template(
        "player_detail.html",
        active_tab="players",
        player=player,
        page_title=f"{player['player']} — Player Stats",
        meta_description=f"Statistics for {player['player']} ({player['team']}) at the FIFA World Cup 2022.",
    )

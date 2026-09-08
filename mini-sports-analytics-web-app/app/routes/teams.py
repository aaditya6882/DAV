"""
app/routes/teams.py
Teams blueprint.
"""

from flask import Blueprint, render_template, request, abort
from app.services.team_service import get_teams_with_stats, get_team_detail, get_all_teams

teams_bp = Blueprint("teams", __name__)


@teams_bp.route("/teams")
def teams():
    q = request.args.get("q", "")
    group = request.args.get("group", "all")
    sort_by = request.args.get("sort", "points_desc")

    team_list = get_teams_with_stats()

    if q:
        team_list = [t for t in team_list if q.lower() in t["team"].lower()]

    if group and group != "all":
        team_list = [t for t in team_list if t.get("group", "") == group]

    sort_options = {
        "points_desc": ("points", True),
        "goals_desc": ("goals_for", True),
        "gd_desc": ("goal_difference", True),
        "wins_desc": ("wins", True),
        "name_asc": ("team", False),
    }
    key, reverse = sort_options.get(sort_by, ("points", True))
    team_list.sort(key=lambda x: x.get(key, 0), reverse=reverse)

    groups = sorted(set(t.get("group", "") for t in get_teams_with_stats() if t.get("group", "") != "—"))

    return render_template(
        "teams.html",
        active_tab="teams",
        teams=team_list,
        groups=groups,
        filters={"q": q, "group": group, "sort": sort_by},
        total=len(team_list),
        page_title="Teams",
        meta_description="All 32 FIFA World Cup 2022 teams with standings, goals, and tournament performance.",
    )


@teams_bp.route("/teams/<path:team_name>")
def team_detail(team_name):
    # URL decode (spaces become %20)
    team_name = team_name.replace("-", " ").title() if "_" in team_name or "-" in team_name else team_name

    # Try exact match first, then fallback
    all_teams = get_all_teams()
    matched = next((t for t in all_teams if t.lower() == team_name.lower()), None)
    if not matched:
        abort(404)

    detail = get_team_detail(matched)
    if not detail:
        abort(404)

    return render_template(
        "team_detail.html",
        active_tab="teams",
        detail=detail,
        page_title=f"{matched} — Team Stats",
        meta_description=f"Complete tournament statistics and match history for {matched} at FIFA World Cup 2022.",
    )

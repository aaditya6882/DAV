"""
app/routes/matches.py
Match Centre blueprint.
"""

from flask import Blueprint, render_template, request, abort
from app.services.match_service import (
    filter_matches,
    get_match_by_id,
    get_stages,
    get_venues,
    get_teams_list,
    get_matches_grouped_by_stage,
)

matches_bp = Blueprint("matches", __name__)


@matches_bp.route("/matches")
def matches():
    stage = request.args.get("stage", "all")
    team = request.args.get("team", "all")
    venue = request.args.get("venue", "all")
    result = request.args.get("result", "all")
    query = request.args.get("q", "")
    sort_by = request.args.get("sort", "date_asc")
    view = request.args.get("view", "grouped")  # grouped or list

    filtered = filter_matches(
        stage=stage, team=team, venue=venue, result=result, query=query, sort_by=sort_by
    )
    match_list = filtered.to_dict(orient="records")

    stages = get_stages()
    venues = get_venues()
    teams = get_teams_list()

    # Grouped by stage view
    grouped = {}
    if view == "grouped" and not query and stage == "all" and team == "all" and venue == "all" and result == "all":
        grouped = get_matches_grouped_by_stage()

    return render_template(
        "matches.html",
        active_tab="matches",
        matches=match_list,
        grouped=grouped,
        stages=stages,
        venues=venues,
        teams=teams,
        filters={"stage": stage, "team": team, "venue": venue, "result": result, "q": query, "sort": sort_by, "view": view},
        total=len(match_list),
        page_title="Matches",
        meta_description="Browse all 64 FIFA World Cup 2022 match results, filter by stage, team, venue, and result.",
    )


@matches_bp.route("/matches/<int:match_id>")
def match_detail(match_id):
    detail = get_match_by_id(match_id)
    if not detail:
        abort(404)

    return render_template(
        "match_detail.html",
        active_tab="matches",
        detail=detail,
        match=detail["match"],
        home_recent=detail["home_recent"],
        away_recent=detail["away_recent"],
        page_title=f"{detail['match']['home_team']} vs {detail['match']['away_team']}",
        meta_description=f"Match details for {detail['match']['home_team']} vs {detail['match']['away_team']} at the FIFA World Cup 2022.",
    )

"""
app/routes/api.py
REST API blueprint — JSON endpoints for all major data types.
"""

from flask import Blueprint, jsonify, request, abort
from app.services.match_service import filter_matches, get_match_by_id, get_all_matches
from app.services.team_service import get_teams_with_stats, get_team_detail, get_all_teams
from app.services.player_service import filter_players, get_player_by_id, get_rankings
from app.services.data_loader import load_groups_data
from app.services.analytics_service import get_goal_analytics, get_team_analytics, get_player_analytics
from app.services.insight_service import get_tournament_records

api_bp = Blueprint("api", __name__, url_prefix="/api")


def _safe(data):
    """Convert any remaining non-serializable types."""
    import pandas as pd
    if isinstance(data, dict):
        return {k: _safe(v) for k, v in data.items()}
    if isinstance(data, list):
        return [_safe(i) for i in data]
    if hasattr(data, "item"):  # numpy scalar
        return data.item()
    if hasattr(data, "isoformat"):  # datetime
        return str(data)
    return data


# ---------- Matches ----------

@api_bp.route("/matches")
def api_matches():
    stage = request.args.get("stage")
    team = request.args.get("team")
    result = request.args.get("result")
    q = request.args.get("q")
    sort = request.args.get("sort", "date_asc")
    df = filter_matches(stage=stage, team=team, result=result, query=q, sort_by=sort)
    return jsonify({"count": len(df), "matches": _safe(df.to_dict(orient="records"))})


@api_bp.route("/matches/<int:match_id>")
def api_match_detail(match_id):
    detail = get_match_by_id(match_id)
    if not detail:
        abort(404)
    return jsonify(_safe(detail))


# ---------- Teams ----------

@api_bp.route("/teams")
def api_teams():
    teams = get_teams_with_stats()
    return jsonify({"count": len(teams), "teams": _safe(teams)})


@api_bp.route("/teams/<path:team_name>")
def api_team_detail(team_name):
    all_teams = get_all_teams()
    matched = next((t for t in all_teams if t.lower() == team_name.lower()), None)
    if not matched:
        abort(404)
    detail = get_team_detail(matched)
    return jsonify(_safe(detail))


# ---------- Players ----------

@api_bp.route("/players")
def api_players():
    q = request.args.get("q")
    team = request.args.get("team")
    position = request.args.get("position")
    sort = request.args.get("sort", "goals_desc")
    players = filter_players(query=q, team=team, position=position, sort_by=sort)
    return jsonify({"count": len(players), "players": _safe(players)})


@api_bp.route("/players/<player_id>")
def api_player_detail(player_id):
    player = get_player_by_id(player_id)
    if not player:
        abort(404)
    return jsonify(_safe(player))


# ---------- Standings ----------

@api_bp.route("/standings")
def api_standings():
    try:
        groups_df = load_groups_data()
        groups = {}
        for g in sorted(groups_df["group"].unique()):
            groups[g] = groups_df[groups_df["group"] == g].sort_values("position").to_dict(orient="records")
        return jsonify(_safe(groups))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------- Analytics ----------

@api_bp.route("/analytics/goals")
def api_analytics_goals():
    return jsonify(_safe(get_goal_analytics()))


@api_bp.route("/analytics/top-scorers")
def api_top_scorers():
    rankings = get_rankings()
    return jsonify(_safe({"top_scorers": rankings["top_scorers"]}))


@api_bp.route("/analytics/team-performance")
def api_team_performance():
    return jsonify(_safe(get_team_analytics()))


# ---------- Compare ----------

@api_bp.route("/compare/teams")
def api_compare_teams():
    team_a = request.args.get("a", "")
    team_b = request.args.get("b", "")
    all_teams = get_all_teams()

    def _find(name):
        return next((t for t in all_teams if t.lower() == name.lower()), None)

    a_name = _find(team_a)
    b_name = _find(team_b)

    if not a_name or not b_name:
        return jsonify({"error": "One or both team names not found"}), 404

    return jsonify({
        "team_a": _safe(get_team_detail(a_name)),
        "team_b": _safe(get_team_detail(b_name)),
    })


@api_bp.route("/compare/players")
def api_compare_players():
    a_id = request.args.get("a", "")
    b_id = request.args.get("b", "")
    a = get_player_by_id(a_id)
    b = get_player_by_id(b_id)
    if not a or not b:
        return jsonify({"error": "One or both player IDs not found"}), 404
    return jsonify({"player_a": _safe(a), "player_b": _safe(b)})


# ---------- Search ----------

@api_bp.route("/search")
def api_search():
    q = request.args.get("q", "").strip().lower()
    if not q or len(q) < 2:
        return jsonify({"players": [], "teams": [], "matches": []})

    # Teams
    all_teams = get_all_teams()
    matched_teams = [t for t in all_teams if q in t.lower()][:5]

    # Players
    players = filter_players(query=q, sort_by="goals_desc")[:5]

    # Matches
    matches_df = filter_matches(query=q)
    match_results = []
    for _, row in matches_df.head(5).iterrows():
        match_results.append({
            "match_id": int(row.get("match_id", 0)),
            "label": f"{row['home_team']} vs {row['away_team']}",
            "score": f"{int(row['home_score'])}–{int(row['away_score'])}",
            "stage": row["stage"],
            "date": str(row["date"])[:10],
        })

    return jsonify({
        "teams": [{"name": t, "url": f"/teams/{t}"} for t in matched_teams],
        "players": [{"name": p["player"], "team": p["team"], "id": p["player_id"]} for p in players],
        "matches": match_results,
    })


# ---------- Predict ----------

@api_bp.route("/predict")
def api_predict_match():
    from app.services.prediction_service import predict_match
    team_a = request.args.get("team_a", "")
    team_b = request.args.get("team_b", "")
    stage = request.args.get("stage", "Group")
    players_a = request.args.getlist("player_a")
    players_b = request.args.getlist("player_b")

    all_teams = get_all_teams()
    if not team_a or not team_b:
        return jsonify({"error": "Please provide both team_a and team_b"}), 400

    def _find(name):
        return next((t for t in all_teams if t.lower() == name.lower()), None)

    a_name = _find(team_a)
    b_name = _find(team_b)

    if not a_name or not b_name:
        return jsonify({"error": "One or both team names not found"}), 404

    res = predict_match(
        a_name,
        b_name,
        stage=stage,
        selected_players_a=players_a if players_a else None,
        selected_players_b=players_b if players_b else None,
    )
    return jsonify(_safe(res))


# ---------- Records ----------

@api_bp.route("/records")
def api_records():
    return jsonify(_safe(get_tournament_records()))


# ---------- Error handlers ----------

@api_bp.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found"}), 404


@api_bp.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error"}), 500

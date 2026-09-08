"""
app/routes/predict.py
Match Prediction & Simulation Blueprint.
"""

from flask import Blueprint, render_template, request, jsonify
from app.services.team_service import get_all_teams
from app.services.prediction_service import predict_match, get_team_key_players, STAGE_FACTORS

predict_bp = Blueprint("predict", __name__)


@predict_bp.route("/predict")
def predict_page():
    all_teams = get_all_teams()
    team_a = request.args.get("team_a", "Argentina")
    team_b = request.args.get("team_b", "France")
    stage = request.args.get("stage", "Final")

    # Safety check: if default team isn't valid or same team selected
    if team_a not in all_teams:
        team_a = all_teams[0] if all_teams else "Argentina"
    if team_b not in all_teams or team_b == team_a:
        team_b = all_teams[1] if len(all_teams) > 1 else team_a

    # Get optional player checkboxes
    players_a_selected = request.args.getlist("player_a")
    players_b_selected = request.args.getlist("player_b")

    result = predict_match(
        team_a_name=team_a,
        team_b_name=team_b,
        stage=stage,
        selected_players_a=players_a_selected if players_a_selected else None,
        selected_players_b=players_b_selected if players_b_selected else None,
    )

    stages = list(STAGE_FACTORS.keys())

    return render_template(
        "predict.html",
        active_tab="predict",
        all_teams=all_teams,
        team_a=team_a,
        team_b=team_b,
        stage=stage,
        stages=stages,
        result=result,
        players_a_selected=players_a_selected,
        players_b_selected=players_b_selected,
        page_title="Match Predictor",
        meta_description="Forecast future and hypothetical football fixtures with QFIFA's statistical match prediction engine.",
    )


@predict_bp.route("/api/predict")
def api_predict():
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
    return jsonify(res)

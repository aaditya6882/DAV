"""
app/services/prediction_service.py
Statistical Match Prediction & Simulation Engine using Poisson Goal Expectancy,
Team Attack/Defense Ratings, and Player Impact Analysis.
"""

import math
from app.services.data_loader import load_processed_data, load_stats_data
from app.services.team_service import get_all_teams, get_team_detail
from app.services.player_service import filter_players

# Stage modifier factors on goal output / defensive caution
STAGE_FACTORS = {
    "Group": 1.0,
    "Round of 16": 0.95,
    "Quarter-final": 0.90,
    "Semi-final": 0.85,
    "Final": 0.82,
}


def _poisson_probability(lmbda, k):
    """Compute Poisson probability P(X = k) = (lmbda^k * e^-lmbda) / k!"""
    if lmbda <= 0:
        return 1.0 if k == 0 else 0.0
    return (math.pow(lmbda, k) * math.exp(-lmbda)) / math.factorial(k)


def get_team_ratings(team_name):
    """Compute Attack Rating, Defense Rating, and Form stats for a team."""
    df = load_processed_data()
    total_tournament_goals = df["total_goals"].sum()
    total_matches = len(df)
    tournament_avg_goals_per_team_per_match = (
        (total_tournament_goals / total_matches / 2) if total_matches > 0 else 1.3
    )

    detail = get_team_detail(team_name)
    if not detail or detail["played"] == 0:
        return {
            "team_name": team_name,
            "played": 0,
            "attack_rating": 1.0,
            "defense_rating": 1.0,
            "goals_per_match": tournament_avg_goals_per_team_per_match,
            "conceded_per_match": tournament_avg_goals_per_team_per_match,
            "win_rate": 50.0,
        }

    gf_per_match = detail["goals_for"] / detail["played"]
    ga_per_match = detail["goals_against"] / detail["played"]

    # Attack rating: relative to tournament average
    attack_rating = max(0.4, gf_per_match / tournament_avg_goals_per_team_per_match)
    # Defense rating: relative to tournament average (lower is better defense)
    defense_rating = max(0.4, ga_per_match / tournament_avg_goals_per_team_per_match)

    return {
        "team_name": team_name,
        "played": detail["played"],
        "wins": detail["wins"],
        "draws": detail["draws"],
        "losses": detail["losses"],
        "goals_for": detail["goals_for"],
        "goals_against": detail["goals_against"],
        "attack_rating": round(attack_rating, 3),
        "defense_rating": round(defense_rating, 3),
        "goals_per_match": round(gf_per_match, 2),
        "conceded_per_match": round(ga_per_match, 2),
        "win_rate": detail["win_rate"],
        "points": detail["points"],
    }


def get_team_key_players(team_name):
    """Return top offensive players for a team."""
    players = filter_players(team=team_name, sort_by="goals_desc")
    # Take players with goals > 0 or assists > 0, up to top 6
    impact_players = [p for p in players if p["goals"] > 0 or p["assists"] > 0][:6]
    if not impact_players:
        impact_players = players[:4]
    return impact_players


def predict_match(team_a_name, team_b_name, stage="Group", selected_players_a=None, selected_players_b=None):
    """
    Perform bivariate Poisson simulation for a match between Team A and Team B.
    Returns win/draw/loss probabilities, predicted score, xG, score matrix, and likely scorers.
    """
    df = load_processed_data()
    total_tournament_goals = df["total_goals"].sum()
    total_matches = len(df)
    base_avg_goals = (
        (total_tournament_goals / total_matches / 2) if total_matches > 0 else 1.3
    )

    ratings_a = get_team_ratings(team_a_name)
    ratings_b = get_team_ratings(team_b_name)

    stage_factor = STAGE_FACTORS.get(stage, 1.0)

    # Base Expected Goals (xG) calculation
    # lambda_a = Attack_A * Defense_B * Avg_Goals * stage_modifier
    lambda_a = ratings_a["attack_rating"] * ratings_b["defense_rating"] * base_avg_goals * stage_factor
    lambda_b = ratings_b["attack_rating"] * ratings_a["defense_rating"] * base_avg_goals * stage_factor

    # Player lineup impact modifier
    all_players_a = get_team_key_players(team_a_name)
    all_players_b = get_team_key_players(team_b_name)

    if selected_players_a is not None and all_players_a:
        # If user explicitly chose specific players, apply a lineup multiplier
        active_ids = set(selected_players_a)
        selected_involvement = sum(
            p["goal_involvement"] for p in all_players_a if p["player_id"] in active_ids
        )
        total_involvement = max(1, sum(p["goal_involvement"] for p in all_players_a))
        player_ratio_a = 0.85 + 0.3 * (selected_involvement / total_involvement)
        lambda_a *= player_ratio_a

    if selected_players_b is not None and all_players_b:
        active_ids_b = set(selected_players_b)
        selected_involvement_b = sum(
            p["goal_involvement"] for p in all_players_b if p["player_id"] in active_ids_b
        )
        total_involvement_b = max(1, sum(p["goal_involvement"] for p in all_players_b))
        player_ratio_b = 0.85 + 0.3 * (selected_involvement_b / total_involvement_b)
        lambda_b *= player_ratio_b

    # Bound lambdas reasonably
    lambda_a = max(0.2, min(4.5, lambda_a))
    lambda_b = max(0.2, min(4.5, lambda_b))

    # Bivariate Poisson Score Matrix up to 5 goals each
    max_goals = 5
    score_matrix = []
    prob_win_a = 0.0
    prob_draw = 0.0
    prob_win_b = 0.0

    best_score = (1, 0)
    best_score_prob = 0.0

    prob_over_2_5 = 0.0
    prob_btts = 0.0

    for i in range(max_goals + 1):
        p_a = _poisson_probability(lambda_a, i)
        row = []
        for j in range(max_goals + 1):
            p_b = _poisson_probability(lambda_b, j)
            p_joint = p_a * p_b
            row.append(round(p_joint * 100, 2))

            if i > j:
                prob_win_a += p_joint
            elif i == j:
                prob_draw += p_joint
            else:
                prob_win_b += p_joint

            if i + j > 2.5:
                prob_over_2_5 += p_joint

            if i > 0 and j > 0:
                prob_btts += p_joint

            if p_joint > best_score_prob:
                best_score_prob = p_joint
                best_score = (i, j)
        score_matrix.append(row)

    # Normalize win/draw/loss probabilities to exactly 100%
    total_prob = prob_win_a + prob_draw + prob_win_b
    if total_prob > 0:
        win_a_pct = round((prob_win_a / total_prob) * 100, 1)
        draw_pct = round((prob_draw / total_prob) * 100, 1)
        win_b_pct = round((prob_win_b / total_prob) * 100, 1)
    else:
        win_a_pct, draw_pct, win_b_pct = 40.0, 20.0, 40.0

    # Adjust rounding discrepancy
    diff = round(100.0 - (win_a_pct + draw_pct + win_b_pct), 1)
    if diff != 0:
        win_a_pct += diff

    # Clean sheet probabilities: P(goals conceded == 0) = e^(-lambda_opponent)
    clean_sheet_a = round(math.exp(-lambda_b) * 100, 1)
    clean_sheet_b = round(math.exp(-lambda_a) * 100, 1)

    # Player Goalscoring Probabilities
    def _compute_player_probs(players, team_xg, team_total_goals):
        player_probs = []
        t_goals = max(1, team_total_goals)
        for p in players:
            p_share = p["goals"] / t_goals if p["goals"] > 0 else 0.05
            p_xg = team_xg * p_share
            # P(at least 1 goal) = 1 - e^(-p_xg)
            p_score = round((1.0 - math.exp(-p_xg)) * 100, 1)
            player_probs.append({
                "player_id": p["player_id"],
                "player": p["player"],
                "goals": p["goals"],
                "assists": p["assists"],
                "goal_prob": p_score,
            })
        player_probs.sort(key=lambda x: x["goal_prob"], reverse=True)
        return player_probs

    scorers_a = _compute_player_probs(all_players_a, lambda_a, ratings_a["goals_for"])
    scorers_b = _compute_player_probs(all_players_b, lambda_b, ratings_b["goals_for"])

    # Historical Head to Head (if any in 2022 dataset)
    h2h_matches = df[
        ((df["home_team"] == team_a_name) & (df["away_team"] == team_b_name))
        | ((df["home_team"] == team_b_name) & (df["away_team"] == team_a_name))
    ].to_dict(orient="records")

    return {
        "team_a": ratings_a,
        "team_b": ratings_b,
        "stage": stage,
        "xg_a": round(lambda_a, 2),
        "xg_b": round(lambda_b, 2),
        "win_a_pct": win_a_pct,
        "draw_pct": draw_pct,
        "win_b_pct": win_b_pct,
        "predicted_score": f"{best_score[0]}-{best_score[1]}",
        "predicted_home_goals": best_score[0],
        "predicted_away_goals": best_score[1],
        "score_matrix": score_matrix,
        "over_2_5_pct": round(prob_over_2_5 * 100, 1),
        "btts_pct": round(prob_btts * 100, 1),
        "clean_sheet_a": clean_sheet_a,
        "clean_sheet_b": clean_sheet_b,
        "scorers_a": scorers_a,
        "scorers_b": scorers_b,
        "key_players_a": all_players_a,
        "key_players_b": all_players_b,
        "h2h": [
            {
                "date": str(m["date"])[:10],
                "stage": m["stage"],
                "score": f"{int(m['home_score'])}–{int(m['away_score'])}",
                "home_team": m["home_team"],
                "away_team": m["away_team"],
            }
            for m in h2h_matches
        ],
    }


def evaluate_model_accuracy():
    """
    Backtest the bivariate Poisson prediction model across all 64 tournament matches
    and return accuracy metrics.
    """
    df = load_processed_data()
    correct_outcome = 0
    correct_exact_score = 0
    correct_over_under = 0
    total = len(df)

    if total == 0:
        return {
            "total_matches": 0,
            "outcome_accuracy": 0.0,
            "over_under_accuracy": 0.0,
            "exact_score_accuracy": 0.0,
            "correct_outcomes": 0,
            "correct_over_under": 0,
            "correct_exact_score": 0,
        }

    for _, row in df.iterrows():
        home_t = row["home_team"]
        away_t = row["away_team"]
        actual_h = int(row["home_score"])
        actual_a = int(row["away_score"])
        stage = row.get("stage", "Group")

        if actual_h > actual_a:
            actual_outcome = "win_a"
        elif actual_h < actual_a:
            actual_outcome = "win_b"
        else:
            actual_outcome = "draw"

        res = predict_match(home_t, away_t, stage=stage)
        pred_a_pct = res["win_a_pct"]
        pred_draw_pct = res["draw_pct"]
        pred_b_pct = res["win_b_pct"]

        if pred_a_pct >= pred_draw_pct and pred_a_pct >= pred_b_pct:
            pred_outcome = "win_a"
        elif pred_b_pct >= pred_a_pct and pred_b_pct >= pred_draw_pct:
            pred_outcome = "win_b"
        else:
            pred_outcome = "draw"

        if pred_outcome == actual_outcome:
            correct_outcome += 1

        pred_h = res["predicted_home_goals"]
        pred_a = res["predicted_away_goals"]
        if pred_h == actual_h and pred_a == actual_a:
            correct_exact_score += 1

        actual_ou = (actual_h + actual_a) > 2.5
        pred_ou = res["over_2_5_pct"] > 50.0
        if actual_ou == pred_ou:
            correct_over_under += 1

    return {
        "total_matches": total,
        "outcome_accuracy": round((correct_outcome / total) * 100, 1),
        "over_under_accuracy": round((correct_over_under / total) * 100, 1),
        "exact_score_accuracy": round((correct_exact_score / total) * 100, 1),
        "correct_outcomes": correct_outcome,
        "correct_over_under": correct_over_under,
        "correct_exact_score": correct_exact_score,
    }


"""
app/services/team_service.py
Team detail pages, tournament journey, and team statistics.
"""

from app.services.data_loader import load_processed_data, load_groups_data
from app.services.statistics import compute_team_stats

_JOURNEY_STAGES = [
    "Group", "Round of 16", "Quarter Final", "Quarter-final",
    "Semi Final", "Semi-final", "Third Place", "Third-place Playoff", "Final",
]
_JOURNEY_LABELS = {
    "Group": "Group Stage",
    "Round of 16": "Round of 16",
    "Quarter Final": "Quarter Finals",
    "Quarter-final": "Quarter Finals",
    "Semi Final": "Semi Finals",
    "Semi-final": "Semi Finals",
    "Third Place": "Third Place Play-off",
    "Third-place Playoff": "Third Place Play-off",
    "Final": "Final",
}


def get_all_teams():
    """Return list of all team names."""
    df = load_processed_data()
    teams = sorted(set(df["home_team"].tolist()) | set(df["away_team"].tolist()))
    return teams


def get_teams_with_stats():
    """Return team stats merged with group info."""
    df = load_processed_data()
    stats = compute_team_stats(df)

    # Try to enrich with group info
    try:
        groups_df = load_groups_data()
        if "group" in groups_df.columns and "team" in groups_df.columns:
            group_map = dict(zip(groups_df["team"], groups_df["group"]))
            stats["group"] = stats["team"].map(group_map).fillna("—")
    except Exception:
        stats["group"] = "—"

    return stats.to_dict(orient="records")


def get_team_detail(team_name):
    """Return full detail for one team."""
    df = load_processed_data()

    team_matches = df[
        (df["home_team"] == team_name) | (df["away_team"] == team_name)
    ].copy().sort_values("date", ascending=True)

    if team_matches.empty:
        return None

    # Per-match result from team's perspective
    records = []
    for _, row in team_matches.iterrows():
        is_home = row["home_team"] == team_name
        if is_home:
            gf = row["home_score"]
            ga = row["away_score"]
            opponent = row["away_team"]
        else:
            gf = row["away_score"]
            ga = row["home_score"]
            opponent = row["home_team"]

        if gf > ga:
            outcome = "Win"
        elif gf < ga:
            outcome = "Loss"
        else:
            outcome = "Draw"

        records.append({
            "match_id": int(row.get("match_id", 0)),
            "date": str(row["date"])[:10],
            "stage": row["stage"],
            "opponent": opponent,
            "goals_for": int(gf),
            "goals_against": int(ga),
            "goal_diff": int(gf - ga),
            "outcome": outcome,
            "home_team": row["home_team"],
            "away_team": row["away_team"],
            "home_score": int(row["home_score"]),
            "away_score": int(row["away_score"]),
        })

    played = len(records)
    wins = sum(1 for r in records if r["outcome"] == "Win")
    draws = sum(1 for r in records if r["outcome"] == "Draw")
    losses = sum(1 for r in records if r["outcome"] == "Loss")
    gf_total = sum(r["goals_for"] for r in records)
    ga_total = sum(r["goals_against"] for r in records)
    win_rate = round(wins / played * 100, 1) if played > 0 else 0.0

    # Tournament journey stages reached
    stages_played = set(team_matches["stage"].tolist())
    journey = []
    seen_labels = set()
    for stage_key in _JOURNEY_STAGES:
        if stage_key in stages_played:
            label = _JOURNEY_LABELS.get(stage_key, stage_key)
            if label not in seen_labels:
                journey.append(label)
                seen_labels.add(label)

    # Group info
    group = "—"
    try:
        groups_df = load_groups_data()
        group_row = groups_df[groups_df["team"] == team_name]
        if not group_row.empty:
            group = group_row.iloc[0]["group"]
    except Exception:
        pass

    return {
        "team_name": team_name,
        "group": group,
        "played": played,
        "wins": wins,
        "draws": draws,
        "losses": losses,
        "goals_for": gf_total,
        "goals_against": ga_total,
        "goal_difference": gf_total - ga_total,
        "points": wins * 3 + draws,
        "win_rate": win_rate,
        "matches": records,
        "journey": journey,
    }

"""
app/services/player_service.py
Player data retrieval, search, filtering, derived metrics, and rankings.
"""

import re
from app.services.data_loader import load_stats_data


def _slugify(name):
    """Create a URL-safe player ID from a name."""
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def _load_players():
    """Load stats.csv and enrich with derived fields."""
    df = load_stats_data().copy()

    # Ensure numeric columns
    for col in ["goals", "assists", "matches_played", "matches_started", "own_goals"]:
        if col in df.columns:
            df[col] = df[col].fillna(0).astype(int)

    # Derived metrics
    df["goal_involvement"] = df["goals"] + df["assists"]
    df["goals_per_match"] = df.apply(
        lambda r: round(r["goals"] / r["matches_played"], 3) if r["matches_played"] > 0 else 0.0,
        axis=1,
    )

    # Stable player ID
    df["player_id"] = df["player"].apply(_slugify)

    return df


def get_all_players():
    return _load_players().to_dict(orient="records")


def filter_players(query=None, team=None, position=None, sort_by="goals_desc"):
    df = _load_players()

    if query and query.strip():
        q = query.strip().lower()
        df = df[
            df["player"].str.lower().str.contains(q, na=False)
            | df["team"].str.lower().str.contains(q, na=False)
        ]

    if team and team != "all":
        df = df[df["team"].str.lower() == team.lower()]

    if position and position != "all":
        if "position" in df.columns:
            df = df[df["position"].str.lower().str.contains(position.lower(), na=False)]

    sort_options = {
        "goals_desc": ("goals", False),
        "goals_asc": ("goals", True),
        "assists_desc": ("assists", False),
        "appearances_desc": ("matches_played", False),
        "starts_desc": ("matches_started", False),
        "involvement_desc": ("goal_involvement", False),
        "gpm_desc": ("goals_per_match", False),
        "name_asc": ("player", True),
    }
    col, asc = sort_options.get(sort_by, ("goals", False))
    df = df.sort_values(col, ascending=asc)

    return df.to_dict(orient="records")


def get_player_by_id(player_id):
    df = _load_players()
    row = df[df["player_id"] == player_id]
    if row.empty:
        return None
    return row.iloc[0].to_dict()


def get_player_teams():
    df = _load_players()
    return sorted(df["team"].unique().tolist())


def get_player_positions():
    df = _load_players()
    if "position" not in df.columns:
        return []
    return sorted(df["position"].dropna().unique().tolist())


def get_rankings():
    df = _load_players()
    return {
        "top_scorers": df.sort_values("goals", ascending=False).head(10).to_dict(orient="records"),
        "top_assists": df.sort_values("assists", ascending=False).head(10).to_dict(orient="records"),
        "most_appearances": df.sort_values("matches_played", ascending=False).head(10).to_dict(orient="records"),
        "most_starts": df.sort_values("matches_started", ascending=False).head(10).to_dict(orient="records"),
        "top_involvement": df.sort_values("goal_involvement", ascending=False).head(10).to_dict(orient="records"),
        "best_gpm": df[df["matches_played"] >= 3].sort_values("goals_per_match", ascending=False).head(10).to_dict(orient="records"),
    }

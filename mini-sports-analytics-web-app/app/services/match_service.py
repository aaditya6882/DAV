"""
app/services/match_service.py
Match data retrieval, filtering, indexing, and detailed match metadata.
"""

from app.services.data_loader import load_processed_data

_STAGE_ORDER = [
    "Group", "Round of 16", "Quarter Final", "Quarter-final",
    "Semi Final", "Semi-final", "Third Place", "Third-place Playoff", "Final",
]


def _df():
    df = load_processed_data().copy()
    if "match_id" not in df.columns:
        df.insert(0, "match_id", range(1, len(df) + 1))
    return df


def get_all_matches():
    return _df()


def filter_matches(stage=None, team=None, venue=None, result=None, query=None, sort_by="date_asc"):
    df = _df()

    if stage and stage != "all":
        df = df[df["stage"].str.lower() == stage.lower()]

    if team and team != "all":
        df = df[
            (df["home_team"].str.lower() == team.lower())
            | (df["away_team"].str.lower() == team.lower())
        ]

    if venue and venue != "all":
        df = df[df["stadium"].str.lower() == venue.lower()]

    if result and result != "all":
        df = df[df["result"] == result]

    if query and query.strip():
        q = query.strip().lower()
        df = df[
            df["home_team"].str.lower().str.contains(q, na=False)
            | df["away_team"].str.lower().str.contains(q, na=False)
            | df["stadium"].str.lower().str.contains(q, na=False)
            | df["city"].str.lower().str.contains(q, na=False)
            | df["stage"].str.lower().str.contains(q, na=False)
        ]

    sort_map = {
        "date_asc": ("date", True),
        "date_desc": ("date", False),
        "goals_desc": ("total_goals", False),
        "goals_asc": ("total_goals", True),
    }
    col, asc = sort_map.get(sort_by, ("date", True))
    df = df.sort_values(col, ascending=asc)

    return df


def get_match_by_id(match_id):
    df = _df()
    try:
        m_id = int(match_id)
    except (ValueError, TypeError):
        return None

    row = df[df["match_id"] == m_id]
    if row.empty:
        return None

    match = row.iloc[0].to_dict()
    home = match["home_team"]
    away = match["away_team"]

    # Previous matches for each team within the tournament
    home_recent = df[
        (df["match_id"] < m_id)
        & ((df["home_team"] == home) | (df["away_team"] == home))
    ].tail(3).to_dict(orient="records")

    away_recent = df[
        (df["match_id"] < m_id)
        & ((df["home_team"] == away) | (df["away_team"] == away))
    ].tail(3).to_dict(orient="records")

    # Determine winner label
    if match["result"] == "home_win":
        match["winner"] = home
    elif match["result"] == "away_win":
        match["winner"] = away
    else:
        match["winner"] = "Draw"

    return {
        "match": match,
        "home_recent": home_recent,
        "away_recent": away_recent,
    }


def get_stages():
    df = _df()
    present = set(df["stage"].unique())
    ordered = [s for s in _STAGE_ORDER if s in present]
    for s in present:
        if s not in ordered:
            ordered.append(s)
    return ordered


def get_venues():
    return sorted(_df()["stadium"].unique().tolist())


def get_teams_list():
    df = _df()
    teams = sorted(set(df["home_team"].tolist()) | set(df["away_team"].tolist()))
    return teams


def get_matches_grouped_by_stage():
    df = _df().sort_values("date", ascending=True)
    grouped = {}
    for stage in _STAGE_ORDER:
        stage_df = df[df["stage"].str.lower() == stage.lower()]
        if not stage_df.empty:
            grouped[stage] = stage_df.to_dict(orient="records")
    # Catch any unlisted stages
    for stage in df["stage"].unique():
        if stage not in grouped:
            stage_df = df[df["stage"] == stage]
            grouped[stage] = stage_df.to_dict(orient="records")
    return grouped

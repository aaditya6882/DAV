"""
app/services/insight_service.py
Dynamic "Did You Know?" facts and tournament records derived from real data.
"""

from app.services.data_loader import (
    load_processed_data,
    load_stats_data,
    load_achievements_data,
)


def get_tournament_records():
    df = load_processed_data()
    stats_df = load_stats_data().copy()

    for col in ["goals", "assists", "matches_played"]:
        if col in stats_df.columns:
            stats_df[col] = stats_df[col].fillna(0).astype(int)

    # Top scorer
    top_scorer_row = stats_df.sort_values("goals", ascending=False).iloc[0]
    top_scorer = f"{top_scorer_row['player']} ({top_scorer_row['goals']} goals)"

    # Top assist
    top_assist_row = stats_df.sort_values("assists", ascending=False).iloc[0]
    top_assist = f"{top_assist_row['player']} ({top_assist_row['assists']} assists)"

    # Highest scoring match
    hs_idx = df["total_goals"].idxmax()
    hs_row = df.loc[hs_idx]
    highest_match = f"{hs_row['home_team']} {int(hs_row['home_score'])}–{int(hs_row['away_score'])} {hs_row['away_team']} ({int(hs_row['total_goals'])} goals)"

    # Biggest victory (largest goal diff)
    df["abs_diff"] = df["goal_difference"].abs()
    bv_idx = df["abs_diff"].idxmax()
    bv_row = df.loc[bv_idx]
    if bv_row["home_score"] > bv_row["away_score"]:
        bv_winner = bv_row["home_team"]
        bv_score = f"{int(bv_row['home_score'])}–{int(bv_row['away_score'])}"
        bv_loser = bv_row["away_team"]
    else:
        bv_winner = bv_row["away_team"]
        bv_score = f"{int(bv_row['away_score'])}–{int(bv_row['home_score'])}"
        bv_loser = bv_row["home_team"]
    biggest_victory = f"{bv_winner} beat {bv_loser} {bv_score}"

    # Highest scoring team (goals for)
    home_gf = df.groupby("home_team")["home_score"].sum()
    away_gf = df.groupby("away_team")["away_score"].sum()
    total_gf = home_gf.add(away_gf, fill_value=0).sort_values(ascending=False)
    top_team_name = total_gf.index[0]
    top_team_goals = int(total_gf.iloc[0])
    highest_scoring_team = f"{top_team_name} ({top_team_goals} goals)"

    # Most matches played (team)
    team_counts = {}
    for _, row in df.iterrows():
        for t in [row["home_team"], row["away_team"]]:
            team_counts[t] = team_counts.get(t, 0) + 1
    most_matches_team = max(team_counts, key=team_counts.get)
    most_matches_count = team_counts[most_matches_team]

    # Most used stadium
    top_stadium = df["stadium"].value_counts().index[0]
    top_stadium_count = int(df["stadium"].value_counts().iloc[0])

    # Champion
    champion = "—"
    try:
        ach = load_achievements_data()
        champ_row = ach[ach["award"].str.lower() == "champion"]
        if not champ_row.empty:
            champion = champ_row.iloc[0]["recipient"]
    except Exception:
        pass

    # Average goals per match
    avg_goals = round(float(df["total_goals"].mean()), 2)

    return {
        "champion": champion,
        "top_scorer": top_scorer,
        "top_scorer_name": top_scorer_row["player"],
        "top_scorer_goals": int(top_scorer_row["goals"]),
        "top_scorer_team": top_scorer_row["team"],
        "top_assist": top_assist,
        "top_assist_name": top_assist_row["player"],
        "top_assist_assists": int(top_assist_row["assists"]),
        "highest_scoring_match": highest_match,
        "biggest_victory": biggest_victory,
        "highest_scoring_team": highest_scoring_team,
        "highest_scoring_team_name": top_team_name,
        "highest_scoring_team_goals": top_team_goals,
        "most_matches_team": most_matches_team,
        "most_matches_count": most_matches_count,
        "most_used_stadium": top_stadium,
        "most_used_stadium_count": top_stadium_count,
        "avg_goals_per_match": avg_goals,
        "total_goals": int(df["total_goals"].sum()),
        "total_matches": len(df),
    }


def get_did_you_know_facts():
    try:
        df = load_processed_data()
        stats_df = load_stats_data().copy()
        for col in ["goals", "assists", "matches_played"]:
            if col in stats_df.columns:
                stats_df[col] = stats_df[col].fillna(0).astype(int)

        facts = []

        # Fact 1: Total goals
        total_goals = int(df["total_goals"].sum())
        facts.append(f"A total of {total_goals} goals were scored across the 2022 World Cup.")

        # Fact 2: Average goals
        avg = round(float(df["total_goals"].mean()), 2)
        facts.append(f"The average number of goals per match was {avg}.")

        # Fact 3: Highest scoring match
        hs = df.loc[df["total_goals"].idxmax()]
        facts.append(
            f"The highest-scoring match was {hs['home_team']} vs {hs['away_team']} with {int(hs['total_goals'])} goals."
        )

        # Fact 4: Number of draws
        draws = int((df["result"] == "draw").sum())
        facts.append(f"{draws} matches ended in a draw during the tournament.")

        # Fact 5: Most goals in a team
        home_gf = df.groupby("home_team")["home_score"].sum()
        away_gf = df.groupby("away_team")["away_score"].sum()
        total_gf = home_gf.add(away_gf, fill_value=0)
        top_team = total_gf.idxmax()
        facts.append(f"{top_team} scored the most goals of any team in the tournament.")

        # Fact 6: Most used city
        top_city = df["city"].value_counts().index[0]
        city_count = int(df["city"].value_counts().iloc[0])
        facts.append(f"{top_city} hosted the most matches — {city_count} in total.")

        # Fact 7: Top scorer's goals
        top_scorer = stats_df.sort_values("goals", ascending=False).iloc[0]
        facts.append(
            f"{top_scorer['player']} finished as the tournament's top scorer with {int(top_scorer['goals'])} goals."
        )

        # Fact 8: Total players
        facts.append(f"{len(stats_df)} players from 32 teams participated in the tournament.")

        # Fact 9: Home wins vs Away wins
        home_wins = int((df["result"] == "home_win").sum())
        away_wins = int((df["result"] == "away_win").sum())
        facts.append(
            f"Home teams won {home_wins} times; away teams won {away_wins} times."
        )

        return facts[:8]  # Return up to 8 facts

    except Exception:
        return ["The 2022 FIFA World Cup was held in Qatar, the first in the Middle East."]


def get_data_quality():
    """Compute dynamic data quality statistics for Data Lab."""
    try:
        df = load_processed_data()
        stats_df = load_stats_data()
        from app.services.data_loader import load_raw_data
        raw_df = load_raw_data()

        return {
            "raw_rows": len(raw_df),
            "raw_cols": len(raw_df.columns),
            "clean_rows": len(df),
            "clean_cols": len(df.columns),
            "missing_values": int(raw_df.isnull().sum().sum()),
            "duplicates": int(raw_df.duplicated().sum()),
            "teams": len(set(df["home_team"]) | set(df["away_team"])),
            "players": len(stats_df),
            "stadiums": df["stadium"].nunique(),
            "cities": df["city"].nunique(),
            "columns": list(df.columns),
            "raw_columns": list(raw_df.columns),
        }
    except Exception as e:
        return {"error": str(e)}

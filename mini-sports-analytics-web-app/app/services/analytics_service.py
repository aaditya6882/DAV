"""
app/services/analytics_service.py
Aggregations for goal distribution, team matrix, stage trends, and venue stats.
"""

from app.services.data_loader import load_processed_data, load_stats_data


def get_goal_analytics():
    df = load_processed_data()

    # Goals distribution (0,1,2,...,N goals per match)
    goals_dist = df["total_goals"].value_counts().sort_index()
    goals_distribution = {str(int(k)): int(v) for k, v in goals_dist.items()}

    # Goals by stage
    goals_by_stage = (
        df.groupby("stage")["total_goals"]
        .agg(["sum", "mean", "count"])
        .rename(columns={"sum": "total", "mean": "avg", "count": "matches"})
        .round(2)
        .reset_index()
        .to_dict(orient="records")
    )

    # Goals by home vs away
    home_goals = int(df["home_score"].sum())
    away_goals = int(df["away_score"].sum())

    # Goals per match over dates
    daily = (
        df.groupby("date")["total_goals"]
        .sum()
        .reset_index()
        .sort_values("date")
    )
    daily["date"] = daily["date"].astype(str)
    goals_over_time = daily.to_dict(orient="records")

    return {
        "goals_distribution": goals_distribution,
        "goals_by_stage": goals_by_stage,
        "home_goals": home_goals,
        "away_goals": away_goals,
        "goals_over_time": goals_over_time,
        "total_goals": int(df["total_goals"].sum()),
        "avg_goals_per_match": round(float(df["total_goals"].mean()), 2),
        "highest_scoring_match": int(df["total_goals"].max()),
    }


def get_team_analytics():
    df = load_processed_data()

    # Goals for each team
    home_gf = df.groupby("home_team")["home_score"].sum()
    away_gf = df.groupby("away_team")["away_score"].sum()
    goals_for = home_gf.add(away_gf, fill_value=0).sort_values(ascending=False)

    home_ga = df.groupby("home_team")["away_score"].sum()
    away_ga = df.groupby("away_team")["home_score"].sum()
    goals_against = home_ga.add(away_ga, fill_value=0)

    # Win/draw/loss per team
    teams = sorted(set(df["home_team"]) | set(df["away_team"]))
    records = []
    for team in teams:
        home = df[df["home_team"] == team]
        away = df[df["away_team"] == team]
        played = len(home) + len(away)
        wins = (home["result"] == "home_win").sum() + (away["result"] == "away_win").sum()
        draws = (home["result"] == "draw").sum() + (away["result"] == "draw").sum()
        losses = played - wins - draws
        gf = int(goals_for.get(team, 0))
        ga = int(goals_against.get(team, 0))
        records.append({
            "team": team,
            "played": int(played),
            "wins": int(wins),
            "draws": int(draws),
            "losses": int(losses),
            "goals_for": gf,
            "goals_against": ga,
            "goal_difference": gf - ga,
            "win_rate": round(wins / played * 100, 1) if played > 0 else 0.0,
        })

    records.sort(key=lambda x: x["goals_for"], reverse=True)
    return records


def get_venue_analytics():
    df = load_processed_data()

    stadium_counts = df["stadium"].value_counts().reset_index()
    stadium_counts.columns = ["stadium", "matches"]
    stadium_goals = df.groupby("stadium")["total_goals"].agg(["sum", "mean"]).reset_index()
    stadium_goals.columns = ["stadium", "total_goals", "avg_goals"]
    stadium_data = stadium_counts.merge(stadium_goals, on="stadium").round(2).to_dict(orient="records")

    city_counts = df["city"].value_counts().reset_index()
    city_counts.columns = ["city", "matches"]
    city_data = city_counts.to_dict(orient="records")

    return {"stadiums": stadium_data, "cities": city_data}


def get_player_analytics():
    df = load_stats_data().copy()
    for col in ["goals", "assists", "matches_played"]:
        if col in df.columns:
            df[col] = df[col].fillna(0).astype(int)

    df["goal_involvement"] = df["goals"] + df["assists"]

    top_scorers = df.sort_values("goals", ascending=False).head(15).to_dict(orient="records")
    top_assists = df.sort_values("assists", ascending=False).head(15).to_dict(orient="records")
    top_involvement = df.sort_values("goal_involvement", ascending=False).head(15).to_dict(orient="records")

    # Goals by team
    team_goals = df.groupby("team")["goals"].sum().sort_values(ascending=False).reset_index()
    team_goals_data = team_goals.to_dict(orient="records")

    return {
        "top_scorers": top_scorers,
        "top_assists": top_assists,
        "top_involvement": top_involvement,
        "team_goals": team_goals_data,
    }


def get_tournament_analytics():
    df = load_processed_data()

    result_counts = df["result"].value_counts().to_dict()

    stage_summary = (
        df.groupby("stage")
        .agg(
            matches=("total_goals", "count"),
            total_goals=("total_goals", "sum"),
            avg_goals=("total_goals", "mean"),
        )
        .round(2)
        .reset_index()
        .to_dict(orient="records")
    )

    return {
        "result_breakdown": {
            "Home Wins": int(result_counts.get("home_win", 0)),
            "Draws": int(result_counts.get("draw", 0)),
            "Away Wins": int(result_counts.get("away_win", 0)),
        },
        "stage_summary": stage_summary,
        "total_matches": len(df),
    }

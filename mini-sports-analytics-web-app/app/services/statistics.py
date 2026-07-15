"""
services/statistics.py
Business Logic Layer — Data Analyst role.

Team- and year-level statistical computations.
"""

import pandas as pd


def compute_team_stats(df):
    """
    Calculate team performance metrics: matches played, wins, draws,
    losses, goals for/against, goal difference, and points
    (3 for a win, 1 for a draw, standard football convention).

    Returns
    -------
    pandas.DataFrame indexed by team, sorted by points descending.
    """
    teams = sorted(set(df["home_team"]) | set(df["away_team"]))
    records = []

    for team in teams:
        home = df[df["home_team"] == team]
        away = df[df["away_team"] == team]

        played = len(home) + len(away)
        wins = (home["result"] == "home_win").sum() + (away["result"] == "away_win").sum()
        losses = (home["result"] == "away_win").sum() + (away["result"] == "home_win").sum()
        draws = played - wins - losses

        goals_for = home["home_score"].sum() + away["away_score"].sum()
        goals_against = home["away_score"].sum() + away["home_score"].sum()

        records.append({
            "team": team,
            "played": int(played),
            "wins": int(wins),
            "draws": int(draws),
            "losses": int(losses),
            "goals_for": int(goals_for),
            "goals_against": int(goals_against),
            "goal_difference": int(goals_for - goals_against),
            "points": int(wins * 3 + draws),
        })

    stats_df = pd.DataFrame(records).sort_values(
        by=["points", "goal_difference", "goals_for"], ascending=False
    ).reset_index(drop=True)

    return stats_df


def compute_year_stats(df):
    """
    Calculate year-level statistics: matches, total & average goals,
    and the number of stages, stadiums, and cities represented.

    Returns
    -------
    pandas.DataFrame indexed by year.
    """
    grouped = df.groupby("year").agg(
        matches=("total_goals", "count"),
        total_goals=("total_goals", "sum"),
        avg_goals_per_match=("total_goals", "mean"),
        stages=("stage", "nunique"),
        stadiums=("stadium", "nunique"),
        cities=("city", "nunique"),
    ).reset_index()

    grouped["avg_goals_per_match"] = grouped["avg_goals_per_match"].round(2)
    grouped = grouped.sort_values(by="matches", ascending=False).reset_index(drop=True)
    return grouped

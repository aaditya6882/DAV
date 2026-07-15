"""
visualizations/tournament.py
Visualization Layer — tournament-specific plots.
"""

import matplotlib.pyplot as plt
import seaborn as sns

from app.services.visualizations.helper import save_figure, get_plot_metadata


def plot_goals_distribution(df):
    """Create goals-per-match distribution histogram."""
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(df["total_goals"], bins=range(0, df["total_goals"].max() + 2),
                 kde=True, color="#2a9d8f", ax=ax)
    ax.set_title("Distribution of Goals per Match")
    ax.set_xlabel("Total Goals in Match")
    ax.set_ylabel("Number of Matches")

    filename = save_figure(fig, "goals_distribution.png")
    return get_plot_metadata(
        title="Goals Distribution",
        filename=filename,
        caption="Shows how many goals are typically scored per match across the dataset.",
    )


def plot_top_scorers(df, top_n=10):
    """Create a bar chart of the top scoring teams (total goals for)."""
    goals_for = (
        df.groupby("home_team")["home_score"].sum()
        .add(df.groupby("away_team")["away_score"].sum(), fill_value=0)
        .sort_values(ascending=False)
        .head(top_n)
    )

    fig, ax = plt.subplots(figsize=(9, 5))
    sns.barplot(x=goals_for.values, y=goals_for.index, hue=goals_for.index,
                palette="viridis", legend=False, ax=ax)
    ax.set_title(f"Top {top_n} Scoring Teams")
    ax.set_xlabel("Total Goals Scored")
    ax.set_ylabel("Team")

    filename = save_figure(fig, "top_scorers.png")
    return get_plot_metadata(
        title="Top Scoring Teams",
        filename=filename,
        caption=f"The {top_n} teams that scored the most goals across all matches.",
    )


def plot_results_breakdown(df):
    """Create a bar chart of match outcomes (home win / draw / away win)."""
    counts = df["result"].value_counts().reindex(
        ["home_win", "draw", "away_win"]
    ).fillna(0)
    labels = ["Home Win", "Draw", "Away Win"]

    fig, ax = plt.subplots(figsize=(7, 5))
    sns.barplot(x=labels, y=counts.values, hue=labels, palette="mako",
                legend=False, ax=ax)
    ax.set_title("Match Result Breakdown")
    ax.set_xlabel("Result Type")
    ax.set_ylabel("Number of Matches")

    filename = save_figure(fig, "results_breakdown.png")
    return get_plot_metadata(
        title="Match Result Breakdown",
        filename=filename,
        caption="How often matches ended in a home win, draw, or away win.",
    )

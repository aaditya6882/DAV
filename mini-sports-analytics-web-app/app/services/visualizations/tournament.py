"""
visualizations/tournament.py
Visualization Layer — tournament & player statistics with Matplotlib/Seaborn + explicit data labels.
Uses all 4 datasets: matches.csv, stats.csv, groups.csv, achievements.csv.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import seaborn as sns

from app.services.visualizations.helper import save_figure, get_plot_metadata
from app.services.data_loader import (
    load_groups_data,
    load_stats_data,
    load_achievements_data,
)


def plot_goals_distribution(df):
    """Goals-per-match histogram with explicit count labels on each bar."""
    counts = df["total_goals"].value_counts().sort_index()

    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.bar(
        counts.index,
        counts.values,
        color="#2a9d8f",
        edgecolor="#1a6b63",
        linewidth=0.8,
        zorder=3,
    )
    # Explicit data labels above each bar
    for bar in bars:
        h = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            h + 0.15,
            str(int(h)),
            ha="center",
            va="bottom",
            fontsize=11,
            fontweight="bold",
            color="#1a1a2e",
        )

    ax.set_title("Distribution of Goals per Match", fontsize=15, fontweight="bold", pad=14)
    ax.set_xlabel("Total Goals in Match", fontsize=11)
    ax.set_ylabel("Number of Matches", fontsize=11)
    ax.set_xticks(counts.index)
    ax.yaxis.grid(True, linestyle="--", alpha=0.5)
    ax.set_axisbelow(True)
    fig.tight_layout()

    filename = save_figure(fig, "goals_distribution.png")
    return get_plot_metadata(
        title="Goals Distribution",
        filename=filename,
        caption="How many goals are typically scored per match. Labels show exact match count.",
    )


def plot_top_scorers(df, top_n=10):
    """Horizontal bar chart of top scoring teams with explicit goal labels."""
    goals_for = (
        df.groupby("home_team")["home_score"]
        .sum()
        .add(df.groupby("away_team")["away_score"].sum(), fill_value=0)
        .sort_values(ascending=True)
        .tail(top_n)
    )

    fig, ax = plt.subplots(figsize=(9, 5))
    palette = sns.color_palette("viridis", len(goals_for))
    bars = ax.barh(goals_for.index, goals_for.values, color=palette, edgecolor="#333", linewidth=0.6)

    # Explicit label inside/end of each bar
    for bar, val in zip(bars, goals_for.values):
        ax.text(
            bar.get_width() - 0.3,
            bar.get_y() + bar.get_height() / 2,
            f"{int(val)} goals",
            va="center",
            ha="right",
            fontsize=10,
            fontweight="bold",
            color="white",
        )

    ax.set_title(f"Top {top_n} Scoring Teams", fontsize=15, fontweight="bold", pad=14)
    ax.set_xlabel("Total Goals Scored", fontsize=11)
    ax.xaxis.grid(True, linestyle="--", alpha=0.4)
    ax.set_axisbelow(True)
    fig.tight_layout()

    filename = save_figure(fig, "top_scorers.png")
    return get_plot_metadata(
        title="Top Scoring Teams",
        filename=filename,
        caption=f"The {top_n} teams that scored the most goals. Labels show exact goal count.",
    )


def plot_results_breakdown(df):
    """Bar chart of match outcomes with explicit count & percentage labels."""
    counts = (
        df["result"]
        .value_counts()
        .reindex(["home_win", "draw", "away_win"])
        .fillna(0)
    )
    labels = ["Home Win", "Draw", "Away Win"]
    colors = ["#2a9d8f", "#e9c46a", "#e76f51"]
    total = counts.sum()

    fig, ax = plt.subplots(figsize=(7, 5))
    bars = ax.bar(labels, counts.values, color=colors, edgecolor="#333", linewidth=0.8, zorder=3)

    # Explicit count + percentage label on each bar
    for bar, val in zip(bars, counts.values):
        pct = val / total * 100
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.3,
            f"{int(val)}\n({pct:.1f}%)",
            ha="center",
            va="bottom",
            fontsize=11,
            fontweight="bold",
            color="#1a1a2e",
        )

    ax.set_title("Match Result Breakdown", fontsize=15, fontweight="bold", pad=14)
    ax.set_xlabel("Result Type", fontsize=11)
    ax.set_ylabel("Number of Matches", fontsize=11)
    ax.yaxis.grid(True, linestyle="--", alpha=0.5)
    ax.set_axisbelow(True)
    fig.tight_layout()

    filename = save_figure(fig, "results_breakdown.png")
    return get_plot_metadata(
        title="Match Result Breakdown",
        filename=filename,
        caption="How often matches ended in a home win, draw, or away win, with exact counts and percentages.",
    )


def plot_top_player_scorers(top_n=10):
    """Horizontal bar chart of individual player goal scorers from stats.csv with labels."""
    stats_df = load_stats_data()
    top_players = (
        stats_df[stats_df["goals"] > 0]
        .sort_values(by=["goals", "assists"], ascending=True)
        .tail(top_n)
    )

    fig, ax = plt.subplots(figsize=(10, 5))
    palette = sns.color_palette("crest", len(top_players))
    bars = ax.barh(top_players["player"], top_players["goals"], color=palette, edgecolor="#333", linewidth=0.6)

    # Explicit label inside bar
    for bar, (_, row) in zip(bars, top_players.iterrows()):
        ax.text(
            bar.get_width() - 0.1,
            bar.get_y() + bar.get_height() / 2,
            f"{int(row['goals'])} goals  ({row['team']})",
            va="center",
            ha="right",
            fontsize=9,
            fontweight="bold",
            color="white",
        )

    ax.set_title("Top Individual Goal Scorers (stats.csv)", fontsize=15, fontweight="bold", pad=14)
    ax.set_xlabel("Goals Scored", fontsize=11)
    ax.xaxis.grid(True, linestyle="--", alpha=0.4)
    ax.set_axisbelow(True)
    fig.tight_layout()

    filename = save_figure(fig, "top_player_scorers.png")
    return get_plot_metadata(
        title="Top Individual Goal Scorers",
        filename=filename,
        caption="Players with the most goals in the tournament. Labels show goals and national team.",
    )


def plot_group_standings():
    """Grouped bar chart of group stage points from groups.csv with explicit labels."""
    groups_df = load_groups_data()

    fig, ax = plt.subplots(figsize=(14, 6))
    palette = sns.color_palette("tab10", 8)

    n_groups = groups_df["group"].nunique()
    group_names = sorted(groups_df["group"].unique())
    bar_width = 0.18
    x_base = range(4)  # up to 4 teams per group

    for i, (grp_name, color) in enumerate(zip(group_names, palette)):
        grp_data = groups_df[groups_df["group"] == grp_name].sort_values("position")
        xs = [x + i * bar_width for x in x_base[:len(grp_data)]]
        bars = ax.bar(xs, grp_data["points"].values, width=bar_width, color=color,
                      edgecolor="#333", linewidth=0.6, label=f"Group {grp_name}", zorder=3)

        # Explicit point + team label inside each bar
        for bar, (_, row) in zip(bars, grp_data.iterrows()):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() / 2,
                f"{row['team']}\n{int(row['points'])}pts",
                ha="center",
                va="center",
                fontsize=7,
                fontweight="bold",
                color="white",
                rotation=90,
            )

    ax.set_title("Group Stage Points by Team (groups.csv)", fontsize=15, fontweight="bold", pad=14)
    ax.set_ylabel("Points Earned", fontsize=11)
    ax.set_xlabel("Team Position within Group", fontsize=11)
    ax.set_xticks([x + 3.5 * bar_width for x in x_base])
    ax.set_xticklabels(["1st", "2nd", "3rd", "4th"])
    ax.yaxis.grid(True, linestyle="--", alpha=0.5)
    ax.set_axisbelow(True)
    ax.legend(title="Group", bbox_to_anchor=(1.01, 1), loc="upper left", fontsize=9)
    fig.tight_layout()

    filename = save_figure(fig, "group_standings.png")
    return get_plot_metadata(
        title="Group Stage Standings",
        filename=filename,
        caption="Points accumulated by each national team during the group stage (groups.csv). Labels show team name and points.",
    )


def plot_tournament_awards():
    """Horizontal summary chart of tournament awards from achievements.csv with recipient labels."""
    ach_df = load_achievements_data()

    colors_team = "#2a9d8f"
    colors_ind = "#e76f51"
    bar_colors = [colors_team if c == "Team" else colors_ind for c in ach_df["category"]]

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(ach_df["award"][::-1], [1] * len(ach_df), color=bar_colors[::-1],
                   edgecolor="#333", linewidth=0.6)

    # Explicit recipient + team label inside each bar
    for bar, (_, row) in zip(bars, ach_df[::-1].iterrows()):
        label = f"{row['recipient']}  ({row['team']})"
        ax.text(
            0.02,
            bar.get_y() + bar.get_height() / 2,
            label,
            va="center",
            ha="left",
            fontsize=11,
            fontweight="bold",
            color="white",
        )

    ax.set_xlim(0, 1.3)
    ax.set_title("FIFA World Cup 2022 Awards (achievements.csv)", fontsize=15, fontweight="bold", pad=14)
    ax.xaxis.set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)

    legend_patches = [
        mpatches.Patch(color=colors_team, label="Team Award"),
        mpatches.Patch(color=colors_ind, label="Individual Award"),
    ]
    ax.legend(handles=legend_patches, loc="lower right", fontsize=10)
    fig.tight_layout()

    filename = save_figure(fig, "tournament_awards.png")
    return get_plot_metadata(
        title="Official Tournament Awards",
        filename=filename,
        caption="Official FIFA awards and recipients from achievements.csv. Color distinguishes Team vs Individual awards.",
    )

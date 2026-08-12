"""
visualizations/geography.py
Visualization Layer — geographic & performance plots with Matplotlib/Seaborn + explicit data labels.
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from app.services.visualizations.helper import save_figure, get_plot_metadata


def plot_stadium_distribution(df, top_n=8):
    """Pie chart of matches per stadium with explicit percentage and count labels."""
    counts = df["stadium"].value_counts()
    top = counts.head(top_n)
    other_total = counts.iloc[top_n:].sum()
    if other_total > 0:
        top = pd.concat([top, pd.Series({"Other": other_total})])

    fig, ax = plt.subplots(figsize=(9, 8))
    colors = sns.color_palette("viridis", len(top))
    wedges, texts, autotexts = ax.pie(
        top.values,
        labels=top.index,
        autopct=lambda pct: f"{pct:.1f}%\n({int(round(pct/100*top.values.sum()))} matches)",
        colors=colors,
        startangle=90,
        wedgeprops={"edgecolor": "white", "linewidth": 1.5},
        pctdistance=0.75,
    )
    for autotext in autotexts:
        autotext.set_fontsize(9)
        autotext.set_fontweight("bold")

    ax.set_title("Matches per Stadium", fontsize=15, fontweight="bold", pad=14)
    fig.tight_layout()

    filename = save_figure(fig, "stadium_distribution.png")
    return get_plot_metadata(
        title="Stadium Distribution",
        filename=filename,
        caption="Share of total matches hosted by each stadium. Labels show percentage and exact match count.",
    )


def plot_heatmap_by_city(df):
    """Annotated heatmap of matches by city vs. tournament stage."""
    pivot = pd.crosstab(df["city"], df["stage"])

    fig, ax = plt.subplots(figsize=(10, max(5, 0.45 * len(pivot))))
    sns.heatmap(
        pivot,
        annot=True,
        fmt="d",
        cmap="YlGnBu",
        linewidths=0.6,
        linecolor="#ddd",
        annot_kws={"fontsize": 12, "fontweight": "bold"},
        ax=ax,
    )
    ax.set_title("Matches by City and Tournament Stage", fontsize=15, fontweight="bold", pad=14)
    ax.set_xlabel("Stage", fontsize=11)
    ax.set_ylabel("City", fontsize=11)
    fig.tight_layout()

    filename = save_figure(fig, "heatmap_by_city.png")
    return get_plot_metadata(
        title="Matches by City & Stage",
        filename=filename,
        caption="Number of matches hosted in each city, broken down by tournament stage. Numbers annotated in every cell.",
    )


def plot_team_performance_matrix(df):
    """Scatter plot of Goals Scored vs Goals Conceded with explicit team name annotations."""
    teams = list(set(df["home_team"]).union(set(df["away_team"])))
    matrix_data = []

    for t in teams:
        home_m = df[df["home_team"] == t]
        away_m = df[df["away_team"] == t]
        goals_for = int(home_m["home_score"].sum() + away_m["away_score"].sum())
        goals_against = int(home_m["away_score"].sum() + away_m["home_score"].sum())
        matches = len(home_m) + len(away_m)
        matrix_data.append({
            "team": t,
            "goals_for": goals_for,
            "goals_against": goals_against,
            "matches": matches,
            "goal_diff": goals_for - goals_against,
        })

    perf_df = pd.DataFrame(matrix_data)

    fig, ax = plt.subplots(figsize=(11, 7))
    scatter = ax.scatter(
        perf_df["goals_against"],
        perf_df["goals_for"],
        s=perf_df["matches"] * 40,
        c=perf_df["goal_diff"],
        cmap="RdYlGn",
        edgecolors="#333",
        linewidth=0.8,
        alpha=0.85,
        zorder=3,
    )
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label("Goal Difference", fontsize=10)

    # Explicit team name annotations on every point
    for _, row in perf_df.iterrows():
        ax.annotate(
            row["team"],
            (row["goals_against"], row["goals_for"]),
            xytext=(5, 4),
            textcoords="offset points",
            fontsize=8,
            fontweight="bold",
            color="#1a1a2e",
        )

    # Reference diagonal line
    max_val = max(perf_df["goals_for"].max(), perf_df["goals_against"].max()) + 1
    ax.plot([0, max_val], [0, max_val], "k--", linewidth=0.8, alpha=0.4, label="Equal goals")
    ax.legend(fontsize=9)

    ax.set_title("Team Performance: Goals Scored vs Goals Conceded", fontsize=15, fontweight="bold", pad=14)
    ax.set_xlabel("Goals Conceded (lower is better)", fontsize=11)
    ax.set_ylabel("Goals Scored (higher is better)", fontsize=11)
    ax.yaxis.grid(True, linestyle="--", alpha=0.4)
    ax.xaxis.grid(True, linestyle="--", alpha=0.4)
    ax.set_axisbelow(True)
    fig.tight_layout()

    filename = save_figure(fig, "team_performance_matrix.png")
    return get_plot_metadata(
        title="Team Performance Matrix",
        filename=filename,
        caption="Goals scored vs conceded for every team. Team names annotated directly on points. Bubble size = matches played.",
    )

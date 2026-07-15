"""
visualizations/geography.py
Visualization Layer — geographic plots (stadiums / cities).
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from app.services.visualizations.helper import save_figure, get_plot_metadata


def plot_stadium_distribution(df, top_n=8):
    """Create a pie chart of matches per stadium (top N, rest grouped as 'Other')."""
    counts = df["stadium"].value_counts()

    top = counts.head(top_n)
    other_total = counts.iloc[top_n:].sum()
    if other_total > 0:
        top = pd.concat([top, pd.Series({"Other": other_total})])

    fig, ax = plt.subplots(figsize=(8, 8))
    colors = sns.color_palette("viridis", len(top))
    ax.pie(top.values, labels=top.index, autopct="%1.0f%%", colors=colors,
           startangle=90, wedgeprops={"edgecolor": "white", "linewidth": 1})
    ax.set_title("Matches per Stadium")

    filename = save_figure(fig, "stadium_distribution.png")
    return get_plot_metadata(
        title="Stadium Distribution",
        filename=filename,
        caption="Share of total matches hosted by each stadium.",
    )


def plot_heatmap_by_city(df):
    """Create a heatmap of matches by city vs. tournament stage."""
    pivot = pd.crosstab(df["city"], df["stage"])

    fig, ax = plt.subplots(figsize=(9, max(5, 0.4 * len(pivot))))
    sns.heatmap(pivot, annot=True, fmt="d", cmap="YlGnBu", linewidths=0.5, ax=ax)
    ax.set_title("Matches by City and Tournament Stage")
    ax.set_xlabel("Stage")
    ax.set_ylabel("City")

    filename = save_figure(fig, "heatmap_by_city.png")
    return get_plot_metadata(
        title="Matches by City & Stage",
        filename=filename,
        caption="Number of matches hosted in each city, broken down by tournament stage.",
    )

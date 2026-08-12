"""
visualizations/generate.py
Integration Layer — orchestrates all visualization generation across all raw datasets.
Uses only Matplotlib/Seaborn (no Plotly).
"""

from app.services.visualizations.tournament import (
    plot_goals_distribution,
    plot_top_scorers,
    plot_top_player_scorers,
    plot_results_breakdown,
    plot_group_standings,
    plot_tournament_awards,
)
from app.services.visualizations.geography import (
    plot_stadium_distribution,
    plot_heatmap_by_city,
    plot_team_performance_matrix,
)


def generate_all_plots(df):
    """
    Orchestrate all visualization generation across matches, groups, stats, and achievements datasets.

    Parameters
    ----------
    df : pandas.DataFrame
        Cleaned, analysis-ready dataframe (matches.csv).

    Returns
    -------
    list[dict] : plot metadata (title, filename, caption, url) for each
    generated visualization, ready to hand to a Jinja2 template.
    """
    plots = []
    # 1. Matches dataset
    plots.append(plot_goals_distribution(df))
    plots.append(plot_top_scorers(df))
    plots.append(plot_results_breakdown(df))

    # 2. Player stats dataset (stats.csv)
    plots.append(plot_top_player_scorers())

    # 3. Group stage dataset (groups.csv)
    plots.append(plot_group_standings())

    # 4. Tournament awards dataset (achievements.csv)
    plots.append(plot_tournament_awards())

    # 5. Venue & Performance analysis (matches.csv)
    plots.append(plot_stadium_distribution(df))
    plots.append(plot_heatmap_by_city(df))
    plots.append(plot_team_performance_matrix(df))
    return plots

"""
visualizations/generate.py
Integration Layer — orchestrates all visualization generation.
"""

from app.services.visualizations.tournament import (
    plot_goals_distribution,
    plot_top_scorers,
    plot_results_breakdown,
)
from app.services.visualizations.geography import (
    plot_stadium_distribution,
    plot_heatmap_by_city,
)


def generate_all_plots(df):
    """
    Orchestrate all visualization generation.

    Parameters
    ----------
    df : pandas.DataFrame
        Cleaned, analysis-ready dataframe.

    Returns
    -------
    list[dict] : plot metadata (title, filename, caption, url) for each
    generated visualization, ready to hand to a Jinja2 template.
    """
    plots = []
    plots.append(plot_goals_distribution(df))
    plots.append(plot_top_scorers(df))
    plots.append(plot_results_breakdown(df))
    plots.append(plot_stadium_distribution(df))
    plots.append(plot_heatmap_by_city(df))
    return plots

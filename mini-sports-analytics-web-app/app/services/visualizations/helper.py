"""
visualizations/helper.py
Visualization Layer — shared utilities used by every plotting module.

Keeps plot-saving and metadata logic in one place so tournament.py and
geography.py stay focused purely on chart content.
"""

import os
import matplotlib
matplotlib.use("Agg")  # headless backend, safe for Flask server processes
import matplotlib.pyplot as plt
import seaborn as sns
from flask import current_app

# Consistent visual theme across all plots
sns.set_theme(style="whitegrid", palette="viridis")


def save_figure(fig, filename):
    """
    Save a matplotlib figure to static/images/plots/.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
    filename : str
        e.g. "goals_distribution.png"

    Returns
    -------
    str : the filename that was saved (for use in get_plot_metadata)
    """
    plots_dir = current_app.config["PLOTS_DIR"]
    os.makedirs(plots_dir, exist_ok=True)

    filepath = os.path.join(plots_dir, filename)
    fig.savefig(filepath, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return filename


def get_plot_metadata(title, filename, caption):
    """
    Return standardized plot metadata for the routes/template layer.

    Returns
    -------
    dict with keys: title, filename, caption, url
    """
    url_prefix = current_app.config["PLOTS_URL_PREFIX"]
    return {
        "title": title,
        "filename": filename,
        "caption": caption,
        "url": f"{url_prefix}/{filename}",
    }

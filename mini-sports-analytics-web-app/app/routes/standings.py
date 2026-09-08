"""
app/routes/standings.py
Standings blueprint.
"""

from flask import Blueprint, render_template
from app.services.data_loader import load_groups_data

standings_bp = Blueprint("standings", __name__)


@standings_bp.route("/standings")
def standings():
    try:
        groups_df = load_groups_data()
        groups = {}
        for g in sorted(groups_df["group"].unique()):
            group_rows = (
                groups_df[groups_df["group"] == g]
                .sort_values("position")
                .to_dict(orient="records")
            )
            groups[g] = group_rows
    except Exception:
        groups = {}

    return render_template(
        "standings.html",
        active_tab="standings",
        groups=groups,
        page_title="Group Standings",
        meta_description="Official FIFA World Cup 2022 group stage standings for all 8 groups (A–H).",
    )

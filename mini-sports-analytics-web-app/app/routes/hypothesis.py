"""
app/routes/hypothesis.py
Blueprint for Statistical Hypothesis Testing Dashboard and API.
"""

from flask import Blueprint, render_template, request, jsonify
from app.services.hypothesis_service import run_all_hypothesis_tests

hypothesis_bp = Blueprint("hypothesis", __name__)


@hypothesis_bp.route("/hypothesis")
def hypothesis_page():
    """Render the interactive hypothesis testing dashboard."""
    try:
        alpha = float(request.args.get("alpha", 0.05))
        if alpha not in [0.01, 0.05, 0.10]:
            alpha = 0.05
    except ValueError:
        alpha = 0.05

    results = run_all_hypothesis_tests(alpha=alpha)

    return render_template(
        "hypothesis.html",
        active_tab="hypothesis",
        results=results,
        page_title="Hypothesis Testing",
        meta_description="Statistical hypothesis testing suite for FIFA World Cup 2022 dataset using t-tests, ANOVA, Chi-Square, and Mann-Whitney tests.",
    )


@hypothesis_bp.route("/api/hypothesis")
def hypothesis_api():
    """API endpoint returning hypothesis test results in JSON format."""
    try:
        alpha = float(request.args.get("alpha", 0.05))
        if alpha not in [0.01, 0.05, 0.10]:
            alpha = 0.05
    except ValueError:
        alpha = 0.05

    results = run_all_hypothesis_tests(alpha=alpha)
    return jsonify(results)

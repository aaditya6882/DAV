"""
app/services/hypothesis_service.py
Service Layer — Statistical Hypothesis Testing Engine for FIFA World Cup 2022.

Implements inferential statistical tests using scipy.stats:
1. Home Advantage Test (Two-Sample Welch's t-Test)
2. Stage Goal Intensity Test (One-Way ANOVA)
3. Match Outcome Uniformity (Chi-Square Goodness-of-Fit)
4. Top Team Goal Superiority (Mann-Whitney U Test)
"""

import numpy as np
import pandas as pd
from scipy import stats
from app.services.data_loader import load_processed_data, load_stats_data


def test_home_advantage(df=None, alpha=0.05):
    """
    Test 1: Two-Sample Welch's t-Test for Home Advantage.
    H0: Average home team goals equal average away team goals (mu_home = mu_away).
    H1: Average home team goals do not equal average away team goals (mu_home != mu_away).
    """
    if df is None:
        df = load_processed_data()

    home_goals = df["home_score"].astype(float).values
    away_goals = df["away_score"].astype(float).values

    n_home, n_away = len(home_goals), len(away_goals)
    mean_home, mean_away = float(np.mean(home_goals)), float(np.mean(away_goals))
    std_home, std_away = float(np.std(home_goals, ddof=1)), float(np.std(away_goals, ddof=1))

    # Welch's t-test (equal_var=False)
    t_stat, p_val = stats.ttest_ind(home_goals, away_goals, equal_var=False)

    # Degrees of freedom for Welch's t-test
    v_home = (std_home ** 2) / n_home
    v_away = (std_away ** 2) / n_away
    df_val = ((v_home + v_away) ** 2) / ((v_home ** 2) / (n_home - 1) + (v_away ** 2) / (n_away - 1)) if (v_home + v_away) > 0 else (n_home + n_away - 2)

    reject_h0 = bool(p_val < alpha)

    if reject_h0:
        interpretation = (
            f"Statistically significant difference detected (p = {p_val:.4f} < {alpha}). "
            f"Home teams averaged {mean_home:.2f} goals vs away teams {mean_away:.2f} goals."
        )
    else:
        interpretation = (
            f"No statistically significant home advantage found (p = {p_val:.4f} >= {alpha}). "
            f"Mean home goals ({mean_home:.2f}) and away goals ({mean_away:.2f}) are statistically comparable."
        )

    return {
        "id": "home_advantage",
        "title": "Home Advantage Hypothesis (Welch's t-Test)",
        "test_name": "Two-Sample Welch's t-Test",
        "null_hypothesis": "H₀: μ_home = μ_away (Home and Away team goal averages are equal)",
        "alt_hypothesis": "H₁: μ_home ≠ μ_away (Home and Away team goal averages differ significantly)",
        "statistic_name": "t-statistic",
        "statistic_value": round(float(t_stat), 4),
        "p_value": round(float(p_val), 4),
        "degrees_of_freedom": round(float(df_val), 2),
        "alpha": alpha,
        "reject_h0": reject_h0,
        "interpretation": interpretation,
        "sample_metrics": {
            "n_home": n_home,
            "n_away": n_away,
            "mean_home": round(mean_home, 2),
            "mean_away": round(mean_away, 2),
            "std_home": round(std_home, 2),
            "std_away": round(std_away, 2),
        },
    }


def test_stage_goal_intensity(df=None, alpha=0.05):
    """
    Test 2: One-Way ANOVA Test for Goal Differences Across Tournament Stages.
    H0: Mean total goals per match are equal across all tournament stages.
    H1: At least one tournament stage has a significantly different mean total goals per match.
    """
    if df is None:
        df = load_processed_data()

    stages = df["stage"].dropna().unique()
    stage_groups = []
    stage_summary = {}

    for st in stages:
        goals = df[df["stage"] == st]["total_goals"].astype(float).values
        if len(goals) > 0:
            stage_groups.append(goals)
            stage_summary[st] = {
                "count": len(goals),
                "mean": round(float(np.mean(goals)), 2),
                "std": round(float(np.std(goals, ddof=1)), 2) if len(goals) > 1 else 0.0,
            }

    if len(stage_groups) > 1:
        f_stat, p_val = stats.f_oneway(*stage_groups)
    else:
        f_stat, p_val = 0.0, 1.0

    reject_h0 = bool(p_val < alpha)

    if reject_h0:
        interpretation = (
            f"Statistically significant variance in goal scoring across tournament stages (F = {f_stat:.2f}, p = {p_val:.4f} < {alpha})."
        )
    else:
        interpretation = (
            f"No statistically significant difference in goal scoring intensity across tournament stages (F = {f_stat:.2f}, p = {p_val:.4f} >= {alpha}). "
            f"Scoring rates remained consistent from group stage through knockout rounds."
        )

    return {
        "id": "stage_intensity",
        "title": "Stage Goal Intensity Hypothesis (One-Way ANOVA)",
        "test_name": "One-Way Analysis of Variance (ANOVA)",
        "null_hypothesis": "H₀: μ_Group = μ_R16 = μ_QF = μ_SF = μ_Final (Goal averages are equal across stages)",
        "alt_hypothesis": "H₁: At least one stage has a significantly different goal average",
        "statistic_name": "F-statistic",
        "statistic_value": round(float(f_stat), 4),
        "p_value": round(float(p_val), 4),
        "alpha": alpha,
        "reject_h0": reject_h0,
        "interpretation": interpretation,
        "stage_breakdown": stage_summary,
    }


def test_outcome_uniformity(df=None, alpha=0.05):
    """
    Test 3: Chi-Square Goodness-of-Fit Test for Match Outcome Distribution.
    H0: Match outcomes (Home Win, Away Win, Draw) are uniformly distributed (1/3 each).
    H1: Match outcomes do not follow a uniform 1/3 distribution.
    """
    if df is None:
        df = load_processed_data()

    counts = df["result"].value_counts()
    home_wins = int(counts.get("home_win", 0))
    away_wins = int(counts.get("away_win", 0))
    draws = int(counts.get("draw", 0))

    observed = np.array([home_wins, away_wins, draws])
    total_matches = int(np.sum(observed))
    expected = np.array([total_matches / 3.0] * 3)

    chi2_stat, p_val = stats.chisquare(f_obs=observed, f_exp=expected)
    df_val = len(observed) - 1

    reject_h0 = bool(p_val < alpha)

    if reject_h0:
        interpretation = (
            f"Match outcomes significantly deviate from a uniform distribution (χ² = {chi2_stat:.2f}, p = {p_val:.4f} < {alpha}). "
            f"Observed counts: Home Wins ({home_wins}), Away Wins ({away_wins}), Draws ({draws})."
        )
    else:
        interpretation = (
            f"Match outcomes do not significantly deviate from equal probability (χ² = {chi2_stat:.2f}, p = {p_val:.4f} >= {alpha})."
        )

    return {
        "id": "outcome_uniformity",
        "title": "Match Outcome Uniformity (Chi-Square Goodness-of-Fit)",
        "test_name": "Chi-Square Goodness-of-Fit Test",
        "null_hypothesis": "H₀: P(Home Win) = P(Away Win) = P(Draw) = 33.33%",
        "alt_hypothesis": "H₁: Match outcomes are not uniformly distributed",
        "statistic_name": "χ² statistic",
        "statistic_value": round(float(chi2_stat), 4),
        "p_value": round(float(p_val), 4),
        "degrees_of_freedom": df_val,
        "alpha": alpha,
        "reject_h0": reject_h0,
        "interpretation": interpretation,
        "outcome_counts": {
            "home_wins": home_wins,
            "away_wins": away_wins,
            "draws": draws,
            "expected_per_category": round(total_matches / 3.0, 1),
            "total_matches": total_matches,
        },
    }


def test_top_team_superiority(df=None, alpha=0.05):
    """
    Test 4: Mann-Whitney U Non-Parametric Test for Top Team Goal Superiority.
    H0: Top 8 quarter-finalist teams score goals from the same distribution as other teams.
    H1: Top 8 teams score significantly higher goals per match.
    """
    if df is None:
        df = load_processed_data()

    # Identify top 8 teams based on goals scored or stage reached
    top_teams = {"Argentina", "France", "Croatia", "Morocco", "Netherlands", "England", "Brazil", "Portugal"}

    top_goals = []
    other_goals = []

    for _, row in df.iterrows():
        if row["home_team"] in top_teams:
            top_goals.append(float(row["home_score"]))
        else:
            other_goals.append(float(row["home_score"]))

        if row["away_team"] in top_teams:
            top_goals.append(float(row["away_score"]))
        else:
            other_goals.append(float(row["away_score"]))

    top_goals = np.array(top_goals)
    other_goals = np.array(other_goals)

    u_stat, p_val = stats.mannwhitneyu(top_goals, other_goals, alternative="greater")

    reject_h0 = bool(p_val < alpha)

    mean_top = float(np.mean(top_goals))
    mean_other = float(np.mean(other_goals))

    if reject_h0:
        interpretation = (
            f"Statistically significant evidence that top quarter-finalist teams score goals at higher rates "
            f"(U = {u_stat:.1f}, p = {p_val:.4f} < {alpha}). Top teams mean: {mean_top:.2f} goals vs other teams: {mean_other:.2f} goals."
        )
    else:
        interpretation = (
            f"No statistically significant difference in goal scoring distributions between top 8 teams and other teams "
            f"(U = {u_stat:.1f}, p = {p_val:.4f} >= {alpha})."
        )

    return {
        "id": "top_team_superiority",
        "title": "Top Team Goal Superiority (Mann-Whitney U Test)",
        "test_name": "Mann-Whitney U Non-Parametric Test",
        "null_hypothesis": "H₀: Top 8 teams and other teams score goals from identical distributions",
        "alt_hypothesis": "H₁: Top 8 teams score significantly more goals per match",
        "statistic_name": "U-statistic",
        "statistic_value": round(float(u_stat), 4),
        "p_value": round(float(p_val), 4),
        "alpha": alpha,
        "reject_h0": reject_h0,
        "interpretation": interpretation,
        "group_metrics": {
            "top_teams_count": len(top_teams),
            "top_teams_match_instances": len(top_goals),
            "other_teams_match_instances": len(other_goals),
            "top_teams_mean_goals": round(mean_top, 2),
            "other_teams_mean_goals": round(mean_other, 2),
        },
    }


def run_all_hypothesis_tests(alpha=0.05):
    """
    Run all 4 statistical hypothesis tests and return a comprehensive summary dictionary.
    """
    df = load_processed_data()

    tests = [
        test_home_advantage(df, alpha=alpha),
        test_stage_goal_intensity(df, alpha=alpha),
        test_outcome_uniformity(df, alpha=alpha),
        test_top_team_superiority(df, alpha=alpha),
    ]

    total_tests = len(tests)
    rejected_count = sum(1 for t in tests if t["reject_h0"])

    return {
        "alpha": alpha,
        "total_tests": total_tests,
        "significant_findings": rejected_count,
        "tests": tests,
    }

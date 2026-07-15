"""
services/eda.py
Business Logic Layer — Data Analyst role.

Exploratory Data Analysis: descriptive statistics, dataset overview,
and outlier detection.
"""

def generate_summary(df):
    """
    Generate descriptive statistics and a data overview.

    Returns
    -------
    dict
        Overview info suitable for passing directly into a template.
    """
    numeric_summary = df[["home_score", "away_score", "total_goals"]].describe().round(2)

    summary = {
        "n_matches": int(len(df)),
        "n_teams": len(set(df["home_team"]) | set(df["away_team"])),
        "n_years": df["year"].nunique(),
        "n_stadiums": df["stadium"].nunique(),
        "n_cities": df["city"].nunique(),
        "date_range": (str(df["date"].min().date()), str(df["date"].max().date())),
        "avg_goals_per_match": round(df["total_goals"].mean(), 2),
        "total_goals_scored": int(df["total_goals"].sum()),
        "result_breakdown": df["result"].value_counts().to_dict(),
        "numeric_summary": numeric_summary.to_dict(),
    }
    return summary


def detect_outliers(df, column="total_goals"):
    """
    Identify outliers in numerical columns using the IQR method.

    Parameters
    ----------
    df : pandas.DataFrame
    column : str
        Numeric column to check for outliers.

    Returns
    -------
    pandas.DataFrame
        Subset of rows flagged as outliers for the given column.
    """
    q1 = df[column].quantile(0.25)
    q3 = df[column].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
    return outliers[["date", "home_team", "away_team", column]].reset_index(drop=True)

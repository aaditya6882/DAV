# README

# Week 1 - Nepal Housing Data Audit & Exploration

**Team:** DataTrails Nepal
**Source data:** `2020-4-27.csv` , scraped Nepali real-estate listings (2,211 rows × 18 columns)

## What This Is

A data-quality audit and exploratory analysis of a real, messy real-estate dataset, built to answer one question for a hypothetical real-estate analytics startup: *"Can this dataset actually be trusted?"* before reporting any housing-price insights from it.

The full pipeline : load, missing-data check, duplicate check, area-unit standardization, price outlier removal, core statistics, and two visualizations is implemented in `notebook.ipynb` and is reproducible end to end.

## Pipeline Summary (verified from executed notebook output)

| Step | Result |
| --- | --- |
| Raw rows / columns | 2,211 / 18 |
| Duplicate titles found | 709 (32%) |
| Raw price range | NPR 15 → NPR 216,000,002,700,000 (corrupted) |
| Unparseable area values | 141 (6.4%) |
| Rows after cleaning | 1,868 (84.5% of original) |
| Cleaned mean price | NPR 13,978,632 |
| Cleaned median price | NPR 6,000,000 |
| Top city by listings | Kathmandu (1,280) |

Full methodology, every cleaning decision, and known limitations are documented in `data_audit_report.md` and `DOCUMENTATION.md`.

## Contents

| File | Description |
| --- | --- |
| `notebook.ipynb` | Full cleaning + analysis pipeline, executed and documented — the single source of truth for all numbers in this folder |
| `DOCUMENTATION.md` | Section-by-section technical documentation of the notebook code: what each cell does, why, and its limitations |
| `data_audit_report.md` | Data quality audit: missing data, issues found, cleaning methodology, trustworthiness verdict |
| `findings.md` | Stakeholder-facing summary of headline numbers and key insight |
| `Worksheet1_Submission.md` | Full Week 1 course worksheet (Parts A–E), ready to submit |
| `visualizations1.png` | Price distribution histogram + listings-by-city bar chart |
| `visualizations2.png` | Price vs. land area scatter plot |
| `cleaned_housing_data.csv` | Cleaned dataset (1,868 rows) used for all analysis and charts, including derived `Area_Aana` and `PricePerAana` columns |

## How to Reproduce

1. Place `2020-4-27.csv` in the same directory as `notebook.ipynb`.
2. Run all cells top to bottom.
3. `visualizations1.png`, `visualizations2.png`, and `cleaned_housing_data.csv` will be (re)generated in the same directory.

## Key Caveat

All numbers in this folder reflect a single combined cleaning filter (price outlier bounds + area sanity range applied together), which removes 343 rows (15.5%) total - including the 141 rows where the area string didn't match any recognized unit format. See `data_audit_report.md` Section 4 for the full breakdown of what that filter removes and why.
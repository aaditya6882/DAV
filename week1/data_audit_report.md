# data_audit_report

# Data Audit Report — Nepal Housing Listings

**Team:** DataTrails Nepal
**Source file:** `2020-4-27.csv`**Dataset:** Scraped Nepali real-estate listings, 2,211 rows × 18 columns
**Audit question:** *"Can this dataset actually be trusted?"*

> All figures below are taken directly from the executed `notebook.ipynb` output, not estimated separately — verified by re-running the pipeline end to end.
> 

---

## 1. Dataset Overview

| Metric | Value |
| --- | --- |
| Total rows | 2,211 |
| Total columns | 18 |
| Columns | Title, Address, City, Price, Bedroom, Bathroom, Floors, Parking, Face, Year, Views, Area, Road, Road Width, Road Type, Build Area, Posted, Amenities |
| Likely source | Web-scraped property listing portal (inferred from "Posted X hours/days ago" field and snapshot-style filename) |

---

## 2. Missing Data Check

| Column | Missing Count | % Missing | Severity |
| --- | --- | --- | --- |
| Year (B.S.) | 1,629 | 73.7% | Critical |
| Floors | 1,172 | 53.0% | Critical |
| Road Type | 785 | 35.5% | High |
| Area (unparseable string) | 141 | 6.4% | Moderate |

**Handling decision:** Year and Floors are missing for the majority of listings — too high a proportion to impute responsibly. Imputing a median/mode value across >50% of a column would fabricate data rather than estimate it, and would silently distort any analysis relying on those fields. These columns are flagged as "Unknown" and excluded from calculations rather than filled in. The 141 unparseable Area values (6.4% of rows — strings that don't match any recognized Aana/Ropani/Sq. Feet/Dhur pattern, including the 4 Bigha-denominated listings) are excluded only from area-dependent calculations, not from the rest of the analysis.

---

## 3. Data Quality Issues

| # | Issue | Example / Evidence | Impact |
| --- | --- | --- | --- |
| 1 | **Inconsistent area units** | `Area` column mixes 5 unit systems: Aana, Sq. Feet, Ropani, Dhur, Bigha | Any price-per-area comparison is meaningless until all units are converted to one standard; 141 rows (6.4%) don't parse into any recognized unit at all |
| 2 | **Corrupted/unrealistic price values** | Minimum price = NPR 15; maximum price = NPR 216,000,002,700,000 (~216 trillion) | A single corrupted value inflates the raw mean to ~NPR 406 billion (raw `Price.describe()` mean = 4.064×10¹¹) — entirely unusable without outlier treatment |
| 3 | **Duplicate listings** | 709 duplicate `Title` values out of 2,211 rows (32%); 0 exact full-row duplicates | Indicates re-posted ads rather than copy-paste errors; inflates apparent city-level supply by roughly a third if uncorrected |
| 4 | **Inconsistent Aana sub-format** | Same unit written as `"0-2-2-2 Aana"` (dash, 4-part), `"0.3.0.0 Aana"` (period, 4-part), and `"3-4 Aana"` (single value) | Naive numeric parsing without handling the traditional Aana–Paisa–Daam–Anna subdivision system produces wrong area values, and inconsistent formats are part of why 141 rows fail to parse cleanly |
| 5 | **Placeholder missing values disguised as data** | `"N/A Aana"`, `"N/A Sq. Feet"` strings found throughout `Build Area` | Not caught by a default `.isna()` check — requires explicit string-pattern handling to avoid being miscounted as valid data |
| 6 | **Coarse geographic granularity** | `City` field only (e.g. "Kathmandu") — no municipality/ward-level field | Hides significant within-city price variation; risks oversimplified location-based conclusions |
| 7 | **Single-day snapshot** | Filename `2020-4-27.csv`; no date/time column beyond relative "Posted X ago" | No trend or time-series analysis is valid from this file alone |

---

## 4. Cleaning Methodology

**Step 1 — Area standardization.** All `Area` values converted to a single Aana-equivalent unit:

- Sq. Feet → ÷ 342.25
- Ropani → × 16 (first segment of multi-part strings only)
- Dhur → × 0.339 (approximate, Terai-region unit)
- Aana (4-part subdivision) → `aana + paisa/4 + daam/16 + anna/64`
- Bigha and any other unrecognized string → returns `NaN`, excluded from area-based steps

**Step 2 — Price outlier treatment.** Standard IQR rule: values above `Q3 + 1.5×IQR` removed, plus an explicit floor of NPR 10,000 to catch corrupted near-zero entries the IQR rule alone would miss.

**Step 3 — Area sanity filter.** Listings with `Area_Aana <= 0` or `Area_Aana >= 200` excluded — this removes both the unparseable (`NaN`) rows from Step 1 and a small number of extreme land-area values (likely commercial/institutional plots).

**Step 4 — Missingness handling.** Floors, Year, and Road Type left unimputed and explicitly flagged as "Unknown" rather than filled with guessed values.

**Result (verified from executed notebook output):**

|  | Value |
| --- | --- |
| Rows before cleaning | 2,211 |
| Rows after cleaning | 1,868 |
| Rows removed | 343 (15.5%) |

Note: the area sanity filter (Step 3) is the larger driver of rows removed here, since it also absorbs the 141 unparseable area values from Step 1 in addition to true price outliers — this single combined filter is why "rows removed" is higher than price-outlier removal alone would suggest.

---

## 5. Core Statistics (Cleaned Data, n = 1,868)

| Metric | Value |
| --- | --- |
| Mean price | NPR 13,978,632 |
| Median price | NPR 6,000,000 |
| Mean ÷ Median ratio | ~2.33× — confirms strong right-skew |

**Top 5 cities by listing count:**

| City | Listings | Median Price (NPR) |
| --- | --- | --- |
| Kathmandu | 1,280 | 9,500,000 |
| Lalitpur | 399 | 4,000,000 |
| Bhaktapur | 76 | 1,800,000 |
| Pokhara | 26 | 7,550,000 |
| Chitwan | 14 | 5,000,000 |

**Reflection — what might be misleading:** "Average price" alone overstates what a typical buyer pays — the mean is more than double the median because of high-end listings. Pokhara's relatively high median price (NPR 7.55M) despite a small listing count (26) is also worth flagging — small samples are more sensitive to a handful of expensive properties and shouldn't be treated with the same confidence as Kathmandu's much larger sample.

---

## 6. Trustworthiness Verdict

**Can this dataset be trusted as-is? No.** In its raw form it would produce a materially wrong headline statistic (a ~NPR 406 billion "average house price") and overstated city-level listing counts. **Can it be trusted after the cleaning steps above? Conditionally yes** — for distribution-level questions (typical price range, relative city ranking, price-vs-area relationship) the cleaned data (n=1,868, 84.5% of the original) supports defensible conclusions. It should **not** be trusted for: precise per-unit-area pricing (area-parsing approximations introduce noise, and 6.4% of rows couldn't be parsed at all), trend/time analysis (single-day snapshot), fine-grained location analysis (City field too coarse), or small-sample city comparisons (e.g. Pokhara/Chitwan, with 26 and 14 listings respectively).

---

## 7. Recommendations Before Production Use

1. Automate the area-unit parser and add unit tests for each of the 5 observed unit formats, plus the 3 Aana sub-formats — specifically investigate why 141 rows (6.4%) fail to parse, since that's a higher rate than initially expected and may indicate an additional unlogged format variant.
2. Replace title-only duplicate detection with a Title + Address composite key for more conservative deduplication.
3. Add automated price sanity bounds (floor/ceiling) at ingestion time, before any row reaches a dashboard.
4. Parse `Address` into a finer-grained location field (ward/neighborhood) rather than relying on the coarse `City` column.
5. Collect repeated daily/weekly snapshots if trend analysis is ever required — this file alone cannot support it.
6. Report city-level statistics with their sample size alongside the price, so small-sample cities (Pokhara, Chitwan) aren't read with the same confidence as Kathmandu/Lalitpur.
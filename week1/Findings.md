# Findings

# Findings : Nepal Housing Price Exploration

**Source:** `2020-4-27.csv`, cleaned via `notebook.ipynb` (n = 1,868 listings, 84.5% of the original 2,211)

## Headline Numbers

- **Median price:** NPR 6,000,000
- **Mean price:** NPR 13,978,632 (mean is ~2.3× the median, confirming strong right-skew - most listings are far below the average)
- **Top 5 cities by listing count:** Kathmandu (1,280), Lalitpur (399), Bhaktapur (76), Pokhara (26), Chitwan (14)
- **Median price by city:** Kathmandu NPR 9.5M | Pokhara NPR 7.55M | Chitwan NPR 5.0M | Lalitpur NPR 4.0M | Bhaktapur NPR 1.8M

## Key Insight

Land area is a weak predictor of price in this market - price is driven far more by city/location than by plot size, based on the price-vs-area scatter plot (`visualizations2.png`). Listings cluster heavily at small-to-moderate land areas across the full price range, with no clear upward trend as area increases.

## A Second Observation Worth Flagging

Pokhara shows the second-highest median price (NPR 7.55M) despite having only 26 listings — far fewer than Kathmandu (1,280) or Lalitpur (399). With such a small sample, this figure is sensitive to just a handful of expensive properties and should not be read with the same confidence as the Kathmandu/Lalitpur numbers, which rest on much larger samples.

## Caveats for Stakeholders

- **City is a coarse label, not a true municipality/ward** — within-city variation (e.g., specific neighborhoods) is hidden.
- **Listing counts are inflated by duplicates.** 709 of 2,211 raw rows (32%) share a duplicate title, indicating re-posted ads; true unique-property counts are lower than raw counts suggest.
- **6.4% of listings (141 rows) had an area value that couldn't be parsed** into any recognized unit and were excluded from area-based analysis — this is a meaningfully large gap that should be investigated further before trusting per-area pricing.
- **Small-sample cities** (Pokhara: 26, Chitwan: 14) should be treated with lower confidence than Kathmandu/Lalitpur.
- **This is a single-day snapshot** (2020-04-27), not a time series — no trend or seasonal claims can be made from this file alone.
# Dataset_Creation

# Dataset Creation Process: 2022 FIFA World Cup Matches

## Overview

This document explains the methodology used to compile the `matches.csv` dataset, which records all 64 matches of the 2022 FIFA World Cup. The dataset was created through a combination of **manual data entry in Microsoft Excel**, **self-written records from memory/notes**, and **web scraping/research from multiple public sources**, followed by cleaning and standardization before final export to CSV.

## Step-by-Step Process

### 1. Planning the Data Structure

Before collecting any data, the schema was planned out first to ensure consistency:

- Decided on the 10 columns needed: `year`, `date`, `stage`, `stadium`, `city`, `home_team`, `away_team`, `home_score`, `away_score`, `result`
- Determined the correct format for each field (e.g., dates as `MM/DD/YYYY`, scores as integers, team names in full form rather than abbreviations)
- Set up an empty Excel workbook (`.xlsx`) with these column headers in row 1, frozen for easy scrolling

### 2. Initial Manual Entry (Self-Written)

A portion of the matches — particularly the ones that were well remembered or already noted down (e.g., group stage openers, the Final, Semi-finals) — were typed directly into Excel from memory and personal notes:

- Match dates, stadiums, and scorelines were entered by hand for matches that were closely followed during the tournament
- This gave a base set of rows to work from and helped establish the formatting conventions before more data was added

### 3. Data Collection via Web Research / Scraping

For the remaining matches, information was gathered by researching multiple public sources online:

- Official FIFA match archives and results pages
- Sports news sites and football statistics websites for verification of scores and stages
- Wikipedia's 2022 FIFA World Cup match summary pages, used to cross-check dates, venues, and stage names
- Where possible, tabular data was copy-pasted from these sources into a scratch sheet, then reformatted to match the target schema

**Note:** "Scraping" here mainly refers to manually copying structured tables from public results pages rather than automated scripts — the small size of the dataset (64 rows) made manual collection practical.

### 4. Consolidation in Excel

All partially collected data (self-written + researched) was brought together into a single Excel sheet:

- Rows were merged into one master sheet, sorted chronologically by `date`
- Used Excel formulas (`=IF`, `=TEXT`, conditional formatting) to spot inconsistent date formats or blank cells
- Applied Excel's **Data Validation** feature to restrict `stage` entries to the six valid categories (Group, Round of 16, Quarter-final, Semi-final, Third Place Play-off, Final), preventing typos like "Groupstage" vs "Group"

### 5. Cross-Verification

Each row was checked against at least one additional independent source to catch errors:

- Verified team names matched official FIFA naming (e.g., "South Korea" vs "Korea Republic" — standardized to the more common form)
- Verified stadium names and their associated host cities were correctly paired (since several stadiums share host cities like Doha)
- Cross-checked scorelines, especially for matches decided by penalty shootouts, to confirm the `result` field reflected the actual match winner r(not just the 90-minute score)

### 6. Cleaning and Standardization

Once all 64 rows were present, a cleaning pass was done directly in Excel:

- Removed extra whitespace and inconsistent capitalization using `TRIM()` and `PROPER()` functions
- Standardized the `date` column format across all rows
- Ensured `home_score` and `away_score` were stored as whole numbers, not text
- Checked for and removed any duplicate rows (e.g., accidentally double-entered matches)
- Confirmed there were exactly 64 rows, matching the known total number of matches in the tournament (48 group + 8 Round of 16 + 4 Quarter-finals + 2 Semi-finals + 1 Third Place Play-off + 1 Final)

### 7. Export to CSV

After the sheet was fully cleaned and verified:

- Used Excel's **Save As → CSV (Comma delimited)** option to export the final sheet
- Re-opened the exported CSV in a text editor to confirm formatting held up correctly (no broken commas within fields, consistent line endings)
- Renamed the final file to `matches.csv`

### 8. Final Quality Check

A last pass was done to make sure the dataset was analysis-ready:

- Confirmed there were no missing/null values in any column
- Spot-checked a random sample of rows against source data one more time
- Confirmed column headers exactly matched the intended schema (lowercase, underscore-separated)

## Tools Used

| Tool | Purpose |
| --- | --- |
| Microsoft Excel | Primary tool for manual entry, consolidation, cleaning, and CSV export |
| Web browser research | Gathering match results from official and public sports sources |
| Excel Data Validation | Enforcing consistent categorical values (e.g., `stage`) |
| Text editor | Verifying final CSV formatting before use |

## Limitations of This Process

- Manual entry and copy-pasting introduces some risk of human error, mitigated by the cross-verification step but not fully eliminated
- Because the dataset was compiled manually rather than through an automated pipeline, it isn't easily reproducible or updatable — any future World Cup would require repeating the process from scratch
- The `result` field simplifies penalty-shootout outcomes into a single winner, which loses some detail (e.g., exact shootout score) that a more detailed dataset might retain
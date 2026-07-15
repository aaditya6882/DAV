# Mini Sports Analytics Web App

Herald College Kathmandu · Centre for AI and Emerging Technologies · 2026

A Flask-based data analytics system demonstrating the full workflow:
**Data → Cleaning → Analysis → Visualization → Web Dashboard**

Built following the layered architecture from the course instruction set:
Flask Routes (presentation) → Service Layer (EDA / Statistics / Visualization)
→ Data Layer (Loader + Preprocessing) → Configuration Layer.

## Dataset

`data/raw/matches.csv` contains 64 matches from the 2022 FIFA World Cup,
including every stage through the final. Its required columns are `year`,
`date`, `stage`, `stadium`, `city`, `home_team`, `away_team`, `home_score`,
and `away_score`. The CSV may also contain `result`; the application
recalculates outcomes from the two score columns to keep analysis consistent.

## Setup

### 1. Create the environment

**Conda (recommended)**
```bash
conda env create -f environment.yml
conda activate sports-analytics
```

**pip**
```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

> Use ONLY one of the two — do not mix Conda and pip installs.

### 2. Run the app

**Mac/Linux**
```bash
export FLASK_APP=app:create_app
flask run
```

**Windows (PowerShell)**
```powershell
$env:FLASK_APP="app:create_app"
flask run
```

### 3. Open it

http://127.0.0.1:5000

### Run with Docker

Build and start the dashboard with Docker Compose:

```bash
docker compose up --build
```

Then open http://127.0.0.1:5000. Stop it with `Ctrl+C`; use
`docker compose down` to remove the container. Alternatively, run
`docker build -t world-cup-dashboard .` followed by
`docker run --rm -p 5000:5000 world-cup-dashboard`.

## Pages

| Route        | Description                                      |
|--------------|---------------------------------------------------|
| `/`          | Dashboard — overview stats, all charts, top teams |
| `/teams`     | Full team standings table                         |
| `/outliers`  | Statistically unusual (outlier) matches           |

## Running tests

Each module can be tested independently:

```bash
python -m tests.test_loader
python -m tests.test_preprocessing
python -m tests.test_statistics
python -m tests.test_visualizations
```

## Project structure

```
mini-sports-analytics-web-app/
├── app/
│   ├── __init__.py            # Flask application factory
│   ├── routes.py               # Application routes (thin — delegates to services)
│   └── services/
│       ├── data_loader.py      # Load raw data
│       ├── preprocessing.py    # Clean and transform data
│       ├── eda.py              # Exploratory data analysis
│       ├── statistics.py       # Statistical computations
│       └── visualizations/
│           ├── helper.py       # Shared plotting utilities
│           ├── tournament.py   # Match and scoring plots
│           ├── geography.py    # Geographic plots
│           └── generate.py     # Orchestrates all plot generation
├── data/
│   ├── raw/                    # Original dataset (do not modify)
│   └── processed/              # Cleaned dataset (generated at runtime)
├── static/images/plots/        # Generated visualizations (generated at runtime)
├── templates/                  # Jinja2 HTML templates
├── tests/                      # Unit tests per module
├── config.py                   # Paths & settings
├── environment.yml
├── requirements.txt
└── README.md
```

## Design notes (by role)

- **Data Engineer** — `data_loader.py` and `preprocessing.py` handle all file
  I/O, type coercion, missing-value handling, and derived columns
  (`total_goals`, `goal_difference`, `result`), so nothing downstream ever
  touches a raw file path.
- **Data Analyst** — `eda.py` and `statistics.py` compute dataset overviews,
  IQR-based outlier detection, per-team win/draw/loss/points tables, and
  per-tournament summaries.
- **Software Developer** — `app/routes.py` stays intentionally thin (per the
  instruction set's warning against heavy computation in routes); the
  Application Factory pattern in `app/__init__.py` keeps configuration and
  blueprint registration explicit and testable.
- **UI/UX Designer** — `templates/` uses a stadium-scoreboard visual theme
  (deep pitch green, scoreboard amber, mono "ticker" numerals) to make the
  dashboard feel like a sports broadcast graphic rather than a generic admin
  panel, while remaining responsive and keyboard-accessible.

## Troubleshooting

| Issue                        | Solution                                              |
|-------------------------------|--------------------------------------------------------|
| `ModuleNotFoundError`         | Activate your environment: `conda activate sports-analytics` |
| Port 5000 already in use      | `flask run --port=5001`                                |
| Plots not showing              | Check `static/images/plots/` write permissions        |
| Data loading fails            | Verify `data/raw/matches.csv` matches the required schema |

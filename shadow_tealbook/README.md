# Shadow Tealbook A — Purdue University

Replication of the Federal Reserve's Tealbook A structure using publicly available data.

## Project Structure

```
shadow_tealbook/
├── config.py              # Series definitions, API keys, settings
├── notebook.ipynb         # Master Jupyter notebook
├── data/
│   └── fred_pulls.py      # FRED API data pipeline
├── cache/                 # Auto-generated parquet cache (gitignore this)
└── quarto/
    ├── _quarto.yml        # Website config
    └── index.qmd          # Homepage
```

## Setup (first time)

### 1. Install dependencies
```bash
pip install fredapi pandas numpy matplotlib pyarrow fastparquet jupyter quarto
```

### 2. Get a FRED API key
- Go to https://fred.stlouisfed.org/docs/api/api_key.html
- Create a free account and request a key (instant)

### 3. Set your API key
**Option A — Environment variable (recommended):**
```bash
export FRED_API_KEY="your_key_here"   # Mac/Linux
set FRED_API_KEY=your_key_here        # Windows
```

**Option B — Directly in notebook:**
In `notebook.ipynb`, cell 1, replace:
```python
os.environ['FRED_API_KEY'] = 'YOUR_FRED_KEY_HERE'
```
with your actual key. Do NOT commit this to a public repo.

### 4. Run the notebook
```bash
cd shadow_tealbook
jupyter notebook notebook.ipynb
```
Run all cells. First run will pull from FRED and cache locally.
Subsequent runs use the cache (refreshes after 12 hours).

## Render the Quarto website

### Install Quarto
Download from https://quarto.org/docs/get-started/

### Render locally
```bash
cd quarto
# Set your FRED key in index.qmd first
quarto render
quarto preview   # opens in browser
```

### Publish to GitHub Pages (auto-updating)
1. Push repo to GitHub
2. Add GitHub Action: `.github/workflows/render.yml`
3. Set `FRED_API_KEY` as a GitHub repo secret (Settings > Secrets)
4. Action runs on schedule and on push, re-renders and deploys

## GitHub Actions workflow (auto-update)
Save as `.github/workflows/render.yml`:
```yaml
name: Render Shadow Tealbook

on:
  schedule:
    - cron: '0 14 * * 1-5'   # weekdays at 2pm UTC (after most data releases)
  push:
    branches: [main]

jobs:
  render:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install fredapi pandas numpy matplotlib pyarrow fastparquet
      - uses: quarto-dev/quarto-actions/setup@v2
      - name: Render Quarto site
        env:
          FRED_API_KEY: ${{ secrets.FRED_API_KEY }}
        run: |
          cd quarto
          quarto render
      - uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./quarto/_site
```

## Adding new series
1. Add entry to `FRED_SERIES` dict in `config.py`
2. Add chart/table code in `notebook.ipynb` or relevant `.qmd` page
3. Re-run notebook or re-render Quarto

## Data notes
- **Vintage data**: For validation against released Tealbooks (2013-2019),
  use Philadelphia Fed RTDSM or FRED API `vintage_dates` parameter.
- **COVID exclusion**: Training window set to 2011-2019 in `config.py`.
  2020 data excluded from model training but included in charts.
- **Cache**: Parquet files in `cache/` directory refresh every 12 hours.
  Delete cache files to force immediate refresh.

## Part roadmap
- **Part 1 (this)**: Realized data pipeline — tables and charts ✓
- **Part 2**: Projections — BVAR model, fan charts
- **Part 3**: LLM-generated narrative — RAG pipeline

---
*Purdue University — Shadow FOMC Project*
*Data: Federal Reserve Bank of St. Louis (FRED)*

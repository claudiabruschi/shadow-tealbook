# Shadow Tealbook A — Setup & Deployment

## Local preview

```bash
cd shadow_tealbook/quarto
export FRED_API_KEY="your_fred_key"
export ANTHROPIC_API_KEY="your_anthropic_key"
quarto preview
```

Browser opens at `http://localhost:4848` with live reload.

## GitHub Pages deployment

1. Push the repo to GitHub
2. Go to **Settings → Pages → Source** → set to **GitHub Actions**
3. Go to **Settings → Secrets → Actions** and add:
   - `FRED_API_KEY` — get free at https://fred.stlouisfed.org/docs/api/api_key.html
   - `ANTHROPIC_API_KEY` — get at https://console.anthropic.com
4. Push to `main` — the workflow renders and deploys automatically
5. Site will be live at `https://YOUR_USERNAME.github.io/shadow-tealbook`

## Scheduled updates

The workflow runs every **Monday at 8am ET** automatically.
To trigger a manual render: GitHub → Actions → "Render & Deploy" → "Run workflow".

## Updating forecasts (each FOMC cycle)

In `quarto/index.qmd`, update the four hard-coded SPF/FOMC values in the
`overview-data` chunk:

```python
spf_gdp_next  = 2.1   # SPF median real GDP next 4 quarters
spf_pce_next  = 2.3   # SPF median PCE inflation next year
fomc_lr_gdp   = 1.8   # FOMC longer-run real GDP (SEP)
fomc_lr_unemp = 4.1   # FOMC longer-run unemployment (SEP)
```

Sources:
- SPF: https://www.philadelphiafed.org/surveys-and-data/real-time-data-research/survey-of-professional-forecasters
- FOMC SEP: https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm

## Structure

```
shadow_tealbook/
├── quarto/
│   ├── _quarto.yml       # Site configuration
│   ├── index.qmd         # Main tabset (Overview, GDP, Labor, Inflation,
│   │                     #   Financial, Special Topics)
│   └── about.qmd         # Project description
├── data/
│   └── fred_pulls.py     # FRED data module with local cache
├── notebook.ipynb        # Development notebook (series validation)
└── SERIES_MAP.md         # Verified FRED ticker registry
.github/
└── workflows/
    └── render.yml        # GitHub Actions: render + deploy to Pages
```

## Pending (post-Bullard feedback)

- [ ] International GDP tab (IMF IFS/WEO API)
- [ ] Financial markets equity data (yfinance)
- [ ] Michigan 5-10yr & SPF 10-yr PCE integration (manual CSV load)
- [ ] News API integration for Special Topics
- [ ] Forecast overlay on charts (SPF confidence bands)

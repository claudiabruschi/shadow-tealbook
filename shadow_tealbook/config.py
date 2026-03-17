"""
Shadow Tealbook A — Project Configuration
==========================================
Central config for API keys, FOMC meeting dates, and all series definitions.
Keep this file local and never commit your API key to a public repo.
Add config.py to your .gitignore.
"""

import os
from datetime import date

# ── API KEYS ──────────────────────────────────────────────────────────────────
# IMPORTANT: Regenerate your FRED key at https://fred.stlouisfed.org/docs/api/api_key.html
# Store as environment variable in production: os.environ.get("FRED_API_KEY")
FRED_API_KEY = os.environ.get("FRED_API_KEY", "YOUR_FRED_KEY_HERE")

# BLS public API (no key required for basic access, but registered key gives higher limits)
# Register free at https://data.bls.gov/registrationEngine/
BLS_API_KEY  = os.environ.get("BLS_API_KEY", "")

# ── PROJECT SETTINGS ──────────────────────────────────────────────────────────
PROJECT_NAME    = "Shadow Tealbook A — Purdue University"
CACHE_DIR       = "cache"          # Local parquet cache directory
CACHE_MAX_AGE_H = 12               # Re-pull from API if cache older than N hours

# Training window: 2011-2019 (excludes 2020 COVID, uses post-Tealbook-rename era)
TRAIN_START = "2011-01-01"
TRAIN_END   = "2019-12-31"

# Live window: pull from 2015 for chart history, through today
HISTORY_START = "2015-01-01"

# ── FOMC MEETING DATES (scheduled 2025-2026) ─────────────────────────────────
# Source: https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm
# Format: (meeting_end_date, tealbook_closing_date_approx)
FOMC_MEETINGS_2025 = [
    (date(2025, 1, 29),  date(2025, 1, 17)),
    (date(2025, 3, 19),  date(2025, 3,  7)),
    (date(2025, 5,  7),  date(2025, 4, 25)),
    (date(2025, 6, 18),  date(2025, 6,  6)),
    (date(2025, 7, 30),  date(2025, 7, 18)),
    (date(2025, 9, 17),  date(2025, 9,  5)),
    (date(2025, 10, 29), date(2025, 10, 17)),
    (date(2025, 12, 10), date(2025, 11, 28)),
]

FOMC_MEETINGS_2026 = [
    (date(2026, 1, 28),  date(2026, 1, 16)),
    (date(2026, 3, 18),  date(2026, 3,  6)),
    (date(2026, 4, 29),  date(2026, 4, 17)),
    (date(2026, 6, 17),  date(2026, 6,  5)),
    (date(2026, 7, 29),  date(2026, 7, 17)),
    (date(2026, 9, 16),  date(2026, 9,  4)),
    (date(2026, 10, 28), date(2026, 10, 16)),
    (date(2026, 12,  9), date(2026, 11, 27)),
]

# ── SERIES CATALOGUE ─────────────────────────────────────────────────────────
# Each entry: FRED ticker -> display metadata
# Structure: { "FRED_ID": { "label", "section", "units", "transform", "notes" } }
#
# transform options:
#   "level"   — use as-is
#   "yoy"     — compute year-over-year % change
#   "ch"      — period-over-period change (levels)
#   "pch"     — period-over-period % change

FRED_SERIES = {

    # ── I. SUMMARY / PROJECTION TABLE VARIABLES ──────────────────────────────
    "GDPC1": {
        "label":    "Real GDP",
        "section":  "summary",
        "units":    "Bil. Ch. 2017$, SAAR",
        "transform":"pch_ann",   # annualized quarterly % change
        "freq":     "Q",
        "notes":    "Advance/second/third releases; subject to revision",
    },
    "UNRATE": {
        "label":    "Unemployment Rate",
        "section":  "summary",
        "units":    "Percent, SA",
        "transform":"level",
        "freq":     "M",
        "notes":    "End-of-quarter reading for projection table",
    },
    "PCEPILFE": {
        "label":    "Core PCE Price Index",
        "section":  "summary",
        "units":    "Index 2017=100",
        "transform":"yoy",
        "freq":     "M",
        "notes":    "Fed preferred inflation measure",
    },
    "PCEPI": {
        "label":    "Total PCE Price Index",
        "section":  "summary",
        "units":    "Index 2017=100",
        "transform":"yoy",
        "freq":     "M",
        "notes":    "",
    },
    "FEDFUNDS": {
        "label":    "Federal Funds Rate (effective)",
        "section":  "summary",
        "units":    "Percent",
        "transform":"level",
        "freq":     "M",
        "notes":    "Key conditioning assumption",
    },
    "DFEDTARU": {
        "label":    "Fed Funds Target Rate (upper bound)",
        "section":  "summary",
        "units":    "Percent",
        "transform":"level",
        "freq":     "D",
        "notes":    "",
    },

    # ── II. DOMESTIC REAL ACTIVITY — Output ───────────────────────────────────
    "A191RL1Q225SBEA": {
        "label":    "Real GDP Growth (annualized)",
        "section":  "domestic_output",
        "units":    "Pct, SAAR",
        "transform":"level",
        "freq":     "Q",
        "notes":    "Direct annualized growth rate from BEA",
    },
    "GDPPOT": {
        "label":    "Potential Real GDP (CBO)",
        "section":  "domestic_output",
        "units":    "Bil. Ch. 2012$, SAAR",
        "transform":"level",
        "freq":     "Q",
        "notes":    "CBO estimate; updated ~2x/year",
    },
    "GDPC1": {
        "label":    "Real GDP (level)",
        "section":  "domestic_output",
        "units":    "Bil. Ch. 2017$, SAAR",
        "transform":"level",
        "freq":     "Q",
        "notes":    "",
    },
    "INDPRO": {
        "label":    "Industrial Production Index",
        "section":  "domestic_output",
        "units":    "Index 2017=100",
        "transform":"yoy",
        "freq":     "M",
        "notes":    "",
    },
    "TCU": {
        "label":    "Capacity Utilization (Total Industry)",
        "section":  "domestic_output",
        "units":    "Percent",
        "transform":"level",
        "freq":     "M",
        "notes":    "",
    },

    # ── II. DOMESTIC REAL ACTIVITY — Consumption & Income ────────────────────
    "PCECC96": {
        "label":    "Real Personal Consumption Expenditures",
        "section":  "consumption",
        "units":    "Bil. Ch. 2017$, SAAR",
        "transform":"pch_ann",
        "freq":     "M",
        "notes":    "",
    },
    "DSPIC96": {
        "label":    "Real Disposable Personal Income",
        "section":  "consumption",
        "units":    "Bil. Ch. 2017$, SAAR",
        "transform":"yoy",
        "freq":     "M",
        "notes":    "",
    },
    "PSAVERT": {
        "label":    "Personal Saving Rate",
        "section":  "consumption",
        "units":    "Percent",
        "transform":"level",
        "freq":     "M",
        "notes":    "",
    },
    "UMCSENT": {
        "label":    "U. of Michigan Consumer Sentiment",
        "section":  "consumption",
        "units":    "Index 1966Q1=100",
        "transform":"level",
        "freq":     "M",
        "notes":    "",
    },
    "RSXFSN": {
        "label":    "Retail Sales ex. Autos & Gas (nominal)",
        "section":  "consumption",
        "units":    "Mil. $, NSA",
        "transform":"yoy",
        "freq":     "M",
        "notes":    "Nominal; use as directional indicator",
    },

    # ── II. DOMESTIC REAL ACTIVITY — Business Investment ─────────────────────
    "PNFIC1": {
        "label":    "Real Nonres. Fixed Investment",
        "section":  "investment",
        "units":    "Bil. Ch. 2017$, SAAR",
        "transform":"pch_ann",
        "freq":     "Q",
        "notes":    "",
    },
    "NEWORDER": {
        "label":    "Manufacturers New Orders: Durable Goods",
        "section":  "investment",
        "units":    "Mil. $, SA",
        "transform":"yoy",
        "freq":     "M",
        "notes":    "Broad durable goods orders; leading capex indicator",
    },
    "ODCPDP1M175NNBR": {
        "label":    "Core Capital Goods Orders (nondefense ex-aircraft, nominal)",
        "section":  "investment",
        "units":    "Mil. $, SA",
        "transform":"yoy",
        "freq":     "M",
        "notes":    "Use CMRMTSPL as alternative if unavailable",
    },
    "IPBUSEQ": {
        "label":    "IP: Business Equipment",
        "section":  "investment",
        "units":    "Index 2017=100",
        "transform":"yoy",
        "freq":     "M",
        "notes":    "",
    },

    # ── II. DOMESTIC REAL ACTIVITY — Housing ─────────────────────────────────
    "HOUST": {
        "label":    "Housing Starts (Total)",
        "section":  "housing",
        "units":    "Thous. units, SAAR",
        "transform":"level",
        "freq":     "M",
        "notes":    "",
    },
    "PERMIT": {
        "label":    "Building Permits",
        "section":  "housing",
        "units":    "Thous. units, SAAR",
        "transform":"level",
        "freq":     "M",
        "notes":    "Leading indicator for starts",
    },
    "HSN1F": {
        "label":    "New Home Sales",
        "section":  "housing",
        "units":    "Thous. units, SAAR",
        "transform":"level",
        "freq":     "M",
        "notes":    "High standard error; treat with caution",
    },
    "SPCS20RSA": {
        "label":    "Case-Shiller HPI (20-city)",
        "section":  "housing",
        "units":    "Index Jan 2000=100",
        "transform":"yoy",
        "freq":     "M",
        "notes":    "2-month publication lag",
    },
    "MORTGAGE30US": {
        "label":    "30-yr Fixed Mortgage Rate",
        "section":  "housing",
        "units":    "Percent",
        "transform":"level",
        "freq":     "W",
        "notes":    "",
    },

    # ── III. LABOR MARKET ─────────────────────────────────────────────────────
    "PAYEMS": {
        "label":    "Nonfarm Payroll Employment",
        "section":  "labor",
        "units":    "Thous., SA",
        "transform":"ch",        # monthly change
        "freq":     "M",
        "notes":    "Compute monthly change from level",
    },
    "USPRIV": {
        "label":    "Private Payrolls",
        "section":  "labor",
        "units":    "Thous., SA",
        "transform":"ch",
        "freq":     "M",
        "notes":    "",
    },
    "U6RATE": {
        "label":    "U-6 Unemployment Rate (broad)",
        "section":  "labor",
        "units":    "Percent, SA",
        "transform":"level",
        "freq":     "M",
        "notes":    "Broader slack measure",
    },
    "CIVPART": {
        "label":    "Labor Force Participation Rate",
        "section":  "labor",
        "units":    "Percent, SA",
        "transform":"level",
        "freq":     "M",
        "notes":    "",
    },
    "EMRATIO": {
        "label":    "Employment-Population Ratio",
        "section":  "labor",
        "units":    "Percent, SA",
        "transform":"level",
        "freq":     "M",
        "notes":    "",
    },
    "JTSJOR": {
        "label":    "JOLTS: Job Openings Rate",
        "section":  "labor",
        "units":    "Percent",
        "transform":"level",
        "freq":     "M",
        "notes":    "~2-month publication lag",
    },
    "JTSQUR": {
        "label":    "JOLTS: Quits Rate",
        "section":  "labor",
        "units":    "Percent",
        "transform":"level",
        "freq":     "M",
        "notes":    "Indicator of worker confidence",
    },
    "IC4WSA": {
        "label":    "Initial Claims (4-week avg)",
        "section":  "labor",
        "units":    "Thous., SA",
        "transform":"level",
        "freq":     "W",
        "notes":    "High-frequency tracker",
    },
    "CES0500000003": {
        "label":    "Avg Hourly Earnings (Private)",
        "section":  "labor",
        "units":    "$",
        "transform":"yoy",
        "freq":     "M",
        "notes":    "Compositional bias; supplement with ECI",
    },
    "OPHNFB": {
        "label":    "Nonfarm Business Productivity",
        "section":  "labor",
        "units":    "Index 2017=100",
        "transform":"yoy",
        "freq":     "Q",
        "notes":    "Subject to significant revision",
    },
    "ULCNFB": {
        "label":    "Unit Labor Costs (Nonfarm Business)",
        "section":  "labor",
        "units":    "Index 2017=100",
        "transform":"yoy",
        "freq":     "Q",
        "notes":    "",
    },
    "NROU": {
        "label":    "Natural Rate of Unemployment (CBO)",
        "section":  "labor",
        "units":    "Percent",
        "transform":"level",
        "freq":     "Q",
        "notes":    "Best public proxy for Fed NAIRU",
    },

    # ── IV. PRICES & INFLATION ────────────────────────────────────────────────
    "CPILFESL": {
        "label":    "Core CPI",
        "section":  "inflation",
        "units":    "Index 1982-84=100",
        "transform":"yoy",
        "freq":     "M",
        "notes":    "Released ~2 wks before PCE; leading signal",
    },
    "CPIAUCSL": {
        "label":    "Total CPI",
        "section":  "inflation",
        "units":    "Index 1982-84=100",
        "transform":"yoy",
        "freq":     "M",
        "notes":    "",
    },
    "WPSFD4": {
        "label":    "PPI: Final Demand",
        "section":  "inflation",
        "units":    "Index 2009=100",
        "transform":"yoy",
        "freq":     "M",
        "notes":    "Leading signal for PCE services inflation",
    },
    "DCOILWTICO": {
        "label":    "WTI Crude Oil Price",
        "section":  "inflation",
        "units":    "$/barrel",
        "transform":"level",
        "freq":     "D",
        "notes":    "Key Tealbook conditioning assumption",
    },
    "GASREGCOVW": {
        "label":    "Gasoline Price (regular, national avg)",
        "section":  "inflation",
        "units":    "$/gallon",
        "transform":"level",
        "freq":     "W",
        "notes":    "",
    },
    "MICH": {
        "label":    "Michigan 1-yr Inflation Expectations",
        "section":  "inflation",
        "units":    "Percent",
        "transform":"level",
        "freq":     "M",
        "notes":    "",
    },
    "T5YIE": {
        "label":    "5-yr TIPS Breakeven Inflation",
        "section":  "inflation",
        "units":    "Percent",
        "transform":"level",
        "freq":     "D",
        "notes":    "",
    },
    "T10YIE": {
        "label":    "10-yr TIPS Breakeven Inflation",
        "section":  "inflation",
        "units":    "Percent",
        "transform":"level",
        "freq":     "D",
        "notes":    "Key long-run anchor signal",
    },
    "T5YIFR": {
        "label":    "5yr5yr Forward Breakeven",
        "section":  "inflation",
        "units":    "Percent",
        "transform":"level",
        "freq":     "D",
        "notes":    "Strips near-term energy volatility",
    },

    # ── V. FINANCIAL CONDITIONS ───────────────────────────────────────────────
    "DGS2": {
        "label":    "2-Year Treasury Yield",
        "section":  "financial",
        "units":    "Percent",
        "transform":"level",
        "freq":     "D",
        "notes":    "",
    },
    "DGS5": {
        "label":    "5-Year Treasury Yield",
        "section":  "financial",
        "units":    "Percent",
        "transform":"level",
        "freq":     "D",
        "notes":    "",
    },
    "DGS10": {
        "label":    "10-Year Treasury Yield",
        "section":  "financial",
        "units":    "Percent",
        "transform":"level",
        "freq":     "D",
        "notes":    "Key long-run benchmark",
    },
    "DGS30": {
        "label":    "30-Year Treasury Yield",
        "section":  "financial",
        "units":    "Percent",
        "transform":"level",
        "freq":     "D",
        "notes":    "",
    },
    "T10Y2Y": {
        "label":    "10yr - 2yr Spread (Term Spread)",
        "section":  "financial",
        "units":    "Percentage points",
        "transform":"level",
        "freq":     "D",
        "notes":    "Recession signal; heavily watched",
    },
    "T10Y3M": {
        "label":    "10yr - 3m Spread",
        "section":  "financial",
        "units":    "Percentage points",
        "transform":"level",
        "freq":     "D",
        "notes":    "Engstrom-Sharpe preferred recession measure",
    },
    "BAMLC0A0CM": {
        "label":    "IG Corporate Spread (OAS)",
        "section":  "financial",
        "units":    "Basis points",
        "transform":"level",
        "freq":     "D",
        "notes":    "",
    },
    "BAMLH0A0HYM2": {
        "label":    "HY Corporate Spread (OAS)",
        "section":  "financial",
        "units":    "Basis points",
        "transform":"level",
        "freq":     "D",
        "notes":    "",
    },
    "NFCI": {
        "label":    "Chicago Fed National Financial Conditions Index",
        "section":  "financial",
        "units":    "Index (z-score)",
        "transform":"level",
        "freq":     "W",
        "notes":    "Positive = tighter conditions",
    },
    "SP500": {
        "label":    "S&P 500 Index",
        "section":  "financial",
        "units":    "Index",
        "transform":"level",
        "freq":     "D",
        "notes":    "",
    },
    "VIXCLS": {
        "label":    "VIX (CBOE Volatility Index)",
        "section":  "financial",
        "units":    "Index",
        "transform":"level",
        "freq":     "D",
        "notes":    "",
    },
    "SOFR": {
        "label":    "SOFR",
        "section":  "financial",
        "units":    "Percent",
        "transform":"level",
        "freq":     "D",
        "notes":    "Replaced LIBOR as key short rate",
    },

    # ── VI. MONEY & BANKING ───────────────────────────────────────────────────
    "M2SL": {
        "label":    "M2 Money Supply",
        "section":  "money",
        "units":    "Bil. $, SA",
        "transform":"yoy",
        "freq":     "M",
        "notes":    "",
    },
    "TOTBKCR": {
        "label":    "Total Bank Credit",
        "section":  "money",
        "units":    "Bil. $, SA",
        "transform":"yoy",
        "freq":     "W",
        "notes":    "",
    },
    "BUSLOANS": {
        "label":    "C&I Loans",
        "section":  "money",
        "units":    "Bil. $, SA",
        "transform":"yoy",
        "freq":     "W",
        "notes":    "",
    },
    "WALCL": {
        "label":    "Fed Balance Sheet (Total Assets)",
        "section":  "money",
        "units":    "Mil. $",
        "transform":"level",
        "freq":     "W",
        "notes":    "QT/QE tracker",
    },
    "DRTSCILM": {
        "label":    "SLOOS: Tightening C&I Standards (net %)",
        "section":  "money",
        "units":    "Net percent",
        "transform":"level",
        "freq":     "Q",
        "notes":    "Senior Loan Officer Survey; key credit signal",
    },

    # ── VII. INTERNATIONAL ────────────────────────────────────────────────────
    "BOPGSTB": {
        "label":    "U.S. Trade Balance (goods & services)",
        "section":  "international",
        "units":    "Mil. $, SA",
        "transform":"level",
        "freq":     "M",
        "notes":    "",
    },
    "RTWEXBGS": {
        "label":    "Real Broad Dollar Index (Fed)",
        "section":  "international",
        "units":    "Index Jan 2006=100",
        "transform":"level",
        "freq":     "M",
        "notes":    "Tealbook preferred dollar measure",
    },
    "DTWEXBGS": {
        "label":    "Nominal Broad Dollar Index",
        "section":  "international",
        "units":    "Index Jan 2006=100",
        "transform":"level",
        "freq":     "D",
        "notes":    "",
    },
    "DEXUSEU": {
        "label":    "EUR/USD Exchange Rate",
        "section":  "international",
        "units":    "USD per EUR",
        "transform":"level",
        "freq":     "D",
        "notes":    "",
    },
    "DEXCHUS": {
        "label":    "CNY/USD Exchange Rate",
        "section":  "international",
        "units":    "CNY per USD",
        "transform":"level",
        "freq":     "D",
        "notes":    "",
    },
    "CLVMNACSCAB1GQEA19": {
        "label":    "Eurozone Real GDP",
        "section":  "international",
        "units":    "Index 2015=100, SA",
        "transform":"pch_ann",
        "freq":     "Q",
        "notes":    "",
    },
    "DCOILWTICO": {
        "label":    "WTI Oil Price",
        "section":  "international",
        "units":    "$/barrel",
        "transform":"level",
        "freq":     "D",
        "notes":    "Also used in inflation section",
    },
    "BAMLEMCBPIOAS": {
        "label":    "EM Corporate Bond Spread",
        "section":  "international",
        "units":    "Basis points",
        "transform":"level",
        "freq":     "D",
        "notes":    "Proxy for EM financial stress",
    },
}

# ── SECTION GROUPINGS (for display order in notebook/website) ─────────────────
SECTION_ORDER = [
    ("summary",          "I. Summary & Outlook"),
    ("domestic_output",  "II-A. Output & Growth"),
    ("consumption",      "II-B. Consumption & Income"),
    ("investment",       "II-C. Business Investment"),
    ("housing",          "II-D. Housing"),
    ("labor",            "III. Labor Market"),
    ("inflation",        "IV. Prices & Inflation"),
    ("financial",        "V. Financial Conditions"),
    ("money",            "VI. Money & Banking"),
    ("international",    "VII. International"),
]

# ── TEALBOOK VISUAL STYLE ─────────────────────────────────────────────────────
# Approximate color palette from actual Tealbook charts
CHART_STYLE = {
    "primary_blue":   "#003087",   # Federal Reserve navy
    "secondary_red":  "#C41E3A",
    "light_gray":     "#D3D3D3",
    "mid_gray":       "#808080",
    "background":     "#FFFFFF",
    "grid_color":     "#E5E5E5",
    "font_family":    "Arial",
    "fig_width":      8.5,
    "fig_height":     4.0,
    "dpi":            150,
}

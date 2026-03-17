"""
Shadow Tealbook A — FRED Data Pull Module
==========================================
Pulls, caches, and transforms all FRED series defined in config.py.
Uses local parquet cache to avoid redundant API calls.
"""

import os
import time
import warnings
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
from fredapi import Fred

warnings.filterwarnings("ignore")

# ── Import config ─────────────────────────────────────────────────────────────
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import FRED_API_KEY, FRED_SERIES, HISTORY_START, CACHE_DIR, CACHE_MAX_AGE_H

# ── Setup ─────────────────────────────────────────────────────────────────────
CACHE_PATH = Path(__file__).parent.parent / CACHE_DIR
CACHE_PATH.mkdir(exist_ok=True)

fred = Fred(api_key=FRED_API_KEY)


# ── Cache helpers ─────────────────────────────────────────────────────────────

def _cache_file(series_id: str) -> Path:
    return CACHE_PATH / f"{series_id}.parquet"


def _cache_valid(series_id: str) -> bool:
    f = _cache_file(series_id)
    if not f.exists():
        return False
    age_h = (time.time() - f.stat().st_mtime) / 3600
    return age_h < CACHE_MAX_AGE_H


def _load_cache(series_id: str) -> pd.Series:
    return pd.read_parquet(_cache_file(series_id)).squeeze()


def _save_cache(series_id: str, s: pd.Series):
    s.to_frame(name="value").to_parquet(_cache_file(series_id))


# ── Core pull ─────────────────────────────────────────────────────────────────

def pull_series(series_id: str, start: str = HISTORY_START,
                force_refresh: bool = False) -> pd.Series:
    """
    Pull a single FRED series. Returns a pd.Series with DatetimeIndex.
    Uses local parquet cache unless force_refresh=True or cache is stale.
    """
    if not force_refresh and _cache_valid(series_id):
        return _load_cache(series_id)
    try:
        s = fred.get_series(series_id, observation_start=start)
        s.index = pd.to_datetime(s.index)
        s.name = series_id
        _save_cache(series_id, s)
        return s
    except Exception as e:
        print(f"  [WARNING] Could not pull {series_id}: {e}")
        # Return cached version if available even if stale
        if _cache_file(series_id).exists():
            print(f"  [INFO] Using stale cache for {series_id}")
            return _load_cache(series_id)
        return pd.Series(name=series_id, dtype=float)


# ── Transforms ────────────────────────────────────────────────────────────────

def apply_transform(s: pd.Series, transform: str) -> pd.Series:
    """
    Apply the specified transform to a raw level series.
    Returns transformed series.
    """
    if transform == "level":
        return s

    elif transform == "yoy":
        # Year-over-year % change
        if s.index.freqstr and "Q" in str(s.index.freqstr):
            return s.pct_change(4) * 100
        else:
            return s.pct_change(12) * 100  # monthly

    elif transform == "pch_ann":
        # Annualized quarterly % change (for GDP growth)
        freq = pd.infer_freq(s.dropna().index)
        if freq and "Q" in freq:
            return ((s / s.shift(1)) ** 4 - 1) * 100
        else:
            # For monthly data: annualize monthly change
            return ((s / s.shift(1)) ** 12 - 1) * 100

    elif transform == "ch":
        # Absolute period-over-period change
        return s.diff()

    elif transform == "pch":
        # Period-over-period % change
        return s.pct_change() * 100

    else:
        return s


# ── Get series with metadata ──────────────────────────────────────────────────

def get_series(series_id: str, transformed: bool = True,
               start: str = HISTORY_START) -> pd.Series:
    """
    Pull a series from FRED (or cache) and optionally apply its
    configured transform from config.py. Returns pd.Series.
    """
    meta = FRED_SERIES.get(series_id, {})
    transform = meta.get("transform", "level")
    raw = pull_series(series_id, start=start)
    if raw.empty:
        return raw
    if transformed:
        return apply_transform(raw, transform)
    return raw


def get_latest(series_id: str) -> tuple:
    """
    Returns (latest_value, latest_date) for a series.
    Useful for dashboard summary stats.
    """
    s = get_series(series_id)
    s = s.dropna()
    if s.empty:
        return (None, None)
    return (round(s.iloc[-1], 3), s.index[-1].date())


# ── Pull all series by section ────────────────────────────────────────────────

def pull_section(section: str, verbose: bool = True) -> dict:
    """
    Pull all series belonging to a given section.
    Returns dict: { series_id: pd.Series (transformed) }
    """
    series_in_section = {
        k: v for k, v in FRED_SERIES.items()
        if v.get("section") == section
    }
    results = {}
    for sid, meta in series_in_section.items():
        if verbose:
            print(f"  Pulling {sid}: {meta['label']}...")
        s = get_series(sid)
        results[sid] = s
    return results


def pull_all(verbose: bool = True) -> dict:
    """
    Pull every series in the catalogue.
    Returns nested dict: { section: { series_id: pd.Series } }
    """
    from config import SECTION_ORDER
    all_data = {}
    seen = set()

    for section_key, section_label in SECTION_ORDER:
        if verbose:
            print(f"\n── {section_label} ──────────────────────────────")
        all_data[section_key] = {}
        for sid, meta in FRED_SERIES.items():
            if meta.get("section") == section_key and sid not in seen:
                if verbose:
                    print(f"  {sid}: {meta['label']}")
                s = get_series(sid)
                all_data[section_key][sid] = s
                seen.add(sid)

    return all_data


# ── Derived series (computed, not direct FRED pulls) ─────────────────────────

def output_gap(start: str = HISTORY_START) -> pd.Series:
    """
    Compute output gap = (Real GDP - Potential GDP) / Potential GDP * 100
    Uses GDPC1 and GDPPOT. Both are quarterly.
    Note: Fed uses FRB/US potential; this is CBO-based proxy.
    """
    gdp  = pull_series("GDPC1",  start=start)
    pot  = pull_series("GDPPOT", start=start)

    # GDPPOT is in 2012 dollars, GDPC1 in 2017 dollars — need to normalize
    # Use ratio approach: compute growth paths and align levels
    # Simpler: just use pct deviation from trend via HP filter as alternative
    # Here we use ratio of indices (both indexed to same base period)
    aligned = pd.concat([gdp, pot], axis=1).dropna()
    aligned.columns = ["gdp", "pot"]

    # Normalize both to 100 at first common observation
    aligned = aligned / aligned.iloc[0] * 100

    gap = (aligned["gdp"] - aligned["pot"]) / aligned["pot"] * 100
    gap.name = "OUTPUT_GAP"
    return gap


def unemployment_gap(start: str = HISTORY_START) -> pd.Series:
    """
    Unemployment gap = Unemployment Rate - Natural Rate (CBO NROU).
    Negative = labor market tighter than neutral.
    """
    u    = pull_series("UNRATE", start=start).resample("QS").mean()
    nrou = pull_series("NROU",   start=start)
    gap  = u - nrou
    gap.name = "UNEMPLOYMENT_GAP"
    return gap.dropna()


def mortgage_spread(start: str = HISTORY_START) -> pd.Series:
    """
    30-yr mortgage rate minus 10-yr Treasury yield.
    Measures housing credit conditions.
    """
    mort  = pull_series("MORTGAGE30US", start=start).resample("MS").mean()
    tsy10 = pull_series("DGS10",        start=start).resample("MS").mean()
    spread = mort - tsy10
    spread.name = "MORTGAGE_SPREAD"
    return spread.dropna()


def real_fed_funds(start: str = HISTORY_START) -> pd.Series:
    """
    Real fed funds rate = Nominal FFR - trailing 12-month core PCE inflation.
    Key Tealbook policy stance indicator.
    """
    ffr      = pull_series("FEDFUNDS",  start=start)
    core_pce = get_series("PCEPILFE", transformed=True, start=start)  # YoY

    # Align to monthly
    ffr_m      = ffr.resample("MS").mean()
    core_pce_m = core_pce.resample("MS").last()

    real_ffr = ffr_m - core_pce_m
    real_ffr.name = "REAL_FFR"
    return real_ffr.dropna()


def yield_curve_snapshot(as_of: str = None) -> pd.DataFrame:
    """
    Return a snapshot of the Treasury yield curve.
    as_of: date string 'YYYY-MM-DD'. Defaults to most recent available.
    """
    tenors = {
        "3M":  "DTB3",
        "6M":  "DTB6",
        "1Y":  "DGS1",
        "2Y":  "DGS2",
        "3Y":  "DGS3",
        "5Y":  "DGS5",
        "7Y":  "DGS7",
        "10Y": "DGS10",
        "20Y": "DGS20",
        "30Y": "DGS30",
    }
    records = []
    for tenor, sid in tenors.items():
        s = pull_series(sid)
        s = s.dropna()
        if s.empty:
            continue
        if as_of:
            # Get value on or before as_of date
            s = s[s.index <= pd.Timestamp(as_of)]
        val = s.iloc[-1] if not s.empty else np.nan
        dt  = s.index[-1].date() if not s.empty else None
        records.append({"tenor": tenor, "yield": val, "date": dt, "fred_id": sid})

    return pd.DataFrame(records).set_index("tenor")


# ── Summary snapshot table ────────────────────────────────────────────────────

def summary_snapshot() -> pd.DataFrame:
    """
    Produce a clean summary table of key indicators for the
    Tealbook-style projection comparison table.
    """
    key_series = {
        "Real GDP Growth (ann., latest Q)":         ("A191RL1Q225SBEA", True),
        "Unemployment Rate":                        ("UNRATE",           True),
        "Core PCE (YoY)":                           ("PCEPILFE",         True),
        "Total PCE (YoY)":                          ("PCEPI",            True),
        "Core CPI (YoY)":                           ("CPILFESL",         True),
        "Nonfarm Payrolls (monthly chg, thous.)":   ("PAYEMS",           True),
        "10-yr Treasury Yield":                     ("DGS10",            True),
        "10yr-2yr Spread":                          ("T10Y2Y",           True),
        "WTI Crude Oil ($/bbl)":                    ("DCOILWTICO",       False),
        "S&P 500":                                  ("SP500",            False),
        "VIX":                                      ("VIXCLS",           False),
        "Broad Dollar Index (real)":                ("RTWEXBGS",         True),
        "Chicago Fed NFCI":                         ("NFCI",             True),
    }

    rows = []
    for label, (sid, transformed) in key_series.items():
        s = get_series(sid, transformed=transformed) if transformed else pull_series(sid)
        s = s.dropna()
        if s.empty:
            rows.append({"Indicator": label, "Latest": "N/A", "As of": "N/A",
                         "3M ago": "N/A", "1Y ago": "N/A"})
            continue

        latest_val  = round(s.iloc[-1], 2)
        latest_date = s.index[-1].date()

        # 3 months ago
        three_mo = s[s.index <= s.index[-1] - pd.DateOffset(months=3)]
        val_3m = round(three_mo.iloc[-1], 2) if not three_mo.empty else "—"

        # 1 year ago
        one_yr = s[s.index <= s.index[-1] - pd.DateOffset(months=12)]
        val_1y = round(one_yr.iloc[-1], 2) if not one_yr.empty else "—"

        rows.append({
            "Indicator": label,
            "Latest":    latest_val,
            "As of":     str(latest_date),
            "3M ago":    val_3m,
            "1Y ago":    val_1y,
        })

    return pd.DataFrame(rows).set_index("Indicator")


# ── Diagnostic: test all series can be pulled ─────────────────────────────────

def test_all_pulls(verbose: bool = True) -> pd.DataFrame:
    """
    Attempt to pull every series in the catalogue.
    Returns a DataFrame summarizing success/failure and latest observation.
    """
    results = []
    for sid, meta in FRED_SERIES.items():
        s = pull_series(sid)
        success = not s.empty
        latest  = str(s.dropna().index[-1].date()) if success and not s.dropna().empty else "N/A"
        n_obs   = len(s.dropna()) if success else 0
        results.append({
            "Series ID":  sid,
            "Label":      meta["label"],
            "Section":    meta["section"],
            "Status":     "OK" if success else "FAILED",
            "N Obs":      n_obs,
            "Latest Obs": latest,
        })
        if verbose:
            status = "✓" if success else "✗"
            print(f"  {status} {sid:30s} {meta['label'][:40]}")

    return pd.DataFrame(results)

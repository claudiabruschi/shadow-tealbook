"""
fred_pulls.py — FRED data fetcher with parquet cache.
Reads FRED_API_KEY from environment variable.
"""

import os
import pandas as pd
from pathlib import Path

CACHE_DIR = Path(__file__).parent / 'cache'
CACHE_DIR.mkdir(exist_ok=True)

try:
    from fredapi import Fred
    _fred = Fred(api_key=os.environ.get('FRED_API_KEY', ''))
except Exception:
    _fred = None


def pull_series(series_id: str, start: str = '2010-01-01') -> pd.Series:
    """
    Pull a FRED series, using a parquet cache to avoid redundant API calls.
    Returns a pandas Series with DatetimeIndex.
    """
    cache_file = CACHE_DIR / f'{series_id}.parquet'

    # Use cache if it exists and is less than 24 hours old
    if cache_file.exists():
        age_hours = (pd.Timestamp.now() - pd.Timestamp(cache_file.stat().st_mtime, unit='s')).total_seconds() / 3600
        if age_hours < 24:
            df = pd.read_parquet(cache_file)
            s = df['value']
            s.index = pd.to_datetime(s.index)
            return s[start:]

    if _fred is None:
        raise RuntimeError('FRED API key not set — set FRED_API_KEY environment variable')

    s = _fred.get_series(series_id, observation_start=start)
    s.name = series_id
    s.index = pd.to_datetime(s.index)

    # Cache to parquet
    df = s.to_frame(name='value')
    df.to_parquet(cache_file)

    return s[start:]


def get_series(series_id: str, start: str = '2010-01-01') -> pd.Series:
    """Alias for pull_series."""
    return pull_series(series_id, start=start)

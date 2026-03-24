"""
fred_pulls.py — FRED data fetcher with parquet cache and retry logic.
Reads FRED_API_KEY from environment variable.
"""

import os
import time
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
    Pull a FRED series with parquet cache and retry on transient errors.
    Returns a pandas Series with DatetimeIndex.
    On persistent failure, returns cached data if available, else empty Series.
    """
    cache_file = CACHE_DIR / f'{series_id}.parquet'

    # Use cache if it exists and is less than 24 hours old
    if cache_file.exists():
        age_hours = (
            pd.Timestamp.now() -
            pd.Timestamp(cache_file.stat().st_mtime, unit='s')
        ).total_seconds() / 3600
        if age_hours < 24:
            try:
                df = pd.read_parquet(cache_file)
                s = df['value']
                s.index = pd.to_datetime(s.index)
                return s[start:]
            except Exception:
                pass  # cache corrupt — fall through to fresh pull

    if _fred is None:
        # No API key — return stale cache if available
        if cache_file.exists():
            try:
                df = pd.read_parquet(cache_file)
                s = df['value']
                s.index = pd.to_datetime(s.index)
                print(f'[WARN] No FRED API key — using stale cache for {series_id}')
                return s[start:]
            except Exception:
                pass
        raise RuntimeError('FRED API key not set — set FRED_API_KEY environment variable')

    # Retry up to 3 times with exponential backoff
    last_err = None
    for attempt in range(3):
        try:
            s = _fred.get_series(series_id, observation_start=start)
            s.name = series_id
            s.index = pd.to_datetime(s.index)

            # Cache to parquet
            df = s.to_frame(name='value')
            df.to_parquet(cache_file)

            return s[start:]

        except Exception as e:
            last_err = e
            if attempt < 2:
                wait = 2 ** attempt  # 1s, 2s
                print(f'[WARN] FRED pull failed for {series_id} (attempt {attempt+1}): {e}. Retrying in {wait}s...')
                time.sleep(wait)
            else:
                print(f'[ERROR] FRED pull failed for {series_id} after 3 attempts: {e}')

    # All retries failed — return stale cache if available
    if cache_file.exists():
        try:
            df = pd.read_parquet(cache_file)
            s = df['value']
            s.index = pd.to_datetime(s.index)
            print(f'[WARN] Using stale cache for {series_id} due to FRED error')
            return s[start:]
        except Exception:
            pass

    # Return empty series so render continues rather than crashing
    print(f'[ERROR] No data available for {series_id} — returning empty series')
    return pd.Series([], dtype=float, name=series_id)


def get_series(series_id: str, start: str = '2010-01-01') -> pd.Series:
    """Alias for pull_series."""
    return pull_series(series_id, start=start)

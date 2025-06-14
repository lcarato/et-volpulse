from __future__ import annotations

import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Iterable

import pandas as pd
import yfinance as yf
from alpha_vantage.timeseries import TimeSeries
import yaml

from .validation import DataGapError, check_completeness

logger = logging.getLogger(__name__)

CONFIG_DIR = Path(__file__).resolve().parent.parent / "config"
TICKER_FILE = CONFIG_DIR / "tickers.yml"

with open(TICKER_FILE, "r") as fh:
    TICKERS: dict[str, str] = yaml.safe_load(fh)

SYMBOLS = list(TICKERS.values())


def _fetch_yfinance(
    symbols: Iterable[str], start: datetime, end: datetime
) -> pd.DataFrame:
    df = yf.download(
        list(symbols), start=start, end=end, group_by="ticker", progress=False
    )
    return df


def _fetch_alpha(symbol: str, start: datetime, end: datetime) -> pd.DataFrame:
    key = os.getenv("ALPHAVANTAGE_KEY")
    ts = TimeSeries(key, output_format="pandas")
    data, _ = ts.get_daily(symbol=symbol, outputsize="full")
    data.index = pd.to_datetime(data.index)
    data = data.loc[start:end]
    data = data.rename(
        columns={
            "1. open": "Open",
            "2. high": "High",
            "3. low": "Low",
            "4. close": "Close",
            "5. volume": "Volume",
        }
    )
    return data


def get_prices(start: datetime, end: datetime) -> pd.DataFrame:
    """Return OHLCV prices for configured tickers."""
    raw = _fetch_yfinance(SYMBOLS, start, end)
    if raw.empty:
        logger.warning("yfinance returned empty, falling back to Alpha Vantage")
        frames = {}
        for sym in SYMBOLS:
            frames[sym] = _fetch_alpha(sym, start, end)
        raw = pd.concat(frames, axis=1)
    stacked = raw.stack(level=0).sort_index()
    stacked.index.names = ["date", "ticker"]
    try:
        check_completeness(stacked)
    except DataGapError as err:
        logger.warning("Data gap detected: %s", err)
        raise
    return stacked

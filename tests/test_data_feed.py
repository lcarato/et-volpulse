import pandas as pd
import pytest

from et_vol_pulse import data_feed
from et_vol_pulse.validation import DataGapError


def test_get_prices_gap(monkeypatch):
    dates = pd.date_range("2024-01-01", periods=5)
    idx = pd.MultiIndex.from_product(
        [dates[2:], ["ICLN", "QCLN"]], names=["date", "ticker"]
    )
    df = pd.DataFrame({"Close": 1.0}, index=idx)

    def fake_download(symbols, start, end, group_by="ticker", progress=False):
        return df.unstack("ticker")

    monkeypatch.setattr(
        data_feed, "_fetch_yfinance", lambda s, start, end: fake_download(s, start, end)
    )
    monkeypatch.setattr(
        data_feed,
        "_fetch_alpha",
        lambda symbol, start, end: df.xs(symbol, level="ticker"),
    )

    with pytest.raises(DataGapError):
        data_feed.get_prices(dates[0], dates[-1])

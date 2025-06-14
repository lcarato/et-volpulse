from __future__ import annotations

from datetime import date, timedelta

import pandas as pd
import streamlit as st

from .data_feed import get_prices
from .weights import get_weights
from .metrics import calc_trvi, get_regime_series
from .validation import check_completeness, DataGapError


@st.cache_data(ttl=3600)
def load_prices(start: date, end: date) -> pd.DataFrame:
    return get_prices(start, end)


def main() -> None:
    st.title("ET Vol Pulse")
    start, end = st.sidebar.date_input(
        "Date range",
        value=(date.today() - timedelta(days=365), date.today()),
    )
    show_benchmark = st.sidebar.checkbox("Overlay benchmark")

    prices = load_prices(start, end)
    try:
        check_completeness(prices, threshold=1.0)
    except DataGapError:
        st.warning("Data incomplete")

    close = prices.unstack("ticker")["Close"]
    ret = close.pct_change().dropna()
    weights = get_weights(pd.Timestamp(end))
    trvi = calc_trvi(ret, weights)
    regimes = get_regime_series(trvi)

    st.line_chart(trvi.dropna(), height=400)
    st.area_chart(regimes.map({"low": 0.2, "normal": 0.5, "high": 0.8}).dropna())

    if show_benchmark:
        st.line_chart(close.get("^VIX"))


if __name__ == "__main__":
    main()

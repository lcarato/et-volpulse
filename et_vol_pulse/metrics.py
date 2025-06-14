from __future__ import annotations

import numpy as np
import pandas as pd


def calc_trvi(ret_df: pd.DataFrame, weights: pd.Series, window: int = 21) -> pd.Series:
    portfolio = ret_df.dot(weights)
    return portfolio.rolling(window).std() * np.sqrt(252)


def get_regime_series(trvi: pd.Series, window: int = 252) -> pd.Series:
    q15 = trvi.rolling(window).quantile(0.15)
    q85 = trvi.rolling(window).quantile(0.85)
    out = []
    for idx in trvi.index:
        if pd.isna(q15.loc[idx]) or pd.isna(q85.loc[idx]) or pd.isna(trvi.loc[idx]):
            out.append(np.nan)
        elif trvi.loc[idx] <= q15.loc[idx]:
            out.append("low")
        elif trvi.loc[idx] >= q85.loc[idx]:
            out.append("high")
        else:
            out.append("normal")
    return pd.Series(out, index=trvi.index, dtype="object")

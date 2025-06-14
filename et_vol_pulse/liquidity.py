from __future__ import annotations

import pandas as pd


def scale_by_liquidity(weights: pd.Series, adv: pd.Series) -> pd.Series:
    scaled = weights * adv
    return scaled / scaled.sum()

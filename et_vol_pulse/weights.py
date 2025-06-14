from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import pandas as pd


class MissingWeightError(Exception):
    """Raised when weight data is missing for requested date."""


DATA_FILE = Path(__file__).resolve().parent.parent / "config" / "energy_shares.csv"
WEIGHTS_DF = pd.read_csv(DATA_FILE, parse_dates=["date"])


def get_weights(date: pd.Timestamp) -> pd.Series:
    eligible = WEIGHTS_DF[WEIGHTS_DF["date"] <= date]
    if eligible.empty:
        raise MissingWeightError(f"No weights for {date}")
    latest_date = eligible["date"].max()
    subset = eligible[eligible["date"] == latest_date]
    weights = pd.Series(subset["share"].values, index=subset["ticker"])
    weights = weights / weights.sum()
    return weights

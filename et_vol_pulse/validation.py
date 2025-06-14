from __future__ import annotations

import logging
import sys
from dataclasses import dataclass
from typing import Iterable

import pandas as pd

logger = logging.getLogger(__name__)


class DataGapError(Exception):
    def __init__(self, symbols: Iterable[str]):
        self.symbols = list(symbols)
        super().__init__("Data gap for: " + ",".join(self.symbols))


def check_completeness(df: pd.DataFrame, threshold: float = 0.8) -> bool:
    expected = (
        df.index.get_level_values(0).nunique() * df.index.get_level_values(1).nunique()
    )
    actual = df.dropna().shape[0]
    completeness = actual / expected
    if completeness < threshold:
        logger.warning(
            "Completeness %.2f below threshold %.2f", completeness, threshold
        )
        raise DataGapError(df.index.get_level_values(1).unique())
    return True


def main() -> int:
    sample = pd.DataFrame({"a": [1, 2]}, index=[0, 1])
    try:
        check_completeness(
            sample.set_index(pd.MultiIndex.from_product([[0, 1], ["a"]]))
        )
    except DataGapError:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

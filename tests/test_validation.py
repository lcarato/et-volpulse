import pandas as pd
import pytest

from et_vol_pulse.validation import check_completeness, DataGapError


def test_check_completeness_fail():
    idx = pd.MultiIndex.from_product(
        [pd.date_range("2024-01-01", periods=3), ["ICLN"]], names=["date", "ticker"]
    )
    df = pd.DataFrame({"Close": [1.0, None, None]}, index=idx)
    with pytest.raises(DataGapError):
        check_completeness(df, threshold=0.8)

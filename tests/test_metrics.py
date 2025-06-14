import numpy as np
import pandas as pd

from et_vol_pulse.metrics import calc_trvi


def test_calc_trvi():
    cov = np.array([[0.1, 0.02, 0.01], [0.02, 0.2, 0.03], [0.01, 0.03, 0.3]])
    weights = pd.Series([0.3, 0.4, 0.3])
    mean = np.zeros(3)
    ret = np.random.multivariate_normal(mean, cov, size=300)
    ret_df = pd.DataFrame(ret, columns=[0, 1, 2])
    trvi = calc_trvi(ret_df, weights)
    expected = np.sqrt(weights.T.dot(cov).dot(weights)) * np.sqrt(252)
    np.testing.assert_allclose(trvi.dropna().iloc[-1], expected, rtol=0.1)

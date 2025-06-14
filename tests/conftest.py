import numpy as np
import pytest


@pytest.fixture(autouse=True)
def _set_seed():
    np.random.seed(0)

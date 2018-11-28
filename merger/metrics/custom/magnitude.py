import pandas as pd
import numpy as np
import math
from ...utils import float64, compact, type_argsort


def value_magnitude(value: float):
    return int(math.floor(math.log10(abs(value))))


def magnitude(A: pd.DataFrame, B: pd.DataFrame)->np.ndarray:
    """Return boolean matrix representing if a given cell i,j has same unit."""
    a, b = [
        np.array([value_magnitude(np.mean(c)) for c in compact(float64(df))]) for df in (A, B)
    ]

    return type_argsort(a[:, None] == b, None, A, B)

from ...utils import float64, compact, type_argsort
import numpy as np
import pandas as pd
from typing import Callable


def pairwise_test(A: pd.DataFrame, B: pd.DataFrame, test: Callable, minimum=500)->np.ndarray:
    a, b = [
        compact(float64(df)) for df in (A, B)
    ]
    return type_argsort(np.array([[test(i, j)[1] if len(i) > minimum and len(j) > minimum else 0 for j in b] for i in a]), None, A, B)

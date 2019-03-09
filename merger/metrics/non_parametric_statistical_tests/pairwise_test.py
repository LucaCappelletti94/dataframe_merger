from ...utils import float64, compact, type_argsort
import numpy as np
import pandas as pd
from typing import Callable
import random



def pairwise_test(A: pd.DataFrame, B: pd.DataFrame, test: Callable)->np.ndarray:
    a, b = [
        compact(df) for df in (A, B)
    ]
    return np.array([[0 if np.all(i==j) else 1/test(i, j)[1] if len(i) and len(j) else  np.inf  for j in b] for i in a])

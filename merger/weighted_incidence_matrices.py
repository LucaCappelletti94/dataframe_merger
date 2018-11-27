import pandas as pd
import numpy as np
from .weighted_matrices import weighted_matrices
from typing import List
from .metrics import METRICS_NUMBER


def weighted_incidence_matrices(dfs: List[pd.DataFrame])-> List[np.ndarray]:
    sizes = [len(df.columns) for df in dfs]
    n = sum(sizes)
    grounds = [np.zeros((n, n)) for i in range(METRICS_NUMBER)]
    for (i, j), matrices in weighted_matrices(dfs):
        x, y = [
            slice(sum(sizes[:k]), sum(sizes[:k-1]) if k > 0 else 0) for k in (i, j)
        ]
        for k, matrix in enumerate(matrices):
            grounds[k][x, y] = matrix
            grounds[k][y, x] = matrix.T
    return grounds

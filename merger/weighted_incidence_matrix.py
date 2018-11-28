import pandas as pd
import numpy as np
from .assignment import assignment
from typing import List


def weighted_incidence_matrix(dfs: List[pd.DataFrame])-> List[np.ndarray]:
    sizes = [len(df.columns) for df in dfs]
    n = sum(sizes)
    ground = np.zeros((n, n))
    for (i, j), M in assignment(dfs):
        x, y = [
            slice(sum(sizes[:k]), sum(sizes[:k+1])) for k in (i, j)
        ]
        ground[x, y] = M
        ground[y, x] = M.T
    return ground

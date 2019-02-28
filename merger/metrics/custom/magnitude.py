import pandas as pd
import numpy as np
import math
from ...mask_decorators import floats

@floats
def magnitude(A: pd.DataFrame, B: pd.DataFrame)->np.ndarray:
    """Return boolean matrix representing if a given cell i,j has same unit."""
    a, b = [
        np.log10(np.nanmean(df.values, axis=0)).astype(int) for df in (A, B)
    ]

    return a[:, None] == b

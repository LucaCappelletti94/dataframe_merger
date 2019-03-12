import pandas as pd
import numpy as np


def units(A: pd.DataFrame, B: pd.DataFrame, sep: str = " | ")->np.ndarray:
    """Return boolean matrix representing if a given cell i,j has same unit."""
    unit_A, unit_B = [
        np.array(
            [None if len(c.split(sep)) == 1 else c.split(sep)[1] for c in df])
        for df in (A, B)
    ]
    return unit_A[:, None] == unit_B

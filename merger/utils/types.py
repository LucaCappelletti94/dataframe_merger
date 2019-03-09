import pandas as pd
import numpy as np
from typing import List


def float64(df: pd.DataFrame)->pd.DataFrame:
    """Return float columns from given DataFrame."""
    return df.select_dtypes(include='float64')


def string(df: pd.DataFrame)->pd.DataFrame:
    """Return string columns from given DataFrame."""
    return df.select_dtypes(include='object')


def compact(df: pd.DataFrame)->pd.DataFrame:
    """Return non nan and non zero values list per column."""
    return [
        df[c][df[c].notnull()].iloc[df[c][df[c].notnull()].nonzero()].values for c in df
    ]


def invert(*arrays: List[np.ndarray])->List[np.ndarray]:
    return [1 - a for a in arrays]

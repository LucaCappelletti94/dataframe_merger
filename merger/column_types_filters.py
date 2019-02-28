import pandas as pd
import numpy as np
from typing import List

def binary_mask(df:pd.DataFrame)->List[bool]:
    """Return a list representing which columns are boolean.
        df:pd.DataFrame, dataframe of which we have to determine the columns.
    """
    return np.array([
        np.all(np.isin(df[col].dropna().unique(), [0,1])) for col in df
    ])

def float_mask(df:pd.DataFrame)->List[bool]:
    """Return a list representing which columns are float.
        df:pd.DataFrame, dataframe of which we have to determine the columns.
    """
    types = df.dtypes.values
    return np.any([
        types == "float64",
        types == "int64"
    ], axis=0)

def objects_mask(df:pd.DataFrame)->List[bool]:
    """Return a list representing which columns are objects-like (strings, for example).
        df:pd.DataFrame, dataframe of which we have to determine the columns.
    """
    return df.dtypes.values == "object"

def datetime_mask(df:pd.DataFrame)->List[bool]:
    """Return a list representing which columns are datetime.
        df:pd.DataFrame, dataframe of which we have to determine the columns.
    """
    return df.dtypes.values == "datetime64[ns]"
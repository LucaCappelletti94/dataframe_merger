import pandas as pd
import numpy as np
from typing import Callable
from .column_types_filters import float_mask, objects_mask, binary_mask, datetime_mask
from pprint import pprint

def mask(df1:pd.DataFrame, df2:pd.DataFrame, column_mask:Callable[[pd.DataFrame], np.ndarray], distance:Callable[[pd.DataFrame, pd.DataFrame], np.ndarray], *args, **kwargs)->pd.DataFrame:
    df1_mask, df2_mask = column_mask(df1), column_mask(df2)
    ground = pd.DataFrame(
        np.full((df2.columns.size, df1.columns.size), np.NaN),
        columns=df1.columns,
        index=df2.columns
    )

    ground.update(pd.DataFrame(
        distance(
            df2[df2.columns[df2_mask]],
            df1[df1.columns[df1_mask]],
            *args,
            **kwargs
        ),
        columns=df1.columns[df1_mask],
        index=df2.columns[df2_mask]
    ))

    return ground

def floats(distance:Callable[[pd.DataFrame, pd.DataFrame], np.ndarray]):
    def wrapped(df1:pd.DataFrame, df2:pd.DataFrame, *args, **kwargs):
        return mask(df1, df2, float_mask, distance, *args, **kwargs)
    return wrapped

def strings(distance:Callable[[pd.DataFrame, pd.DataFrame], np.ndarray]):
    def wrapped(df1:pd.DataFrame, df2:pd.DataFrame, *args, **kwargs):
        return mask(df1, df2, objects_mask, distance, *args, **kwargs)
    return wrapped

def binaries(distance:Callable[[pd.DataFrame, pd.DataFrame], np.ndarray]):
    def wrapped(df1:pd.DataFrame, df2:pd.DataFrame, *args, **kwargs):
        return mask(df1, df2, binary_mask, distance, *args, **kwargs)
    return wrapped

def datetimes(distance:Callable[[pd.DataFrame, pd.DataFrame], np.ndarray]):
    def wrapped(df1:pd.DataFrame, df2:pd.DataFrame, *args, **kwargs):
        return mask(df1, df2, datetime_mask, distance, *args, **kwargs)
    return wrapped
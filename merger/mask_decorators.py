import pandas as pd
import numpy as np
from typing import Callable
from .column_types_filters import float_mask, objects_mask, binary_mask, datetime_mask
from pprint import pprint

def column_mask(df1:pd.DataFrame, df2:pd.DataFrame, column_type:Callable[[pd.DataFrame], np.ndarray], distance:Callable[[pd.DataFrame, pd.DataFrame], np.ndarray], *args, **kwargs)->pd.DataFrame:
    df1_mask, df2_mask = column_type(df1), column_type(df2)
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

def row_mask(df1:pd.DataFrame, df2:pd.DataFrame, column_type:Callable[[pd.DataFrame], np.ndarray], distance:Callable[[pd.DataFrame, pd.DataFrame], np.ndarray], *args, **kwargs)->pd.DataFrame:
    distances = distance(
        df2[df2.columns[column_type(df2)]],
        df1[df1.columns[column_type(df1)]],
        *args,
        **kwargs
    )
    if len(distances)==0:
        distances = np.full((df2.index.size, df1.index.size), np.nan)
    else:
        distances = np.nanmean(distances, axis=0)
    
    return pd.DataFrame(
        distances,
        columns=df1.index,
        index=df2.index
    )

def floats(distance:Callable[[pd.DataFrame, pd.DataFrame], np.ndarray], mask:Callable):
    def wrapped(df1:pd.DataFrame, df2:pd.DataFrame, *args, **kwargs):
        return mask(df1, df2, float_mask, distance, *args, **kwargs)
    return wrapped

def strings(distance:Callable[[pd.DataFrame, pd.DataFrame], np.ndarray], mask:Callable):
    def wrapped(df1:pd.DataFrame, df2:pd.DataFrame, *args, **kwargs):
        return mask(df1, df2, objects_mask, distance, *args, **kwargs)
    return wrapped

def binaries(distance:Callable[[pd.DataFrame, pd.DataFrame], np.ndarray], mask:Callable):
    def wrapped(df1:pd.DataFrame, df2:pd.DataFrame, *args, **kwargs):
        return mask(df1, df2, binary_mask, distance, *args, **kwargs)
    return wrapped

def datetimes(distance:Callable[[pd.DataFrame, pd.DataFrame], np.ndarray], mask:Callable):
    def wrapped(df1:pd.DataFrame, df2:pd.DataFrame, *args, **kwargs):
        return mask(df1, df2, datetime_mask, distance, *args, **kwargs)
    return wrapped

def row_floats(distance:Callable[[pd.DataFrame, pd.DataFrame], np.ndarray]):    
    return floats(distance, row_mask)

def row_strings(distance:Callable[[pd.DataFrame, pd.DataFrame], np.ndarray]):   
    return strings(distance, row_mask)

def row_binaries(distance:Callable[[pd.DataFrame, pd.DataFrame], np.ndarray]):  
    return binaries(distance, row_mask)

def row_datetimes(distance:Callable[[pd.DataFrame, pd.DataFrame], np.ndarray]): 
    return datetimes(distance, row_mask)

def column_floats(distance:Callable[[pd.DataFrame, pd.DataFrame], np.ndarray]):    
    return floats(distance, column_mask)

def column_strings(distance:Callable[[pd.DataFrame, pd.DataFrame], np.ndarray]):   
    return strings(distance, column_mask)

def column_binaries(distance:Callable[[pd.DataFrame, pd.DataFrame], np.ndarray]):  
    return binaries(distance, column_mask)

def column_datetimes(distance:Callable[[pd.DataFrame, pd.DataFrame], np.ndarray]): 
    return datetimes(distance, column_mask)
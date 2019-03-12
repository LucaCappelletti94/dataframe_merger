import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import manhattan_distances
from ...mask_decorators import row_floats



@row_floats
def weighted_mse(A: pd.DataFrame, B: pd.DataFrame):
    return [
        (manhattan_distances(
            np.nan_to_num(A.values),
            np.nan_to_num(B.values)
        )/manhattan_distances(
            np.nan_to_num(A.values),
            -np.nan_to_num(B.values))**2
        ) for column in set(A.columns) & set(B.columns)
    ]
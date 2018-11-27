import numpy as np
import pandas as pd


def matrix_type_argsort(matrix: np.matrix, df: pd.DataFrame) ->np.ndarray:
    """Return given `matrix` sorted using given `df` DataFrame types."""
    return matrix[np.argsort(
        list(zip(*sorted(zip(df.dtypes, range(len(df.dtypes))))))[1]), :]


def type_argsort(floats: np.matrix,
                 strings: np.matrix,
                 df1: pd.DataFrame,
                 df2: pd.DataFrame,
                 fill: float=0) -> np.ndarray:
    """Return combined matrix sorted in both axis using given dataframes types."""
    ground = np.full((df1.shape[1], df2.shape[1]), float(fill))
    if floats is not None:
        ground[:floats.shape[0], :floats.shape[1]] = floats
    if strings is not None:
        ground[-strings.shape[0]:, -strings.shape[1]:] = strings
    return matrix_type_argsort(matrix_type_argsort(ground, df1).T, df2).T

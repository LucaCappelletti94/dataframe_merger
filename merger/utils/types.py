import pandas as pd


def float64(df: pd.DataFrame)->pd.DataFrame:
    """Return float columns from given DataFrame."""
    return df.select_dtypes(include='float64')


def string(df: pd.DataFrame)->pd.DataFrame:
    """Return string columns from given DataFrame."""
    return df.select_dtypes(include='object')


def compact(df: pd.DataFrame)->pd.DataFrame:
    """Return non nan and non zero values list per column."""
    return [
        df[c][df[c].notnull()].iloc[df[c][df[c].notnull()].nonzero()] for c in df
    ]

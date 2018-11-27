import pandas as pd
from .weighted_incidence_matrices import weighted_incidence_matrices
import os


def merge(path: str):
    return weighted_incidence_matrices([
        pd.read_csv("{path}/{csv}".format(path=path,
                                          csv=csv), index_col=["name"])
        for path, dirs, csvs in os.walk(path)
        for csv in csvs if csv.endswith(".csv")
    ][:2])

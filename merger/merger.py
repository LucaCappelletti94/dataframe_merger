import pandas as pd
from .weighted_incidence_matrix import weighted_incidence_matrix
import os


def merge(path: str):
    return weighted_incidence_matrix([
        pd.read_csv("{path}/{csv}".format(path=path,
                                          csv=csv), index_col=["name"])
        for path, dirs, csvs in os.walk(path)
        for csv in csvs if csv.endswith(".csv")
    ])

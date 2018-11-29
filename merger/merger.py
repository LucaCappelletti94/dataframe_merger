import pandas as pd
import numpy as np
from .weighted_incidence_matrix import weighted_incidence_matrix
from .scip import maximal_circles_model
from pprint import pprint
import os


def circle(e, i, start):
    if e[i] != start:
        return [i] + circle(e, e[i], start)
    return [i]


def circles(e):
    found = []
    for start in e:
        if all([start not in c for c in found]):
            found.append(circle(e, start, start))
    return found


def merge(path: str):
    dfs = [
        pd.read_csv("{path}/{csv}".format(path=path,
                                          csv=csv), index_col=["name"])
        for path, dirs, csvs in os.walk(path)
        for csv in csvs if csv.endswith(".csv")
    ]
    model = maximal_circles_model(weighted_incidence_matrix(dfs))

    model.optimize()
    x = model.data
    e = {i: j for (i, j), edge in x.items()
         if model.getVal(edge) == 1}

    columns = np.concatenate([df.columns for df in dfs])

    for c in circles(e):
        print(columns[c])

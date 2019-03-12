import pandas as pd
import numpy as np
from typing import List, Dict
from .column_alignment import column_alignment
from .row_metrics import weighted_mse, rows_tfidf_cosine_distances
from .tfidf_utils import vectorizer
from IPython.display import display
from sklearn.preprocessing import normalize

def compose(dfs:List[pd.DataFrame], groups:List[List[int]]):
    columns = [col for df in dfs for col in df]
    indices = [i for i, df in enumerate(dfs) for c in df]

    copy = [
        df.copy() for df in dfs
    ]

    for group in groups:
        for e in group[1:]:
            copy[indices[e]].rename(
                columns={
                    columns[e]:columns[group[0]]
                },
                inplace=True
            )
    
    for df in copy:
        for column in columns:
            if column not in df:
                df[column] = np.nan 

    
    return copy

def group_to_sets(group):
    return [set(s) for s in group]

def score(dfs:List[pd.DataFrame], data_corpus, path:str, knp:List[float], weights:List[float])->float:
    other_groups, composed = column_alignment(
        path,
        len(dfs),
        knp,
        weights
    )

    composed_sets = group_to_sets(composed)

    total = 0

    for other_group in other_groups:
        nan_percentage = np.mean([
            np.mean(pd.isna(df).values) for df in compose(dfs, other_group)
        ])
        matches = sum([
            any([match == c for c in composed_sets]) for match in group_to_sets(other_group)
        ])
        total += (1-nan_percentage)*matches/len(other_group)
    return total

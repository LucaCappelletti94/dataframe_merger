from .metrics import columns_tfidf_cosine_distances, dataframes_tfidf_cosine_distances, corpora, vectorizer, units, pairwise_kolmogorov_smirnov_test, pairwise_mann_whitney_u_test
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from typing import Callable, List, Tuple
from multiprocessing import Pool, cpu_count
from tqdm import tqdm


def weighted_matrices_job(task: Tuple[Tuple[TfidfVectorizer, TfidfVectorizer], Tuple[pd.DataFrame, pd.DataFrame], Tuple[int, int]])->Tuple[Tuple[int, int], List[np.ndarray]]:
    (df_vectorizer, columns_vectorizer), (A, B), (i, j) = task
    return ((i, j), [
        dataframes_tfidf_cosine_distances(A, B, df_vectorizer),
        columns_tfidf_cosine_distances(A, B, columns_vectorizer)
    ] + [
        metric(A, B) for metric in (
            units,
            pairwise_kolmogorov_smirnov_test,
            pairwise_mann_whitney_u_test
        )
    ])


def weighted_matrices(dfs: List[pd.DataFrame])->List[Tuple[Tuple[int, int], List[np.ndarray]]]:
    vectorizers = [
        vectorizer(corpus) for corpus in corpora(dfs)
    ]
    jobs = [(vectorizers, (A, B), (i, j)) for i, A in enumerate(dfs)
            for j, B in enumerate(dfs[i:], i) if i != j]
    with Pool(min(cpu_count(), len(jobs))) as p:
        return list(tqdm(p.imap(weighted_matrices_job, jobs), total=len(jobs)))

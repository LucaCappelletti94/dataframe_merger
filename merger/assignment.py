from .metrics import columns_tfidf_cosine_similarity, dataframes_tfidf_cosine_similarity, corpora, vectorizer, units, magnitude, pairwise_kolmogorov_smirnov_test, pairwise_mann_whitney_u_test
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from typing import Callable, List, Tuple
from multiprocessing import Pool, cpu_count
from tqdm import tqdm
from .utils import invert, land
from scipy.optimize import linear_sum_assignment


def costs(A: pd.DataFrame, B: pd.DataFrame, columns_vectorizer: TfidfVectorizer, df_vectorizer: TfidfVectorizer):
    return invert(
        dataframes_tfidf_cosine_similarity(A, B, df_vectorizer),
        columns_tfidf_cosine_similarity(A, B, columns_vectorizer),
        *[
            metric(A, B) for metric in (
                pairwise_kolmogorov_smirnov_test,
                # pairwise_mann_whitney_u_test,
            )
        ])


def masks(A: pd.DataFrame, B: pd.DataFrame):
    return land(
        units(A, B),
        magnitude(A, B)
    )


def assignment_job(task: Tuple[Tuple[pd.DataFrame, pd.DataFrame, TfidfVectorizer, TfidfVectorizer], Tuple[int, int], Tuple[int, int]])->Tuple[Tuple[int, int], List[np.ndarray]]:
    (A, B, v1, v2), (n, m), (i, j) = task
    ground_sum = np.zeros((n, m))
    mask = masks(A, B)
    for C in costs(A, B, v1, v2):
        ground = np.zeros((n, m))
        C[~mask] = 1
        ground[linear_sum_assignment(C)] = 1
        ground[np.greater_equal(C, 0.75)] = 0
        ground_sum += ground

    return ((i, j), ground_sum)


def assignment(dfs: List[pd.DataFrame])->List[Tuple[Tuple[int, int], List[np.ndarray]]]:
    vectorizers = [
        vectorizer(corpus) for corpus in corpora(dfs)
    ]
    jobs = [((A, B, *vectorizers), (A.shape[1], B.shape[1]), (i, j)) for i, A in enumerate(dfs)
            for j, B in enumerate(dfs[i:], i) if i != j]
    with Pool(min(cpu_count(), len(jobs))) as p:
        return list(tqdm(p.imap(assignment_job, jobs), total=len(jobs)))

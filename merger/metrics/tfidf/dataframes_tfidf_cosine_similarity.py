from ...utils import string, compact, type_argsort
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def dataframes_tfidf_cosine_similarity(A: pd.DataFrame, B: pd.DataFrame, vectorizer: TfidfVectorizer):
    a, b = [
        np.array([np.mean(vectorizer.transform(c), axis=0) for c in compact(string(df))]) for df in (A, B)
    ]

    if a.size == 0 or b.size == 0:
        return np.zeros((A.shape[1], B.shape[1]))

    similarity = cosine_similarity(a.squeeze(axis=1), b.squeeze(axis=1))

    return type_argsort(None, similarity, A, B)

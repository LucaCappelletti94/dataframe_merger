from ...utils import string, compact, type_argsort
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_distances


def dataframes_tfidf_cosine_distances(A: pd.DataFrame, B: pd.DataFrame, vectorizer: TfidfVectorizer):
    try:
        return type_argsort(None, cosine_distances(*[
            [np.mean(vectorizer.transform(c), axis=0) for c in compact(string(df))] for df in (A, B)
        ]), A, B, fill=1)
    except ValueError:
        return np.ones((A.shape[1], B.shape[1]))

from ...utils import string, compact
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def columns_tfidf_cosine_similarity(A: pd.DataFrame, B: pd.DataFrame, vectorizer: TfidfVectorizer):
    try:
        return cosine_similarity(*[
            vectorizer.transform(df.columns) for df in (A, B)
        ])
    except (AttributeError):
        return np.zeros((A.shape[1], B.shape[1]))

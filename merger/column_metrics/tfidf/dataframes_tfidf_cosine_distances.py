from ...utils import compact
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_distances
from ...mask_decorators import column_strings

@column_strings
def dataframes_tfidf_cosine_distances(A: pd.DataFrame, B: pd.DataFrame, vectorizer: TfidfVectorizer):
    return cosine_distances(*[
        np.array([np.mean(vectorizer.transform(c), axis=0) for c in compact(df)]).squeeze(axis=1) for df in (A, B)
    ])
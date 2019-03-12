import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_distances
from ...mask_decorators import column_strings

@column_strings
def columns_tfidf_cosine_distances(A: pd.DataFrame, B: pd.DataFrame, vectorizer: TfidfVectorizer):
    return cosine_distances(*[
        vectorizer.transform(df.columns) for df in (A, B)
    ])

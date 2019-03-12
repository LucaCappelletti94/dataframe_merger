import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_distances
from ...mask_decorators import row_strings

@row_strings
def rows_tfidf_cosine_distances(A: pd.DataFrame, B: pd.DataFrame, vectorizer: TfidfVectorizer):
    return [
        cosine_distances(*[
            vectorizer.transform(df[column]) for df in (A, B)
        ]) for column in set(A.columns) & set(B.columns)
    ]
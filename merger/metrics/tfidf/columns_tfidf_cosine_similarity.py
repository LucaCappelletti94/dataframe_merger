from ...utils import string, compact
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from ...mask_decorators import strings

@strings
def columns_tfidf_cosine_similarity(A: pd.DataFrame, B: pd.DataFrame, vectorizer: TfidfVectorizer):
    return cosine_similarity(*[
        vectorizer.transform(df.columns) for df in (A, B)
    ])

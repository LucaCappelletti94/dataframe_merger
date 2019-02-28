from ...utils import compact, type_argsort
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from ...mask_decorators import strings

@strings
def dataframes_tfidf_cosine_similarity(A: pd.DataFrame, B: pd.DataFrame, vectorizer: TfidfVectorizer):
    return cosine_similarity(*[
        np.array([np.mean(vectorizer.transform(c), axis=0) for c in compact(df)]).squeeze(axis=1) for df in (A, B)
    ])
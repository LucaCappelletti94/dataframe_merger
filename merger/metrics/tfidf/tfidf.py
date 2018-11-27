from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from typing import List, Callable


def vectorizer(corpus: List[str], preprocessor=None, stop_words=None, max_df=1.0, min_df=1)->TfidfVectorizer:
    return TfidfVectorizer(
        input=corpus,
        preprocessor=preprocessor,
        stop_words=stop_words,
        max_df=max_df,
        min_df=min_df
    )

from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from typing import List, Callable


def vectorizer(corpus: List[str], preprocessor=None, stop_words=None)->TfidfVectorizer:
    try:
        my_tfidf = TfidfVectorizer(
            preprocessor=preprocessor,
            stop_words=stop_words,
        )
        my_tfidf.fit(corpus)
        return my_tfidf
    except ValueError:
        return None

from .metrics import pairwise_kolmogorov_smirnov_test, pairwise_mann_whitney_u_test, corpora, vectorizer, columns_tfidf_cosine_similarity, dataframes_tfidf_cosine_similarity, magnitude
from .dataframe_loader import dataframe_loader
import itertools
import os

def batch(source:str, sink:str):
    dfs = dataframe_loader(source)
    columns_corpus, data_corpus = corpora(dfs)
    metrics = {
        "kolmogorov": (pairwise_kolmogorov_smirnov_test, []),
        "mann": (pairwise_mann_whitney_u_test, []),
        "columns_tfidf":(columns_tfidf_cosine_similarity, [vectorizer(columns_corpus)]),
        "dataframes_tfidf":(dataframes_tfidf_cosine_similarity, [vectorizer(data_corpus)]),
        "magnitude":(magnitude, [])
    }

    for i, (df1, df2) in enumerate(itertools.combinations(dfs, 2)):
        path = "{root}/{i}".format(root=sink, i=i)
        os.makedirs(path, exist_ok=True)
        for metric, (callback, args) in metrics.items():
            callback(df1, df2, *args).to_csv("{path}/{metric}.csv".format(path=path, metric=metric))
from .metrics import pairwise_kolmogorov_smirnov_test, pairwise_mann_whitney_u_test, corpora, vectorizer, columns_tfidf_cosine_distances, dataframes_tfidf_cosine_distances, magnitude
from .dataframe_loader import dataframe_loader
import itertools
import os
from typing import Tuple

def batch(source:str, sink:str)->int:
    dfs = dataframe_loader(source)
    columns_corpus, data_corpus = corpora(dfs)
    metrics = {
        "kolmogorov": (pairwise_kolmogorov_smirnov_test, []),
        "mann": (pairwise_mann_whitney_u_test, []),
        "columns_tfidf":(columns_tfidf_cosine_distances, [vectorizer(columns_corpus)]),
        "dataframes_tfidf":(dataframes_tfidf_cosine_distances, [vectorizer(data_corpus)]),
        "magnitude":(magnitude, [])
    }

    dataframes_number = len(dfs)

    for metric, (callback, args) in enumerate(metrics.values()):
        for i in range(dataframes_number):
            for j in range(dataframes_number):
                if i<=j:
                    path = "{sink}/{metric}".format(sink=sink, metric=metric)
                    os.makedirs(path, exist_ok=True)
                    callback(dfs[i], dfs[j], *args).to_csv("{path}/{i}-{j}.csv".format(path=path, i=i, j=j))
    
    return len(dfs), [col for df in dfs for col in df]
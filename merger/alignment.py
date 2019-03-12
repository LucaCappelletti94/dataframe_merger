from .dataframe_loader import dataframe_loader
from .tfidf_utils import corpora
from .score import score
from bayes_opt import BayesianOptimization
from .column_metrics import pairwise_kolmogorov_smirnov_test, pairwise_mann_whitney_u_test, columns_tfidf_cosine_distances, dataframes_tfidf_cosine_distances, magnitude
import os
from .tfidf_utils import vectorizer
from typing import Tuple, List, Dict, Callable
import pandas as pd
from multiprocessing import cpu_count, Pool
import numpy as np
from .column_alignment import column_alignment
from tqdm import tqdm_notebook as tqdm

class Alignment:
    def __init__(self, source:str, output:str, tmp:str="tmp"):
        self._dfs = dataframe_loader(source)
        self._columns = [col for df in self._dfs for col in df]
        self._indices = [i for i, df in enumerate(self._dfs) for c in df]
        self._dataframes_number = len(self._dfs)
        self._output = output
        self._tmp = tmp
        self._source = source
        self._columns_corpus, self._data_corpus = [
            vectorizer(c) for c in corpora(self._dfs)
        ]
        self._metrics = {
            "kolmogorov": (pairwise_kolmogorov_smirnov_test, []),
            "mann": (pairwise_mann_whitney_u_test, []),
            "columns_tfidf":(columns_tfidf_cosine_distances, [self._columns_corpus]),
            "dataframes_tfidf":(dataframes_tfidf_cosine_distances, [self._data_corpus]),
            "magnitude":(magnitude, [])
        }
        self._metrics_number = len(self._metrics)
        
    def _metric_tasks(self):
        return [
            {
                "path":self._tmp,
                "callback":callback,
                "args":[self._dfs[i], self._dfs[j], *args],
                "output":"{path}/{metric}/{i}-{j}.csv".format(path=self._tmp, metric=metric, i=i, j=j)
            } for metric, (callback, args) in enumerate(self._metrics.values()) for i in range(self._dataframes_number) for j in range(self._dataframes_number) if i<=j]

    def _job(self, path:str, callback:Callable, args:List, output:str):
        os.makedirs(path, exist_ok=True)
        callback(*args).to_csv(output)

    def _job_callback(self, kwargs):
        self._job(**kwargs)

    def _determine_metrics(self):
        # with Pool(cpu_count()) as p:
        #     list(p.imap(self._job_callback, self._metric_tasks()))
        tasks = self._metric_tasks()
        for task in tqdm(tasks):
            self._job_callback(task)

    def _compose_dfs(self, groups:List[List[int]]):
        copy = [
            df.copy() for df in self._dfs
        ]

        for group in groups:
            for e in group[1:]:
                copy[self._indices[e]].rename(
                    columns={
                        self._columns[e]:self._columns[group[0]]
                    },
                    inplace=True
                )
        
        for df in copy:
            for column in self._columns:
                if column not in df:
                    df[column] = np.nan 

        
        return copy

    def _group_to_sets(self, group):
        return [set(s) for s in group]

    def _score(self, **kwargs)->float:
        knps = [
            kwargs["knp{i}".format(i=i)] for i in range(self._metrics_number)
        ]

        weights = [
            kwargs["w{i}".format(i=i)] for i in range(self._metrics_number)
        ]
        
        other_groups, composed = column_alignment(
            self._tmp,
            len(self._dfs),
            knps,
            weights,
        )

        composed_sets = self._group_to_sets(composed)

        total = 0

        for other_group in other_groups:
            nan_percentage = np.mean([
                np.mean(pd.isna(df).values) for df in self._compose_dfs(other_group)
            ])
            total += (1-nan_percentage)
        return total

    def run(self):
        self._determine_metrics()
        pbounds = {
            "{p}{i}".format(p=p, i=i):(0,1) for p in ["knp", "w"] for i in range(self._metrics_number)
        }

        optimizer = BayesianOptimization(
            f=self._score,
            pbounds=pbounds,
            random_state=1,
        )

        optimizer.maximize(
            init_points=self._metrics_number,
            n_iter=3,
        )
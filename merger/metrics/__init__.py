from .non_parametric_statistical_tests import pairwise_kolmogorov_smirnov_test, pairwise_mann_whitney_u_test
from .custom import units
from .tfidf import columns_tfidf_cosine_distances, dataframes_tfidf_cosine_distances, vectorizer, corpora

METRICS_NUMBER = 5

__all__ = ['pairwise_kolmogorov_smirnov_test',
           'pairwise_mann_whitney_u_test', 'units', 'columns_tfidf_cosine_distances', 'dataframes_tfidf_cosine_distances', 'vectorizer', 'corpora', 'METRICS_NUMBER']

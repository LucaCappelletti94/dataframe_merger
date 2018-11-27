from .pairwise_test import pairwise_test
from scipy.stats import ks_2samp
import pandas as pd
import numpy as np


def pairwise_kolmogorov_smirnov_test(A: pd.DataFrame, B: pd.DataFrame)->np.ndarray:
    return pairwise_test(A, B, ks_2samp)

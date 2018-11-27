from .pairwise_test import pairwise_test
from scipy.stats import mannwhitneyu
import pandas as pd
import numpy as np


def pairwise_mann_whitney_u_test(A: pd.DataFrame, B: pd.DataFrame)->np.ndarray:
    return pairwise_test(A, B, mannwhitneyu)

import pandas as pd
from ..utils import compact, string
from typing import List


def dataframes_corpus(dfs: List[pd.DataFrame])->List[str]:
    return [v for df in dfs for c in compact(string(df)) for v in c]

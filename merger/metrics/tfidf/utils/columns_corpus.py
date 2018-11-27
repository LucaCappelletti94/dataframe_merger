import pandas as pd
from typing import List


def columns_corpus(dfs: List[pd.DataFrame])->List[str]:
    return [c for df in dfs for c in df]

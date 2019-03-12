from .columns_corpus import columns_corpus
from .dataframes_corpus import dataframes_corpus
import pandas as pd
from typing import List, Tuple


def corpora(dfs: List[pd.DataFrame])->Tuple[List[str], List[str]]:
    return columns_corpus(dfs), dataframes_corpus(dfs)

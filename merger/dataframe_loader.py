import pandas as pd
import os
from typing import List

def dataframe_loader(path:str)->List[pd.DataFrame]:
    """Return a list with all dataframes from given drectory in csv.
        path:str, directory from which to load the csv documents.
    """
    return [
        pd.read_csv("{path}/{file}".format(path=path, file=file), index_col=0, usecols=[0,1,2,3,4,5]) for file in os.listdir(path) if file.endswith(".csv")
    ]
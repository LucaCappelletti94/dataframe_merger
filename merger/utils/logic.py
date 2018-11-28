import numpy as np
from typing import List


def land(*args: List[np.ndarray])->np.ndarray:
    return np.all(args, axis=0)

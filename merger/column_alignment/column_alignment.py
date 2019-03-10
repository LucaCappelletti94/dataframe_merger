from subprocess import call, PIPE
from typing import List
import os

def strs(array:List[float])->List[str]:
    return [
        str(a) for a in array
    ]

def column_alignment(source:str, output:str, datasets:int, known_negatives_percentages:List[float], weights:List[float]):
    script =  "{script_dir}/cmake-build-release/column_alignment".format(script_dir=os.path.dirname(os.path.realpath(__file__)))
    metrics=len(known_negatives_percentages)
    call([" ".join([script, source, output, str(datasets), str(metrics), *strs(known_negatives_percentages), *strs(weights)])], shell=True)
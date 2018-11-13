import os
import numpy as np
import pandas as pd
import re
import json
import n2w
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_distances, euclidean_distances
from typing import List


def load_df(filename: str, path: str = "csv"):
    return pd.read_csv(
        "{path}/{filename}.csv".format(path=path, filename=filename),
        index_col="name")


with open("./fat classifier/fat_codes.json", "r", encoding="UTF8") as f:
    fats = json.load(f)
fat_keys = list(fats.keys())
fat_keys.sort(key=len, reverse=True)


def vitamin_heuristics(name: str)->str:
    return name.lower().replace("vitamina ", "vitamina_").replace("vit. ", "vitamina_")


def percentage_heuristics(name: str)->str:
    return name.replace("%", "percentuale")


def g_mg_heuristics(name: str)->str:
    name = name.replace("(", " ").replace(")", " ").replace("|", " ")
    name = name.replace("mg", "milligrammi").replace(
        " g ", "grammi").replace("mcg", "microgrammi")
    return re.sub(" g$", "grammi", name)


def fat_heuristic(name: str)->str:
    global fats, fat_keys

    for key in fat_keys:
        if key in name:
            name.replace(key, "{value} {key}".format(
                value=fats[key]["eng"], key=key))

    if ":" in name:
        name = re.sub(r"(C\d+:\d+)\s(\w)", r"\1_\2", name)
        for number in re.findall("\d+", name):
            name = name.replace(number, n2w.convert(int(number)))
        name = name.replace(":", "_")

    if "÷" in name:
        name = name.replace("÷", "rate")

    return name


def apply_heuristics(A: np.ndarray) -> np.ndarray:
    return np.array([fat_heuristic(g_mg_heuristics(percentage_heuristics(vitamin_heuristics(a)))) for a in A])


def match(A: pd.DataFrame, B: pd.DataFrame,
          threshold: float = 0.8) -> pd.DataFrame:
    Ac = A.columns
    Bc = B.columns
    a = np.nanmean(np.array(A), axis=0).reshape(-1, 1)
    b = np.nanmean(np.array(B), axis=0).reshape(-1, 1)
    Ae = apply_heuristics(Ac)
    Be = apply_heuristics(Bc)
    vectorizer = TfidfVectorizer()
    vectorizer.fit(np.concatenate([Ae, Be]))
    X = vectorizer.transform(Ae)
    Y = vectorizer.transform(Be)

    mean_matrix = euclidean_distances(a, b)
    tfidf_distances = euclidean_distances(X, Y)
    distances = (tfidf_distances / np.nanmax(tfidf_distances) +
                 0*mean_matrix / np.nanmax(mean_matrix))
    distances[distances > threshold] = np.inf
    #np.fill_diagonal(distances, np.inf)

    infinite_rows = np.all(distances == np.inf, axis=1)
    distances = distances[~infinite_rows]

    A1 = Ac[~infinite_rows]
    x_indices, y_indices = np.arange(A1.size), np.nanargmin(distances, axis=1)

    x, y = A1[x_indices], Bc[y_indices]

    df = pd.DataFrame({
        "Original": y,
        "Matched": x,
        "Values": np.nanmin(distances, axis=1)
    })

    df = df.sort_values("Values")

    return df


crea, bda, vn = load_df("crea"), load_df("bda"), load_df("valori_alimentari")


def replace_header(df, old, new, path):
    df[new] = df[old]
    df = df.drop(columns=[old])
    df.to_csv(path)
    return df


r = match(crea, bda, threshold=0.9)

for original, match, value in r.values:
    if original == match:
        continue
    while True:
        print(chr(27) + "[2J")
        inp = input("I found \033[1m{original}\033[0m and \033[1m{match}\033[0m. Should I merge them? [(y)/n] ".format(
            original=original, match=match))
        if inp == "y":
            done = False
            while True:
                h = int(input("Which header should I use? [1/2/n] "))
                if h == 1:
                    crea = replace_header(
                        crea, original, match, "csv/crea.csv")
                    done = True
                    break
                elif h == 2:
                    bda = replace_header(bda, match, original, "csv/bda.csv")
                    done = True
                    break
                elif h == "n":
                    break
                else:
                    print("What did you mean? Please retry.")
            if done:
                break
        elif inp == "n":
            print("Ok, leaving it be.")
            break
        else:
            print("What did you mean? Please retry.")

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


def matcher(A: pd.DataFrame, B: pd.DataFrame,
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
    # np.fill_diagonal(distances, np.inf)

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


df1, path_df1 = bda, "csv/bda.csv"
df2, path_df2 = crea, "csv/crea.csv"


while True:
    r = matcher(df1, df2, threshold=0.8)

    n = 0
    for original, match, value in r.values:
        if original == match:
            continue
        n += 1

    if not n:
        break

    print("I have found {n} possible matches. ".format(n=n))
    input("Press any key to continue...")
    for original, match, value in r.values:
        done = False
        if original == match:
            continue
        while True:
            print(chr(27) + "[2J")
            print("I found \033[1m{original}\033[0m and \033[1m{match}\033[0m. Should I merge them?".format(
                original=original, match=match))
            print("Their respective mean is: {mean_1:.5f}, {mean_2:.5f}".format(
                mean_1=np.nanmean(df1[original]),
                mean_2=np.nanmean(df2[match])
            ))
            inp = input("[(y)/n] ")
            if inp == "y":
                while True:
                    h = int(input("Which header should I use? [1/2/n] "))
                    if h == 1:
                        df1 = replace_header(
                            df1, original, match, path_df1)
                        done = True
                        break
                    elif h == 2:
                        df2 = replace_header(
                            df2, match, original, path_df2)
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
        if done:
            break

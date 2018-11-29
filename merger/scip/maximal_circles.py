from pyscipopt import Model, quicksum
import numpy as np


def maximal_circles_model(rewards: np.ndarray):
    model = Model("Maximal Circles")
    N = rewards.shape[1]
    x = {(i, j): model.addVar(vtype="B", name="x({i},{j})".format(i=i, j=j))
         for i in range(N) for j in range(N) if not np.isclose(rewards[i, j], 0)}

    for i, _ in x:
        model.addCons(quicksum(x[i, j]
                               for k, j in x if k == i) <= 1, "Unitary({i})".format(i=i))
        model.addCons(quicksum(x[i, j] - x[j, i]
                               for k, j in x if k == i) == 0, "Circularity({i})".format(i=i))
    model.setObjective(quicksum(x[i, j]*rewards[i, j]
                                for i, j in x), "maximize")
    model.data = x
    return model

from pyscipopt import Model, quicksum


def maximal_circles_model(rewards):
    model = Model("Maximal Circles")
    N = rewards.shape[1]
    x = {(i, j): model.addVar(vtype="B", name="x({i},{j})".format(i=i, j=j))
         for i in range(N) for j in range(N)}

    for i in range(N):
        model.addCons(quicksum(x[i, j]
                               for j in range(N)) <= 1, "Circularity({i})".format(i=i))
        model.addCons(quicksum(x[i, j]
                               for j in range(N)) == quicksum(x[j, i]
                                                              for j in range(N)), "Circularity({i})".format(i=i))

    model.addCons(quicksum(x[i, j] for i in range(N) for j in range(
        N) if rewards[i, j] == 0) == 0, "NoZeroRewards")
    model.addCons(quicksum(x[i, i] for i in range(N)) == 0, "Selfloops")

    model.setObjective(quicksum(x[i, j]*rewards[i, j]
                                for i in range(N)
                                for j in range(N)), "maximize")
    model.data = x
    return model

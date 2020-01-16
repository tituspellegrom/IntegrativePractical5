
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import gurobipy as gp
#import plotMap as pm
import classes

def run_day(company, day):
    print("####################################")
    print(f"RUNNING {company.name} for {day}")

    N = company.stores
    V = company.hub_and_stores
    A = [(i, j) for i in V for j in V if i != j]
    c_km = company.stores_km
    c_min = company.stores_min
    Q = company.truck_capacity
    q = {i: i.demand[day] for i in V}

    mdl = gp.Model("CVRP")

    x = mdl.addVars(A, vtype=gp.GRB.BINARY)
    u = mdl.addVars(V, vtype=gp.GRB.CONTINUOUS)

    mdl.modelSense = gp.GRB.MINIMIZE
    mdl.setObjective(company.cost_km * gp.quicksum(x[i, j] * c_km[i, j] for i, j in A) +  # km cost
                     company.cost_min * gp.quicksum(x[i, j] * c_min[i, j] for i, j in A) +  # travel cost
                     company.cost_min * company.UNLOADING_ROLL * gp.quicksum(  # unloading cost
        math.ceil(q[i] / (company.TOMATOES_PER_BOX * company.BOXES_PER_ROLL)) for i in N
    ) +
                     company.truck_cost * company.trucks +  # truck cost
                     company.roll_cost * math.ceil(sum([demand for demand in q.values()]) /  # storage cost
                                                   (company.TOMATOES_PER_BOX * company.BOXES_PER_ROLL)
                                                   )
                     )

    mdl.addConstrs(gp.quicksum(x[i, j] for j in V if j != i) == 1 for i in N);
    mdl.addConstrs(gp.quicksum(x[i, j] for i in V if i != j) == 1 for j in N);
   # mdl.addConstr(gp.quicksum(x[V[0], j] for j in N) == gp.quicksum(x[i, V[0]] for i in N));

    mdl.addConstrs((x[i, j] == 1) >> (u[i] + q[j] == u[j]) for i, j in A if i != V[0] and j != V[0]);
    mdl.addConstrs(u[i] >= q[i] for i in V);
    mdl.addConstrs(u[i] <= Q for i in V)

    mdl.Params.Timelimit = 80

    mdl.setParam(gp.GRB.Param.Cuts, 2)
    mdl.setParam(gp.GRB.Param.Heuristics, 1)

    mdl.optimize()

    active_arcs = [a for a in A if x[a].x > 0.99]
    for i, j in active_arcs:
        pass
        #print(f"{i}=>{j}")

    # pm.plotPoints(mData)
    # pm.plotLine(active_arcs, mData)

    if gp.GRB.OPTIMAL:
        return mdl.objVal
    else:
        return None


def run_company(company):
    total = 0

    for day in classes.Days:
        day_cost = run_day(company, day)
        total += day_cost

    return total




###########################################################
### start main
if __name__ == "__main__":
    main()

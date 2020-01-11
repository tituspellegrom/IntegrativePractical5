import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import gurobipy as gp

# eigen module
import data

def main():

    # Initialisation
    N = data.stores
    V = data.stores_and_hub
    A = data.stores_and_hub_edges
    km = data.stores_km
    min = data.stores_min

    ckm = data.COST_PER_KM
    cmin = data.COST_PER_MIN
    crpd  = data.COST_PER_TROLLEY
    ctr = data.COST_PER_TRUCK

    Q = data.TROLLEY_CAPACITY * data.BOXES_PER_TROLLEY * data.TOMATOES_PER_BOX
    q = data.stores_demand

    trips = tuple(f"Trip{i}" for i in range(100))
    print(q)

    # Output
    mdl = gp.Model("CVRP")

    x = mdl.addVars(trips, A, vtype=gp.GRB.BINARY)
    u = mdl.addVars(N, vtype=gp.GRB.CONTINUOUS)

    mdl.modelSense = gp.GRB.MINIMIZE

    mdl.setObjective(gp.quicksum(x[trip, i, j] * km[i, j] for i, j in A for trip in trips))

    mdl.addConstrs(gp.quicksum(x[trip, i, j] for trip in trips for j in N if j != i) == 1 for i in N);
    mdl.addConstrs(gp.quicksum(x[trip, i, j] for i, j in A if i == data.HUB and j != data.HUB) == 1 for trip in trips)

    mdl.addConstrs(gp.quicksum(x[trip, i, j] for i, j in A if j == store) ==
                   gp.quicksum(x[trip, i, j] for i, j in A if i == store)
                   for store in N for trip in trips)

    mdl.addConstrs(gp.quicksum( q[j] * x[trip, i, j] for i, j in A if i != j and j != data.HUB)
                   <= Q for trip in trips)

    # TODO: Add sub-tour eliminination contraint => means no cycles without the hub

    # TODO: add trip time constraint to fit in 24-hours with data.TRUCKS available



    # # Om model af te kappen
    # mdl.Params.MIPGap = 0.001
    # #mdl.Params.TimeLimit = 45
    mdl.optimize()

    # # zit vast de goede tussen
    # mdl.write("out.mps")
    # mdl.write("out.sol")
    # mdl.write("out.hnt")
    # mdl.write("out.prm")
    # mdl.write("out.attr")
    # mdl.write("out.json")



if __name__ == "__main__":
    main()

# literature: https://hrcak.srce.hr/file/285563


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import gurobipy as gp

# eigen module
import data
import math

def main():

    # Initialisation
    N = data.stores
    V = data.stores_and_hub
    A = data.stores_and_hub_edges
    km = data.stores_km
    time = data.stores_min

    ckm = data.COST_PER_KM
    cmin = data.COST_PER_MIN
    crpd  = data.COST_PER_TROLLEY
    ctr = data.COST_PER_TRUCK
    ult = data.UNLOAD_TIME_PER_TROLLEY

    Q = data.TROLLEY_CAPACITY * data.BOXES_PER_TROLLEY * data.TOMATOES_PER_BOX
    q = data.stores_demand

    trucks = tuple(f"truck{i}" for i in range(data.AMOUNT_OF_TRUCKS+1))
    trips = tuple(f"Trip{i}" for i in range(10))

    # Output
    mdl = gp.Model("CVRP")

    x = mdl.addVars(trucks, trips, A, vtype=gp.GRB.BINARY)

    mdl.modelSense = gp.GRB.MINIMIZE

    # TODO: set unloading cost
    mdl.setObjective(ckm * gp.quicksum(x[truck, trip, i, j] * km[i, j] for i, j in A for trip in trips for truck in trucks) +
                     cmin * gp.quicksum(x[truck, trip, i, j] * time[i, j] for i, j in A for trip in trips for truck in trucks) +
                     ctr * data.AMOUNT_OF_TRUCKS +
                     crpd * math.ceil(sum(demand for demand in q.values()) / (data.TOMATOES_PER_BOX * data.BOXES_PER_TROLLEY))
                     )


    # Every store is visited by a truck exactly once
    mdl.addConstrs(gp.quicksum(x[truck, trip, i, j] for trip in trips for truck in trucks for j in N if j != i) == 1
                   for i in N);

    # All trips start at the hub
    # TODO: Only equal to 1 when the trip is in fact not zero!!!  Empty trips should not leave and go back to hub!!
    mdl.addConstrs(gp.quicksum(x[truck, trip, i, j] for i, j in A if i == data.HUB and j != data.HUB) == 1
                   for trip in trips for truck in trucks )

    # all trips must end at the hub
    mdl.addConstrs(gp.quicksum(x[truck, trip, i, j] for i, j in A if j == store) ==
                   gp.quicksum(x[truck, trip, i, j] for i, j in A if i == store)
                   for store in N for trip in trips for truck in trucks)

    mdl.addConstrs(gp.quicksum( q[j] * x[truck, trip, i, j] for i, j in A if i != j and j != data.HUB)
                   <= Q for trip in trips for truck in trucks)

    # TODO: Add sub-tour eliminination contraint => means no cycles without the hub

    # Every truck's trips should sum up to less than 24 hours
    mdl.addConstrs(gp.quicksum(x[truck, trip, i, j] * time[i, j] for i, j in A if i != j for trip in trips ) <= 24*60 for truck in trucks)

    mdl.optimize()
    print('Obj: %g' % mdl.objVal)

    # # zit vast de goede tussen
    # mdl.write("out.mps")
    # mdl.write("out.sol")
    # mdl.write("out.hnt")
    # mdl.write("out.prm")
    # mdl.write("out.attr")
    # mdl.write("out.json")



if __name__ == "__main__":
    main()

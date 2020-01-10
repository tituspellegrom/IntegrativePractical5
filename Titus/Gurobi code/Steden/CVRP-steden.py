#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CVRP.py

Purpose:
    ...

Version:
    1       First start

Date:
    09/01/20

@author: rsl640
"""
###########################################################
### Imports

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import gurobipy as gp

# eigen module
import steden as titus_data

###########################################################
### main
def main():

    # Initialisation
    N = titus_data.cities
    #V = titus_data.cities_and_hub
    A = titus_data.city_edges
    km = titus_data.city_km
    min = titus_data.city_min
    ict = titus_data.in_city_time
    tr = titus_data.amount_of_trucks
    trcp = titus_data.truck_capacity
    ckm = titus_data.cost_per_km
    cmin = titus_data.cost_per_min
    crpd  = titus_data.cost_per_roll_per_day
    ctr = titus_data.cost_per_truck_per_day

    Q = tr*trcp*10*50        # tomato capacity
    q = titus_data.city_demand

    # Output
    mdl = gp.Model("CVRP")

    x = mdl.addVars(A, vtype=gp.GRB.BINARY)
    u = mdl.addVars(N, vtype=gp.GRB.CONTINUOUS)

    mdl.modelSense = gp.GRB.MINIMIZE

    mdl.setObjective(ckm * gp.quicksum(x[i, j] * km[i, j] for i, j in A) +            # kilometers
                     cmin * gp.quicksum(x[i, j] * min[i, j] for i, j in A) +          # between city travel time
                     cmin * gp.quicksum(len(d)*ict for d in q.values()) +             # in city travel time
                     crpd * gp.quicksum(u[i] for i in N) +                            # storage cost
                     ctr * tr                                                         # truck cost
                     )

    mdl.addConstrs(gp.quicksum(x[i, j] for j in N if j != i) == 1 for i in N);
    mdl.addConstrs(gp.quicksum(x[i, j] for i in N if i != j) == 1 for j in N);
    mdl.addConstrs((x[i, j] == 1) >> (u[i] + sum(q[i]) == u[j]) for i, j in A if i != titus_data.hub
                                                                                and j != titus_data.hub
                                                                                and i in q);    # Not all cities have
                                                                                                # branches with demand

    mdl.addConstrs(u[i] >= sum(q[i]) for i in N if i in q );    # cities with stores need >= demand unloaded
    mdl.addConstrs(u[i] == 0 for i in N if i not in q);         # cities without stores don't need unloading
    mdl.addConstrs(u[i] <= Q for i in N);

    # Om model af te kappen
    mdl.Params.MIPGap = 0.1
    #mdl.Params.TimeLimit = 45
    mdl.optimize()

    # zit vast de goede tussen
    mdl.write("out.mps")
    mdl.write("out.sol")
    mdl.write("out.hnt")
    mdl.write("out.prm")
    mdl.write("out.attr")
    mdl.write("out.json")

    # active_arcs = [a for a in A if x[a].x > 0.99]
    # print(active_arcs)
    #
    # plt.plot(xc[0], yc[0], c='r', marker='s')
    # plt.scatter(xc[1:], yc[1:], c='b')
    # for i, j in active_arcs:
    #     plt.plot([xc[i], xc[j]], [yc[i], yc[j]], c='g')
    # plt.show()


###########################################################
### start main
if __name__ == "__main__":
    main()

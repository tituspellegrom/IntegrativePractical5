
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import gurobipy as gp
import plotMapV2 as pm
import classes

###########################################################
     
def checkLoops(active_arcs):
    iNumberOfLoops = 0
    hub = active_arcs[0][0].branch_id
    vColors = ['b', 'g', 'r', 'c', 'm', 'y', 'b', 'g', 'r', 'c', 'm', 'y', 'b', 'g', 'r', 'c', 'm', 'y', 'b', 'g', 'r', 'c', 'm', 'y', 'b', 'g', 'r', 'c', 'm', 'y', 'b', 'g', 'r', 'c', 'm', 'y']
    
    for i in active_arcs:
        if i[0].branch_id == hub:
            iNumberOfLoops +=1
    
    for i in range(iNumberOfLoops):
        vLoop = [(active_arcs[i][0], active_arcs[i][1])]
        currentSearch = active_arcs[i][1]
        iSum = active_arcs[i][1].demand[classes.Days.maandag]
        for k in range(100):
            if currentSearch.branch_id == hub:
                    break
            for j in active_arcs:
                if j[0] == currentSearch:
                    vLoop.append((j[0], j[1]))
                    currentSearch = j[1]
                    iSum += j[1].demand[classes.Days.maandag]
                    break
                    
        pm.plotLine(vLoop, vColors[i])
        print(iSum)


def main():
    # Initialisation

    company = classes.AH
    N = company.stores
    V = company.hub_and_stores
    A = [(i,j) for i in V for j in V if i != j]
    c_km = company.stores_km
    c_min = company.stores_min
    Q = company.truck_capacity
    q = {i: i.demand[classes.Days.maandag] for i in V}

    mdl = gp.Model("CVRP")
    
    x = mdl.addVars(A, vtype=gp.GRB.BINARY)
    u = mdl.addVars(N, vtype=gp.GRB.CONTINUOUS)

    mdl.modelSense = gp.GRB.MINIMIZE
    mdl.setObjective(company.cost_km * gp.quicksum(x[i,j]*c_km[i,j] for i, j in A) +                # km cost
                     company.cost_min * gp.quicksum(x[i,j]*c_min[i,j] for i, j in A) +              # travel cost
                     company.cost_min * company.UNLOADING_ROLL * gp.quicksum(                       # unloading cost
                                    math.ceil(q[i] / (company.TOMATOES_PER_BOX * company.BOXES_PER_ROLL)) for i in N
                                                                            ) +
                     company.truck_cost * company.trucks +                                          # truck cost
                     company.roll_cost * math.ceil(sum([demand for demand in q.values()]) /             # storage cost
                                                   (company.TOMATOES_PER_BOX * company.BOXES_PER_ROLL)
                                                   )
                     )

    mdl.addConstrs(gp.quicksum(x[i,j] for j in V if j != i) == 1 for i in N);
    mdl.addConstrs(gp.quicksum(x[i,j] for i in V if i != j) == 1 for j in N);
    mdl.addConstrs((x[i,j] == 1) >> (u[i]+q[i] == u[j]) for i,j in A if i != V[0] and j != V[0]);
    mdl.addConstrs(u[i] >= q[i] for i in N);
    mdl.addConstrs(u[i] + q[i] <= Q for i in N)

    mdl.Params.Timelimit = 80
    mdl.setParam(gp.GRB.Param.Cuts, 2)
    mdl.setParam(gp.GRB.Param.Heuristics, 1)

    mdl.optimize()
    
    active_arcs = [a for a in A if x[a].x>0.99]
    '''
    for i, j in active_arcs:
        print(f"{i}=>{j}")
    '''  
    pm.plotPoints(classes.df_cities.values)
    checkLoops(active_arcs)

###########################################################
### start main
if __name__ == "__main__":
    main()

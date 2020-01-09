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

###########################################################
### main
def main():
    # Initialisation
    rnd = np.random
    rnd.seed(3)
    
    n = 10
    xc = rnd.rand(n+1)*200
    yc = rnd.rand(n+1)*200

    N = [i for i in range(1, n+1)]
    V = [0] + N
    A = [(i,j) for i in V for j in V if i!=j]
    c = {(i,j): np.hypot(xc[i]-xc[j], yc[i]-yc[j]) for i,j in A}
    Q = 20
    q = {i: rnd.randint(1,10) for i in N}
    
    # Output
    mdl = gp.Model("CVRP")
    
    x = mdl.addVars(A, vtype=gp.GRB.BINARY)
    u = mdl.addVars(N, vtype=gp.GRB.CONTINUOUS)
    
    mdl.modelSense = gp.GRB.MINIMIZE
    mdl.setObjective(gp.quicksum(x[i,j]*c[i,j] for i,j in A))
    
    mdl.addConstrs(gp.quicksum(x[i,j] for j in V if j!=i)==1 for i in N);
    mdl.addConstrs(gp.quicksum(x[i,j] for i in V if i!=j)==1 for j in N);
    mdl.addConstrs((x[i,j]==1) >> (u[i]+q[i]==u[j]) for i,j in A if i!=0 and j!=0);
    mdl.addConstrs(u[i]>=q[i] for i in N);
    mdl.addConstrs(u[i]<=Q for i in N);
    
    mdl.optimize()
    
    active_arcs = [a for a in A if x[a].x>0.99]
    print(active_arcs)
    
    plt.plot(xc[0], yc[0], c='r', marker='s')
    plt.scatter(xc[1:], yc[1:], c='b')
    for i,j in active_arcs:
        plt.plot([xc[i], xc[j]], [yc[i], yc[j]], c='g')
    plt.show()
    
###########################################################
### start main
if __name__ == "__main__":
    main()

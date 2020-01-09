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
def readData():
    sData = "TestDATA.xlsx"
    dData = pd.read_excel(sData)
    mData = dData.values
    return mData

def readDataCosts():
    sData = "TestDATACosts.xlsx"
    dData = pd.read_excel(sData)
    mData = dData.values
    return mData

def main():
    # Initialisation
    mData = readData()
    mDataCosts = readDataCosts()
    #print(np.size(mDataCosts))
    
    #print(n)
    N = mData[1:,0]
    #print(N)
    V = [0]
    V = np.append(V, N)
    #print(V)
    A = [(i,j) for i in V for j in V if i!=j]
    #print(A)
    c = {(i,j): mDataCosts[i][j] for i,j in A}
    #print(c)
    Q = 10000
    q = {i: mData[i, 2] for i in N}
    #print(q)
    
    
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
    #print(mData[active_arcs[i][0]][1])
    
    for i in range(6):
        print(mData[active_arcs[i][0]][1], "->", mData[active_arcs[i][1]][1])
    
    
    
###########################################################
### start main
if __name__ == "__main__":
    main()

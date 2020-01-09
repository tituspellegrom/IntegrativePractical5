import pandas as pd
import gurobipy as gp


def generate_arcs(nodes, matrix):
    dict = {}

    rows = matrix.shape[0]
    columns = matrix.shape[1]

    for i in range(rows):
        for j in range(columns):
            if i == j:
                continue

            names = (nodes[i], nodes[j])
            arc_val = matrix.iloc[i, j]

            if not arc_val:
                arc_val = matrix.iloc[j, i]

            dict[names] = arc_val
    return dict


demand = pd.read_excel('AH-maandag-1store.xlsx')
distance = pd.read_excel('km.xlsx')
distance = distance.where((pd.notnull(distance)), None)

#cost_per_km = 0.8

hub_location = "Nijmegen"
locations = distance.iloc[:, 0].tolist()
distance = distance.iloc[:, 1:]

arcs, km = gp.multidict(generate_arcs(locations, distance))
arcs = gp.tuplelist(arcs)

inflow = {}
for index, row in demand.iterrows():
    inflow[row[0]] = -row.iloc[1]
inflow[hub_location] = sum(demand.iloc[:, 1])

m = gp.Model('netflow')


flow = {}
for i, j in arcs:
    flow[i, j] = m.addVar(obj=min[i, j], name=f"flow {i}_{j}")

m.update()




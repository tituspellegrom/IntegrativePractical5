# literature: https://hrcak.srce.hr/file/285563

import pandas as pd
import gurobipy as gp
from itertools import chain, combinations
# eigen module
import data
import DFS


def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(1,len(s)+1))


def main():

    # Initialisation
    N = data.stores
    #S = powerset(N)
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

    ### TEST
    test_q = q.copy()
    test_q[data.HUB] = 0
    print(test_q)

    trucks = tuple(f"truck{i}" for i in range(data.AMOUNT_OF_TRUCKS+1))
    trips = tuple(f"Trip{i}" for i in range(3))

    # Output
    mdl = gp.Model("CVRP")

    x = mdl.addVars(trucks, trips, A, vtype=gp.GRB.BINARY)
    y = mdl.addVars(trucks, trips, V, vtype=gp.GRB.CONTINUOUS)
    print(y)
    print(x)

    mdl.update()
    mdl.modelSense = gp.GRB.MINIMIZE

    # TODO: set unloading cost
    mdl.setObjective(ckm * gp.quicksum(x[truck, trip, i, j] * km[i, j] for i, j in A for trip in trips for truck in trucks) +
                     cmin * gp.quicksum(x[truck, trip, i, j] * time[i, j] for i, j in A for trip in trips for truck in trucks)
                    # ctr * data.AMOUNT_OF_TRUCKS +
                    # crpd * math.ceil(sum(demand for demand in q.values()) / (data.TOMATOES_PER_BOX * data.BOXES_PER_TROLLEY)) +
                    # 1000 * gp.quicksum([DFS.count_cycles(DFS.reduce_graph([(i, j) for i, j in A if gp.x[truck, trip, i, j] == 1]),
                    #                                         [(i, j) for i, j in A if x[truck, trip, i, j].X == 1]
                    #                                     ) - 1 ] for trip in trips for truck in trucks)

                    )

    # EVERY STORE VISITED ONLY ONCE
    mdl.addConstrs(gp.quicksum(x[truck, trip, i, j] for trip in trips for truck in trucks for j in N if j != i) == 1
                   for i in N);

    # 1 TIME LEAVING HUB
    mdl.addConstrs(gp.quicksum(x[truck, trip, i, j] for i, j in A if i == data.HUB and j != data.HUB) == 1
                   for trip in trips for truck in trucks)

    # EVERY NODE 1 TRUCK GOING IN => 1 GOING OUT
    mdl.addConstrs(gp.quicksum(x[truck, trip, i, j] for i, j in A if j == store) ==
                   gp.quicksum(x[truck, trip, i, j] for i, j in A if i == store)
                   for store in V for trip in trips for truck in trucks)

    # ROUTE CAPACITY
    mdl.addConstrs(gp.quicksum( q[j] * x[truck, trip, i, j] for i, j in A if i != j and j != data.HUB)
                   <= Q for trip in trips for truck in trucks)

    ### 2e Paper
    #mdl.addConstrs(test_q[v] <= y[truck, trip, v[0], v[1]] for v in V for trip in trips for truck in trucks)
    #mdl.addConstrs(y[truck, trip, v[0], v[1]] <= Q for v in V for trip in trips for truck in trucks)
    #mdl.addConstrs(y[truck, trip, j[0], j[1]] >= y[truck, trip, i[0], i[1]] + test_q[j]*x[truck, trip, i, j] - Q * (1 - x[truck, trip, i, j]) for i in V for j in V if i!=j or (i==j and i==data.HUB) for trip in trips for truck in trucks)


    #mdl.addConstrs([] for i, j in A)
    # mdl.addConstrs(DFS.count_cycles(DFS.reduce_graph([(i, j) for i, j in A if x[truck, trip, i, j].x == 1]),
    #                                 [(i, j) for i, j in A if x[truck, trip, i, j].x == 1]
    #                                 )
    #                 == 1 for trip in trips for truck in trucks)

    # TIME CONSTRAINT
    mdl.addConstrs(gp.quicksum(x[truck, trip, i, j] * time[i, j] for i, j in A for trip in trips) <= 24*60 for truck in trucks)

    mdl.optimize()

    ###########################################
    ## OUTPUT #################################
    mdl.write("out.mps")
    mdl.write("out.sol")
    mdl.write("out.hnt")
    mdl.write("out.prm")
    mdl.write("out.attr")
    mdl.write("out.json")

    dict_ = {}

    if mdl.status == gp.GRB.OPTIMAL:
        for truck in trucks:
            for trip in trips:
                edges = [(i, j) for i, j in A if x[truck, trip, i, j].X == 1]
                graph = DFS.reduce_graph(edges)
                print(f"Edges: {edges}")
                print(f"We count {DFS.count_cycles(graph, edges)} cycles")
                for i, j in A:
                    if x[truck, trip, i, j].X > 0:
                        dict_[(truck, trip, i, j)] = x[truck, trip, i, j].X

    output = pd.DataFrame([[key[0], key[1], key[2][0], key[2][1], key[3][0], key[3][1], value] for key, value, in dict_.items()],
                          columns=["Truck" , "Trip", "From City", "From Branch", "To City", "To Branch", "CheckValue"])
    output.to_excel("Trips.xlsx")


if __name__ == "__main__":
    main()

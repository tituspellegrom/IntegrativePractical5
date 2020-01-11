import pandas as pd
import gurobipy as gp


def create_city_demand(cities, demand):
    city_demand = {}

    for index, row in demand.iterrows():
        city, demands = row[0], row[1:]


        if city not in cities:
            raise ReferenceError("De opgegeven winkelstad bestaat niet in het netwerk!")

        city_demand[city] = sum([round(demand) for demand in demands if demand is not None])

    return city_demand


def create_edge_dict(nodes, matrix):
    dict = {}

    rows = matrix.shape[0]
    columns = matrix.shape[1]

    for i in range(rows):
        for j in range(columns):
            if i == j:
                continue

            names = (nodes[i], nodes[j])
            edge_val = matrix.iloc[i, j]

            if edge_val is None:
                edge_val = matrix.iloc[j, i]

            dict[names] = edge_val
    return dict



hub = "Nijmegen"
in_city_time = 5
amount_of_trucks = 5
truck_capacity = 36
cost_per_km = 0.8
cost_per_min = 10/60
cost_per_roll_per_day = 5.8
cost_per_truck_per_day = 110


df_demand = pd.read_excel('AH-Maandag.xlsx', header=None)
df_demand = df_demand.where((pd.notnull(df_demand)), None)
df_km = pd.read_excel('km.xlsx')
df_km = df_km.where((pd.notnull(df_km)), None)
df_min = pd.read_excel('min.xlsx')
df_min = df_min.where((pd.notnull(df_min)), None)

cities, df_cities_km = list(df_km.iloc[:, 0]),  df_km.iloc[:, 1:]
df_cities_min = df_min.iloc[:, 1:]

city_demand = create_city_demand(cities, df_demand)

city_km = create_edge_dict(cities, df_cities_km)
city_min = create_edge_dict(cities, df_cities_min)

city_edges = [*city_km.keys()]


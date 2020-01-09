import pandas as pd
import gurobipy as gp


def create_stores_demand(cities, demand):
    stores_demand = {}

    for index, row in demand.iterrows():
        city, demands = row[0], row[1:]

        if city not in cities:
            raise ReferenceError("De opgegeven winkelstad bestaat niet in het netwerk!")

        for i, demand in enumerate(demands):
            if demand and demand > 0:
                store = (city, i)
                stores_demand[store] = demand

    return stores_demand


def create_edge_dict(nodes, matrix):
    dict = {}

    rows = matrix.shape[0]
    columns = matrix.shape[1]

    for i in range(rows):
        for j in range(columns):

            names = (nodes[i], nodes[j])
            edge_val = matrix.iloc[i, j]

            if edge_val is None:
                edge_val = matrix.iloc[j, i]

            dict[names] = edge_val
    return dict


def create_store_edges(stores, city_matrix, same_city_value=0):
    stores_edges = {}

    for store1 in stores:
        for store2 in stores:
            store1_city, store1_branch = store1[0], store1[1]
            store2_city, store2_branch = store2[0], store2[1]

            if store1_city == store2_city:
                # Enforce edge to itself = 0
                if store1_branch == store2_branch:
                    edge_value = 0
                else:
                    edge_value = same_city_value

            else:
                edge_value = city_matrix[(store1_city, store2_city)]

            stores_edges[(store1, store2)] = edge_value

    return stores_edges


hub = ("Nijmegen", 'hub')

df_demand = pd.read_excel('AH-Maandag.xlsx', header=None)
df_demand = df_demand.where((pd.notnull(df_demand)), None)
df_km = pd.read_excel('km.xlsx')
df_km = df_km.where((pd.notnull(df_km)), None)
df_min = pd.read_excel('min.xlsx')
df_min = df_min.where((pd.notnull(df_min)), None)

cities, df_cities_km = list(df_km.iloc[:, 0]),  df_km.iloc[:, 1:]
df_cities_min = df_min.iloc[:, 1:]

stores_demand = create_stores_demand(cities, df_demand)
stores = [*stores_demand.keys()]

# Meant to differentiate the hub from stores
stores_and_hub = (*stores, hub)

cities_km = create_edge_dict(cities, df_cities_km)
stores_km = create_store_edges(stores_and_hub, cities_km, same_city_value=0)      # same_city stores  => 0 km apart

cities_min = create_edge_dict(cities, df_cities_min)
stores_min = create_store_edges(stores_and_hub, cities_min, same_city_value=5)    # same_city stores => 5 min apart

stores_edges = [*stores_km.keys()]

#print(stores)
#print(stores_edges)
#print(stores_demand)
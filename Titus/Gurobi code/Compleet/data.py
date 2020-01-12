import pandas as pd


def create_stores_demand(demand):
    stores_demand = {}

    # Keep track of cities where no store is present
    # Used to still include those cities as possible route nodes
    #cities_named = { city : False for city in CITIES}


    for index, row in demand.iterrows():
        city, demands = row[0], row[1:]

        if city not in CITIES:
            raise ReferenceError("De opgegeven winkelstad bestaat niet in het netwerk!")

        for i, demand in enumerate(demands):
            if demand and demand > 0:
                store = (city, i)
                stores_demand[store] = round(demand)

                #cities_named[city] = True

    # for city, named in cities_named.items():
    #     if named is False:
    #         fake_store = (city, 0)
    #         stores_demand[fake_store] = 0
    #         print(city)

    return stores_demand


def create_edge_dict(nodes, matrix):
    dict = {}

    rows = matrix.shape[0]
    columns = matrix.shape[1]

    if rows != columns:
        raise ValueError("Matrix must be symmetric")

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


def create_store_edges(stores, city_matrix, same_city_value=0):
    stores_edges = {}

    for store1 in stores:
        for store2 in stores:
            store1_city, store1_branch = store1[0], store1[1]
            store2_city, store2_branch = store2[0], store2[1]

            if store1_city == store2_city:
                # Ignore edge to itself
                if store1_branch == store2_branch:
                    if store1_branch == 'hub':
                        edge_value = 0
                    else:
                        continue
                else:
                    edge_value = same_city_value

            else:
                edge_value = city_matrix[(store1_city, store2_city)]

            stores_edges[(store1, store2)] = edge_value

    return stores_edges


CITIES = ['Alkmaar ', 'Amersfort', 'Amsterdam', 'Apeldoorn', 'Arnhem', 'Breda', 'Delft', 'Den Helder', 'Dordrecht',
          'Ede', 'Eindhoven', 'Enkhuizen', 'Gouda', 'Haarlem', 'Heerhugowaard', 'Hoorn', 'Huizen', 'Leiden',
          'Medemblik', 'Nieuwegein', 'Nijmegen', 'Oss', 'Rotterdam', 'Schagen', "'s-Hertogenbosch", 'The Hague',
          'Tilburg', 'Utrecht', 'Wageningen', 'Zaandam']

HUB = ('Nijmegen', 'hub')

IN_CITY_TIME = 5
AMOUNT_OF_TRUCKS = 5
TROLLEY_CAPACITY = 36
COST_PER_KM = 0.8
COST_PER_MIN = 10/60
COST_PER_TROLLEY = 5.8
COST_PER_TRUCK = 110
UNLOAD_TIME_PER_TROLLEY = 1.4
TOMATOES_PER_BOX = 50
BOXES_PER_TROLLEY = 10

# imports
df_demand = pd.read_excel('AH-Maandag.xlsx', header=None)
df_demand = df_demand.where((pd.notnull(df_demand)), None)
df_km = pd.read_excel('km.xlsx')
df_km = df_km.where((pd.notnull(df_km)), None)
df_min = pd.read_excel('min.xlsx')
df_min = df_min.where((pd.notnull(df_min)), None)

df_cities_km = df_km.iloc[:, 1:]
df_cities_min = df_min.iloc[:, 1:]

stores_demand = create_stores_demand(df_demand)
stores = [*stores_demand.keys()]

# Meant to differentiate the hub from stores
stores_and_hub = (*stores, HUB)

cities_km = create_edge_dict(CITIES, df_cities_km)
stores_km = create_store_edges(stores_and_hub, cities_km, same_city_value=0)      # same_city stores  => 0 km apart

cities_min = create_edge_dict(CITIES, df_cities_min)
stores_min = create_store_edges(stores_and_hub, cities_min, same_city_value=5)    # same_city stores => 5 min apart

stores_and_hub_edges = [*stores_min.keys()]

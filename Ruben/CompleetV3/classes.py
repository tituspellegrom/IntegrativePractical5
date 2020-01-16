from aenum import UniqueEnum, extend_enum
import pandas as pd


def create_cities(df_cities):
    for index, row in df_cities.iterrows():
        extend_enum(Cities, row['Name'].strip(), row['Name'], row['Longitude'], row['Latitude'])


def create_edge_dict(cities, matrix):
    dict = {}

    rows = matrix.shape[0]
    columns = matrix.shape[1]

    if rows != columns:
        raise ValueError("Matrix must be symmetric")

    for i in range(rows):
        for j in range(columns):

            if i == j:
                continue

            edge_val = matrix.iloc[i, j] or matrix.iloc[j, i]

            city1 = Cities.get_city(cities[i])
            city2 = Cities.get_city(cities[j])
            dict[city1, city2] = edge_val
    return dict


def create_store_edges(stores, city_dictionary, same_city_value=0):
    stores_edges = {}

    for store1 in stores:
        for store2 in stores:

            if store1.city == store2.city:
                # Ignore edge to itself
                if store1.branch_id == store2.branch_id:
                    if store1.branch_id == 'hub':
                        edge_value = 0
                    else:
                        continue
                else:
                    edge_value = same_city_value

            else:
                edge_value = city_dictionary[store1.city, store2.city]

            stores_edges[store1, store2] = edge_value

    return stores_edges


class Cities(UniqueEnum):
    _init_ = 'string longitude latitude'

    def __str__(self):
        return self.string

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'{self.value!r}, {self.string!r})')

    @classmethod
    def get_city(cls, string):
        for c in cls:
            if c.string == string:
                return c


class Days(UniqueEnum):
    _init_ = 'value, string'

    maandag = 0, 'Maandag'
    dinsdag = 1, 'Dinsdag'
    woensdag = 2, 'Woensdag'
    donderdag = 3, 'Donderdag'
    vrijdag = 4, 'Vrijdag'
    zaterdag = 5, 'Zaterdag'

    def __str__(self):
        return self.string

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'{self.value!r}, {self.string!r})')


class Company:

    UNLOADING_ROLL = 1.4
    TOMATOES_PER_BOX = 50
    BOXES_PER_ROLL = 10
    IN_CITY_TIME = 5
    IN_CITY_DISTANCE = 0

    def __init__(self, name, roll_capacity, truck_cost, cost_km, cost_hour, roll_cost, trucks, hub):
        self.name = name
        self.roll_capacity = roll_capacity
        self.truck_cost = truck_cost
        self.cost_km = cost_km
        self.cost_min = cost_hour / 60
        self.roll_cost = roll_cost
        self.trucks = trucks
        self.hub_city = hub
        self.create_stores()
        self.hub_store = Store(self, hub, 'hub')
        for day in Days:
            self.hub_store.add_demand(day, 0)
        self.load_demand()
        self.hub_and_stores = [self.hub_store] + self.stores

    @property
    def truck_capacity(self):
        return self.TOMATOES_PER_BOX * self.BOXES_PER_ROLL * self.roll_capacity

    def load_demand_day(self, day):
        df_demand = pd.read_excel(f"{INPUT_FOLDER}/{self.name}-{day}.xlsx", header=None)
        df_demand = df_demand.where((pd.notnull(df_demand)), None)
        return df_demand

    def create_stores(self):
        self.stores = []
        df_demand = self.load_demand_day(Days.maandag)
        for index, row in df_demand.iterrows():
            city = Cities.get_city(row[0])

            for i in range(5):
                if row[i+1]:
                    self.stores.append(Store(self, city, i))

    def load_demand(self):
        for day in Days:
            df_demand = self.load_demand_day(day)
            for index, row in df_demand.iterrows():
                city = Cities.get_city(row[0])
                for i in range(5):
                    branch_demand = row[i+1]
                    if branch_demand:
                        store = self.lookup_store(city, i)
                        store.add_demand(day, branch_demand)

    def lookup_store(self, city, branch_id):
        for store in self.stores:
            if store.city == city and store.branch_id == branch_id:
                return store
        raise LookupError(f"Could not find {city} {branch_id} in stores")

    @property
    def stores_km(self):
        return create_store_edges(self.hub_and_stores, cities_km, same_city_value=0)

    @property
    def stores_min(self):
        return create_store_edges(self.hub_and_stores, cities_min, same_city_value=5)

    def __str__(self):
        return f"{self.name}"


class Store:

    def __init__(self, company, city, branch_id):
        self.company = company
        self.city = city
        self.branch_id = branch_id
        self.demand = {}

    def add_demand(self, day, demand):
        self.demand[day] = demand

    def __str__(self):
        return f"{self.company.name}_{self.city}_{self.branch_id}"

    def __hash__(self):
        return hash(str(self))


INPUT_FOLDER = 'Input/'

df_cities = pd.read_excel(INPUT_FOLDER+'cities.xlsx')
df_km = pd.read_excel(INPUT_FOLDER+'km.xlsx')
df_km = df_km.where((pd.notnull(df_km)), None)
df_min = pd.read_excel(INPUT_FOLDER+'min.xlsx')
df_min = df_min.where((pd.notnull(df_min)), None)

create_cities(df_cities)
cities_km = create_edge_dict(df_km.iloc[:, 0], df_km.iloc[:, 1:])
cities_min = create_edge_dict(df_min.iloc[:, 0], df_min.iloc[:, 1:])

AH = Company("AH", 36, 110, 0.8, 10, 5.8, 5, Cities.Nijmegen)

#J = Company("J", 30, 105, 1, 9.9, 6, 4, Cities.Tilburg)
#K = Company("K", 28, 107, 0.7, 10.1, 5.6, 5, Cities.Haarlem)
#FFL = Company("FFL", 40, 110, 0.9, 9.5, 5, 15, Cities.Huizen)



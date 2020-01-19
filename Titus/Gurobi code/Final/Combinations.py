import classes
import CVRP
import copy
from itertools import chain, combinations
import pandas as pd

def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(1,len(s)+1))


clients = [classes.AH, classes.J, classes.K]
combos = powerset(clients)
cost = {}

for combo in combos:
    shell = copy.deepcopy(classes.FFL)

    for company in combo:
        shell.stores.extend([store for store in company.stores])
    combo_cost = CVRP.run_company(shell)
    key = "+".join([str(company) for company in combo])
    cost[key] = combo_cost

print(cost)
cost_df = pd.DataFrame.from_dict(cost, orient='index')
cost_df.to_excel("costs.xlsx")



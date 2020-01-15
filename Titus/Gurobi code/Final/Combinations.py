import classes
import CVRP
import copy
from itertools import chain, combinations

def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(1,len(s)+1))


clients = [classes.AH, classes.J, classes.K]
combos = powerset(clients)

for combo in combos:
    shell = copy.deep(classes.FFL)
    print([company.name for company in combo])





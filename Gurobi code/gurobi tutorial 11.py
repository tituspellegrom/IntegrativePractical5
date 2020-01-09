
# see objective value
model.ObjVal

# display decision variables
model.printAttr('X')

# read a model from a file
read()

# Gurobi needs:
# parameters => for algorithm (max time duration etc)
# Attributes => data input
# Environment => has global settings (created automatically in python)

# parameters
setParam()

# Primary
Model #the model
Var # a variable
Constr # a constraint

Model.setObjective(expression) # set the objective function

# Workflow
# create all variable objects
# set objective function
# create constraints
# run optimization

# linear AND quadratic are supported by guropy


# use QuickSum build gurobi instead of sum() in python
# MUCH faster
obj = quicksum(cost[a]*x[a] for a in arcs)

# voorbeeld
# voor alle i constraints => the som van alle X[i,j] <= 5
for i in I:
    m.addConstr(quicksum(x[i,j] for j in J) <=5)

# Nog sneller:
m.addConstr((x.sum(i,'*') <= 5) for i in I)

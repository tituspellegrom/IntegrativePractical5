import gurobipy

nodes = ['Alkmaar', 'Amersfoort', 'Amsterdam']

print(nodes)

arcs, min = gurobipy.multidict({
    ('Alkmaar', 'Amersfoort') : 70,
    ('Amersfoort', 'Alkmaar') : 70,
    ('Alkmaar' , 'Amsterdam') : 43,
    ('Amsterdam' , 'Alkmaar') : 43,
    ('Amersfoort', 'Amsterdam') : 49,
    ( 'Amsterdam', 'Amersfoort') : 49,
})


arcs = gurobipy.tuplelist(arcs)
print(arcs)
print(min)

inflow = {
    'Alkmaar' : -50,
    'Amersfoort' : -50,
    'Amsterdam' : 100,
}

m = gurobipy.Model('netflow')

flow = {}
for i, j in arcs:
    flow[i, j] = m.addVar(obj=min[i, j], name=f"flow {i}_{j}")

m.update()

for j in nodes:
        m.addConstr(
          gurobipy.quicksum(flow[i,j] for i,j in arcs.select('*',j)) +
              inflow[j] ==
          gurobipy.quicksum(flow[j,k] for j,k in arcs.select(j,'*')),
                   'node_%s' % (j))

m.optimize()

# Print solution
if m.status == gurobipy.GRB.status.OPTIMAL:
    solution = m.getAttr('x', flow)
    for i,j in arcs:
        if solution[i,j] > 0:
            print('%s -> %s: %g' % (i, j, solution[i,j]))


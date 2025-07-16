import pulp

transport_prob = pulp.LpProblem('Transport_Problem', pulp.LpMinimize)

costs = {
    ('Warehouse1', 'Store1'): 4,
    ('Warehouse1', 'Store2'): 6,
    ('Warehouse1', 'Store3'): 8,
    ('Warehouse2', 'Store1'): 2,
    ('Warehouse2', 'Store2'): 4,
    ('Warehouse2', 'Store3'): 5
}

supply = {
    'Warehouse1': 100,
    'Warehouse2': 150
}

demand = {
    'Store1': 80,
    'Store2': 70,
    'Store3': 100
}

x = pulp.LpVariable.dicts("Transport", costs.keys(), lowBound=0, cat='Integer')

transport_prob += pulp.lpSum(costs[i, j] * x[i, j] for i, j in costs), "Total_Transportation_Cost"

for w in supply:
    transport_prob += pulp.lpSum(x[w, s] for s in demand if (w, s) in x) <= supply[w], f"Supply_Constraint_{w}"

for s in demand:
    transport_prob += pulp.lpSum(x[w, s] for w in supply if (w, s) in x) >= demand[s], f"Demand_Constraint_{s}"

transport_prob.solve()

print("Transportation Plan:")
for v in transport_prob.variables():
    print(f"{v.name} = {v.varValue}")

print(f"Total Transportation Cost = {pulp.value(transport_prob.objective)}")

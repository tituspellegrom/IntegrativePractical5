# create adjacency matrix of the graph given.

# maintain a counter num_of_connected_components to store the number of cycles in the graph.]

# maintain an array of boolean(ARR) to store traversal status of vertices of the graph. TRUE-traversed, FALSE- untraversed.

# start DFS from any vertex V whose ARR value is false(not yet traversed) and
# maintain temporary list of vertices traversed for V and if you encounter the same vertex V again in DFS then that means its a cycle
# and then make all the entries true in the boolean array ARR for the vertices present in the temporary list
# (the reason we need to make all entries of vertices present in the list to true in ARR is
# that we have already encountered a loop which contains these vertices and need not perform DFS on them) and increment the counter num_of_connected_components by 1.

# Repeat steps 3-4 till there is no vertices left untraversed.

import data as data

def neighbors(node, A):
    neighbors = []
    for i, j in A:
        if i == node:
            neighbors.append(j)

    return neighbors


def DFS(node, A, visited=None):
    if visited is None:
        del visited
        visited = []

    for n in neighbors(node, A):
        if n in visited:
            return visited
        visited.append(n)
        return DFS(n, A, visited)


def not_analysed(analysed):
    return [n for n, value in analysed.items() if value is False]


def count_cycles(N, A):
    analysed = {node: False for node in N}
    print(analysed)
    cycles = []

    while len(not_analysed(analysed)) > 0:
        to_analyse = not_analysed(analysed)

        visited = DFS(to_analyse[0], A)
        if visited:
            cycles.append(visited)
            for n in visited:
                analysed[n] = True

    return len(cycles)


def reduce_graph(edges):
    # Removes all nodes with degree == 0
    list_ = []
    for i, j in edges:
        if i not in list_:
            list_.append(i)
        if j not in list_:
            list_.append(j)

    return list_


cycles = count_cycles(reduce_graph(data.example_trip), data.example_trip)
print(cycles)




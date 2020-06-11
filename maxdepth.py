from math import inf


ramos = {"a", "b", "c", "d", "e", "f", "g"}

# ramo: prerequisitos de este
prerreq = {
    "a": ["b"],
    "b": ["c", "g"],
    "c": ["d"],
    "d": [],
    "e": ["f", "d"],
    "f": ["g"],
    "g": []
}


# Crea alpha'[u] -> todos los nodos v que tienen como requisito a u
# Acá es O(V + E) pero en issues se dice que se considere O(E)
succs = {ramo: set() for ramo in ramos}
for key, value in prerreq.items():
    for v in value:
        succs[v].add(key)


# DFS con tiempos. La closed list representa el orden topológico
def dfsVisit(u, time, visited, closed):
    visited.add(u)
    time += 1
    for succ in succs[u]:
        if succ not in visited:
            time = dfsVisit(succ, time, visited, closed)
    closed.insert(0, u)
    time += 1
    return time


# Visto en clases, itera una vez sobre cada vertice y arista, por lo que es O(V+E)
def toposort():
    time = 1
    visited = set()
    closed = []
    for u in ramos:
        if u not in visited:
            time = dfsVisit(u, time, visited, closed)
    return closed


if __name__ == "__main__":

    L = toposort()
    # Le asignamos semestre 1 a los nodos sin prerequisitos y -infinito al resto
    # O(V)
    semestre = {}
    for u in L:
        if prerreq[u]:
            semestre[u] = -inf
        else:
            semestre[u] = 1

    # Para cada vertice (en el orden topológico) recorro todas sus aristas y
    # acualizo el semestre en el que deberían estar -> O(E + V)
    for u in L:
        for v in succs[u]:
            if semestre[v] < semestre[u] + 1:
                semestre[v] = semestre[u] + 1

    # for u, d in dist.items():
    #     print(f"El curso {u} debe tomarse el semestre {d}")

    # Damos el formato pedido O(V)
    output = {}
    for u, s in semestre.items():
        if s not in output:
            output[s] = set()
        output[s].add(u)

    # Imprimimos O(V)
    for sem, cursos in output.items():
        print(f"Semestre {sem}:", cursos)

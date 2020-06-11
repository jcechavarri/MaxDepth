"""
Notar que las complejidades de cada paso son distintas a las mencionadas en el
informe por simplicidad de implementación (Me era más facil iterar de nuevo que
guardar otro parámetro). Aún así la complejidad final del algoritmo es la misma.

:)

"""


class Node:

    def __init__(self, value):
        self.value = value
        self.rep = None
        # alpha[u]
        self.pred = []
        # alpha'[u]
        self.succ = []
        self.color = None
        self.start_time = None
        self.end_time = None

    def assign(self, rep):
        if self.rep == None:
            self.rep = rep
            for v in self.pred:
                v.assign(rep)

    def kosaraju(self, nodes):
        L = self.topoSort(nodes)
        for u in L:
            u.assign(u)

        cfc = {}
        for u in L:
            val = u.rep.value
            if val not in cfc:
                cfc[val] = set()
            cfc[val].add(u.value)
        return cfc

    def dfsVisit(self, time, L):
        self.color = "gray"
        self.start_time = time
        time += 1
        for v in self.succ:
            if v.color == "white":
                time = v.dfsVisit(time, L)
        self.color = "black"
        self.end_time = time
        L.insert(0, self)
        time += 1
        return time

    @staticmethod
    def dfs(nodes, L):
        time = 1
        for u in nodes:
            u.color = "white"
        for u in nodes:
            if u.color == "white":
                time = u.dfsVisit(time, L)

    def topoSort(self, nodes):
        L = []
        self.dfs(nodes, L)
        return L

    def __repr__(self):
        return f"Node {self.value}"


if __name__ == "__main__":

    # values of nodes
    V = {"a", "b", "c", "d", "e", "f", "g"}

    # node: predecesors
    E = {"a": ["b", "g"],
         "b": ["c", "g"],
         "c": ["d", "g", "b"],
         "d": ["a", "b"],
         "e": ["f", "d", "g"],
         "f": ["g", "e"],
         "g": []}

    # Create nodes of G
    nodes = {v: Node(v) for v in V}

    # Link nodes
    for value, preds in E.items():
        n = nodes[value]
        for pred in preds:
            p = nodes[pred]
            if p not in n.pred:
                n.pred.append(p)
            if n not in p.succ:
                p.succ.append(n)

    # Just a random node of G
    tree = nodes["a"]

    # PASO 1
    # Get CFCs
    cfc = tree.kosaraju(nodes.values())

    # PASO 2
    # node_value: rep_Node
    new_nodes = {}
    # Create nodes of G^CFC
    for rep, vorts in cfc.items():
        node = Node(rep)
        for vort in vorts:
            new_nodes[vort] = node

    # Link nodes
    for value, preds in E.items():
        n = new_nodes[value]
        for pred in preds:
            p = new_nodes[pred]
            if n not in p.succ and n is not p:
                p.succ.append(n)

    # PASO 3
    e1 = 0
    # Count links inside components
    for component in cfc.values():
        if len(component) > 1:
            e1 += len(component)

    # PASO 4
    # Count edges between components
    for comp in cfc:
        node = new_nodes[comp]
        e1 += len(node.succ)

    # PASO 5
    # Count edges in original graph
    e2 = 0
    for node in nodes.values():
        e2 += len(node.succ)

    delta = e2 - e1
    print("Delta E =", delta)

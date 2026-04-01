import sys
from typing import TextIO, Tuple

class Graph:

    def __init__(self) -> None:
        self.graph: dict[str, dict[str, dict[str, int]]] = {} # {node: {neighbor: { capacity; int, flow: int}}
        return

    def add_edge(self, u, v):
        self.graph[u][v] = { "capacity": 0, "flow": 0}
        self.graph[v][u] = { "capacity": 0, "flow": 0}
        return


    def set_edge_capacity(self, u, v, capacity):
        self.graph[u][v]["capacity"] = capacity
        self.graph[v][u]["capacity"] = capacity
        return

    def remove_edge(self, u, v):
        self.graph[u][v]["capacity"] = 0
        self.graph[v][u]["capacity"] = 0
        return

    def add_node(self, node):
        self.graph[node] = {}
        return

    """
    def remove_node(self, node):
        for neighbor, _ in self.graph[node]:
            filter(lambda n: n != node, self.graph[neighbor])
            #self.graph[neighbor] = {n: int(w) for n, w in self.graph[neighbor] if n != node}

            del self.graph[node]
        return
    """

    def capacity(self, u, v):
        try:
            for (neighbor, capacity) in self.graph[u]:
                if neighbor == v:
                    return capacity;
            return None
        except:
            return None

    def contains(self, u):
        return u in self.graph

    def get(self, u):
        return self.graph[u]

    def vertices(self):
        return [node for node in self.graph]

    def __repr__(self) -> str:
        res = []
        for node in self.graph:
            res.append(f"{node}: {self.graph.get(node)}\n")
        return "".join(res)[:-1]


def main():
    input = sys.stdin
    input = open("data/secret/0mini.in")
    
    # Build the graph. 
    graph, min_capacity, edges_to_remove = parse(input)
    
    #Use Ford-Fulkerson/preflow-push to find the maximum flow. 
    flow = preflow_push(graph)

    i = 0
    while i < len(edges_to_remove):
        #Then, remove one route/edge by updating its capacity to 0.
        graph.remove_edge(edges_to_remove[i][0], edges_to_remove[i][1])
        #Find maximum flow for that graph. 
        new_flow = preflow_push(graph)
        
        # If it is less than C, then we return the previous
        if new_flow >= min_capacity:
            flow = new_flow
            i += 1
        else: 
            break 

    
    print(f"{i} {flow}")
    return


def preflow_push(graph: Graph):
    return 21


def parse(input: TextIO):
    lines = input.read().splitlines()

    _, m_edges, c_min_capacity, _= map(int, lines[0].split(" "))

    graph = Graph()

    edges = []
    for i in range(1, 1 + m_edges):
        u, v, capacity = lines[i].split(" ")

        edges.append((u, v))

        if not graph.contains(u):
            graph.add_node(u)
        if not graph.contains(v):
            graph.add_node(v)
        graph.add_edge(u, v)
        graph.set_edge_capacity(u, v, capacity)

    print(graph)

    to_remove = []
    for line in lines[1 + m_edges:]:
        to_remove.append(edges[int(line)]) 

    return graph, int(c_min_capacity), to_remove


main()

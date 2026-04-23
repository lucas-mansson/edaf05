import sys
import copy
from collections import deque
from typing import TextIO

class Graph:

    def __init__(self) -> None:
        self.graph: dict[str, dict[str, dict[str, int]]] = {} # {node: {neighbor: { capacity; int, flow: int}}
        return

    def add_edge(self, u, v):
        self.graph[u][v] = { "capacity": 0, "flow": 0}
        self.graph[v][u] = { "capacity": 0, "flow": 0}
        return

    def set_edge_capacity(self, u, v, capacity: int):
        self.graph[u][v]["capacity"] = capacity
        self.graph[v][u]["capacity"] = capacity
        return

    def get_residual_capacity(self, u, v):
        return self.graph[u][v]["capacity"] - self.graph[u][v]["flow"]

    def capacity(self, u, v):
        return self.graph[u][v]["capacity"]

    def set_edge_flow(self, u, v, flow: int):
        self.graph[u][v]["flow"] = flow 
        self.graph[v][u]["flow"] = flow
        return

    def update_edge_flow(self, u, v, amount: int):
        self.graph[u][v]["flow"] += amount 
        self.graph[v][u]["flow"] -= amount
        return

    def flow(self, u, v):
        return self.graph[u][v]["flow"]

    def reset_flows(self):
        for u in self.nodes():
            for v in self.neighbors(u):
                self.graph[u][v]["flow"] = 0

    def remove_edge(self, u, v):
        self.graph[u][v]["capacity"] = 0
        self.graph[v][u]["capacity"] = 0
        return

    def add_node(self, node):
        self.graph[node] = {}
        return

    def neighbors(self, node):
        return self.graph[node]

#    def remove_node(self, node):
#        for neighbor, _ in self.graph[node]:
#            filter(lambda n: n != node, self.graph[neighbor])
#            #self.graph[neighbor] = {n: int(w) for n, w in self.graph[neighbor] if n != node}
#            del self.graph[node]
#        return

    def contains(self, u):
        return u in self.graph

    def get(self, u):
        return self.graph[u]

    def nodes(self):
        return self.graph.keys()

    def nbr_nodes(self):
        return len(self.graph)

    def __repr__(self) -> str:
        res = []
        for node in self.graph:
            res.append(f"{node}: {self.graph.get(node)}\n")
        return "".join(res)[:-1]


def main():
    input = sys.stdin
    #input = open("data/secret/3large.in")
    #input = open("data/secret/2med.in")
    
    # Build the graph. 
    graph, min_capacity, edges_to_remove = parse(input)
    
    #Use Ford-Fulkerson to find the maximum flow. 
    flow = float("inf")

    l = 0
    r = len(edges_to_remove)
    while l < r:
        mid = l + (r - l + 1) // 2

        res_graph = copy.deepcopy(graph)
        for (u, v) in edges_to_remove[:mid]:
            res_graph.remove_edge(u, v)

        res_graph.reset_flows()
        new_flow = ford_fulkerson(res_graph, source="0", sink=str(graph.nbr_nodes() - 1))

        if new_flow >= min_capacity:
            flow = new_flow
            l = mid
        else: 
            r = mid - 1

    print(f"{l} {flow}")
    return


def ford_fulkerson(graph: Graph, source: str, sink: str):
    max_flow = 0

    while True:
        # Find path
        parent = bfs(graph, source, sink)
        if parent is None: 
            break

        # Go back through path to find min capacity which is the flow
        path_flow = float("inf")
        curr = sink
        while curr != source:
            prev = parent[curr]  #type: ignore
            res_cap = graph.capacity(prev, curr) - graph.flow(prev, curr)
            path_flow = min(path_flow, res_cap)
            curr = prev

        if path_flow == 0:
            continue

        # update flows
        curr = sink
        while curr != source:
            prev = parent[curr] #type: ignore 
            graph.update_edge_flow(prev, curr, int(path_flow))
            curr = prev

        max_flow += path_flow
    
    return max_flow


def bfs(graph:Graph, source, sink):

    parent = {node: None for node in graph.nodes()}
    parent[source] = source 

    queue = deque([source])
    while len(queue) > 0:

        curr = queue.popleft()

        for neighbor in graph.neighbors(curr):
            residual_cap = graph.capacity(curr, neighbor) - graph.flow(curr, neighbor)

            if parent[neighbor] is None and residual_cap > 0:
                parent[neighbor] = curr
                if neighbor == sink:
                    return parent
                queue.append(neighbor)

    return None


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
        graph.set_edge_capacity(u, v, int(capacity))

    to_remove = [edges[int(line)] for line in lines[1 + m_edges:]]

    return graph, int(c_min_capacity), to_remove


main()

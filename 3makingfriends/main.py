import sys
import heapq
from typing import TextIO, Tuple

def main():
    #input = sys.stdin
    input = open("data/secret/3large.in")

    graph = make_graph(input)
    res = jarnik(graph, "1")

    print(sum(res))
    
    return


class Graph:

    def __init__(self) -> None:
        self.graph: dict[str, list[Tuple]] = {} # {node: [(neighbor, weight)]}
        return

    def add_edge(self, u, v, weight):
        self.graph[u].append((v, weight))
        self.graph[v].append((u, weight))
        return

    def add_node(self, node):
        self.graph[node] = []
        return

    def remove_node(self, node):
        for neighbor, _ in self.graph[node]:
            self.graph[neighbor] = [(n, w) for n, w in self.graph[neighbor] if n != node]

        del self.graph[node]
        return

    def weight(self, u, v):
        try:
            for neighbor, weight in self.graph[u]:
                if neighbor == v:
                    return weight;
            return None
        except:
            return None

    def get(self, u):
        return self.graph[u]

    def vertices(self):
        return [node for node in self.graph]

    def __str__(self) -> str:
        return str(self.graph)


# Jarniks algorithm
# Input w(e) weight of edge e = (u, v). We also write w(u, v)
# a root node r in V
# Output minimum spanning tree T
def jarnik(graph: Graph, root: str):
    mst = [] # resulting "tree" (only a list of integers, representing edge weights)
    visited = {root} # Keeps track of visited nodes

    queue = [] # We could add neighbors here but that would require updating distances
    for neighbor, weight in graph.get(root):
        heapq.heappush(queue, (weight, root, neighbor)) # sorts by weight O(log n) time complexity

    # while Q != empty 
    while len(queue) > 0:
        # select a v which minimizes w(u, v) where u not in Q, v in Q 
        # remove v from Q
        weight, _, v = heapq.heappop(queue) # select v with smallest weight

        if v not in visited:
            visited.add(v)
            # add (u, v) to T
            mst.append(weight)
            # add neighbors 
            for neighbor, weight in graph.get(v): 
                if neighbor not in visited:
                    heapq.heappush(queue, (weight, root, neighbor))
    return mst
# we use a PriorityQueue for Q with d(v), the distance to node V - Q, as keys

# Kruskals algorithm
# input w(e) weight of edge e = (u, v). We also write w(u, v)
# output minimum spanning tree T
def kruskal(_: Graph):
    T = {}
    # B <- E
    # while B != empty
    # select an edge e with minimal weight
    # if T union { e } does not create a cycle then:
        # add e to T
    # remove e from B

    return T


def make_graph(input: TextIO):
    graph = Graph()

    lines = input.read().splitlines()
    nbr_nodes, nbr_edges = lines[0].split()
    for i in range(int(nbr_nodes)):
        graph.add_node(str(i + 1))
    for j in range(int(nbr_edges)):
        line = lines[j + 1].split(" ")
        graph.add_edge(line[0], line[1], int(line[2]))

    return graph


main()

from collections import deque
import sys


def main():
    lines = sys.stdin.read().splitlines()
    nbr_words, nbr_queries = lines[0].split()

    words = lines[1:int(nbr_words) + 1]
    queries = lines[-int(nbr_queries):]

    graph = read_words_into_graph(words)

    for query in queries:
        source, goal = query.split()
        print(bfs(graph, source, goal))


def bfs(graph, source, goal):

    visited = { source }
    distances = { source: 0 }

    queue = deque([source])
    while len(queue) > 0:
        curr = queue.popleft()
        if curr == goal:
            return distances[curr]

        for neighbor in graph[curr]:
            if neighbor not in visited:
                distances[neighbor] = distances[curr] + 1
                queue.append(neighbor)
                visited.add(neighbor)

    return "Impossible"


def contains_all_letters(word1, word2):
    word1 = list(word1)
    word2 = list(word2)
    
    for char in word1:
        if char in word2:
            del word2[word2.index(char)]
        else:
            return False
    return True


def read_words_into_graph(words):
    graph = {}
    for i, node in enumerate(words):
        graph[node] = []

        for j, to in enumerate(words):
            if i == j:
                continue

            if(contains_all_letters(node[-4:], to)):
                graph[node].append(to)

    return graph


main()

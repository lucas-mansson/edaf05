import sys
from typing import TextIO

def main():
    input = sys.stdin
    #input = open("data/secret/0mini.in")
    
    # Characters maps the characters to the index
    # costs[i][j] is the cost of chainging characters[i] to a characters[j]
    # We use the character map to get the cost by costs[characters[char1]][characters[char2]]
    chars, costs, queries = parse(input)

    for query in queries:
        word1, word2 = solve(chars, costs, query, delta=-4)
        print(word1, word2)

    return


def solve(chars, costs, query, delta):

    word1 = query[0]
    word2 = query[1]

    word1_len = len(word1)
    word2_len = len(word2)
    
    a = [[0 for _ in range(word2_len + 1)] for _ in range(word1_len + 1)]

    for i in range(word1_len + 1):
        for j in range(word2_len + 1):
            if i == 0: # (0, j)
                a[i][j] = j * delta
            elif j == 0: # (j, 0)
                a[i][j] = i * delta
            else:
                char1_i = chars[word1[i-1]]
                char2_i = chars[word2[j-1]]

                cost = costs[char1_i][char2_i]

                opt1 = cost + a[i-1][j-1] # type: ignore
                opt2 = delta + a[i][j-1] # type: ignore
                opt3 = delta + a[i-1][j] # type: ignore
                
                a[i][j] = max(opt1, opt2, opt3)

    i, j = word1_len, word2_len
    res1, res2 = [], []

    # We walk backward to find the optimal path
    while i > 0 or j > 0:
        current = a[i][j]
        char1 = word1[i-1]
        char2 = word2[j-1]

        # Check if we walked diagonally to get here
        if i > 0 and j > 0:
            cost = costs[chars[char1]][chars[char2]]

            if current == cost + a[i-1][j-1]:
                res1.append(char1)
                res2.append(char2)
                j -= 1
                i -= 1
                continue

        # did we walk "up"?
        if i > 0 and current == delta + a[i-1][j]:
            res1.append(char1)
            res2.append("*")
            i -= 1
            continue

        # did we walk "right"?
        if j > 0 and current == delta + a[i][j-1]:
            res1.append("*")
            res2.append(char2)
            j -= 1
            continue

    return "".join(res1)[::-1], "".join(res2)[::-1]


def parse(input_file: TextIO):
    lines = input_file.read().splitlines()
    
    chars = lines[0].split()
    chars = {char: idx for idx, char in enumerate(chars)}
    k = len(chars)

    costs = []
    for i in range(1, k + 1):
        costs.append([int(x) for x in lines[i].split()])

    queries = [line.split() for line in lines[k+2:]]

    return chars, costs, queries


main()

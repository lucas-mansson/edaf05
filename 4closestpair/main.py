import math 
from typing import TextIO

class Point:

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def distance_to(self, p):
        return math.sqrt((self.x - p.x)**2 + (self.y - p.y)**2)

    def __repr__(self):
        return f"({self.x}, {self.y})"


def distance(p1: Point, p2: Point):
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)


def main():
    #input = sys.stdin
    input = open("data/sample/1.in")
    plane = make_plane(input) 

    return


def find_closest_points(px, py):
    

    if len(px) <= 2:
        pass

    return


def make_plane(input: TextIO):
    plane: list[Point] = []
    lines = input.read().splitlines()

    for line in lines[1:]:
        x, y = line.split(" ")
        plane.append(Point(int(x), int(y)))

    px, py = sorted(plane, key=lambda p: p.x), sorted(plane, key=lambda p: p.y)
    find_closest_points(px, py)

    return plane 

main()

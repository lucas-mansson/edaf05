import sys
import math 
from typing import TextIO

class Point:

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def distance_to(self, p) -> float:
        return math.sqrt((self.x - p.x)**2 + (self.y - p.y)**2)

    def __repr__(self):
        return f"({self.x}, {self.y})"


def main():
    input = sys.stdin
    #input = open("data/secret/4large2.in")
    plane = make_plane(input) 

    res = closest_points(plane)
    print(f"{res:.6f}")
    return


def closest_points(plane: list[Point]):
    px, py = sorted(plane, key=lambda p: p.x), sorted(plane, key=lambda p: p.y)
    return closest(px, py, len(px))


def closest(px: list[Point], py: list[Point], n: int) -> float:
    # base case, if we only have two points then we return that distance
    if n == 2: 
        return px[0].distance_to(px[1])
    if n <= 1:
        return float("inf")
    
    mid = n // 2
    mid_point = px[mid] # this is where we split the plane

    # Create two sorted arrays Lx and Rx from Px
    lx, rx = px[:mid], px[mid:]

    # Create two sorted arrays Ly and Ry from Py
    ly, ry = [], []
    for p in py:
        if p.x < mid_point.x:
            ly.append(p)
        else:
            ry.append(p)
    
    # solve the two subproblems (lx, ly, n/2) and (rx, ry, n - n/2)
    # compute delta as the minimum from these subproblems
    delta =  min(closest(lx, ly, mid), closest(rx, ry, n - mid))

    # plane containing points within delta, sorted by y
    # create sorted array S from Py
    s = [point for point in py if abs(point.x - mid_point.x) < delta] 

    if len(s) == 0:
        return delta

    # Check each ponts in S to see if any nearby points is closer than delta
    # "One point p in S is checked at a time. The distances from p to each of the 6 points 
    # on the other side in S (according to Y-coordinates) are checked to see if it has less
    # than the shortest distance found so far"
    min_s_dist = delta
    for i, p in enumerate(s):
        for j in range(i+1, min(i+7, len(s))):
            min_s_dist = min(p.distance_to(s[j]), min_s_dist)

    return min_s_dist


def make_plane(input: TextIO):
    plane: list[Point] = []
    lines = input.read().splitlines()

    for line in lines[1:]:
        x, y = line.split(" ")
        plane.append(Point(int(x), int(y)))

    return plane 


main()

# had damn issues with the sentence about loops which is literally useless

# --- Day 3: Crossed Wires ---
# The gravity assist was successful, and you're well on your way to the Venus refuelling station. During the rush back on Earth, the fuel management system wasn't completely installed, so that's next on the priority list.

# Opening the front panel reveals a jumble of wires. Specifically, two wires are connected to a central port and extend outward on a grid. You trace the path each wire takes as it leaves the central port, one wire per line of text (your puzzle input).

# The wires twist and turn, but the two wires occasionally cross paths. To fix the circuit, you need to find the intersection point closest to the central port. Because the wires are on a grid, use the Manhattan distance for this measurement. While the wires do technically cross right at the central port where they both start, this point does not count, nor does a wire count as crossing with itself.

# For example, if the first wire's path is R8,U5,L5,D3, then starting from the central port (o), it goes right 8, up 5, left 5, and finally down 3:

# ...........
# ...........
# ...........
# ....+----+.
# ....|....|.
# ....|....|.
# ....|....|.
# .........|.
# .o-------+.
# ...........
# Then, if the second wire's path is U7,R6,D4,L4, it goes up 7, right 6, down 4, and left 4:

# ...........
# .+-----+...
# .|.....|...
# .|..+--X-+.
# .|..|..|.|.
# .|.-X--+.|.
# .|..|....|.
# .|.......|.
# .o-------+.
# ...........
# These wires cross at two locations (marked X), but the lower-left one is closer to the central port: its distance is 3 + 3 = 6.

# Here are a few more examples:

# R75,D30,R83,U83,L12,D49,R71,U7,L72
# U62,R66,U55,R34,D71,R55,D58,R83 = distance 159
# R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
# U98,R91,D20,R16,D67,R40,U7,R15,U6,R7 = distance 135
# What is the Manhattan distance from the central port to the closest intersection?

# --- Part Two ---
# It turns out that this circuit is very timing-sensitive; you actually need to minimize the signal delay.

# To do this, calculate the number of steps each wire takes to reach each intersection; choose the intersection where the sum of both wires' steps is lowest. If a wire visits a position on the grid multiple times, use the steps value from the first time it visits that position when calculating the total value of a specific intersection.

# The number of steps a wire takes is the total number of grid squares the wire has entered to get to that location, including the intersection being considered. Again consider the example from above:

# ...........
# .+-----+...
# .|.....|...
# .|..+--X-+.
# .|..|..|.|.
# .|.-X--+.|.
# .|..|....|.
# .|.......|.
# .o-------+.
# ...........
# In the above example, the intersection closest to the central port is reached after 8+5+5+2 = 20 steps by the first wire and 7+6+4+3 = 20 steps by the second wire for a total of 20+20 = 40 steps.

# However, the top-right intersection is better: the first wire takes only 8+5+2 = 15 and the second wire takes only 7+6+2 = 15, a total of 15+15 = 30 steps.

# Here are the best steps for the extra examples from above:

# R75,D30,R83,U83,L12,D49,R71,U7,L72
# U62,R66,U55,R34,D71,R55,D58,R83 = 610 steps
# R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
# U98,R91,D20,R16,D67,R40,U7,R15,U6,R7 = 410 steps
# What is the fewest combined steps the wires must take to reach an intersection?

from collections import deque

global_movements = {
    'R': (1, 0),
    'L': (-1, 0),
    'U': (0, 1),
    'D': (0, -1),
}

def manhattan(x1, x2):
    d = 0
    for (el1, el2) in zip(x1, x2):
        d += abs(el2 - el1)
    return d

def walk(wire):
    # returns the points through which the wire passes without the starting point
    points = [(0,0)]
    for el in wire:
        move = global_movements[el[0]]
        for step in range(el[1]):
            current = points[-1]
            points.append((current[0]+move[0], current[1]+move[1]))
    points.pop(0)
    return points

def find_closest_manhattan(start, points):
    md = float('inf')
    for point in points:
        d = manhattan(start, point)
        md = d if d < md else md
    return md

def find_step_distance(start, wire, goal):
    distance = 0
    for el in wire:
        if el == goal:
            return distance + 1
        distance += 1

def find_combined_closest(start, w1, w2, goals):
    min_distance = float('inf')
    for goal in goals:
        d1 = find_step_distance(start, w1, goal)
        d2 = find_step_distance(start, w2, goal)
        comb = d1 + d2
        min_distance = comb if comb < min_distance else min_distance
    return min_distance

w1 = input().split(",")
w2 = input().split(",")

for i, e in enumerate(w1):
    w1[i] = (e[0], int(e[1:]))
for i, e in enumerate(w2):
    w2[i] = (e[0], int(e[1:]))

l1 = walk(w1)
l2 = walk(w2)
intersections = list(set(l1) & set(l2))
start = (0,0)
print("Part one - manhattan distance to closest intersection:", find_closest_manhattan(start, intersections))
print("Part two - combined walking distance to closest intersection:", find_combined_closest(start, l1, l2, intersections))

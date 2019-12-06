from collections import deque

class Planet():
    def __init__(self, planet_id, parent=None):
        self.id = planet_id
        self.parent = parent
        self.children = set()
    
    def calculate_orbits(self):
        if self.parent is None:
            return 0
        return self.parent.calculate_orbits() + 1
    
    def is_COM(self):
        return self.parent is None
    
    def add_child(self, planet):
        self.children |= {planet}
    
    def add_parent(self, planet):
        self.parent = planet
    
    def __repr__(self):
        string = self.id + " -> ["
        for child in self.children:
            string += child.id + ','
        return string + "]"

with open("input.txt", 'r') as puzzle_input:
    planets = dict()
    for line in puzzle_input:
        if line == '':
            break
        line = line.split(")")
        parent = line[0]
        child = line[1][:-1]
        parent = planets[parent] if parent in planets else Planet(parent)
        child = planets[child] if child in planets else Planet(child)
        parent.add_child(child)
        child.add_parent(parent)
        planets[child.id] = child
        planets[parent.id] = parent

    orbits = sum([planets[p].calculate_orbits() for p in planets])
    print("Total number of orbits:", orbits)

    start = planets['YOU'].parent
    end = planets['SAN'].parent
    visited = set()
    queue = deque([(start, 0)])
    while len(queue) > 0:
        current = queue.popleft()
        if current[0] in visited:
            continue
        visited |= {current[0]}
        if current[0] == end:
            steps = current[1]
            break
        if not current[0].is_COM()
            if current[0].parent == end:
                steps = current[1] + 1
                break
            else:
                queue.extend([(current[0].parent, current[1]+1)])
        else:
            if end in current[0].children:
                steps = current[1] + 1
                break
            else:
                queue.extend([(c, current[1]+1) for c in current[0].children])
    print("Orbital transfers required to get to Santa:", steps)

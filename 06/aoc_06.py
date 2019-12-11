test_input = ["COM)B","B)C","C)D","D)E","E)F","B)G","G)H","D)I","E)J","J)K","K)L","K)YOU","I)SAN"]

class StellarBody():
    def __init__(self, name, orbits):
        self.name = name
        self.orbits = orbits
        self.orbitted = set()

    def add_orbiter(self, orbiter):
        self.orbitted.add(orbiter)

    def add_orbits(self, orbits):
        self.orbits = orbits

    def has_parent(self):
        return True if self.orbits is not None else False

    def __repr__(self):
        return ("Name: %s Orbits: %s Orbiters: %s\n" %
                (self.name, self.orbits, [o.name for o in self.orbitted]))

    def __str__(self):
        return self.name

def build_system(stellar_map):
    stellar_system = dict()
    for relation in stellar_map:
        parent, child = relation.rstrip().split(')')
        if parent not in stellar_system:
            body = StellarBody(parent, None)
            stellar_system[parent] = body
        else:
            body = stellar_system[parent]
        if child not in stellar_system:
            orbiter = StellarBody(child, body)
            stellar_system[child] = orbiter
        else:
            orbiter = stellar_system[child]
            orbiter.add_orbits(body)
        body.add_orbiter(orbiter)
    return stellar_system

def count_orbits(system):
    o_count = 0
    for object in system.values():
        while(object.has_parent()):
            o_count += 1
            object = object.orbits
    return o_count

ex_system = build_system(test_input)
assert count_orbits(ex_system) == 54

with open('input.txt') as f:
    input_file = f.readlines()

full_system = build_system(input_file)
print(count_orbits(full_system))

### PART 2

def shortest_path(stellar_system, start, goal):
    start_pos = stellar_system[start]
    goal_pos = stellar_system[goal]
    start_map = list()
    goal_map = list()
    while (not set(start_map).intersection(goal_map)):
        start_pos = start_pos.orbits if start_pos.has_parent() else start_pos
        goal_pos = goal_pos.orbits if goal_pos.has_parent() else goal_pos
        start_map.append(start_pos.name)
        goal_map.append(goal_pos.name)
    (common_ancestor,) = set(start_map).intersection(goal_map)
    return (len(start_map[:start_map.index(common_ancestor)])
            + len(goal_map[:goal_map.index(common_ancestor)]))

assert shortest_path(ex_system, 'YOU', 'SAN') == 4
print(shortest_path(full_system, 'YOU', 'SAN'))

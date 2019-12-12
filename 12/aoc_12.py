from typing import NamedTuple
from collections import defaultdict
from itertools import combinations
from copy import deepcopy
from math import gcd

class Position(NamedTuple):
    x: int
    y: int
    z: int

class Velocity(NamedTuple):
    x: int
    y: int
    z: int

class Moon():
    def __init__(self, name, position):
        self.name = name
        self.position = Position(*position)
        self.velocity = Velocity(0,0,0)

    def apply_velocity(self):
        self.position = Position(*[sum(x) for x in zip(self.position, self.velocity)])

    def apply_gravity(self, vel_delta):
        self.velocity = Velocity(*[sum(x) for x in zip(self.velocity, vel_delta)])

    def get_energy(self):
        return sum(map(abs, self.position)) * sum(map(abs, self.velocity))

    def compare_on_axis(self, other, axis):
        if axis == 0:
            return (self.position.x == other.position.x and self.velocity.x == other.velocity.x)
        elif axis == 1:
            return (self.position.y == other.position.y and self.velocity.y == other.velocity.y)
        elif axis == 2:
            return (self.position.z == other.position.z and self.velocity.z == other.velocity.z)
        else:
            return False

    def __repr__(self):
        return ("%s, %s" % (self.position, self.velocity))

    def __str__(self):
        return ("%s: %s, %s" % (self.name, self.position, self.velocity))

    def __eq__(self, other):
        if isinstance(other, Moon):
            return (self.position == other.position and self.name == other.name and self.velocity == other.velocity)
        return False


def get_initial_positions(input_f, verbose=0):
    if verbose:
        print("Loading system %s:" % input_f)
    system = dict()
    with open(input_f) as f:
        names = ['Io', 'Europa', 'Ganymede', 'Callisto']
        for name, line in zip(names, f):
            line = line.rstrip().replace('>', '').replace('<', '')
            line = line.split(',')
            pos = map(int,(line[0].split('=')[1], line[1].split('=')[1], line[2].split('=')[1]))
            moon = Moon(name, pos)
            if verbose:
                print(moon)
            system[name] = moon
    return system

def vel_delta(pos_1, pos_2):
    if pos_1 == pos_2:
        return 0
    elif pos_1 > pos_2:
        return -1
    else:
        return 1


def calculate_gravity(system):
    velocity_delta = defaultdict(lambda: Velocity(0,0,0))
    for obj_1, obj_2 in combinations(system.values(), 2):
        velocity_delta_1 = Velocity(*map(vel_delta, obj_1.position, obj_2.position))
        velocity_delta_2 = Velocity(*map(lambda a: -1*a, velocity_delta_1))
        velocity_delta[obj_1.name] = Velocity(*[sum(x) for x in zip(velocity_delta[obj_1.name], velocity_delta_1)])
        velocity_delta[obj_2.name] = Velocity(*[sum(x) for x in zip(velocity_delta[obj_2.name], velocity_delta_2)])
    return velocity_delta

def zip_dicts(*dcts):
    for i in set(dcts[0]).intersection(*dcts[1:]):
        yield tuple(d[i] for d in dcts)

def compare_states(initial_state, orbits, system, step):
    axes = {0: 'x', 1: 'y', 2: 'z'}
    for i in range(3):
        if all(moon.compare_on_axis(initial_state[name], i) for name, moon in system.items()):
            print("%s axis aligned at %i." % (axes[i], step))
            if axes[i] not in orbits:
                orbits[axes[i]] = step

def simulate_system(system, runtime=-1, verbose=0):
    step = 0
    orbits = {}
    initial_state = deepcopy(system)
    while True:
        if verbose:
            print("Step %i" % (step))
            print(system)
        velocity_deltas = calculate_gravity(system)
        for moon in system.values():
            moon.apply_gravity(velocity_deltas[moon.name])
            moon.apply_velocity()
        step += 1
        if runtime == -1:
            compare_states(initial_state, orbits, system, step)
            if all(keys in orbits for keys in ['x', 'y', 'z']):
                return orbits
        elif step >= runtime:
            break
    if verbose:
        print("Step %i" % step)
        print(system)

def calculate_energy(system):
    return sum(map(Moon.get_energy, system.values()))

def lcm(a,b):
    return int((a*b) / gcd(a,b))

def orbit_steps(x, y, z):
    return lcm(lcm(x,y),z)

### TESTS
test_system_1 = get_initial_positions('test_1.txt')
simulate_system(test_system_1, 10)
assert test_system_1['Io'].position == Position(2,1,-3)
assert test_system_1['Europa'].position == Position(1,-8,0)
assert test_system_1['Ganymede'].velocity == Velocity(3,2,-3)
assert test_system_1['Callisto'].velocity == Velocity(1,-1,-1)

assert calculate_energy(test_system_1) == 179

test_system_2 = get_initial_positions('test_2.txt')
simulate_system(test_system_2, 100)
assert test_system_2['Io'].position == Position(8,-12,-9)
assert test_system_2['Ganymede'].velocity == Velocity(-3,7,4)

assert calculate_energy(test_system_2) == 1940

### PART 1
jupiter_system = get_initial_positions('input.txt')
simulate_system(jupiter_system, 1000)
print("Silver: %i" % calculate_energy(jupiter_system))


### PART 2
print("Test 1:")
test_system_1 = get_initial_positions('test_1.txt')
orbits = simulate_system(test_system_1)
assert orbit_steps(*orbits.values()) == 2772

print("Test 2:")
test_system_2 = get_initial_positions('test_2.txt')
orbits = simulate_system(test_system_2)
assert orbit_steps(*orbits.values()) == 4686774924

jupiter_system = get_initial_positions('input.txt')
print("Full run:")
orbits = simulate_system(jupiter_system)
print("Gold: %i" % orbit_steps(*orbits.values()))

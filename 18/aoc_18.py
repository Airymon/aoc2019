import math
import string
from collections import deque, defaultdict
from itertools import combinations
import numpy as np

def read_map(from_file):
    full_map = []
    with open(from_file) as f:
        for line in f:
            full_map.append([x for x in line.rstrip()])
    return np.array(full_map)

def display_map(full_map):
    for line in full_map:
        for char in line:
            print(char, end='')
        print('')
    return 1

def shortest_path_len(full_map, a, b):
    # find shortest paths from a to b dependent on whether we can access certain doors
    explored = set()
    next_nodes = deque([])
    start_node = (np.where(full_map == a)[0][0], np.where(full_map == a)[1][0])
    next_nodes.append((start_node, 0, set()))
    while next_nodes:
        node, dist, doors = next_nodes.popleft()
        explored.add(node)
        if full_map[node] == b:
            return dist, doors
        elif full_map[node] == '#':
            continue
        else:
            if full_map[node] in string.ascii_uppercase:
                doors.add(full_map[node].lower())
            neighbors = [tuple(map(sum, zip(node, (1,0)))),
                         tuple(map(sum, zip(node, (-1,0)))),
                         tuple(map(sum, zip(node, (0,1)))),
                         tuple(map(sum, zip(node, (0,-1))))]
            for neighbor in neighbors:
                if neighbor not in explored:
                    next_nodes.append((neighbor, dist+1, doors.copy()))
    return math.inf, set()

def enumerate_possible_states(keys, positions, distances):
    states = {}
    init_state = ('@', set(), 0) # at the start we have no keys and are at '@'
    to_visit = deque(list())
    to_visit.append(init_state)
    while to_visit:
        current_state = to_visit.popleft()
        #print(current_state)
        pos, keychain, distance_now = current_state
        state = (pos, tuple(sorted(keychain)))
        if state not in states or states[state] > distance_now:
            states[state] = distance_now
            for key in keys - keychain:
                i_tup = (pos, key) if (pos, key) in distances else (key, pos)
                dist, doors = distances[i_tup]
                if doors <= keychain:
                    next_state = (key, keychain.copy() | {key}, distance_now + dist)
                    to_visit.append(next_state)
    return states


def find_shortest_path(states, keys):
    min_val = math.inf
    for key, value in states.items():
        pos, keychain = key
        if len(keychain) == len(keys):
            if min_val > value:
                min_val = value
    return min_val

def find_path_for_map(in_map, goal):
    keys = set(chr(x) for x in range(ord('a'),ord(goal)+1))
    positions = keys | {'@'}
    distances = dict()
    for start, goal in combinations(list(positions), 2):
        dist, doors = shortest_path_len(in_map, start, goal)
        distances[(start, goal)] = (dist, doors)
    states = enumerate_possible_states(keys, positions, distances)
    return find_shortest_path(states, keys)

### TESTS PART 1
test01 = read_map('test_01.txt')
goal = 'b'
assert find_path_for_map(test01, goal) == 8

test02 = read_map('test_02.txt')
goal = 'f'
assert find_path_for_map(test02, goal) == 86

test03 = read_map('test_03.txt')
goal = 'g'
assert find_path_for_map(test03, goal) == 132

test04 = read_map('test_04.txt')
goal = 'p'
assert find_path_for_map(test04, goal) == 136

test05 = read_map('test_05.txt')
goal = 'i'
assert find_path_for_map(test05, goal) == 81

### PART 1
print("\n PART 1 START \n")

full_map = read_map('input.txt')
goal = 'z'
print("Silver: %i" % find_path_for_map(full_map, goal))

### PART 2
# we just split the problem into 4 problems that run independent from one another
# for this we manipulate the maps and then run the same algorithm as before

def split_map(full_map):
    h, w = full_map.shape
    q1 = np.array([full_map[i][:(h // 2)+1] for i in range((w // 2)+1)])
    q2 = np.array([full_map[i][(h // 2):] for i in range((w // 2)+1)])
    q3 = np.array([full_map[i][:(h // 2)+1] for i in range((w // 2), w)])
    q4 = np.array([full_map[i][(h // 2):] for i in range((w // 2), w)])
    return q1, q2, q3, q4

def remove_doors(full_map):
    keys_in_segment = set()
    for line in full_map:
        for position in line:
            if position in string.ascii_lowercase:
                keys_in_segment.add(position)
    w, h = full_map.shape
    for i in range(w):
        for j in range(h):
            if full_map[(i,j)] in string.ascii_uppercase and full_map[i,j].lower() not in keys_in_segment:
                full_map[(i,j)] = '.'
    return full_map, keys_in_segment

def calculate_distance_four_quadrants(quadrants):
    total_dist = 0
    for quadrant in quadrants:
        in_map, keys = quadrant
        positions = keys | {'@'}
        distances = dict()
        for start, goal in combinations(list(positions), 2):
            dist, doors = shortest_path_len(in_map, start, goal)
            distances[(start, goal)] = (dist, doors)
        states = enumerate_possible_states(keys, positions, distances)
        total_dist += find_shortest_path(states, keys)
    return total_dist

test06 = read_map('test_06.txt')
all_quadrants = split_map(test06)
transformed_quadrants = []
for quadrant in all_quadrants:
    t_quadrant = remove_doors(quadrant)
    transformed_quadrants.append(t_quadrant)
assert calculate_distance_four_quadrants(transformed_quadrants) == 8

### PART 2
full_map = read_map('input_p2.txt')
all_quadrants = split_map(full_map)
transformed_quadrants = []
for quadrant in all_quadrants:
    t_quadrant = remove_doors(quadrant)
    transformed_quadrants.append(t_quadrant)
print("Gold %i" % calculate_distance_four_quadrants(transformed_quadrants))

from collections import defaultdict
from math import atan2, pi


def read_asteroid_map(path):
    asteroid_map = set()
    with open(path) as f:
        for i, line in enumerate(f):
            line = line.rstrip()
            for j, char in enumerate(line):
                if char == "#":
                    asteroid_map.add((j,i))
    return asteroid_map

def abs_distance(tup):
    return sum(map(abs, tup))

def asteroid_positions_at_loc(loc, asteroid_map):
    positions = defaultdict(list)
    asteroid_map.remove(loc)
    for asteroid in asteroid_map:
        rel_pos = tuple(x-y for x,y in zip(asteroid, loc))
        #norm_pos = tuple(map(lambda a: a / sum(map(abs,rel_pos)), rel_pos))
        positions[atan2(*rel_pos)].append(asteroid)
    for asteroids in positions.values():
        asteroids.sort(key=abs_distance)
    return positions

### PART 1
def max_visible(input_f):
    asteroid_map = read_asteroid_map(input_f)
    visibility_map = dict()
    for asteroid in asteroid_map:
        visibility_map[asteroid] = len(asteroid_positions_at_loc(asteroid, asteroid_map.copy()))
    return visibility_map

assert max(max_visible("test_1.txt").values()) == 8
assert max(max_visible("test_2.txt").values()) == 33
assert max(max_visible("test_3.txt").values()) == 35
assert max(max_visible("test_4.txt").values()) == 41
assert max(max_visible("test_5.txt").values()) == 210

visible_locs = max_visible("input.txt")
print("Silver: %i at %s" % (max(visible_locs.values()), max(visible_locs, key=visible_locs.get)))

### PART 2
location = max(visible_locs, key=visible_locs.get)

def shoot_laser(positions):
    order_laser = sorted(positions.keys(), reverse=True)
    order_destruction = []
    while bool(positions):
        for angle in order_laser:
            if angle in positions:
                target = positions[angle].pop(0)
                order_destruction.append(target)
                if len(positions[angle]) == 0:
                    del positions[angle]
    return order_destruction

def shoot_laser_v2(position):
    order_laser = list()
    for angle, asteroids in position.items():
        for i, asteroid in enumerate(asteroids):
            order_laser.append((angle-i*2*pi, asteroid))
    return [y for x,y in sorted(order_laser, key=lambda tup: tup[0], reverse=True)]

test_6 = read_asteroid_map("test_6.txt")
loc = (8,3)
asteroids = asteroid_positions_at_loc(loc, test_6)
dead_asteroids = shoot_laser_v2(asteroids.copy())
assert dead_asteroids[8] == (15,1)
test_7 = read_asteroid_map("test_5.txt")
loc = (11,13)
asteroids = asteroid_positions_at_loc(loc, test_7)
dead_asteroids = shoot_laser_v2(asteroids.copy())
assert dead_asteroids[199] == (8,2)

asteroids = asteroid_positions_at_loc(location, read_asteroid_map("input.txt"))
dead_asteroids = shoot_laser_v2(asteroids.copy())
print("Gold: %i" % (100*dead_asteroids[199][0] + dead_asteroids[199][1]))

import enum
from math import *

input_text = []
with open('input.txt') as r:
    for line in r:
        input_text.append(line.rstrip().split(','))

class Directions(enum.Enum):
    Right = 'R'
    Left = 'L'
    Up = 'U'
    Down = 'D'

input_wires = []
for line in input_text:
    wire = []
    for entry in line:
        dir = Directions(entry[0])
        size = int(entry[1:])
        wire.append((dir, size))
    input_wires.append(wire)

def move_right(pos, size):
    return (pos[0], pos[1] + size)

def move_left(pos, size):
    return (pos[0], pos[1] - size)

def move_up(pos, size):
    return (pos[0] - size, pos[1])

def move_down(pos, size):
    return (pos[0] + size, pos[1])

move_actions = {Directions.Right: move_right, Directions.Left: move_left,
                Directions.Down: move_down, Directions.Up: move_up}

def get_set_of_points(start, wire):
    points = set()
    pos = start
    for step in wire:
        new_pos = move_actions[step[0]](pos, step[1])
        if step[0] == Directions.Right or step[0] == Directions.Left:
            new_points = [(new_pos[0], s) for s in range(min(pos[1],new_pos[1]),max(pos[1],new_pos[1]))]
        else:
            new_points = [(s, new_pos[1]) for s in range(min(pos[0],new_pos[0]),max(pos[0],new_pos[0]))]
        pos = new_pos
        set_points = set(new_points)
        points.update(set_points)
    return points

points_a = get_set_of_points((0,0), input_wires[0])
points_b = get_set_of_points((0,0), input_wires[1])
shared_p = points_a.intersection(points_b)
print(shared_p)

def manhattan_distance(x,y):
    return sum(abs(a-b) for a,b in zip(x,y))

distances = []
for intersect in shared_p:
    dist = manhattan_distance((0,0), intersect)
    distances.append(dist)
print(min(distances))

## Part 2

def steps_until_point(start, wire, goal):
    points = list()
    pos = start
    for step in wire:
        new_pos = move_actions[step[0]](pos, step[1])
        if step[0] == Directions.Right or step[0] == Directions.Left:
            new_points = [(new_pos[0], s) for s in range(min(pos[1],new_pos[1]),max(pos[1],new_pos[1]))]
        else:
            new_points = [(s, new_pos[1]) for s in range(min(pos[0],new_pos[0]),max(pos[0],new_pos[0]))]
        if goal in new_points:
            new_points = new_points[:new_points.index(goal)]
            points.extend(new_points)
            return len(points)
        pos = new_pos
        points.extend(new_points)
    return len(points)

dist_list = []
for point in shared_p:
    wire_1 = steps_until_point((0,0), input_wires[0], point)
    wire_2 = steps_until_point((0,0), input_wires[1], point)
    dist_list.append(wire_1 + wire_2)
print(min(dist_list))

import numpy as np
import string
from typing import NamedTuple
from collections import deque

class Position(NamedTuple):
    x: int
    y: int

class Node():
    def __init__(self, position, label):
        self.position = position
        self.label = label
        self.neighbors = set()

    def add_neighbor(self, position):
        self.neighbors.add(position)

def read_maze(input_f):
    maze = list()
    max_width = 0
    with open(input_f) as f:
        for line in f:
            line = line.rstrip()
            max_width = len(line) if len(line) > max_width else max_width
            layer = list()
            for char in line:
                layer.append(char)
            maze.append(layer)
    for layer in maze:
        if len(layer) < max_width:
            layer.extend([' '] * (max_width - len(layer)))
    return np.array(maze)

def draw_maze(maze_list):
    for layer in maze_list:
        print(''.join(layer))

def label_portals_at(pos, char, maze_list):
    height = len(maze_list)
    width = len(maze_list[0])
    if pos.y+1 < height and maze_list[(pos.y+1, pos.x)] in string.ascii_uppercase:
        if pos.y+2 < height and maze_list[(pos.y+2, pos.x)] == '.':
            return Position(pos.x, pos.y+2), char+maze_list[(pos.y+1, pos.x)]
        else:
            return Position(pos.x, pos.y-1), char+maze_list[(pos.y+1, pos.x)]
    elif pos.x+1 < width and maze_list[(pos.y, pos.x+1)] in string.ascii_uppercase:
         if pos.x+2 < width and maze_list[(pos.y, pos.x+2)] == '.':
             return Position(pos.x+2, pos.y), char+maze_list[(pos.y, pos.x+1)]
         else:
             return Position(pos.x-1, pos.y), char+maze_list[(pos.y, pos.x+1)]
    else:
        return pos, char

def maze_to_map(maze_list):
    full_map = dict()
    height = len(maze_list)
    width = len(maze_list[0])
    for y in range(height):
        for x in range(width):
            location = Position(x,y)
            if maze_list[(y,x)] == ' ' or maze_list[(y,x)] == '#':
                continue
            elif maze_list[(y,x)] in string.ascii_uppercase:
                location, label = label_portals_at(location, maze_list[y,x], maze_list)
                if label == maze_list[(y,x)]:
                    continue
                if label != 'ZZ' and label != 'AA':
                    if location.x == 2 or location.x == width-3 or location.y == 2 or location.y == height-3:
                        outer = 'U'
                    else:
                        outer = 'I'
                else:
                    outer=''
                full_map[location] =  label+outer
            else:
                if location in full_map:
                    continue
                full_map[location] = maze_list[(y,x)]
    return full_map

def map_to_graph(maze_map):
    maze_graph = dict()
    for position, label in maze_map.items():
        node = Node(position, label)
        for delta in [(1,0), (-1,0), (0,1), (0,-1)]:
            neighbor_pos = Position(position.x + delta[0], position.y + delta[1])
            if neighbor_pos in maze_map:
                node.add_neighbor(neighbor_pos)
        if label != '.' and label != 'AA' and label != 'ZZ':
            tele_location = [location for location, tel_label in maze_map.items() if tel_label[:2] == label[:2] and location != position][0]
            print("%s with label %s teleports to %s" % (position, label, tele_location))
            node.add_neighbor(tele_location)
        maze_graph[position] = node
    return maze_graph

def get_start_pos(maze_map):
    for position, label in maze_map.items():
        if label == 'AA':
            return position

def shortest_path(maze_graph, start_pos):
    # do BFS counting steps to goal
    visited = set()
    start_node = maze_graph[start_pos]
    queue = deque([(start_node, 0)])
    while True:
        node, dist = queue.popleft()
        visited.add(node.position)
        if node.label == 'ZZ':
            return dist
        for neighbor in node.neighbors:
            if neighbor not in visited:
                queue.append((maze_graph[neighbor], dist+1))

### PART 1 TEST
print("Test 1")
maze = read_maze('test_01.txt')
draw_maze(maze)
maze_map = maze_to_map(maze)
maze_graph = map_to_graph(maze_map)
assert shortest_path(maze_graph, get_start_pos(maze_map)) == 23


print("\nTest 2")
maze = read_maze('test_02.txt')
draw_maze(maze)
maze_map = maze_to_map(maze)
maze_graph = map_to_graph(maze_map)
assert shortest_path(maze_graph, get_start_pos(maze_map)) == 58

### PART 1

print("\n PART 1 START \n")
maze = read_maze('input.txt')
draw_maze(maze)
maze_map = maze_to_map(maze)
maze_graph = map_to_graph(maze_map)
print("Silver: %i" % shortest_path(maze_graph, get_start_pos(maze_map)))

### TEST PART 2

def shortest_path_recursive(maze_graph, start_pos):
    # do BFS counting steps to goal in n layers
    visited = set() # we keep track of the layer in the visited
    start_node = maze_graph[start_pos]
    queue = deque([(start_node, 0, 0)])
    while True:
        node, dist, layer = queue.popleft()
        visited.add((node.position, layer))
        if node.label == 'ZZ' and layer == 0:
            return dist
        elif node.label[-1] == 'U' and layer == 0:
            no_teleport = True
        else:
            no_teleport = False
        for neighbor in node.neighbors:
            if layer > 20:
                continue
            elif node.label[-1] == 'U' and maze_graph[neighbor].label[-1] == 'I' and no_teleport:
                # we are on the outer layer and cant teleport outwards
                continue
            elif node.label[-1] == 'I' and maze_graph[neighbor].label[-1] == 'U':
                # we are stepping one layer further out
                new_layer = layer - 1
            elif node.label[-1] == 'U' and maze_graph[neighbor].label[-1] == 'I':
                # we are stepping one layer further down
                new_layer = layer + 1
            else:
                # we are just moving within the layer
                new_layer = layer
            if (neighbor, new_layer) not in visited:
                queue.append((maze_graph[neighbor], dist+1, new_layer))

print("\nTest 3")
maze = read_maze('test_03.txt')
draw_maze(maze)
maze_map = maze_to_map(maze)
maze_graph = map_to_graph(maze_map)
assert shortest_path_recursive(maze_graph, get_start_pos(maze_map)) == 396

###
print("\n PART 2 START \n")
maze = read_maze('input.txt')
draw_maze(maze)
maze_map = maze_to_map(maze)
maze_graph = map_to_graph(maze_map)
print("Gold: %i" % shortest_path_recursive(maze_graph, get_start_pos(maze_map)))

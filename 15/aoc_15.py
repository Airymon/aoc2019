import math
import time
from enum import Enum
from typing import NamedTuple
from collections import deque
from intcode import IntcodeComputer

class FieldType(Enum):
    WALL = 0
    FIELD = 1
    OSYS = 2
    OXY = 3

class Direction(Enum):
    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4

movement = {Direction.NORTH: (0,-1), Direction.SOUTH: (0, 1),
            Direction.WEST: (-1, 0), Direction.EAST: (1, 0)}

opposite = {Direction.NORTH: Direction.SOUTH,
            Direction.SOUTH: Direction.NORTH,
            Direction.WEST: Direction.EAST,
            Direction.EAST: Direction.WEST}

class Position(NamedTuple):
    x: int
    y: int

class Field():
    def __init__(self, position, type, prev_dist):
        self.position = position
        self.type = FieldType(type)
        if self.type is not FieldType.WALL:
            self.dist = prev_dist + 1
        else:
            self.dist = math.inf

    def update_dist(self, dist):
        self.dist = dist

class RepairDroid():
    def __init__(self, program, visualize=0):
        self.computer = IntcodeComputer(program, [], "Arcade Cabinet")
        self.areamap = dict()
        self.visualize = visualize
        self.startpos = Position(0,0)
        self.areamap[self.startpos] = Field(self.startpos, 1, -1)
        self.currentpos = self.startpos

    def move_droid(self, direction):
        move = movement[direction]
        new_pos = Position(self.currentpos.x + move[0], self.currentpos.y + move[1])
        self.computer.add_input(direction.value)
        output = self.computer.run_program()
        if new_pos not in self.areamap:
            new_field = Field(new_pos, output[-1], self.areamap[self.currentpos].dist)
            self.areamap[new_pos] = new_field
            if new_field.type == FieldType.WALL:
                return False
            else:
                self.currentpos = new_pos
                return True
        elif self.areamap[new_pos].type != FieldType.WALL:
            if self.areamap[new_pos].dist < self.areamap[self.currentpos].dist-1:
                # we found a shorter path to the current position
                self.areamap[self.currentpos].update_dist(self.areamap[new_pos].dist+1)
            self.currentpos = new_pos
            return False
        else:
            return False

    def draw_map(self):
        min_x = min(x for x,y in self.areamap.keys())
        max_x = max(x for x,y in self.areamap.keys())
        min_y = min(y for x,y in self.areamap.keys())
        max_y = max(y for x,y in self.areamap.keys())
        x_range = max_x - min_x
        y_range = max_y - min_y
        full_map = ""
        for y in range(y_range+1):
            for x in range(x_range+1):
                position = Position(x+min_x, y+min_y)
                if position == self.currentpos:
                    full_map = full_map + "D"
                elif position not in self.areamap:
                    full_map = full_map + "#"
                elif self.areamap[position].type == FieldType.FIELD:
                    full_map = full_map + " "
                elif self.areamap[position].type == FieldType.WALL:
                    full_map = full_map + "|"
                elif self.areamap[position].type == FieldType.OSYS:
                    full_map = full_map + "X"
                elif self.areamap[position].type == FieldType.OXY:
                    full_map = full_map + "O"
            full_map = full_map + "\n"
        print(full_map)
        print("")

    def traverse_grid(self):
        directions = [Direction.EAST, Direction.SOUTH, Direction.NORTH, Direction.WEST]
        steps = deque(directions)
        i = 0
        while steps:
            i+=1
            next_move = steps.popleft()
            if self.visualize:
                time.sleep(0.5)
                print("Step: %i" % i)
                self.draw_map()
            if self.move_droid(next_move):
                prev = opposite[next_move]
                steps.appendleft(prev)
                move_order = directions[:]
                move_order.remove(prev)
                for entry in reversed(move_order):
                    steps.appendleft(entry)
            else:
                continue
        self.draw_map()

### PART 1
def shortest_path(area_map):
    for entry in area_map.values():
        if entry.type == FieldType.OSYS:
            return entry.dist

print("\n PART 1 START \n")
with open('input.txt') as f:
    data = f.readline()
    input_list = data.split(',')
input_prog = list(map(int, input_list))
repairdroid = RepairDroid(input_prog)
repairdroid.traverse_grid()
print("Silver: %i" % shortest_path(repairdroid.areamap))

### PART 2
full_map = repairdroid.areamap

def locate_oxygen_system(area_map):
    for pos, entry in area_map.items():
        if entry.type == FieldType.OSYS:
            return pos

def oxygen_spread(oxygen, area_map):
    new_oxy = set()
    for pos in oxygen:
        up = Position(pos.x, pos.y-1)
        down = Position(pos.x, pos.y+1)
        left = Position(pos.x-1, pos.y)
        right = Position(pos.x+1, pos.y)
        for neighbor in [up, down, left, right]:
            if neighbor in area_map and area_map[neighbor].type != FieldType.WALL and area_map[neighbor].type != FieldType.OXY:
                area_map[neighbor].type = FieldType.OXY
                new_oxy.add(neighbor)
    return new_oxy, area_map

def simulate_oxygen(oxy_system, repairdroid, visualize=0):
    step = 0
    oxygen = {oxy_system}
    area_map = repairdroid.areamap
    area_map[oxy_system].type = FieldType.OXY
    while oxygen:
        if visualize:
            print("Step: %i" % step)
            repairdroid.draw_map()
            time.sleep(0.5)
        oxygen, area_map = oxygen_spread(oxygen, area_map)
        step += 1
    repairdroid.draw_map()
    # last step we check but dont spread any more oxygen
    return step-1

oxygen_system = locate_oxygen_system(full_map)
print("Gold: %i" % simulate_oxygen(oxygen_system, repairdroid))

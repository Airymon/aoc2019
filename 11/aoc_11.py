from enum import Enum
from collections import defaultdict
from typing import List, Dict, NamedTuple
from intcode import IntcodeComputer

class Direction(Enum):
    Left = 0
    Up = 1
    Right = 2
    Down = 3

class Position(NamedTuple):
    x: int
    y: int

movement = {Direction.Left: (-1,0), Direction.Up: (0,-1),
            Direction.Right: (1,0), Direction.Down: (0,1)}

class EHPR():
    def __init__(self, program):
        self.painted = defaultdict(int)
        self.position = Position(0,0)
        self.direction = Direction.Up
        self.computer = IntcodeComputer(program, [], "Emergency Hull Painting Robot", 0)

    def set_start_color(self, color):
        self.painted[self.position] = color

    def move(self, command):
        new_direction = (Direction(((self.direction.value + 1) % 4)) if command
                            else Direction(((self.direction.value - 1) % 4)))
        new_position = Position(*(sum(x) for x in zip(self.position, movement[new_direction])))
        self.direction = new_direction
        self.position = new_position

    def paint_square(self, color):
        self.painted[self.position] = color

    def execute_step(self):
        self.computer.add_input(self.painted[self.position])
        self.computer.run_program()
        output = self.computer.get_output()
        color, command = output[-2:]
        self.paint_square(color)
        self.move(command)

### PART 1
print("\n PART 1 START \n")
with open('input.txt') as f:
    data = f.readline()
    input_list = data.split(',')
input_prog = list(map(int, input_list))
roboy = EHPR(input_prog)
while (not roboy.computer.has_stopped()):
    roboy.execute_step()
print("Silver: %i" % len(roboy.painted))

### PART 2
print("\n PART 2 START \n")

def display_paintjob(painted_locations):
    min_x = min(x for x,y in painted_locations.keys())
    min_y = min(y for x,y in painted_locations.keys())
    max_x = max(x for x,y in painted_locations.keys())
    max_y = max(y for x,y in painted_locations.keys())
    x_range = max_x - min_x
    y_range = max_y - min_y
    for y in range(y_range+1):
        for x in range(x_range+1):
            position = Position(x+min_x, y+min_y)
            print("X", end='') if painted_locations[position] else print(" ", end='')
        print("")


roboy = EHPR(input_prog)
roboy.set_start_color(1)
while (not roboy.computer.has_stopped()):
    roboy.execute_step()
print("Paintjob done. Engaging cameras.")
print("Gold: ")
display_paintjob(roboy.painted)

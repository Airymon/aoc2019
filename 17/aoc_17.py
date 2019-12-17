import time
from typing import NamedTuple
from intcode import IntcodeComputer

class Position(NamedTuple):
    x: int
    y: int

class SpaceRoomba():
    def __init__(self, program, input_inst=[], verbose=0):
        self.computer = IntcodeComputer(program, input_inst, "Aft Scaffolding Control and Information Interface", verbose)
        self.position = Position(0,0)
        self.map = dict()

    def get_image_from_camera(self):
        image_output = self.computer.run_program()
        self.image_output = image_output
        return image_output

    def produce_scaffolding_map(self):
        s_map = dict()
        x, y = 0, 0
        for num in self.image_output:
            if num == 35:
                pos = Position(x,y)
                s_map[pos] = '#'
                x += 1
            elif num == 10:
                x = 0
                y += 1
            else:
                x += 1
        return s_map

def draw_map(image_output):
    str = ''
    for num in image_output:
        str = str + chr(num)
    print(str)


### PART 1

def calculate_intersections(s_map):
    deltas = [(1,0), (-1,0), (0,1), (0,-1)]
    intersections = set()
    for scaffolding in s_map:
        neighbors = [tuple(x+y for x,y in zip(scaffolding, delta)) for delta in deltas]
        if all(neighbor in s_map for neighbor in neighbors):
            intersections.add(scaffolding)
    return intersections

def insert_at_loc(image, locations, char):
    # For showing objects on the map at certain locations
    new_image = list()
    x, y = 0, 0
    for entry in image:
        if Position(x,y) in locations:
            new_image.append(ord(char))
        else:
            new_image.append(entry)
        x += 1
        if entry == 10:
            x = 0
            y += 1
    return new_image

print("\n PART 1 START \n")

with open('input.txt') as f:
    data = f.readline()
    input_list = data.split(',')
input_prog = list(map(int, input_list))

roomba = SpaceRoomba(input_prog)
image = roomba.get_image_from_camera()
img_len = len(image)
print("Camera Image:")
draw_map(image)

s_map = roomba.produce_scaffolding_map()
intersections = calculate_intersections(s_map)

new_image = insert_at_loc(image, intersections, 'O')
print("Intersections marked:")
draw_map(new_image)

print("Silver: %i" % sum(intersection.x * intersection.y for intersection in intersections))

### PART 2

def to_input_instruction(INSTR):
    input_prog = []
    for char in INSTR:
        input_prog.append(ord(char))
    return input_prog

def show_path(output, im_len):
    start_index = 0
    iteration = 0
    while start_index < len(output):
        if iteration == 1:
            #skip the text thats thrown in between
            start_index += 66
        draw_map(output[start_index:start_index+im_len])
        start_index += im_len
        time.sleep(0.2)
        iteration += 1

print("\n PART 2 START \n")

# It was faster to figure this out by hand for once so the path is just copied from paper
# I could retrace my steps to find this solution to make it into an algorithm at some point
whole_path = ['L6', 'R12', 'L6', 'R12', 'L10', 'L4', 'L6', 'L6', 'R12', 'L6', 'R12', 'L10', 'L4', 'L6', 'L6', 'R12', 'L6', 'L10', 'L10', 'L4', 'L6', 'R12', 'L10', 'L4', 'L6', 'L10', 'L10', 'L4', 'L6', 'L6', 'R12', 'L6', 'L10', 'L10', 'L4', 'L6']
MAIN = "A,B,A,B,A,C,B,C,A,C\n"
A = "L,6,R,12,L,6\n"
B = "R,12,L,10,L,4,L,6\n"
C = "L,10,L,10,L,4,L,6\n"
DISPLAY = "n\n"
assert len(MAIN) <= 21
assert len(A) <= 21
assert len(B) <= 21
assert len(C) <= 21

manual_prog = input_prog[:]
manual_prog[0] = 2
instructions = to_input_instruction(MAIN+A+B+C+DISPLAY)
roomba = SpaceRoomba(manual_prog, verbose=0)
roomba.computer.add_prog_input(instructions)
roomba.computer.run_program()
output = roomba.computer.get_output()
show_path(output, img_len)

print("\nGold: %i" % output[-1])

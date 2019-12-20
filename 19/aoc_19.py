from typing import NamedTuple
from intcode import IntcodeComputer

class Position(NamedTuple):
    x: int
    y: int

class FlyingDrone():
    def __init__(self, program):
        self.current_position = Position(0,0)
        self.computer = IntcodeComputer(program, list(Position(0,0)), "SpaceDroneNavigation")

    def navigate_to_pos(self, position):
        self.computer.add_prog_input(list(position))
        self.computer.run_program()
        output = self.computer.get_output()
        self.current_position = position
        return output[0]

### PART 1

print("\n PART 1 START \n")

with open('input.txt') as f:
    data = f.readline()
    input_list = data.split(',')
input_prog = list(map(int, input_list))

space_map_2 = list()
space_map = dict()
for i in range(50):
    new_line = list()
    for j in range(50):
        spacedrone = FlyingDrone(input_prog)
        new_pos = Position(j,i)
        result = spacedrone.navigate_to_pos(new_pos)
        new_line.append(result)
        space_map[new_pos] = result
    space_map_2.append(new_line)

print("Silver: %i" % sum(space_map.values()))

for j,map_line in enumerate(space_map_2):
    for i, entry in enumerate(map_line):
        if entry:
            print('#', end='')
        else:
            print('.', end='')
    print("")

### PART 2
print("\n PART 2 START \n")
# absolute spaghetti code solution because I couldn't figure out a closed form.

def get_upper_bound(program, size):
    # finds an upper bound upper left corner on a sizexsize square
    x, y = 5, 6
    # rough pattern is 10,11 for a x+1/x+1 sized square with an extra +5/6 every 4 steps
    # this actually gets us within single digit range from the actual solution
    x = x + size*10 + size//4 * 5
    y = y + size*11 + size//4 * 6
    # quick check if we can fit at this position (should always work)
    spacedrone_1 = FlyingDrone(program)
    spacedrone_2 = FlyingDrone(program)
    if not spacedrone_1.navigate_to_pos(Position(x+99, y)) and spacedrone_2.navigate_to_pos(Position(x,y+99)):
        raise RuntimeError("Couldn't fit the spot, wrong pattern?")
    return x,y

def step_back_y(x, y, program):
    last_y = y
    while True:
        # check if our spot is still on the beam
        spacedrone_confirm = FlyingDrone(program)
        if not spacedrone_confirm.navigate_to_pos(Position(x,y)):
            print("Fell off the beam")
            break
        # move up the y axis until we cant fit x+99 any more
        spacedrone_y = FlyingDrone(program)
        if not spacedrone_y.navigate_to_pos(Position(x+99,y)):
            # our previous y was the minimum axis
            y = last_y
            break
        last_y = y
        y -= 1
    return y

def step_back_x(x, y, program):
    last_x = x
    while True:
        # check if our spot is still on the beam
        spacedrone_confirm = FlyingDrone(program)
        if not spacedrone_confirm.navigate_to_pos(Position(x,y)):
            print("Fell off the beam")
            break
        # move up the x axis until we cant fit y+99 any more
        spacedrone_x = FlyingDrone(program)
        if not spacedrone_x.navigate_to_pos(Position(x,y+99)):
            # our previous x was the minimum axis
            x = last_x
            break
        last_x = x
        x -= 1
    return x

def step_back_both(x, y, program):
    last_x = x
    while True:
        # check if our spot is still on the beam
        spacedrone_confirm = FlyingDrone(program)
        if not spacedrone_confirm.navigate_to_pos(Position(x,y)):
            print("Fell off the beam")
            break
        # move up the x axis until we cant fit y+99 any more
        spacedrone_x = FlyingDrone(program)
        if not spacedrone_x.navigate_to_pos(Position(x,y+99)):
            # our previous x was the minimum axis
            x = last_x
            y = last_y
            break
        spacedrone_y = FlyingDrone(program)
        if not spacedrone_y.navigate_to_pos(Position(x+99,y)):
            # our previous x was the minimum axis
            x = last_x
            y = last_y
            break
        last_x = x
        last_y = y
        x -= 1
        y -= 1
    return x, y

def backwards_fit(coords, program):
    x, y = coords # these are a close upper bound on our actual coordinates
    new_x, new_y = 0, 0
    # while there is still an update we havent reached the boundary
    # trying to step back diagonally until we no longer fit, then adjust on x and y axis
    # alternatingly
    while True:
        new_x, new_y = step_back_both(x, y, program)
        new_y = step_back_y(new_x, new_y, program)
        new_x = step_back_x(new_x, new_y, program)
        if x == new_x and y == new_y:
            break
        else:
            x = new_x
            y = new_y
    return new_x, new_y

coords = get_upper_bound(input_prog, 100)
min_coords = backwards_fit(coords, input_prog)

print("Gold: %i" % (min_coords[0]*10000 + min_coords[1]))

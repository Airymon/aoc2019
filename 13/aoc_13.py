import sys
import time
import keyboard
from intcode import IntcodeComputer

tiles = {0: ' ', 1: '|', 2: 'X', 3: '_', 4: 'O'}

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

class ArcadeCabinet():
    def __init__(self, program, free_play=0):
        if free_play:
            program = program[:]
            program[0] = 2
        self.computer = IntcodeComputer(program, [], "Arcade Cabinet")
        self.display = dict()
        self.ball , self.tile = None, None

    def draw_screen(self):
        max_x = max(x for x,y in self.display.keys())
        max_y = max(y for x,y in self.display.keys())
        score = self.display[(-1,0)] if (-1,0) in self.display else 0
        printstr = "\tSCORE:\t %i\n" % score
        for y in range(max_y+1):
            for x in range(max_x+1):
                printstr = printstr +"%s" % tiles[self.display[(x,y)]]
            printstr = printstr + "\n"
        sys.stdout.write(printstr)

    def parse_instruction(self, instruction):
        x, y, tile = instruction
        self.display[(x,y)] = tile
        if tile == 4:
            self.ball = x
        elif tile == 3:
            self.tile = x

    def joystick(self, key='n'):
        if keyboard.is_pressed('a') or key == 'a':
            self.computer.add_input(-1)
        elif keyboard.is_pressed('d') or key == 'd':
            self.computer.add_input(1)
        elif keyboard.is_pressed('s') or key == 's':
            self.computer.add_input(0)

    def self_play(self):
        if self.tile > self.ball:
            return 'a'
        elif self.tile < self.ball:
            return 'd'
        else:
            return 's'

    def run_game(self):
        i_counter = 0
        while not self.computer.has_stopped():
            time.sleep(0.07)
            output = self.computer.run_program()
            for instruction in chunks(output, 3):
                self.parse_instruction(instruction)
            self.draw_screen()
            self.computer.input_l.clear()
            key = self.self_play()
            self.joystick(key)
            """
            if i_counter % 100 == 0 and (-1,0) in self.display:
                sys.stdout.write("\r")
                sys.stdout.flush()
                sys.stdout.write("Score: %i" % self.display[(-1,0)])
            """
        #print("")
        self.draw_screen()


### PART 1
print("\n PART 1 START \n")
with open('input.txt') as f:
    data = f.readline()
    input_list = data.split(',')
input_prog = list(map(int, input_list))
wall_ball = ArcadeCabinet(input_prog)
wall_ball.run_game()
print("Silver: %i" % list(wall_ball.display.values()).count(2))

### PART 2
print("\n PART 2 START \n")
wall_ball = ArcadeCabinet(input_prog, 1)
wall_ball.run_game()

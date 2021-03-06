import sys
import time
import keyboard
from intcode import IntcodeComputer

tiles = {0: ' ', 1: '|', 2: 'X', 3: '_', 4: 'O'}

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

class ArcadeCabinet():
    def __init__(self, program, free_play=False, auto=False, display=True):
        if free_play:
            program = program[:]
            program[0] = 2
        self.computer = IntcodeComputer(program, [], "Arcade Cabinet")
        self.gamestate = dict()
        self.ball , self.tile = None, None
        self.auto = auto
        self.display = display

    def draw_screen(self):
        max_x = max(x for x,y in self.gamestate.keys())
        max_y = max(y for x,y in self.gamestate.keys())
        score = self.gamestate[(-1,0)] if (-1,0) in self.gamestate else 0
        printstr = "\tSCORE:\t %i\n" % score
        for y in range(max_y+1):
            for x in range(max_x+1):
                printstr = printstr +"%s" % tiles[self.gamestate[(x,y)]]
            printstr = printstr + "\n"
        sys.stdout.write(printstr)

    def parse_instruction(self, instruction):
        x, y, tile = instruction
        self.gamestate[(x,y)] = tile
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

    def score_counter(self):
        score = self.gamestate[(-1,0)] if (-1,0) in self.gamestate else 0
        sys.stdout.write("\r")
        sys.stdout.flush()
        sys.stdout.write("Score: %i" % score)

    def run_game(self):
        while not self.computer.has_stopped():
            output = self.computer.run_program()
            for instruction in chunks(output, 3):
                self.parse_instruction(instruction)
            if self.display:
                self.draw_screen()
                time.sleep(0.07)
            else:
                self.score_counter()
            self.computer.input_l.clear()
            key = self.self_play() if self.auto else None
            self.joystick(key)
        sys.stdout.write('\n')
        self.draw_screen()


### PART 1
print("\n PART 1 START \n")
with open('input.txt') as f:
    data = f.readline()
    input_list = data.split(',')
input_prog = list(map(int, input_list))
breakout = ArcadeCabinet(input_prog, display=False)
breakout.run_game()
print("Silver: %i" % list(breakout.gamestate.values()).count(2))

### PART 2
print("\n PART 2 START \n")
breakout = ArcadeCabinet(input_prog, free_play=True, auto=True, display=True)
breakout.run_game()
print("\nGold: %i" % breakout.gamestate[(-1,0)])

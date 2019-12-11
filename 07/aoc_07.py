from itertools import permutations
import string

class IntcodeComputer():
    output_l, opt_hist, history = [], [], []
    i_pointer = 0
    def __init__(self, program, input_l, name):
        self.program = program[:]
        self.input_l = input_l[:]
        self.name = name
        self.stopped = False

        self.optfuncs = {1: self.plus, 2: self.mult, 3: self.store_input, 4: self.output,
                         5: self.jump_if_true, 6: self.jump_if_false, 7: self.less_than, 8: self.equals}
        self.history.append(program[:])

    def add_input(self, number):
        self.input_l.append(number)

    def get_output(self):
        return self.output_l[-1]

    def get_history(self):
        return self.history

    def get_opt_history(self):
        return self.opt_hist

    def has_stopped(self):
        return self.stopped

    def plus(self, i, prog, **kwargs):
        """
        Args:
            i = index
            prog = program
            params = 0 address 1 immediate
        """
        a, b, c = prog[i+1:i+4]
        mode_b, mode_a = kwargs['params'][-2:]
        arg_a = a if mode_a else prog[a]
        arg_b = b if mode_b else prog[b]
        prog[c] = arg_a + arg_b
        return i+4, prog

    def mult(self, i, prog, **kwargs):
        """
        Args:
            i = index
            prog = program
            params = 0 address 1 immediate
        """
        a, b, c = prog[i+1:i+4]
        mode_b, mode_a = kwargs['params'][-2:]
        arg_a = a if mode_a else prog[a]
        arg_b = b if mode_b else prog[b]
        prog[c] = arg_a * arg_b
        return i+4, prog

    def store_input(self, i, prog, **kwargs):
        """
        Args:
            i = index
            prog = program
            input = provided input
        """
        i_val = kwargs['input']
        prog[prog[i+1]] = i_val
        return i+2, prog

    def output(self, i, prog, **kwargs):
        """
        Args:
            a = address
            prog = program list
            mode_a = 0 position 1 immediate
        """
        a = prog[i+1]
        mode_a = kwargs['params'][-1]
        arg_a = a if mode_a else prog[a]
        self.output_l.append(arg_a)
        return i+2, prog

    def jump_if_true(self, i, prog, **kwargs):
        """
        Args:
            i = index
            prog = program
            params = 0 position 1 immediate
        """
        a, b = prog[i+1:i+3]
        mode_b, mode_a = kwargs['params'][-2:]
        arg_a = a if mode_a else prog[a]
        arg_b = b if mode_b else prog[b]
        return (arg_b, prog) if arg_a else (i+3, prog)

    def jump_if_false(self, i, prog, **kwargs):
        """
        Args:
            i = index
            prog = program
            params = 0 position 1 immediate
        """
        a, b = prog[i+1:i+3]
        mode_b, mode_a = kwargs['params'][-2:]
        arg_a = a if mode_a else prog[a]
        arg_b = b if mode_b else prog[b]
        return (arg_b, prog) if not arg_a else (i+3, prog)

    def less_than(self, i, prog, **kwargs):
        """
        Args:
            i = index,
            prog = program
            params = 0 position 1 immediate
        """
        a, b, c = prog[i+1:i+4]
        mode_b, mode_a = kwargs['params'][-2:]
        arg_a = a if mode_a else prog[a]
        arg_b = b if mode_b else prog[b]
        prog[c] = 1 if arg_a < arg_b else 0
        return i+4, prog

    def equals(self, i, prog, **kwargs):
        """
        Args:
            i = index
            prog = program
            params = 0 position 1 immediate
        """
        a, b, c = prog[i+1:i+4]
        mode_b, mode_a = kwargs['params'][-2:]
        arg_a = a if mode_a else prog[a]
        arg_b = b if mode_b else prog[b]
        prog[c] = 1 if arg_a == arg_b else 0
        return i+4, prog

    def halt(self):
        self.stopped = True
        return True

    def run_program(self):
        while (True):
            intcode = str(self.program[self.i_pointer])
            intcode = '0'*(5-len(intcode))+intcode
            optcode = int(intcode[-2:])
            params = list(map(int,intcode[:-2]))
            arguments = {'params': params}
            if optcode == 99:
                #print("%s: Got halt - Stopping." % self.name)
                self.halt()
                break
            elif optcode == 3 :
                if not self.input_l:
                    #print("%s: Waiting for input." % self.name)
                    break
                else:
                    arguments['input'] = self.input_l.pop(0)
            self.i_pointer, self.program = self.optfuncs[optcode](self.i_pointer, self.program[:], **arguments)
            self.history.append(self.program)
            self.opt_hist.append(optcode)
        return True

### TESTCASES DAY 05
test_list = []
with open('../05/input.txt') as r:
    data = r.readline()
    test_list = data.split(',')
test_list = list(map(int, test_list))

int_comp = IntcodeComputer(test_list, [1], "Intcode Test Machine 1")
int_comp.run_program()
assert int_comp.get_output() == 13210611
int_comp = IntcodeComputer(test_list, [5], "Intcode Test Machine 2")
int_comp.run_program()
assert int_comp.get_output() == 584126

### PART 1
def run_regular(settings, program):
    outputs = []
    for setting in settings:
        prev_out = 0
        for i, char in enumerate(string.ascii_uppercase[:5]):
            amplifier = IntcodeComputer(program[:], [setting[i], prev_out], ("Amplifier %s" % char))
            amplifier.run_program()
            prev_out = amplifier.get_output()
        outputs.append(prev_out)
    return max(outputs)

set_a = [4,3,2,1,0]
input_prog_a = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
set_b = [0,1,2,3,4]
input_prog_b = [3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0]
set_c = [1,0,4,3,2]
input_prog_c = [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]

amp_settings = list(permutations(range(5), 5))
assert run_regular(amp_settings, input_prog_a) == 43210
assert run_regular(amp_settings, input_prog_b) == 54321
assert run_regular(amp_settings, input_prog_c) == 65210

with open('input.txt') as f:
    data = f.readline()
    input_list = data.split(',')
input_prog = list(map(int, input_list))

print("Silver: %i" % run_regular(amp_settings, input_prog))

### PART 2
def run_feedback(settings, program, start_val):
    outputs = []
    for setting in settings:
        machines = []
        prev_out = start_val
        for i, char in enumerate(string.ascii_uppercase[:5]):
            amplifier = IntcodeComputer(program, [setting[i]], ("Amplifier %s" % char))
            machines.append(amplifier)
        while (not all(map(lambda x: x.has_stopped(), machines))):
            for amplifier in machines:
                amplifier.add_input(prev_out)
                amplifier.run_program()
                prev_out = amplifier.get_output()
        outputs.append(prev_out)
    return max(outputs)

set_d = [9,8,7,6,5]
input_prog_d = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
set_e = [9,7,8,5,6]
input_prog_e = [3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]

amp_settings = list(permutations(range(5,10), 5))
assert run_feedback(amp_settings, input_prog_d, 0) == 139629729
assert run_feedback(amp_settings, input_prog_e, 0) == 18216

print("Gold: %i" % run_feedback(amp_settings, input_prog, 0))

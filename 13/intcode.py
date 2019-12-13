from collections import defaultdict
import string
import keyboard

class IntcodeComputer():
    def __init__(self, program, input_l, name, verbose=0):
        self.program = defaultdict(int)
        for idx, value in enumerate(program):
            self.program[idx] = value
        self.prog_len = len(program)
        self.input_l = input_l[:]
        self.name = name
        self.verbose = verbose
        self.stopped = False
        self.i_pointer = 0
        self.r_pointer = 0
        self.output_l, self.history= [], []

        self.optfuncs = {1: self.plus, 2: self.mult, 3: self.store_input, 4: self.output,
                         5: self.jump_if_true, 6: self.jump_if_false, 7: self.less_than,
                         8: self.equals, 9: self.adjust_rel}

    def add_input(self, number):
        self.input_l.append(number)

    def get_output(self):
        return self.output_l

    def get_history(self):
        return self.history

    def has_stopped(self):
        return self.stopped

    def check_address(self, address):
        return True if address >= 0 else False

    def get_argument(self, program, address, relative, mode):
        """
        Returns the value to be manipulated dependent on mode
        """
        if mode == 0:
            if not self.check_address(address):
                raise RuntimeError("Negative address encountered: %i" % address)
            return program[address]
        elif mode == 2:
            if not self.check_address(relative+address):
                raise RuntimeError("Negative address encountered: %i" % relative+address)
            return program[relative+address]
        elif mode == 1:
            return address
        else:
            raise RuntimeError("Unknown mode: %i" % mode)

    def get_storage_address(self, program, address, relative, mode):
        """
        Returns the address of the location dependent on mode
        """
        if mode == 0:
            if not self.check_address(address):
                raise RuntimeError("Negative address encountered %i" % address)
            return address
        elif mode == 2:
            if not self.check_address(relative + address):
                raise RuntimeError("Negative address encountered %i" % relative+address)
            return relative+address
        else:
            raise RuntimeError("Unknown store mode: %i" % mode)

    def plus(self, i, r, prog, **kwargs):
        """
        Args:
            i = index
            r = relative index
            prog = program
            params = 0 address 1 immediate 2 relative
        """
        a, b, c = prog[i+1], prog[i+2], prog[i+3]
        mode_c, mode_b, mode_a = kwargs['params'][-3:]
        arg_a = self.get_argument(prog, a, r, mode_a)
        arg_b = self.get_argument(prog, b, r, mode_b)
        adr = self.get_storage_address(prog, c, r, mode_c)
        prog[adr] = arg_a + arg_b
        return i+4, r, prog

    def mult(self, i, r, prog, **kwargs):
        """
        Args:
            i = index
            r = relative index
            prog = program
            params = 0 address 1 immediate 2 relative
        """
        a, b, c = prog[i+1], prog[i+2], prog[i+3]
        mode_c, mode_b, mode_a = kwargs['params'][-3:]
        arg_a = self.get_argument(prog, a, r, mode_a)
        arg_b = self.get_argument(prog, b, r, mode_b)
        adr = self.get_storage_address(prog, c, r, mode_c)
        prog[adr] = arg_a * arg_b
        return i+4, r, prog

    def store_input(self, i, r, prog, **kwargs):
        """
        Args:
            i = index
            r = relative index
            prog = program
            input = provided input
            params = 0 position 1 immediate 2 relative
        """
        i_val = kwargs['input']
        mode_a = kwargs['params'][-1]
        index = self.get_storage_address(prog, prog[i+1], r, mode_a)
        prog[index] = i_val
        return i+2, r, prog

    def output(self, i, r, prog, **kwargs):
        """
        Args:
            a = address
            prog = program list
            params = 0 position 1 immediate 2 relative
        """
        a = prog[i+1]
        mode_a = kwargs['params'][-1]
        arg_a = self.get_argument(prog, a, r, mode_a)
        if self.verbose:
            print("Diagnosis check: %i" % arg_a)
        self.output_l.append(arg_a)
        return i+2, r, prog

    def jump_if_true(self, i, r, prog, **kwargs):
        """
        Args:
            i = index
            r = relative index
            prog = program
            params = 0 position 1 immediate 2 relative
        """
        a, b = prog[i+1], prog[i+2]
        mode_b, mode_a = kwargs['params'][-2:]
        arg_a = self.get_argument(prog, a, r, mode_a)
        arg_b = self.get_argument(prog, b, r, mode_b)
        return (arg_b, r, prog) if arg_a else (i+3, r, prog)

    def jump_if_false(self, i, r, prog, **kwargs):
        """
        Args:
            i = index
            r = relative index
            prog = program
            params = 0 position 1 immediate 2 relative
        """
        a, b = prog[i+1], prog[i+2]
        mode_b, mode_a = kwargs['params'][-2:]
        arg_a = self.get_argument(prog, a, r, mode_a)
        arg_b = self.get_argument(prog, b, r, mode_b)
        return (arg_b, r, prog) if not arg_a else (i+3, r, prog)

    def less_than(self, i, r, prog, **kwargs):
        """
        Args:
            i = index,
            r = relative index
            prog = program
            params = 0 position 1 immediate 2 relative
        """
        a, b, c = prog[i+1], prog[i+2], prog[i+3]
        mode_c, mode_b, mode_a = kwargs['params'][-3:]
        arg_a = self.get_argument(prog, a, r, mode_a)
        arg_b = self.get_argument(prog, b, r, mode_b)
        adr = self.get_storage_address(prog, c, r, mode_c)
        prog[adr] = 1 if arg_a < arg_b else 0
        return i+4, r, prog

    def equals(self, i, r, prog, **kwargs):
        """
        Args:
            i = index
            r = relative index
            prog = program
            params = 0 position 1 immediate 2 relative
        """
        a, b, c = prog[i+1], prog[i+2], prog[i+3]
        mode_c, mode_b, mode_a = kwargs['params'][-3:]
        arg_a = self.get_argument(prog, a, r, mode_a)
        arg_b = self.get_argument(prog, b, r, mode_b)
        adr = self.get_storage_address(prog, c, r, mode_c)
        prog[adr] = 1 if arg_a == arg_b else 0
        return i+4, r, prog

    def adjust_rel(self, i, r, prog, **kwargs):
        """
        Args:
            i = index
            r = relative index
            prog = program
            params = 0 position 1 immediate 2 relative
        """
        a = prog[i+1]
        mode_a = kwargs['params'][-1]
        arg_a = self.get_argument(prog, a, r, mode_a)
        return i+2, r+arg_a, prog

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
                if self.verbose:
                    print("%s: Got halt - Stopping." % self.name)
                self.halt()
                break
            elif optcode == 3:
                if not self.input_l:
                    if self.verbose:
                        print("%s: Waiting for input." % self.name)
                    break
                else:
                    arguments['input'] = self.input_l.pop(0)
            self.i_pointer, self.r_pointer, self.program = self.optfuncs[optcode](
                self.i_pointer, self.r_pointer, self.program, **arguments)
            self.history.append(intcode)
        return self.output_l

if __name__ == "__main__":
    ### TESTCASES DAY 05
    test_list = []
    with open('../05/input.txt') as r:
        data = r.readline()
        test_list = data.split(',')
    test_list = list(map(int, test_list))

    print("Running basic tests.")
    int_comp = IntcodeComputer(test_list, [1], "Intcode Test Machine 1", 1)
    int_comp.run_program()
    assert int_comp.get_output()[-1] == 13210611
    int_comp = IntcodeComputer(test_list, [5], "Intcode Test Machine 2", 1)
    int_comp.run_program()
    assert int_comp.get_output()[-1] == 584126
    print("Basic test passed.")

    ### TESTCASES DAY 07
    def run_regular(settings, program):
        outputs = []
        for setting in settings:
            prev_out = 0
            for i, char in enumerate(string.ascii_uppercase[:5]):
                amplifier = IntcodeComputer(program[:], [setting[i], prev_out], ("Amplifier %s" % char))
                amplifier.run_program()
                prev_out = amplifier.get_output()[-1]
            outputs.append(prev_out)
        return max(outputs)

    set_a = [4,3,2,1,0]
    input_prog_a = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
    set_b = [0,1,2,3,4]
    input_prog_b = [3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0]
    set_c = [1,0,4,3,2]
    input_prog_c = [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]

    print("Running amplifier tests.")
    assert run_regular([set_a], input_prog_a) == 43210
    assert run_regular([set_b], input_prog_b) == 54321
    assert run_regular([set_c], input_prog_c) == 65210
    print("Amplifier test passed.")

    ### TESTCASES DAY 09
    test_09_a = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
    testcomp = IntcodeComputer(test_09_a[:], [], "Testcomp Quine", 1)
    print("Starting run with %s" % testcomp.name)
    testcomp.run_program()
    assert testcomp.get_output() == test_09_a
    print("Passed.")

    test_09_b = [1102,34915192,34915192,7,4,7,99,0]
    testcomp = IntcodeComputer(test_09_b[:], [], "Testcomp 16 digit int", 1)
    print("Starting run with %s" % testcomp.name)
    testcomp.run_program()
    assert len(str(testcomp.get_output()[-1])) == 16
    print("Passed.")

    test_09_c = [104,1125899906842624,99]
    testcomp = IntcodeComputer(test_09_c[:], [], "Testcomp large integer", 1)
    print("Starting run with %s" %testcomp.name)
    testcomp.run_program()
    assert testcomp.get_output()[-1] == 1125899906842624
    print("Passed.")

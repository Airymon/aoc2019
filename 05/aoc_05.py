input_list = []

with open('input.txt') as r:
    input = r.readline()
    input_list = input.split(',')

input_list = list(map(int, input_list))

def plus(a, b, c, prog, mode_a=0, mode_b=0):
    """
    Args:
        a = argument address
        b = argument address
        c = store address
        prog = program list
        mode_a = 0 position 1 immediate
        mode_b = 0 position 1 immediate
    """
    c_prog = prog.copy()
    arg_a = a if mode_a else prog[a]
    arg_b = b if mode_b else prog[b]
    c_prog[c] = arg_a + arg_b
    return c_prog

def mult(a, b, c, prog, mode_a=0, mode_b=0):
    """
    Args:
        a = argument address
        b = argument address
        c = store address
        prog = program list
        mode_a = 0 position 1 immediate
        mode_b = 0 position 1 immediate
    """
    c_prog = prog.copy()
    arg_a = a if mode_a else prog[a]
    arg_b = b if mode_b else prog[b]
    c_prog[c] = arg_a * arg_b
    return c_prog

def input(a, prog, input_val):
    """
    Args:
        a = store address
        input_val = store value
        prog = program list
    """
    c_prog = prog.copy()
    c_prog[a] = input_val
    return c_prog

def output(a, prog, mode_a):
    """
    Args:
        a = address
        prog = program list
        mode_a = 0 position 1 immediate
    """
    arg_a = a if mode_a else prog[a]
    print("Diagnostic output: %s" % arg_a)
    return True

def jump_if_true(a, b, i, prog, mode_a=0, mode_b=0):
    """
    Args:
        a = first parameter
        b = address
        i = program pointer
        prog = program list
        mode_a = 0 position 1 immediate
        mode_b = 0 position 1 immediate
    """
    arg_a = a if mode_a else prog[a]
    arg_b = b if mode_b else prog[b]
    return arg_b if arg_a else i+3

def jump_if_false(a, b, i, prog, mode_a=0, mode_b=0):
    """
    Args:
        a = first parameter
        b = address
        i = program pointer
        prog = program list
        mode_a = 0 position 1 immediate
        mode_b = 0 position 1 immediate
    """
    arg_a = a if mode_a else prog[a]
    arg_b = b if mode_b else prog[b]
    return arg_b if not arg_a else i+3

def less_than(a, b, c, prog, mode_a=0, mode_b=0):
    """
    Args:
        a = first parameter
        b = second parameter
        c = address
        prog = program list
        mode_a = 0 position 1 immediate
        mode_b = 0 position 1 immediate
    """
    c_prog = prog.copy()
    arg_a = a if mode_a else prog[a]
    arg_b = b if mode_b else prog[b]
    c_prog[c] = 1 if arg_a < arg_b else 0
    return c_prog

def equals(a, b, c, prog, mode_a=0, mode_b=0):
    """
    Args:
        a = first parameter
        b = second parameter
        c = address
        prog = program list
        mode_a = 0 position 1 immediate
        mode_b = 0 position 1 immediate
    """
    c_prog = prog.copy()
    arg_a = a if mode_a else prog[a]
    arg_b = b if mode_b else prog[b]
    c_prog[c] = 1 if arg_a == arg_b else 0
    return c_prog

def halt():
    print("Got halt - Stopping.")
    return True

optcode = {1: plus, 2: mult, 3: input, 4: output,
           5: jump_if_true, 6: jump_if_false, 7: less_than, 8: equals,
           99: halt}

def run_intcode(program, input):
    i = 0
    history = []
    while (True):
        intcode = str(program[i])
        intcode = '0'*(5-len(intcode))+intcode
        opcode = int(intcode[-2:])
        history.append(opcode)
        params = intcode[:-2]
        if opcode == 99:
            optcode[opcode]()
            break
        elif opcode in [1,2,7,8]:
            program = optcode[opcode](program[i+1], program[i+2], program[i+3],
                                      program, int(params[-1]), int(params[-2]))
            i += 4
        elif opcode == 3:
            program = optcode[opcode](program[i+1], program, input)
            i += 2
        elif opcode == 4:
            optcode[opcode](program[i+1], program, int(params[-1]))
            i += 2
        elif opcode == 5 or opcode == 6:
            i = optcode[opcode](program[i+1], program[i+2], i, program,
                                int(params[-1]), int(params[-2]))
        else:
            raise RuntimeError("Invalid opcode %s" % opcode)

input_var = 5

ex_1 = [3,9,8,9,10,9,4,9,99,-1,8]
ex_2 = [3,9,7,9,10,9,4,9,99,-1,8]
ex_3 = [3,3,1108,-1,8,3,4,3,99]
ex_4 = [3,3,1107,-1,8,3,4,3,99]

ex_j_1 = [3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9]
ex_j_2 = [3,3,1105,-1,9,1101,0,0,12,4,12,99,1]

large_ex = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]

run_intcode(input_list.copy(), input_var)

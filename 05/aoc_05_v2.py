def plus(i, prog, **kwargs):
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

def mult(i, prog, **kwargs):
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

def store_input(i, prog, **kwargs):
    """
    Args:
        i = index
        prog = program
        input = provided input
    """
    i_val = kwargs['input']
    prog[prog[i+1]] = i_val
    return i+2, prog

def output(i, prog, **kwargs):
    """
    Args:
        a = address
        prog = program list
        mode_a = 0 position 1 immediate
    """
    a = prog[i+1]
    mode_a = kwargs['params'][-1]
    arg_a = a if mode_a else prog[a]
    print("Diagnostic output: %s" % arg_a)
    return i+2, prog

def jump_if_true(i, prog, **kwargs):
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

def jump_if_false(i, prog, **kwargs):
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

def less_than(i, prog, **kwargs):
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

def equals(i, prog, **kwargs):
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

optfuncs = {1: plus, 2: mult, 3: store_input, 4: output,
            5: jump_if_true, 6: jump_if_false, 7: less_than, 8: equals}

def run_intcode(program, i_val):
    i = 0
    program = program[:]
    opt_hist, history = [], []
    while (True):
        intcode = str(program[i])
        intcode = '0'*(5-len(intcode))+intcode
        optcode = int(intcode[-2:])
        params = list(map(int,intcode[:-2]))
        arguments = {'params': params, 'input': i_val}
        if optcode == 99:
            print("Got halt - Stopping.")
            break
        i, program = optfuncs[optcode](i, program[:], **arguments)
        history.append(program)
        opt_hist.append(optcode)
    return history, opt_hist

input_list = []

with open('input.txt') as r:
    data = r.readline()
    input_list = data.split(',')

input_list = list(map(int, input_list))
run_intcode(input_list, 5)

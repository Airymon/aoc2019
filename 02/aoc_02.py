from itertools import zip_longest

input_list = []

with open('input.txt') as r:
    input = r.readline()
    input_list = input.split(',')

input_list = list(map(int, input_list))

def plus(a,b):
    return a+b

def mult(a,b):
    return a*b

optcode = {1: plus, 2: mult}

def batch(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]

def memory_run(init_memory, a, b):
    memory = init_memory.copy()
    memory[1] = a
    memory[2] = b
    for code in batch(memory, 4):
        if code[0] == 99:
            break
        memory[code[3]] = optcode[code[0]](memory[code[1]], memory[code[2]])
    return memory[0]

#print(memory_run(input_list, 12, 2))
for i in range(100):
    for j in range(99,-1,-1):
        if memory_run(input_list, i, j) == 19690720:
            print(100*i + j)
            break

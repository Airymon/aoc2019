from collections import deque
import numpy as np

test_deck = deque(list(range(10)))

def deal_into_stack(stack):
    stack = stack.copy()
    stack.reverse()
    return stack

def cut_n(stack, n):
    stack = stack.copy()
    if n > 0:
        for amount in range(n):
            element = stack.popleft()
            stack.append(element)
    elif n < 0:
        for amount in range(abs(n)):
            element = stack.pop()
            stack.appendleft(element)
    return stack

def deal_with_increment(stack, n):
    stack = stack.copy()
    new_stack = np.zeros(len(stack))
    pos = 0
    for number in stack:
        new_stack[pos] = number
        pos = (pos + n) % len(stack)
    return deque(new_stack.astype(int))

assert list(deal_into_stack(deal_into_stack(deal_with_increment(test_deck, 7)))) == [0,3,6,9,2,5,8,1,4,7]
assert list(deal_into_stack(deal_with_increment(cut_n(test_deck, 6), 7))) == [3,0,7,4,1,8,5,2,9,6]
assert list(cut_n(deal_with_increment(deal_with_increment(test_deck, 7), 9), -2)) == [6,3,0,7,4,1,8,5,2,9]
assert list(cut_n(deal_with_increment(deal_with_increment(cut_n(deal_with_increment(cut_n(cut_n(deal_with_increment(cut_n(deal_into_stack(test_deck), -2), 7), 8), -4), 7), 3), 9), 3), -1)) == [9,2,5,8,1,4,7,0,3,6]

### PART 1

functions = {'deal into new stack': deal_into_stack,
             'cut': cut_n,
             'deal with increment': deal_with_increment}

def check_int(s):
    # helper function to check if we can parse a string into an int
    if s[0] in ('-', '+'):
        return s[1:].isdigit()
    return s.isdigit()

full_deck = deque(list(range(10007)))

with open('input.txt') as f:
    deck = full_deck
    for line in f:
        line = line.rstrip()
        commands = line.split()
        if check_int(commands[-1]):
            arg = int(commands[-1])
            func = ' '.join(commands[:-1])
            deck = functions[func](deck, arg)
        else:
            deck = functions[line](deck)

print("Silver: %i" % deck.index(2019))

### PART 2
rev_instructions = list()
with open('input.txt') as f:
    for line in f:
        line = line.rstrip()
        commands = line.split()
        if check_int(commands[-1]):
            arg = int(commands[-1])
            func = ' '.join(commands[:-1])
        else:
            arg = ''
            func = ' '.join(commands)
        rev_instructions.append((func, arg))

def reverse_operations(operations, size, offset=0, inc_mul=1):
    # process an offset and increment between two adjacent numbers
    # the default increment is 1 but might change according to shuffle
    for instruction in operations:
        if instruction[0] == "deal into new stack":
            # reverse shifts the offset and reverses our increment
            offset -= inc_mul
            inc_mul *= -1
        elif instruction[0] == "deal with increment":
            # take the mod inv of the instruction in the ring
            inc_mul *= pow(instruction[1], size-2, size)
        elif instruction[0] == "cut":
            # push the offset according to the instruction and the increment
            offset += instruction[1] * inc_mul
    return offset, inc_mul

def compute_order(size, repeats, pos, offset, inc_mul):
    # we need to do this repeats times to get to the correct one
    # increment is done by potentiation in the ring of ints mod repeats
    increment = pow(inc_mul, repeats, size)
    # offset as the sum of the geometric series
    offset = offset * (1 - increment) * pow((1 - inc_mul) % size, size-2, size)
    return (offset + pos * increment) % size

n = 10007
r = 1
pos = 7744

offset, mult = reverse_operations(rev_instructions, n)
assert compute_order(n, r, pos, offset, mult) == 2019

n = 119315717514047
r = 101741582076661
pos = 2020

offset, mult = reverse_operations(rev_instructions, n)
print("Gold: %i" % compute_order(n, r, pos, offset, mult))

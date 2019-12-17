def apply_pattern(sequence, pos, start, pattern):
    n = len(pattern)
    startpos = pos - start
    sum = 0
    for i, digit in enumerate(sequence[startpos:]):
        sum += digit * pattern[(i+startpos+1)//pos % n]
    out_dig = abs(sum) % 10
    return out_dig

def compute_phase(sequence, pattern, start):
    new_sequence = list()
    for pos in range(start, len(sequence)+start):
        new_sequence.append(apply_pattern(sequence, pos, start, pattern))
    return new_sequence

def get_fft_encoding(sequence, pattern, num_phases, start=1):
    for phase in range(num_phases):
        sequence = compute_phase(sequence, pattern, start)
    return ''.join(str(x) for i,x in enumerate(sequence) if i < 8)

### TEST PART 1
ex_1 = "12345678"
ex_2 = "80871224585914546619083218645595"
ex_3 = "19617804207202209144916044189917"
ex_4 = "69317163492948606335995924319873"
pattern = [0,1,0,-1]

assert get_fft_encoding([int(x) for x in ex_1], pattern, 4) == "01029498"
assert get_fft_encoding([int(x) for x in ex_2], pattern, 100) == "24176176"
assert get_fft_encoding([int(x) for x in ex_3], pattern, 100) == "73745418"
assert get_fft_encoding([int(x) for x in ex_4], pattern, 100) == "52432133"

### PART 1
with open('input.txt') as f:
    full_input = f.read().strip()

print("Silver: %s" % get_fft_encoding([int(x) for x in full_input], pattern, 100))

### TEST PART 2

def compute_phase_easy(sequence):
    new_sequence = list()
    sum = 0
    for pos in range(len(sequence)-1, -1, -1):
        sum += sequence[pos]
        new_sequence.append(sum % 10)
    return list(reversed(new_sequence))

def get_fft_easy(sequence, num_phases):
    for phase in range(num_phases):
        sequence = compute_phase_easy(sequence)
    return ''.join(str(x) for i,x in enumerate(sequence) if i < 8)

ex_5 = "03036732577212944063491565474664"
ex_6 = "02935109699940807407585447034323"
ex_7 = "03081770884921959731165446850517"

s_5 = int(ex_5[:7])
f_5 = ex_5 * 10000
r_5 = f_5[s_5:]

s_6 = int(ex_6[:7])
f_6 = ex_6 * 10000
r_6 = f_6[s_6:]

s_7 = int(ex_7[:7])
f_7 = ex_7 * 10000
r_7 = f_7[s_7:]

assert get_fft_easy([int(x) for x in r_5], 100) == "84462026"
assert get_fft_easy([int(x) for x in r_6], 100) == "78725270"
assert get_fft_easy([int(x) for x in r_7], 100) == "53553731"

### PART 2
# This is still sort of slow but the problem doesnt generalize well anyways
s_i = int(full_input[:7])
f_i = full_input * 10000
r_i = f_i[s_i:]

print("Gold: %s" % get_fft_easy([int(x) for x in r_i], 100))

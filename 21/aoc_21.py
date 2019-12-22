from intcode import IntcodeComputer

def draw_last_moments(last_moments):
    str = ''
    for num in last_moments:
        str = str + chr(num)
    print(str)

def to_ascii_instruction(instruction):
    ascii_instr = []
    for char in instruction:
        ascii_instr.append(ord(char))
    return ascii_instr

### PART 1

print("\n PART 1 START \n")

with open('input.txt') as f:
    data = f.readline()
    input_list = data.split(',')
input_prog = list(map(int, input_list))

instruction="""NOT C J
OR D T
AND T J
NOT A T
OR T J
WALK
"""

ascii_instr = to_ascii_instruction(instruction)

springdroid = IntcodeComputer(input_prog, ascii_instr, "Spring Droid Machine")
springdroid.run_program()
last_moments = springdroid.get_output()
#draw_last_moments(last_moments)
print("Silver: %i" % last_moments[-1])

### PART 2
print("\n PART 2 START \n")

instruction="""NOT C J
NOT A T
OR T J
NOT B T
OR T J
NOT D T
NOT T T
AND T J
AND E T
OR H T
AND T J
RUN
"""

ascii_instr = to_ascii_instruction(instruction)

springdroid = IntcodeComputer(input_prog, ascii_instr, "Spring Droid Machine")
springdroid.run_program()
last_moments = springdroid.get_output()
#draw_last_moments(last_moments)
print("Gold: %i" % last_moments[-1])

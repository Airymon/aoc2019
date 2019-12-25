from intcode import IntcodeComputer

with open('input.txt') as f:
    data = f.readline()
    input_list = data.split(',')
input_prog = list(map(int, input_list))

def to_ascii_instruction(instruction):
    ascii_instr = []
    for char in instruction:
        ascii_instr.append(ord(char))
    return ascii_instr

def print_output(intcode_instruction):
    str = ''
    for digit in intcode_instruction:
        str = str + chr(digit)
    print(str)

adventure = IntcodeComputer(input_prog, [], "Cryostasis")
adventure.run_program()
output = adventure.get_output()
print_output(output)

while not adventure.has_stopped():
    get_input = input(">")
    input_instruction = to_ascii_instruction(get_input+"\n")
    adventure.add_prog_input(input_instruction)
    adventure.run_program()
    output = adventure.get_output()
    print_output(output)

print("Game Over.")

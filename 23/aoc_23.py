from intcode import IntcodeComputer

with open('input.txt') as f:
    data = f.readline()
    input_list = data.split(',')
input_prog = list(map(int, input_list))


### PART 1
intcode_network = dict()
for i in range(50):
    computer = IntcodeComputer(input_prog, [i], "Network Address %i" % i)
    intcode_network[i] = computer

run_network = True

while run_network:
    for id, computer in intcode_network.items():
        print("Run computer %i" % id)
        computer.run_program()
        output = computer.get_output()
        print(output)
        if output:
            if output[0] == 255:
                run_network = False
                print("Silver: %i" % output[2])
                break
            chunk_size= 3
            for i in range(0, len(output), chunk_size):
                instruction = output[i:i+chunk_size]
                intcode_network[instruction[0]].add_prog_input(instruction[1:])

### PART 2

class NAT():
    def __init__(self):
        self.x = None
        self.y = None

    def add_prog_input(self, instruction):
        self.x = instruction[0]
        self.y = instruction[1]

intcode_network = dict()
for i in range(50):
    computer = IntcodeComputer(input_prog, [i], "Network Address %i" % i)
    intcode_network[i] = computer
intcode_network[255] = NAT()
run_network = True

nat_history = list()

while run_network:
    all_idle = True
    for id, computer in intcode_network.items():
        if id == 255:
            continue
        print("Run computer %i" % id)
        computer.run_program()
        output = computer.get_output()
        print(output)
        if output:
            all_idle = False
            chunk_size= 3
            for i in range(0, len(output), chunk_size):
                instruction = output[i:i+chunk_size]
                intcode_network[instruction[0]].add_prog_input(instruction[1:])
    if all_idle and intcode_network[255].x is not None:
        NAT = intcode_network[255]
        print("NAT sends package to 0")
        print(NAT.x, NAT.y)
        intcode_network[0].add_prog_input([NAT.x, NAT.y])
        if nat_history:
            if nat_history[-1] == NAT.y:
                run_network = False
                print("Gold: %i" % NAT.y)
                break
        nat_history.append(NAT.y)

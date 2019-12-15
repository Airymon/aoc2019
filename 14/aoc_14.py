import random
import math
from collections import defaultdict

class FuelCalculator():
    def __init__(self, input_f):
        self.ORE = 0 # total ore required
        self.reactions = dict() # how reactions work
        self.storage = defaultdict(int) # stores surplus from reaction
        self.requirements = defaultdict(int) # what needs producing
        self.parse_reactions(input_f)

    def parse_reactions(self, input_f):
        with open(input_f) as f:
            all_f = f.readlines()
            for reaction in all_f:
                required, produced = reaction.strip().split('=>')
                p_quant, p_elem = produced.strip().split(' ')
                p_quant = int(p_quant)
                self.reactions[p_elem] = [('YIELD', p_quant)]
                required = required.strip().split(',')
                for entry in required:
                    r_quant, r_elem = entry.strip().split(' ')
                    r_quant = int(r_quant)
                    self.reactions[p_elem].append((r_elem, r_quant))

    def calc_requirement(self, element, requirement):
        if requirement >= self.storage[element]:
            requirement = requirement - self.storage[element]
            self.storage[element] = 0
        else:
            self.storage[element] -= requirement
            requirement = 0
        return requirement

    def chem_reaction(self, element, multiplier=1):
        _, react_yield, materials = *self.reactions[element][0], self.reactions[element][1:]
        for material, requirement in materials:
            if material == 'ORE':
                self.ORE += requirement * multiplier
            else:
                self.requirements[material] += requirement * multiplier
        return react_yield * multiplier

    def produce_element(self, element, requirement):
        requirement = self.calc_requirement(element, requirement)
        _, react_yield = self.reactions[element][0]
        multiplier = math.ceil(requirement / react_yield)
        current_yield = self.chem_reaction(element, multiplier)
        surplus = current_yield - requirement
        self.storage[element] += surplus

    def calculate_cost(self, element, quantity):
        self.requirements[element] += quantity
        while len(self.requirements) > 0:
            element = random.choice(list(self.requirements.keys()))
            self.produce_element(element, self.requirements[element])
            self.requirements.pop(element, None)
        return self.ORE


### PART 1 TESTS
T1 = FuelCalculator('test_1.txt')
assert T1.calculate_cost('FUEL', 1) == 31

T2 = FuelCalculator('test_2.txt')
assert T2.calculate_cost('FUEL', 1) == 165

T3 = FuelCalculator('test_3.txt')
assert T3.calculate_cost('FUEL', 1) == 13312

T4 = FuelCalculator('test_4.txt')
assert T4.calculate_cost('FUEL', 1) == 180697

T5 = FuelCalculator('test_5.txt')
assert T5.calculate_cost('FUEL', 1) == 2210736

### PART 1
FC = FuelCalculator('input.txt')
print("Silver: %i" % FC.calculate_cost('FUEL', 1))

### PART 2
def get_bounds(input_f, resource):
    fuel = 0
    ORE = 0
    while ORE < resource:
        fuel = fuel * 10 if fuel else 1
        FC = FuelCalculator(input_f)
        ORE = FC.calculate_cost('FUEL', fuel)
    u_bound = fuel
    l_bound = fuel // 10
    return u_bound, l_bound

def get_max_fuel(bounds, input_f, resource):
    u_bound, l_bound = bounds
    prev_fuel = 0
    while True:
        fuel = (u_bound + l_bound) // 2
        if prev_fuel == fuel:
            return fuel
        FC = FuelCalculator(input_f)
        ORE = FC.calculate_cost('FUEL', fuel)
        prev_fuel = fuel
        if ORE == resource:
            return fuel
        elif ORE > resource:
            u_bound = fuel
        elif ORE < resource:
            l_bound = fuel

def max_fuel(input_f, resource):
    # find upper and lower bound
    bounds = get_bounds(input_f, resource)
    # binary search for max amount
    fuel = get_max_fuel(bounds, input_f, resource)
    return fuel

max_ore = 1000000000000

assert max_fuel('test_3.txt', max_ore) == 82892753
assert max_fuel('test_4.txt', max_ore) == 5586022
assert max_fuel('test_5.txt', max_ore) == 460664

print("Gold: %i" % max_fuel('input.txt', max_ore))

num_list = []

with open('input.txt') as r:
    for line in r:
        num = int(line)
        num_list.append(num)


def calc_fuel(item):
    fuel = (item//3) - 2
    return fuel

total = 0
for item in num_list:
    fuel_req = calc_fuel(item)
    while fuel_req > 0:
        total += fuel_req
        fuel_req = calc_fuel(fuel_req)

print(total)

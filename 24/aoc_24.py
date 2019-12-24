import time

def read_into_array(map_string):
    full_map = list()
    for line in map_string.splitlines():
        line = line.rstrip()
        x_coord = list()
        for char in line:
            x_coord.append(char)
        full_map.append(x_coord)
    return full_map

def display_map(eris_map, display=True):
    str = ""
    for row in eris_map:
        for char in row:
            str = str + char
        str = str + '\n'
    if display:
        print(str)
    return str

def get_neighbors(position):
    pos_x, pos_y = position
    neighbors = {(pos_x+1, pos_y), (pos_x-1, pos_y), (pos_x, pos_y+1), (pos_x, pos_y-1)}
    if pos_x == 0:
        neighbors.discard((pos_x-1, pos_y))
    elif pos_x == 4:
        neighbors.discard((pos_x+1, pos_y))
    if pos_y == 0:
        neighbors.discard((pos_x, pos_y-1))
    elif pos_y == 4:
        neighbors.discard((pos_x, pos_y+1))
    return neighbors

def run_one_step(eris_map):
    new_map = list()
    for y in range(len(eris_map)):
        x_coords = list()
        for x in range(len(eris_map[0])):
            neighbors = get_neighbors((x,y))
            n_count = 0
            for neighbor in neighbors:
                pos_x, pos_y = neighbor
                if eris_map[pos_y][pos_x] == '#':
                    n_count +=1
            if eris_map[y][x] == '#':
                if n_count == 1:
                    x_coords.append('#')
                else:
                    x_coords.append('.')
            else:
                if n_count == 1 or n_count == 2:
                    x_coords.append('#')
                else:
                    x_coords.append('.')
        new_map.append(x_coords)
    return new_map

def find_repeating_state(eris_map):
    map_history = set()
    min = 0
    while True:
        display_str = display_map(eris_map, display=False)
        if display_str not in map_history:
            map_history.add(display_str)
        else:
            return eris_map, min
        eris_map = run_one_step(eris_map)
        min += 1

def calculate_biodiversity_score(eris_map):
    flat_map = [item for sublist in eris_map for item in sublist]
    score = 0
    for pos, entry in enumerate(flat_map):
        if entry == '#':
            score += pow(2, pos)
    return score

### TEST PART 1

test_input="""....#
#..#.
#..##
..#..
#...."""

test_map = read_into_array(test_input)
goal_map, minute = find_repeating_state(test_map)
assert calculate_biodiversity_score(goal_map) == 2129920

### PART 1

with open('input.txt') as f:
    map_str = f.read()
full_map = read_into_array(map_str)
goal_map, minute = find_repeating_state(full_map)
print("After %i minutes:" % minute)
display_map(goal_map)
print("Silver: %i" % calculate_biodiversity_score(goal_map))

### PART 2

test_input="""....#
#..#.
#.?##
..#..
#...."""

def generate_empty_map(eris_map):
    empty_map = list()
    for layer in eris_map:
        empty_layer = list()
        for char in layer:
            if char == '?':
                empty_layer.append(char)
            else:
                empty_layer.append('.')
        empty_map.append(empty_layer)
    return empty_map

def get_neighbors_recursive(current_layer_num, position):
    pos_x, pos_y = position
    neighbors = {(current_layer_num, pos_x+1, pos_y),
                 (current_layer_num, pos_x-1, pos_y),
                 (current_layer_num, pos_x, pos_y+1),
                 (current_layer_num, pos_x, pos_y-1)}
    if pos_x == 0:
        neighbors.add((current_layer_num-1, 1, 2))
        neighbors.discard((current_layer_num, pos_x-1, pos_y))
    elif pos_x == 4:
        neighbors.add((current_layer_num-1, 3, 2))
        neighbors.discard((current_layer_num, pos_x+1, pos_y))
    if pos_y == 0:
        neighbors.add((current_layer_num-1, 2, 1))
        neighbors.discard((current_layer_num, pos_x, pos_y-1))
    elif pos_y == 4:
        neighbors.add((current_layer_num-1, 2, 3))
        neighbors.discard((current_layer_num, pos_x, pos_y+1))
    if pos_x == 2 and pos_y == 1:
        neighbors.discard((current_layer_num, pos_x, pos_y+1))
        for x in range(5):
            neighbors.add((current_layer_num+1, x, 0))
    elif pos_x == 2 and pos_y == 3:
        neighbors.discard((current_layer_num, pos_x, pos_y-1))
        for x in range(5):
            neighbors.add((current_layer_num+1, x, 4))
    elif pos_x == 1 and pos_y == 2:
        neighbors.discard((current_layer_num, pos_x+1, pos_y))
        for y in range(5):
            neighbors.add((current_layer_num+1, 0, y))
    elif pos_x == 3 and pos_y == 2:
        neighbors.discard((current_layer_num, pos_x-1, pos_y))
        for y in range(5):
            neighbors.add((current_layer_num+1, 4, y))
    return neighbors

def recursive_grid(eris_map, num_steps):
    empty_map = generate_empty_map(eris_map)
    recursive_layers = dict()
    start_layer = 0
    recursive_layers[start_layer] = eris_map
    for step in range(num_steps):
        if step % 2 == 0:
            min_layer = min(recursive_layers.keys())
            max_layer = max(recursive_layers.keys())
            recursive_layers[min_layer-1] = [x[:] for x in empty_map]
            recursive_layers[max_layer+1] = [x[:] for x in empty_map]
        new_recursive_layer = dict()
        for layer, layer_map in recursive_layers.items():
            new_map = list()
            for y in range(len(eris_map)):
                x_coords = list()
                for x in range(len(eris_map[0])):
                    neighbors = get_neighbors_recursive(layer, (x, y))
                    n_count = 0
                    for neighbor in neighbors:
                        neighbor_layer, neighbor_x, neighbor_y = neighbor
                        if neighbor_layer not in recursive_layers:
                            continue
                        if recursive_layers[neighbor_layer][neighbor_y][neighbor_x] == '#':
                            n_count += 1
                    if layer_map[y][x] == '#':
                        if n_count == 1:
                            x_coords.append('#')
                        else:
                            x_coords.append('.')
                    elif layer_map[y][x] == '?':
                        x_coords.append('?')
                    else:
                        if n_count == 1 or n_count == 2:
                            x_coords.append('#')
                        else:
                            x_coords.append('.')
                new_map.append(x_coords)
            new_recursive_layer[layer] = new_map
        recursive_layers = new_recursive_layer
    return recursive_layers

def count_bugs(recursive_layers):
    count = 0
    for layer in recursive_layers.values():
        for axis in layer:
            for tile in axis:
                if tile == '#':
                    count +=1
    return count

def print_layers(all_layers):
    for layer, layer_map in sorted(all_layers.items()):
        print("Layer %i" % layer)
        display_map(layer_map)

test_map = read_into_array(test_input)
all_layers = recursive_grid(test_map, 10)
assert count_bugs(all_layers) == 99
print("After 10 minutes:")
print_layers(all_layers)

full_map_pt_2 = [x[:] for x in full_map]
full_map_pt_2[2][2] = '?'
all_layers = recursive_grid(full_map_pt_2, 200)
print("Gold: %i" % count_bugs(all_layers))
#print_layers(all_layers)

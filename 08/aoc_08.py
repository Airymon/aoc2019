import numpy as np

sample_format = [2,3]
sample_input = '123456789012'

def format_image(input_string, format):
    array = [int(c) for c in input_string]
    layer_size = len(array) // np.prod(format)
    array = np.array(array).reshape(layer_size, format[0], format[1])
    return array

def calculate_min_zeros_product(image):
    counts = {}
    for i, layer in enumerate(image):
        counts[i] = np.count_nonzero(layer==0)
    min_layer = min(counts, key=counts.get)
    ones = np.count_nonzero(image[min_layer]==1)
    twos = np.count_nonzero(image[min_layer]==2)
    return ones * twos

assert calculate_min_zeros_product(format_image(sample_input, sample_format)) == 1

with open('input.txt') as f:
    full_input = f.readline().rstrip()

full_format = [6,25]
full_image = format_image(full_input, full_format)
print("Silver: %i" % calculate_min_zeros_product(full_image))

### PART 2

test_input = '0222112222120000'
test_shape = [2,2]

def decode_image(image, format):
    decoded_image = np.full(format, 2)
    for layer in reversed(image):
        layer_pos = np.where(layer!=2)
        decoded_image[layer_pos] = layer[layer_pos]
    return decoded_image

assert np.ndarray.flatten(decode_image(format_image(test_input, test_shape), test_shape)).tolist() == [0,1,1,0]

def print_image(image):
    for row in image:
        for pixel in row:
            print("X" if pixel == 1 else " ", end="")
        print("")

print("Gold: ")
print_image(decode_image(full_image, full_format))

input = [246540,787419]

def two_same_digits(number):
    prev = '0'
    prev_2 = '0'
    t_val = False
    for i, digit in enumerate(number):
        if i == 1:
            if digit is prev:
                t_val = True
            prev_2 = prev
            prev = digit
        if i > 1:
            if t_val and int(digit) > int(prev):
                return True
            elif digit is prev and digit is not prev_2:
                t_val = True
            elif digit is prev and digit is prev_2:
                t_val = False
            prev_2 = prev
            prev = digit
        else:
            prev = digit
    return t_val

def non_decreasing(number):
    prev = 0
    for digit in number:
        if int(digit) < prev:
            return False
        prev = int(digit)
    return True

count = 0
for i in range(input[0], input[1]):
    number = str(i) #[int(n) for n in str(i)]
    if two_same_digits(number) and non_decreasing(number):
        count +=1
print(count)

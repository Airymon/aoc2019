input = [246540,787419]

def non_decreasing(i_range):
     return (x for x in i_range if
                all(int(a) <= int(b) for a,b in zip(str(x), str(x)[1:])))

def dubs(i_range):
    return (x for x in i_range if
                any(val == 2 for val in [str(x).count(c) for c in str(x)]))

print(len(set(non_decreasing(dubs(range(*input))))))

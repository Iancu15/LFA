'''
-------------------- Exercise 1 --------------------
90
-------------------- Exercise 2 --------------------
89
-------------------- Exercise 3 --------------------
[2, 0, 1, 5, 4]
-------------------- Exercise 4 --------------------
False
True
True
-------------------- Exercise 5 --------------------
[5, 6, 7, 8, 9]
-------------------- Exercise 6 --------------------
{'f': 1, 'o': 2, 'r': 1, 'm': 2, 'a': 7, 'l': 2, ' ': 3, 'n': 2, 'g': 2, 'u': 2, 'e': 1, 's': 1, 'd': 1, 't': 2}
-------------------- Exercise 7 --------------------
['g', 'u', 'd', 'f', 'l', 's', 'r', 'e', 'm', 't', 'a', 'o', 'n', ' ']
-------------------- Exercise 8 --------------------
[('Popescu', 27), ('Ionescu', 29)]
-------------------- Exercise 9 --------------------
[0]
[3, 2]
[1, 2, 4, 5]
'''

from functools import reduce

def ex1(l):
    max_num = l[0]
    for e in l:
        max_num = max(max_num, e)
    return max_num

def ex2(l, start, stop):
    max_num = l[start]
    for e in l[start:stop]:
        max_num = max(max_num, e)
    return max_num

def ex3(l):
    max_size = 0
    max_slice = None
    start = -1
    for i in range(0, len(l)):
        e = l[i]
        if start == -1 and e > 0:
            start = i
        if start >= 0 and e < 0:
            size = i - start
            if size > max_size:
                max_slice = l[start:i]
                max_size = size
            start = -1

    end = len(l) - 1
    size = end - start
    if start >= 0 and size > max_size:
        max_slice = l[start:end]

    return max_slice

def ex4(l):
    isPalindrom = True
    for i in range(0, round(len(l) / 2)):
        if l[i] != l[-(i + 1)]:
            isPalindrom = False

    return isPalindrom

def ex5(l):
    l.sort()
    stack = l[:]
    end = len(stack) - 1
    i = end - 1
    prev = stack.pop()
    max_slice = [prev]
    max_size = 1
    size = 1
    while len(stack) > 0:
        e = stack.pop()
        if e == prev - 1:
            size += 1
        else:
            if size > max_size:
                max_size = size
                max_slice = l[i + 1:end + 1]
            end = i
            size = 1
        prev = e
        i -= 1

    if size > max_size:
        max_slice = l[0:end]

    return max_slice


def ex6(l):
    d = {}
    for e in l:
        if e in d:
            d[e] += 1
        else:
            d[e] = 1

    return d

def ex7(l):
    s = set()
    for e in l:
        s.add(e)

    return s

def age_and_gender(x):
    year = "19" + x[1:3]
    if x[0] == '5' or x[0] == '6':
        year = "20" + x[1:3]

    gender = 'F'
    if x[0] == '1' or x[0] == '5':
        gender = 'M'

    return (2021 - int(year), gender)

def ex8(l):
    lst = [(x, age_and_gender(y[0:3])) for (_, x, y) in l]
    avg_age = reduce(lambda x, y: x + y, map(lambda x: x[1][0], lst)) / len(lst)
    return [(x, y) for (x, (y, _)) in filter(lambda x: x[1][0] < avg_age and x[1][1] == 'F', lst)]

def ex9(file, source):
    f = open(file, "r")
    line = f.readline()
    d = {}
    n = int(line)
    for i in range(0, int(n)):
        d[i] = []

    line = f.readline()
    while line:
        splitted_line = line.split(" ")
        if splitted_line[1] == 'O':
            src = int(splitted_line[0])
            dest = int(splitted_line[2])
            d[src].append(dest)
        line = f.readline()

    l = [source]
    stack = [source]
    while len(stack) > 0:
        curr = stack.pop()
        for e in d[curr]:
            if e not in l:
                l.append(e)
                stack.append(e)

    return l


def main():
    print('-------------------- Exercise 1 --------------------')
    l = [9, 34, 56, 7, 89, 2, 90, 67, 23, 5]
    print(ex1(l))

    print('-------------------- Exercise 2 --------------------')
    l = [9, 34, 56, 7, 89, 2, 90, 67, 23, 5]
    start, stop = 2, 5
    print(ex2(l, start, stop))

    print('-------------------- Exercise 3 --------------------')
    l = [1, 3, -1, 2, 0, 1, 5, 4, -2, 4, 5, -3, 0, 1, 2]
    print(ex3(l))

    print('-------------------- Exercise 4 --------------------')
    l1 = [9, 34, 56, 7, 89, 2, 90, 67, 23, 5]
    l2 = [2, 1, 3, 2, 4, 4, 2, 3, 1, 2]
    l3 = [2, 1, 3, 2, 4, 9, 4, 2, 3, 1, 2]
    print(ex4(l1))
    print(ex4(l2))
    print(ex4(l3))

    print('-------------------- Exercise 5 --------------------')
    l = [7, 56, 44, 5, 77, 6, 9, 67, 8, 5]
    print(ex5(l))

    print('-------------------- Exercise 6 --------------------')
    l = 'formal languages and automata'
    print(ex6(l))

    print('-------------------- Exercise 7 --------------------')
    l = 'formal languages and automata'
    print(ex7(l))

    print('-------------------- Exercise 8 --------------------')
    l = [('Ana', 'Popescu', '2940101375829'), ('Maria', 'Ionescu', '2920101675835'),
         ('Matei', 'Teodorescu', '5020101673498'), ('Andreea', 'Florescu', '2780101437865')]
    print(ex8(l))

    print('-------------------- Exercise 9 --------------------')
    file = 'ex9.txt'
    source1, source2, source3 = 0, 3, 1
    print(ex9(file, source1))
    print(ex9(file, source2))
    print(ex9(file, source3))

if __name__ == "__main__":
    main()

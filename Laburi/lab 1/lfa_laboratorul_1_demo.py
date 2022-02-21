# python - multi-paradigm programming language
# coding style - imperative, procedural, object-oriented, functional

# python --version
# python3 --version
# https://docs.python.org/3.9/

# the product of the list elements
l = [1, 5, 4, 3, 7]

# imperative
product = 1
for e in l:
    product *= e
print(product)

# procedural
def compute_product(l):
    product = 1
    for e in l:
        product *= e
    return product
print(compute_product(l))

# object-oriented
class ListOp(object):
    def __init__(self, l):
        self.l = l
    def compute_product(self):
        self.product = 1
        for e in l:
            self.product *= e
x = ListOp(l)
x.compute_product()
print(x.product)

# functional
from functools import reduce
from types import resolve_bases
product = reduce(lambda x, y: x * y, l)
print(product)

# PEP 8 - style guide for python code
#  https://www.python.org/dev/peps/pep-0008
# pylint - code analysis for python

# type(param) - param type
# type annotations
# https://docs.python.org/3.9/library/typing.html

# built-in functions
# https://docs.python.org/3.9/library/functions.html

# from typing import List
# def compute_sum_k(l: List[int], k: int) -> int:
def compute_sum_k(l: list, k: int) -> int:
    return sum(l[:k])
print(compute_sum_k(l, 3))

def print_str(s: str) -> None:
    print(s)
print_str('formal langugages and automata')

# data structures
# https://docs.python.org/3.9/tutorial/datastructures.html
# list, stack - l = list() or [] - ordered, mutable
#   list slicing l[start:stop:step]
#   list comprehension [<expr> for <elem> in <it>]
# dict - d = dict() or {} - keeps the insertion order of keys, mutable
# set - s = set() or {} - unordered, mutable, no duplicates
#   union - s1 | s2
#   intersection - s1 & s2
#   difference - s1 - s2
#   symmetric difference - s1 ^ s2
# fronzenset - s = frozenset(ds) - unordered, immutable, no duplicates, hashable
# tuple - t = tuple() or () - ordered, immutable, hashable
# https://www.geeksforgeeks.org/differences-and-applications-of-list-tuple-set-and-dictionary-in-python/

for i in range(len(l)):
    print(l[i])

for e in l:
    print(e)

for i, e in enumerate(l):
    print((i, e))

print([x**3 for x in l])

# lambda expression - lambda <args>: <expr>
# map - map(<func>, <it>)
# filter - filter(<func>, <it>)
# reduce - reduce(<func>, <it>)
# casting map/filter object to list object

from math import exp

def square(x):
    return x**2

print(list(map(square, l)))
print(list(map(exp, l)))
print(list(map(int, ['1', '2', '3'])))
print(list(map(lambda x: x + 1, l)))

print(list(filter(lambda x: x > 3, l)))
print(list(filter(lambda x: x % 2 == 0 and x < 5, l)))

print(reduce(lambda x, y: x + y, l))
print(reduce(lambda x, y: max(x, y), l))
print(reduce(lambda x, y: x if x > y else y, l))

# is - True for the same object
# == - True for equal object
r = l
print(r is l, r == l)
r = l[:]
print(r is l, r == l)

# _ - ignore a value
# functions with any number of arguments
#   *args - positional arguments assigned to args tuple
#   **kwargs - keyword arguments assigned to kwargs tuple

def demo(x, y=1, *args, **kwargs):
    print('x :', x)
    print('y :', y)
    print('args: ', args)
    print('kwargs: ', kwargs)

    _ = sum(args)

demo(10, 20, 30, 40, a=50, b=60)
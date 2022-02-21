import sys

class Expr:
    pass

class Symbol(Expr):
    def __init__(self, x):
        self.x = x

    def __str__(self):
        return f'{self.x}'

    # in situatia noastra Symbol practic ar fi mereu complet ca fix dupa ce
    # citesc simbolul il adaug in stiva ca Symbol(token)
    def is_completed(self):
        if self.x != None:
            return True

        return False

class Concat(Expr):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        if isinstance(self.x, Union) and isinstance(self.y, Union):
            return f'({self.x})({self.y})'
        elif isinstance(self.x, Union) and isinstance(self.y, Union) == False:
            return f'({self.x}){self.y}'
        elif isinstance(self.x, Union) == False and isinstance(self.y, Union):
            return f'{self.x}({self.y})'
        else:
            return f'{self.x}{self.y}'

    def is_completed(self):
        if self.x != None and self.y != None:
            return True

        return False

class Star(Expr):
    def __init__(self, x):
        self.x = x

    def __str__(self):
        if isinstance(self.x, Symbol):
            return f'{self.x}*'
        else:
            return f'({self.x})*'

    def is_completed(self):
        if self.x != None:
            return True

        return False

class Union(Expr):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f'{self.x} U {self.y}'

    def is_completed(self):
        if self.x != None and self.y != None:
            return True

        return False

def process_expr(s: str) -> Expr:
    tokens = (sys.argv[1]).split(" ")
    stack = []

    for token in tokens:
        if token == "CONCAT":
            stack.append(Concat(None, None))
        elif token == "STAR":
            stack.append(Star(None))
        elif token == "UNION":
            stack.append(Union(None, None))
        else:
            stack.append(Symbol(token))

        while len(stack) > 1:
            expr1 = stack.pop()
            # daca ultimul element din stiva nu e completat, atunci n-am ce
            # reducere sa fac pentru ca reduc adaugand elemente completate in
            # elemente necompletate
            if expr1.is_completed() == False:
                stack.append(expr1)
                break

            expr2 = stack.pop()
            # daca penultimul element e completat, atunci si restul sunt
            # completate pentru ca altfel ar fi facut parte dintr-un alt
            # element
            if expr2.is_completed():
                stack.append(expr2)
                stack.append(expr1)
                break

            if isinstance(expr2, Star):
                stack.append(Star(expr1))
            elif isinstance(expr2, Union):
                if expr2.x == None:
                    stack.append(Union(expr1, None))
                else:
                    stack.append(Union(expr2.x, expr1))
            elif isinstance(expr2, Concat):
                if expr2.x == None:
                    stack.append(Concat(expr1, None))
                else:
                    stack.append(Concat(expr2.x, expr1))

    if len(stack) > 1:
        return None

    return stack.pop()

# format python3 dfa-regexp.py [string in prenex form]
# exemplu python3 dfa-regexp.py "CONCAT STAR UNION a b STAR c"
def main():
    if len(sys.argv) < 2:
        print("Enter command arguments!")
        return

    expr = process_expr(sys.argv[1])
    if (expr == None):
        print("Invalid prenex form!")
    else:
        print(expr)

if __name__ == "__main__":
    main()

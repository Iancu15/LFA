from ast import *

def interpret_expr(expr, store):
    if expr.type == 'v':
        return store[expr.left]
    elif expr.type == 'i':
        return int(expr.left)

    result_left = interpret_expr(expr.left, store)
    result_right = interpret_expr(expr.right, store)

    def add():
        return result_left + result_right

    def sub():
        return result_left - result_right

    def product():
        return result_left * result_right

    def greaterthan():
        return result_left > result_right

    def equals():
        return result_left == result_right

    switcher = {
        '+': add(),
        '-': sub(),
        '*': product(),
        '>': greaterthan(),
        '==': equals(),
    }

    return switcher.get(expr.type)

def interpret_instruction_list(list, store):
    for prog in list:
        store = interpret_prog(prog, store)

    return store

def interpret_while(expr, prog, store):
    while (interpret_expr(expr, store)):
        store = interpret_prog(prog, store)

    return store

def interpret_if(expr, then_branch, else_branch, store):
    if (interpret_expr(expr, store)):
        return interpret_prog(then_branch, store)
    else:
        return interpret_prog(else_branch, store)

def interpret_assign(variable, expr, store):
    store[variable.left] = interpret_expr(expr, store)
    return store

def interpret_prog(prog, store):
    if isinstance(prog, InstructionList):
        return interpret_instruction_list(prog.list, store)
    elif isinstance(prog, While):
        return interpret_while(prog.expr, prog.prog, store)
    elif isinstance(prog, If):
        return interpret_if(prog.expr, prog.then_branch, prog.else_branch, store)
    elif isinstance(prog, Assign):
        return interpret_assign(prog.variable, prog.expr, store)

def interpret_code(prog):
    return interpret_prog(prog, {})

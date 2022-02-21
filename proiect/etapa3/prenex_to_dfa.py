from prenex_to_expr import process_expr
from make_nfa import Nfa
from make_dfa import Basic_Dfa
import sys

def prenex_to_dfa(prenex_form):
    expr = process_expr(prenex_form)
    if (expr == None):
        print("Invalid prenex form!")

    nfa = Nfa(expr)
    dfa = Basic_Dfa(nfa)
    return dfa

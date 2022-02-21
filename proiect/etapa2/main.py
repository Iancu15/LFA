from make_regex import process_expr
from make_nfa import Nfa
from make_dfa import Dfa
import sys

# format python3 main.py [input file] [output file]
# exemplu python3 main.py testxy.in testxy.out
def main():
    if len(sys.argv) < 2:
        print("Enter command arguments!")
        return

    f = open(sys.argv[1], "r")
    prenex_form = f.read()
    expr = process_expr(prenex_form)
    if (expr == None):
        print("Invalid prenex form!")

    nfa = Nfa(expr)
    dfa = Dfa(nfa)
    g = open(sys.argv[2], "w")
    g.write(dfa.get_alphabet() + "\n")
    g.write(repr(dfa.get_number_of_states()) + "\n")
    g.write(repr(dfa.get_initial_state()) + "\n")

    for final_state in dfa.get_final_states():
        g.write(repr(final_state) + " ")

    g.write("\n")
    for (start_state, letter), end_state in dfa.get_delta().items():
        g.write(repr(start_state) + ",'" + letter + "'," + repr(end_state) + "\n")

if __name__ == "__main__":
    main()

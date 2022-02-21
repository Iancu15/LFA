from transform_to_prenex import parse_regex
from prenex_to_dfa import prenex_to_dfa
import sys

def process_lex_file(lex_file):
    f = open(lex_file, "r")
    dfas = []
    while True:
        line = f.readline()
        if line == "":
            break

        splitted_line = line.split(' ', 1)
        prenex_form = parse_regex(splitted_line[1].split(';')[0])
        dfa = prenex_to_dfa(prenex_form)
        

# format: python3 main.py [lex file] [input file] [output file]
# exemplu: python3 main.py tests/T3/regex/T3.1/T3.1.lex tests/T3/regex/T3.1/input/T1.1.1.in out
def main():
    if len(sys.argv) < 3:
        print("Enter command arguments!")
        return

    process_lex_file(sys.argv[1])

if __name__ == "__main__":
    main()

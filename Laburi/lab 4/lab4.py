import sys

class Dfa:
    def __init__(self, file):
        f = open(file, "r")
        self.initial_state = int(f.readline())
        self.alphabet = set()
        self.final_states = set()
        self.delta = {}
        # n se afla pe a doua linie si reprezinta numarul de configuratii
        # (aveam nevoie de el sa stiu cand ajung la ultima linie)
        n = int(f.readline())
        line = f.readline()
        for i in range(0, n):
            splitted_line = line.split(" ")
            self.delta[(State(int(splitted_line[0])), splitted_line[1])] = State(int(splitted_line[2]))
            self.alphabet.add(splitted_line[1])
            line = f.readline()

        splitted_line = line.split(" ")
        for e in splitted_line:
            self.final_states.add(int(e))

    def next_configuration(self, configuration):
        (state, word) = configuration
        if (state, word[0]) not in self.delta:
            return None

        next_state = self.delta[(state, word[0])]
        return (next_state, word[1:])

    def is_accepted(self, word):
        configuration = (State(self.initial_state), word)
        while 1:
            configuration = self.next_configuration(configuration)
            if configuration is None:
                return False

            (next_state, next_word) = configuration
            if next_word == '':
                return next_state.value in self.final_states

class State:
    def __init__(self, value):
        self.value = value

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.value == other.value
        else:
            return False

    def __repr__(self):
        return "%s" % self.value

def add_token(is_accepted_prev, lexem):
    (is_accepted_prev_3, is_accepted_prev_4, is_accepted_prev_5) = is_accepted_prev
    if is_accepted_prev_3:
        return "3:" + lexem

    if is_accepted_prev_4:
        return "4:" + lexem

    if is_accepted_prev_5:
        return "5:" + lexem

    return None

def process_word(dfa_3, dfa_4, dfa_5, word):
    next_lexem_start = 0;
    output = ""
    while next_lexem_start < len(word):
        is_accepted_prev = (False, False, False)
        for i in range(next_lexem_start, len(word)):
            is_accepted_3 = dfa_3.is_accepted(word[next_lexem_start:i + 1])
            is_accepted_4 = dfa_4.is_accepted(word[next_lexem_start:i + 1])
            is_accepted_5 = dfa_5.is_accepted(word[next_lexem_start:i + 1])
            if (is_accepted_3, is_accepted_4, is_accepted_5) == (False, False, False):
                if is_accepted_prev == (False, False, False):
                    return None

                lexem = word[next_lexem_start:i]
                next_lexem_start = i
                lexem_token_str = add_token(is_accepted_prev, lexem)
                output += " " + lexem_token_str
                break
            elif i == len(word) - 1:
                lexem = word[next_lexem_start:i + 1]
                next_lexem_start = i + 1
                is_accepted = (is_accepted_3, is_accepted_4, is_accepted_5)
                lexem_token_str = add_token(is_accepted, lexem)
                output += " " + lexem_token_str

            is_accepted_prev = (is_accepted_3, is_accepted_4, is_accepted_5)

    return output[1:]

# format: python3 lab4.py [word]
# exemplu: python3 lab4.py abaaabbabaaaab
def main():
    if len(sys.argv) < 2:
        print("Enter command arguments!")
        return

    dfa_3 = Dfa("dfa-3.txt")
    dfa_4 = Dfa("dfa-4.txt")
    dfa_5 = Dfa("dfa-5.txt")
    output = process_word(dfa_3, dfa_4, dfa_5, sys.argv[1])
    if output == None:
        print("Eroare de parsare!")
    else:
        print(output)

if __name__ == "__main__":
    main()

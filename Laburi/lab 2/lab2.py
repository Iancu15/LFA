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

# format: python3 lab2.py [next_configuration|is_accepted] [word] [state]
# exemplu: python3 lab2.py next_configuration a 0
def main():
    if len(sys.argv) < 3:
        print("Enter command arguments!")
        return
    dfa = Dfa("dfa.txt")

    if sys.argv[1] == "next_configuration":
        print(dfa.next_configuration((State(int(sys.argv[3])), sys.argv[2])))
    else:
        print(dfa.is_accepted(sys.argv[2]))

if __name__ == "__main__":
    main()

from transform_to_prenex import parse_regex
from make_dfa import Basic_Dfa
from prenex_to_expr import process_expr
from make_nfa import Nfa
from parser import parse_lexems
from interpreter import interpret_code
import sys

class Dfa:
	def find_sink_states(self):
		delta_inverse = {}
		# creez multimea tranzitiilor inverse, cum o stare poate avea mai
		# multi predecesori cu o tranzitie ce are aceeasi litera, dictionarul
		# va returna o lista cu toti predecesorii
		for (start_state, letter), end_state in self.delta.items():
			if (end_state, letter) not in delta_inverse:
				delta_inverse[(end_state, letter)] = [start_state]
			else:
				start_states = delta_inverse[(end_state, letter)]
				start_states.append(start_state)

		not_sink_states = []
		stack = []
		not_sink_states.extend(self.final_states)
		stack.extend(self.final_states)
		# parcurg cu DFS de la starile finale la orice alte stari in care
		# se poate ajunge din acestea pe tranzitiile inverse
		# toate aceste stari nu vor sink states
		while len(stack) > 0:
			end_state = stack.pop()
			for letter in self.alphabet:
				try:
					start_states = delta_inverse[(end_state, letter)]
					for start_state in start_states:
						if start_state not in not_sink_states:
							stack.append(start_state)
							not_sink_states.append(start_state)
				except KeyError:
					pass

		# orice stare care nu apartine multimii de stari care nu sunt sink
		# states vor fi sink states
		self.sink_states = set()
		for (start_state, letter), end_state in self.delta.items():
			if start_state not in not_sink_states:
				self.sink_states.add(start_state)
			if end_state not in not_sink_states:
				self.sink_states.add(end_state)

		# iau un sink state din multime pe care il desemnez sink state default
		# toate tranzitiile nedefinite in DFA vor ajunge in acest sink state
		self.default_sink_state = State(None)
		for sink_state in self.sink_states:
			self.default_sink_state = sink_state
			break

	def __init__(self, basic_dfa, token, word):
		self.word = word
		self.alphabet = basic_dfa.get_alphabet()
		self.token = token
		self.initial_state = basic_dfa.get_initial_state()
		self.final_states = basic_dfa.get_final_states()
		self.delta = basic_dfa.get_delta()
		self.find_sink_states()

	# configuratia e formata din stare, ultimul index al cuvantului relativ la
	# input si un bool ce zice daca starea in care s-a ajuns e sink state sau nu
	def next_configuration(self, configuration):
		(state, last_index, is_sink_state) = configuration
		if state == None:
			state = self.initial_state

		last_char = self.word[last_index]
		next_index = last_index + 1
		if is_sink_state:
			return (state, next_index, is_sink_state)

		if (state, last_char) not in self.delta:
			return (self.default_sink_state, next_index, True)

		next_state = self.delta[(state, last_char)]
		if next_state in self.sink_states:
			return (next_state, next_index, True)

		return (next_state, next_index, is_sink_state)

	# intoarce None daca e in sink state, False daca e intr-o stare non finala
	# ce nu e sink state si True daca este intr-o stare finala
	def is_accepted(self, configuration):
		(state, last_index, is_sink_state) = configuration
		if is_sink_state:
			return None

		if state not in self.final_states:
			return False

		return True

	def get_token(self):
		return self.token

	def __repr__(self):
		return repr(self.alphabet +
		" | " + self.token +
		" | " + repr(self.initial_state) +
		" | " + repr(self.final_states) +
		" | " + repr(self.delta) +
		" | " + repr(self.sink_states))

class State:
	def __init__(self, value):
		self.value = value

	def __hash__(self):
		return hash(self.value)

	# pentru set
	def __eq__(self, other):
		if isinstance(other, self.__class__):
			return self.value == other.value
		else:
			return False

	def __repr__(self):
		return "%s" % self.value

	# pentru parcugerea tranzitiilor din delta
	def __iter__(self):
		return iter(self.value)

# intoarce perechea token lexem
# token-ul este cel al DFA-ului cu prioritate cea mai mare
def get_lexem_token_pair(is_accepted_prev, dfas, lexem):
	for i in range(0, len(is_accepted_prev)):
		if is_accepted_prev[i]:
			return (dfas[i].get_token(), lexem.replace('\n', '\\n'))

	return None

# intoarce True daca toate DFA-urile au ajuns in sink state, False altfel
def all_reject(is_accepted):
	for is_accepted_elem in is_accepted:
		if is_accepted_elem != None:
			return False

	return True

def process_word(dfas, word, output_file, process_type):
	if process_type == "lexer":
		g = open(output_file, "w")

	lexem_token_pairs = []
	next_lexem_start = 0;

	# newlines retine pozitiile din fisier a newlines-urilor precedente
	# literei procesate curent
	newlines = []
	while next_lexem_start < len(word):
		is_accepted_prev = [False for i in range(0, len(word))]
		configs = [dfa.next_configuration((None, next_lexem_start, False)) for dfa in dfas]
		last_accepted_index = -1;
		# parcurg restul inputului de la start-ul urmatorului posibil lexem
		for i in range(next_lexem_start, len(word)):
			if word[i] == '\n' and i not in newlines:
				newlines.append(i)

			is_accepted = [dfas[i].is_accepted(configs[i]) for i in range(0, len(dfas))]
			if any(is_accepted):
				# daca s-a consumat inputul si lexem-ul format e acceptat
				# de vreun DFA, atunci se scrie perechea token lexem si se
				# termina programul
				if i == len(word) - 1:
					lexem = word[next_lexem_start:i + 1]
					next_lexem_start = i + 1
					lexem_token_pair = get_lexem_token_pair(is_accepted, dfas, lexem)
					lexem_token_pairs.append(lexem_token_pair)
					if process_type == "lexer":
						(token, lexem) = lexem_token_pair
						lexem_token_str = token + " " + lexem
						g.write(lexem_token_str)

					break

				# daca este acceptat de vreun DFA si nu s-a ajuns la final,
				# atunci este salvata ultima pozitie a lexem-ului acceptat
				# si starea lexer-ului in acel moment (daca DFA-urile erau
				# in cautare, acceptau sau respingeau)
				is_accepted_prev = is_accepted
				last_accepted_index = i
			else:
				if all_reject(is_accepted):
					# daca toate DFA-urile au ajuns in sink state si nu a
					# fost un lexem acceptat anterior, atunci afisez eroare
					# in format-ul din enunt cu caracterul si linia la care
					# se afla
					if last_accepted_index == -1:
						g.close()
						g = open(output_file, "w")
						char_index = i

						# contorizez caracterul de la ultimul newline de
						# dinainte de acesta
						if len(newlines) > 0:
							char_index -= newlines[-1] + 1

						g.write("No viable alternative at character " +
						repr(char_index) + ", line " + repr(len(newlines)))
						g.close()
						return

					# daca toate DFA-urile au ajuns in sink state si a fost
					# un lexem acceptat anterior se va lua acela cu ultimul
					# index cel mai mare
					lexem = word[next_lexem_start:last_accepted_index + 1]
					next_lexem_start = last_accepted_index + 1
					lexem_token_pair = get_lexem_token_pair(is_accepted_prev, dfas, lexem)
					lexem_token_pairs.append(lexem_token_pair)
					if process_type == "lexer":
						(token, lexem) = lexem_token_pair
						lexem_token_str = token + " " + lexem
						g.write(lexem_token_str + "\n")

					# ma intorc inapoi in input asa ca vreau sa pastrez
					# doar newline-urile care se afla inaintea inceputului
					# urmatorului lexer
					newlines = [nwln for nwln in newlines if nwln < next_lexem_start]
					break

			# daca am ajuns la final consumand tot input-ul si nu am gasit
			# niciun lexem acceptat pe drum de la ultimul lexem scris in fisier,
			# atunci afisez eroarea corespunzatoare in fisier
			if i == len(word) - 1 and last_accepted_index == -1 and any(is_accepted) == False:
				if process_type == "lexer":
					g.close()
					g = open(output_file, "w")
					g.write("No viable alternative at character EOF, line " + repr(len(newlines)))
					g.close()

				return
				break

			configs = [dfas[i].next_configuration(configs[i]) for i in range(0, len(dfas))]

	if process_type == "lexer":
		g.close()

	return lexem_token_pairs

def read_input(input_file):
	f = open(input_file, "r")
	input = f.read()
	f.close()

	return input

def prenex_to_dfa(prenex_form):
	expr = process_expr(prenex_form)
	if (expr == None):
		print("Invalid prenex form!")

	nfa = Nfa(expr)
	dfa = Basic_Dfa(nfa)
	return dfa

def process_lex_file(lex_file, word):
	f = open(lex_file, "r")
	dfas = []
	while True:
		line = f.readline()
		if line == "":
			break

		splitted_line = line.split(' ', 1)
		token = splitted_line[0]
		prenex_form = parse_regex(splitted_line[1].split(';')[0])
		basic_dfa = prenex_to_dfa(prenex_form)
		dfas.append(Dfa(basic_dfa, token, word))

	return dfas

def runcompletelexer(dfa_file, input_file, output_file):
	input = read_input(input_file)
	dfas = process_lex_file(dfa_file, input)
	process_word(dfas, input, output_file, "lexer")

def get_ast(input_file):
	input = read_input(input_file)
	dfas = process_lex_file("prog.lex", input)
	lexem_token_pairs = process_word(dfas, input, "", "parser")
	return parse_lexems(lexem_token_pairs)

def runparser(input_file, output_file):
	prog = get_ast(input_file)
	with open(output_file, 'w+') as f:
	    f.write(str(prog))

def interpretcode(input_file):
	prog = get_ast(input_file)
	store = interpret_code(prog)
	print(store)

# python3 CompleteLexer.py tests/T3/prog/input/1.in
def main():
    interpretcode(sys.argv[1])

if __name__ == "__main__":
    main()

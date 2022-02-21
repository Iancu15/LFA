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

	def __init__(self, dfa_input_list, word):
		self.word = word
		self.alphabet = dfa_input_list[0].replace('\\n', '\n')
		self.token = dfa_input_list[1]
		self.initial_state = State(dfa_input_list[2])
		self.final_states = [State(state) for state in dfa_input_list[-1].split()]
		transitions = dfa_input_list[3:-1]
		self.delta = {}
		for transition in transitions:
			trans_elems = transition.split(',')
			letter = trans_elems[1][1:-1]
			if letter == '\\n':
				letter = '\n'

			key = (State(trans_elems[0]), letter)
			self.delta[key] = State(trans_elems[2])

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
def add_token(is_accepted_prev, dfas, lexem):
	for i in range(0, len(is_accepted_prev)):
		if is_accepted_prev[i]:
			return dfas[i].get_token() + " " + lexem.replace('\n', '\\n')

	return None

# intoarce True daca toate DFA-urile au ajuns in sink state, False altfel
def all_reject(is_accepted):
	for is_accepted_elem in is_accepted:
		if is_accepted_elem != None:
			return False

	return True

def process_word(dfas, word, output_file):
	g = open(output_file, "w")
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
					lexem_token_str = add_token(is_accepted, dfas, lexem)
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
					lexem_token_str = add_token(is_accepted_prev, dfas, lexem)
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
				g.close()
				g = open(output_file, "w")
				g.write("No viable alternative at character EOF, line " + repr(len(newlines)))
				g.close()
				return
				break

			configs = [dfas[i].next_configuration(configs[i]) for i in range(0, len(dfas))]

	g.close()

def read_dfas(dfa_file, word):
	f = open(dfa_file, "r")
	dfas = []
	dfa = []
	lines = f.read().splitlines()
	for line in lines:
		# linia goala e cea dintre dfa-uri, adaug dfa-ul recent citit si
		# continui cu urmatorul
		if line == '':
			dfas.append(dfa)
			dfa = []
		else:
			dfa.append(line)

	dfas.append(dfa)
	f.close()
	return [Dfa(input_list, word) for input_list in dfas]

def read_input(input_file):
	f = open(input_file, "r")
	input = f.read()
	f.close()

	return input

def runlexer(dfa_file, input_file, output_file):
	input = read_input(input_file)
	dfas = read_dfas(dfa_file, input)
	process_word(dfas, input, output_file)

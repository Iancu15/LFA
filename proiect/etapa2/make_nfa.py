from make_regex import Symbol
from make_regex import Star
from make_regex import Union
from make_regex import Concat

class Nfa:
	# se parcurge recursiv expresia regulata, intai se ajunge la cel
	# mai de jos nivel (simbolii) si se creeaza nfa pentru acestia, urmand
	# ca pe baza lor sa fie generate nfa-urile pentru nivelul superior si
	# tot asa pana ramane un singur nfa la final
	def __init__(self, reg_expr):
		self.alphabet = ""
		self.initial_state = State(0)
		self.final_state = State(1)
		self.states = []

		# concat nu creeaza stari noi
		if not isinstance(reg_expr, Concat):
			self.states.append(self.initial_state)
			self.states.append(self.final_state)

		self.delta = {}

		if isinstance(reg_expr, Symbol):
			self.create_eps_trans_groups()
			symbol = reg_expr.x
			self.delta[(self.initial_state, symbol)] = self.final_state
			self.alphabet = symbol
		elif isinstance(reg_expr, Star):
			nfa = Nfa(reg_expr.x)
			self.states += nfa.get_states()
			self.rename_states()
			self.create_eps_trans_groups()
			self.add_alphabet(nfa.get_alphabet())

			self.add_delta(nfa.get_delta())
			self.add_eps_trans(self.initial_state, nfa.get_initial_state())
			self.add_eps_trans(self.initial_state, self.final_state)
			self.add_eps_trans(nfa.get_final_state(), self.final_state)
			self.add_eps_trans(nfa.get_final_state(), nfa.get_initial_state())
		else:
			nfa1 = Nfa(reg_expr.x)
			nfa2 = Nfa(reg_expr.y)
			self.states += nfa1.get_states() + nfa2.get_states()
			if isinstance(reg_expr, Concat):
				self.initial_state = nfa1.get_initial_state()
				self.final_state = nfa2.get_final_state()

			self.rename_states()
			self.create_eps_trans_groups()
			self.add_alphabet(nfa1.get_alphabet())
			self.add_alphabet(nfa2.get_alphabet())

			self.add_delta(nfa1.get_delta())
			self.add_delta(nfa2.get_delta())
			if isinstance(reg_expr, Union):
				self.add_eps_trans(self.initial_state, nfa1.get_initial_state())
				self.add_eps_trans(self.initial_state, nfa2.get_initial_state())
				self.add_eps_trans(nfa1.get_final_state(), self.final_state)
				self.add_eps_trans(nfa2.get_final_state(), self.final_state)
			elif isinstance(reg_expr, Concat):
				self.add_eps_trans(nfa1.get_final_state(), nfa2.get_initial_state())

		self.complete_eps_groups()

	# adauga in grupul de epsilon tranzitii al starilor, starile
	# in care se ajunge trecand prin cel putin 2 epsilon tranzitii
	def complete_eps_groups(self):
		for state in self.states:
			eps_stack = []
			eps_list = [state]

			# parcurg starile in care se ajunge direct printr-o singura
			# epsilon tranzitie
			for eps_state in self.delta[(state, 'ε')]:
				if eps_state != state:
					eps_stack.append(eps_state)
					eps_list.append(eps_state)

			# se parcurg pe rand starile adaugate anterior pe stiva
			# si pentru fiecare se parcurg starile direct accesibile printr-o
			# singura epsilon tranzitie, cele care nu se afla deja in grupul
			# epsilon al starii curente sunt adaugate in grup si sunt
			# adaugate pe stiva pentru a fi parcurse si grupurile de
			# epsilon tranzitii ale acestora
			while len(eps_stack) != 0:
				curr_state = eps_stack.pop()
				for eps_state in self.delta[(curr_state, 'ε')]:
					if eps_state not in eps_list:
						eps_stack.append(eps_state)
						eps_list.append(eps_state)
						self.delta[(state, 'ε')].add(eps_state)

	# renumeroteaza starile
	def rename_states(self):
		i = 0
		for state in self.states:
			state.set_value(i)
			i += 1

	# adauga delta-ul nfa-ului de la nivelul inferior
	def add_delta(self, delta):
		for (start_state, letter), end_state in delta.items():
			if letter == 'ε':
				for end_state_elem in end_state:
					self.delta[(start_state, 'ε')].add(end_state_elem)
			else:
				self.delta[(start_state, letter)] = end_state

	# adauga alfabetul nfa-ului de la nivelul inferior
	def add_alphabet(self, alphabet):
		for letter in alphabet:
			if letter not in self.alphabet:
				self.alphabet += letter

	# creeaza grupul de epsilon tranzitii al tuturor starilor
	def create_eps_trans_groups(self):
		for state in self.states:
			self.delta[(state, 'ε')] = set(state)

	def add_eps_trans(self, start_state, end_state):
		self.delta[(start_state, 'ε')].add(end_state)

	def __repr__(self):
		return repr(repr(self.states) +
		" | " + repr(self.initial_state) +
		" | " + repr(self.final_state) +
		" | " + repr(self.delta) +
        " | " + repr(self.alphabet))

	def get_states(self):
		return self.states

	def get_initial_state(self):
		return self.initial_state

	def get_final_state(self):
		return self.final_state

	def get_delta(self):
		return self.delta

	def get_alphabet(self):
		return self.alphabet

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
		return iter([self])

	def set_value(self, value):
		self.value = value

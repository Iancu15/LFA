from make_nfa import State
from make_nfa import Nfa

class Basic_Dfa:
	def __init__(self, nfa):
		self.alphabet = nfa.get_alphabet()
		self.initial_state = State(0)
		self.final_states = []
		self.states = [self.initial_state]
		self.delta = {}
		nfa_delta = nfa.get_delta()

		# starea initiala a dfa-ului va fi formata din grupul de epsilon
		# tranzitii al starii initiale ale nfa-ului
		# fiecare grup de epsilon tranzitii din nfa corespunde unei stari in dfa
		# stack -> grupurile de epsilon tranzitii din nfa ce urmeaza a fi
		# procesate
		# stack_values -> grupurile de epsilon tranzitii ce au fost sau
		# urmeaza a fi procesate
		# stack_values_dict -> face corespodenta intre grupurile de epsilon
		# tranzitii din nfa si starile din dfa (corespondenta 1:1)
		initial_group_states = nfa_delta[(nfa.get_initial_state(), 'ε')]
		initial_group_set = set(initial_group_states)
		stack = [initial_group_set]
		stack_values = [initial_group_set]
		stack_values_dict = {}
		stack_values_dict[frozenset(initial_group_states)] = self.initial_state
		state_value = 1
		while len(stack) > 0:
			start_group_states = stack.pop()
			dfa_start_state = stack_values_dict[frozenset(start_group_states)]

			# pentru fiecare litera din alfabet se creeaza grupul de stari
			# in care se ajunge din grupul curent de stari pe tranzitia literei
			# respective
			# grupul de stari in care se ajunge e format din reuniunea
			# grupurilor tranzitiilor epsilon ale starilor in care se ajungea
			# in nfa din fiecare stare ce face parte din grupul de start de
			# stari
			for letter in self.alphabet:
				end_group_states = set()
				for start_state in start_group_states:
					if (start_state, letter) in nfa_delta:
						end_state = nfa_delta[(start_state, letter)]
						for eps_state in nfa_delta[(end_state, 'ε')]:
							end_group_states.add(eps_state)

				# daca sunt stari in care se ajunge din grupul de start de
				# stari, atunci daca nu a fost sau urmeaza a fi procesat
				# grupul de stari final, voi crea o noua stare care sa-i
				# corespunda
				# starea nou creata sau cea existenta (daca era deja in
				# stack_values) va fi pusa ca stare de final pentru
				# configuratia formata din starea corespondenta grupului
				# de start de stari si litera curenta
				if len(end_group_states) > 0:
					if end_group_states not in stack_values:
						stack_values.append(end_group_states)
						new_state = State(state_value)
						state_value += 1
						self.states.append(new_state)
						stack_values_dict[frozenset(end_group_states)] = new_state
						stack.append(end_group_states)

					end_state = stack_values_dict[frozenset(end_group_states)]
					self.delta[(dfa_start_state, letter)] = end_state

		# starile corespondente grupurilor de stari ce contin cel putin o
		# stare finala din nfa vor deveni stari finale in dfa
		for state_group in stack_values:
			if nfa.get_final_state() in state_group:
				self.final_states.append(stack_values_dict[frozenset(state_group)])

		self.add_sink_state()

	def is_pair_in_delta(self, pair):
		for iter_pair in self.delta:
			if pair == iter_pair:
				return True

		return False

	# creez starea sink si fac ca toate configuratiile care nu au o stare finala
	# sa aiba ca stare finala sink state-ul
	def add_sink_state(self):
		sink_state = State(None)
		for state in self.states:
			for letter in self.alphabet:
				if not self.is_pair_in_delta((state, letter)):
					self.delta[(state, letter)] = sink_state

		for letter in self.alphabet:
			self.delta[(sink_state, letter)] = sink_state

		sink_state.set_value(len(self.states))
		self.states.append(sink_state)

	def __repr__(self):
		return repr(self.alphabet +
        " | " + repr(self.states) +
		" | " + repr(self.initial_state) +
		" | " + repr(self.final_states) +
		" | " + repr(self.delta))

	def get_number_of_states(self):
		return len(self.states)

	def get_initial_state(self):
		return self.initial_state

	def get_final_states(self):
		return self.final_states

	def get_delta(self):
		return self.delta

	def get_alphabet(self):
		return self.alphabet

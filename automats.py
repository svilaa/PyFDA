#!/usr/bin/python

# Author: Sergi Vila Almenara

import sys
import os

from collections import deque


class State:
	def __init__(self, name):
		self.name = name
		self.transitions = {}
	
	def put_transition(self, symbol, state):
		self.transitions[symbol] = state

	def get_next_state(self, symbol):
		return self.transitions[symbol]

	def get_symbols(self):
		return self.transitions.keys()

	def has_symbol(self, symbol):
		return symbol in self.transitions

	def __str__(self):
		return self.name

	def __repr__(self):
		return self.__str__()

	def __eq__(self, other):
		return self.name == other.name

	def __hash__(self):
		return hash(self.name)

	def __cmp__(self, other):
		return cmp(self.name, other.name)


class AFD:
	def __init__(self, symbols, states, initials, finals):
		self.list_states = sorted(states.values(), key = lambda x: (len(x.name), x) )
		self.symbols = symbols
		self.states = states
		self.initials = initials
		self.finals = finals


	def show_list(self, lis):
		return ' '.join([x.__str__() for x in lis])


	def show(self):
		print "Alphabet:", self.show_list(self.symbols)
		print "Set of states:", self.show_list(self.list_states)
		print "Initial states:", self.show_list(self.initials)
		print "Final states:", self.show_list(self.finals)
		print "Transitions:"
		for state in self.list_states:
			print '    ', state.name, '->', state.transitions


	def get_representant_class(self, state_set):
		state_names = [state.name for state in state_set]
		minimum = min(state_names)
		return minimum


	def define_class_state(self, state, classes):
		for clas in classes:
			if state in clas:
				return clas


	def get_transition_sequence(self, state, classes):
		sequence = ""
		for symbol in sorted(state.get_symbols()):
			next_state = state.get_next_state(symbol)
			contained_class = self.define_class_state(next_state, classes)
			representant_class = self.get_representant_class(contained_class)
			sequence += representant_class + ":"
		return sequence


	def next_step(self, classes):
		next_classes = []
		for clas in classes:
			dict_class = {}
			for state in clas:
				seq = self.get_transition_sequence(state, classes)
				dict_class.setdefault(seq, []).append(state)

			next_classes.extend(set(x) for x in dict_class.values())

		return next_classes


	def remove_state_from_structures(self, state):
		self.list_states.remove(state)
		del self.states[state.name]
		if state in self.initials:
			self.initials.remove(state)
		if state in self.finals:
			self.finals.remove(state)


	def adapt_clas_state(self, state, symbol, representant, clas):
		if state.get_next_state(symbol) in clas:
			state.put_transition(symbol, representant)
		else:
			representant.put_transition(symbol, state.get_next_state(symbol))
	

	def adapt_other_state(self, state, symbol, representant, clas):
		if state.get_next_state(symbol) in clas:
			state.put_transition(symbol, representant)


	def substitute_states(self, representant, clas):
		for state in self.list_states:
			for symbol in state.get_symbols()[:]:
				if state in clas:
					self.adapt_clas_state(state, symbol, representant, clas)
				else:
					self.adapt_other_state(state, symbol, representant, clas)


	def initial_state_special_case(self, state, representant):
		if state in self.initials and representant not in self.initials:
				self.initials.append(representant)


	def delete_minimized_states(self, classes_to_minimize):
		for clas in classes_to_minimize:
			representant = self.states[self.get_representant_class(clas)]
			for state in clas:
				if state is not representant:
					self.initial_state_special_case(state, representant)
					self.remove_state_from_structures(state)


	def minimize_states(self, classes):
		classes_to_minimize = [list(x) for x in classes if len(x) > 1]
		for clas in classes_to_minimize:
			representant = self.get_representant_class(clas)
			self.substitute_states(self.states[representant], clas)
		self.delete_minimized_states(classes_to_minimize)


	def minimize(self):
		classes = []
		classes.append(set(self.list_states) - set(self.finals))
		classes.append(set(self.finals))
		equal = False

		while not equal:
			next_classes = self.next_step(classes)
			if classes == next_classes:
				equal = True
			else:
				classes = next_classes

		self.minimize_states(next_classes)


	def get_complementary_finals(self):
		return [x for x in self.list_states if x not in self.finals]


	def get_complementary(self):
		return AFD(self.symbols, self.states, self.initials, self.get_complementary_finals())


	def combined_states_to_string(self, state_list):
		return '(' + state_list[0].__str__() + ',' + state_list[1].__str__() + ')'


	def obtain_next_combined_state(self, state, symbol):
		next_state1 = state[0].get_next_state(symbol)
		next_state2 = state[1].get_next_state(symbol)
		return [next_state1, next_state2]


	def calculate_finals(self, left_list, right_list, new_states):
		final_states = []
		for final_left in left_list:
			for final_right in right_list:
				new_final_name = self.combined_states_to_string([final_left, final_right])
				if new_final_name in new_states:
					final_states.append(new_states[new_final_name])
		return final_states


	def obtain_finals_intersec(self, afd, new_states):
		return list(set(self.calculate_finals(self.finals, afd.finals, new_states)))


	def obtain_finals_union(self, afd, new_states):
		final_states = []
		final_states.extend(self.calculate_finals(self.finals, afd.list_states, new_states))
		final_states.extend(self.calculate_finals(self.list_states, afd.finals, new_states))	
		return list(set(final_states))


	def combine(self, afd):
		new_symbols = self.symbols[:]
		queue = deque()
		initial_list = [self.initials[0], afd.initials[0]]
		queue.append(initial_list)
		new_states = {}
		initial_name = self.combined_states_to_string(initial_list)
		initial_state = State(initial_name)
		new_initials = [initial_state]
		new_states[initial_name] = initial_state

		while(len(queue) is not 0):
			state_combined = queue.popleft()
			state_name = self.combined_states_to_string(state_combined)
			state = new_states[state_name]
			for symbol in new_symbols:
				next_state_list = self.obtain_next_combined_state(state_combined, symbol)
				next_state_name = self.combined_states_to_string(next_state_list)
				if next_state_name not in new_states:
					new_states[next_state_name] = State(next_state_name)
					queue.append(next_state_list)
				state.put_transition(symbol, new_states[next_state_name])
		
		return new_symbols, new_states, new_initials


	def get_union(self, afd):
		new_symbols, new_states, new_initials = self.combine(afd)
		new_finals = self.obtain_finals_union(afd, new_states)
		return AFD(new_symbols, new_states, new_initials, new_finals)


	def get_intersection(self, afd):
		new_symbols, new_states, new_initials = self.combine(afd)
		new_finals = self.obtain_finals_intersec(afd, new_states)
		return AFD(new_symbols, new_states, new_initials, new_finals)


class AFDNameReducer:
	def __init__(self, afd):
		self.afd = afd
		self.translates = {}
		self.new_states = {}
		self.new_state_list = []


	def get_name_reduction(self):
		self.prepare_structures()
		self.do_translated_transitions()
		new_initials = self.get_translated_list(self.afd.initials)
		new_finals = self.get_translated_list(self.afd.finals)
		return AFD(self.afd.symbols, self.new_states, new_initials, new_finals)


	def prepare_structures(self):
		for i, state in enumerate(self.afd.list_states):
			new_state = State(str(i))
			self.translates[state.name] = new_state.name
			self.new_states[new_state.name] = new_state
			self.new_state_list.append(new_state)


	def do_translated_transitions(self):
		for state in self.afd.list_states:
			for symbol in state.get_symbols():
				self.do_transition(state, symbol)


	def get_translated_state(self, old_state):
		new_state_name = self.translates[old_state.name]
		return self.new_states[new_state_name]


	def do_transition(self, old_state, symbol):
		new_state = self.get_translated_state(old_state)
		next_state = old_state.get_next_state(symbol)
		new_next_state = self.get_translated_state(next_state)
		new_state.put_transition(symbol, new_next_state)


	def get_translated_list(self, old_list):
		new_list = []
		for old_state in old_list:
			new_state = self.get_translated_state(old_state)
			new_list.append(new_state)
		return new_list


class AFDWriter:
	def __init__(self, afd):
		self.afd = afd


	def write_symbols(self, output):
		print >>output, 's', ' '.join(self.afd.symbols)


	def obtain_list(self, lis):
		return ' '.join(sorted([x.__str__() for x in lis], key = lambda x: (len(x), x)))

	def write_state_line(self, output):
		print >>output, 'e', self.obtain_list(self.afd.list_states)


	def write_initial_states_line(self, output):
		print >>output, 'i', self.obtain_list(self.afd.initials)


	def write_final_states_line(self, output):
		print >>output, 'f', self.obtain_list(self.afd.finals)


	def write_states(self, output):
		self.write_state_line(output)
		self.write_initial_states_line(output)
		self.write_final_states_line(output)


	def write_transitions(self, output):
		for state in sorted(self.afd.list_states, key = lambda x: (len(x.name), x)):
			for symbol in sorted(state.get_symbols(), key = lambda x: (len(x), x)):
				print >>output, 't', state, symbol, state.get_next_state(symbol)


	def write(self, fname):
		f = open(fname, 'w')
		print >>f, "p afd"
		self.write_symbols(f)
		self.write_states(f)
		self.write_transitions(f)
		f.close()


class AFDReader:
	def __init__(self, fname):
		self.symbols = []
		self.states = {}
		self.initials = []
		self.finals = []
		self.read(fname)


	def put_states(self, line):
		for state in line[1:]:
			s = State(state)
			self.states[state] = s


	def get_state(self, state):
		return self.states[state]


	def put_special_states(self, line):
		special_states = []
		for state in line[1:]:
			s = self.get_state(state)
			special_states.append(s)
		return special_states


	def read(self, fname):
		f = open(fname, 'r')
		for line in f:
			l = line.split()
			if l[0] == 's':
				self.symbols.extend(l[1:])
			elif l[0] == 'e':
				self.put_states(l)
			elif l[0] == 'i':
				states = self.put_special_states(l)
				self.initials.extend(states)
			elif l[0] == 'f':
				states = self.put_special_states(l)
				self.finals.extend(states)
			elif l[0] == 't':
				self.get_state(l[1]).put_transition(l[2], self.get_state(l[3]))
		f.close()


	def get_AFD(self):
		return AFD(self.symbols, self.states, self.initials, self.finals)


class Solver:
	def __init__(self, problem):
		self.problem = problem


	def solve(self, word):
		for init_state in self.problem.initials:
			current_state = init_state
			for symbol in word:
				current_state = current_state.get_next_state(symbol)

			if current_state in self.problem.finals:
				return True

		return False
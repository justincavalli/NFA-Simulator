# Name: pa2.py
# Author(s): Justin Cavalli
#			 Shaydon Bodemar
# Date:	26 September 2020
# Description: Generate DFAs from NFAs

class NFA:
	""" Simulates an NFA """

	def __init__(self, nfa_filename):
		"""
		Initializes NFA from the file whose name is
		nfa_filename.  (So you should create an internal representation
		of the nfa.)
		"""
		# read the input file
		file1 = open(nfa_filename, "r")
		self._num_states = int(file1.readline().rstrip('\n'))
		self._alphabet = file1.readline().rstrip('\n')
		self._transition_table = {}
		transition_val = True
		# loops through all transition values (lines) in file
		while(transition_val):
			file_input = file1.readline()
			if("'" in file_input):
				# set value for transition in dictionary
				tokens = file_input.split()
				if(tokens[0] + tokens[1] in self._transition_table):
					self._transition_table[tokens[0] + tokens[1]].append(tokens[2])
				else:
					self._transition_table[tokens[0] + tokens[1]] = [tokens[2]]
			else:
			    transition_val = False
		file_input = file1.readline()
		self._start_state = file_input.rstrip('\n')
		file_input = file1.readline()
		self._accept_states = file_input.split()


	def toDFA(self, dfa_filename):
		"""
		Converts the "self" NFA into an equivalent DFA
		and writes it to the file whose name is dfa_filename.
		The format of the DFA file must have the same format
		as described in the first programming assignment (pa1).
		This file must be able to be opened and simulated by your
		pa1 program.

		This function should not read in the NFA file again.  It should
		create the DFA from the internal representation of the NFA that you 
		created in __init__.
		"""
		# create sorted list of start states for the dfa start state
		start_states = [self._start_state]
		start_states = self.epsilon_transitions(start_states)
		start_states = list(dict.fromkeys(start_states))
		start_states.sort(key=int)
		dfa_start_state = ",".join(start_states)

		dfa_transition_table = {}

		# create queue of values for new states encountered
		state_queue = []
		state_queue.append(str(0))
		state_queue.append(dfa_start_state)

		#num_dfa_states = 2
		# enqueue all standalone nfa states
		for i in range(1, self._num_states+1):
			state_queue.append(str(i))
			#num_dfa_states += 1

		# create list of accept states and determine if start state is accepted
		dfa_accept_states = []
		for nfa_state in start_states:
			if nfa_state in self._accept_states:
				dfa_accept_states.append(dfa_start_state)
				break

		# loop as long as queue contains any unhandled states created
		while(len(state_queue) > 0):
			dfa_state = state_queue.pop(0)
			# know which states from the nfa are present in this dfa state
			nfa_states = dfa_state.split(',')
			# find destination state for every alphabet item
			for item in self._alphabet:
				dfa_entry = dfa_state + '\'' + item + '\''
				if dfa_entry in dfa_transition_table:
					continue
				temp = []
				# add destinations to running list for every nfa state present in the dfa state
				for state in nfa_states:
					if state + '\'' + item + '\'' in self._transition_table:
						temp.extend(self._transition_table[state + '\'' + item + '\''])
					else:
						temp.append(str(0))
				# ensure list has only unique, sorted values
				temp = self.epsilon_transitions(temp)
				temp = list(dict.fromkeys(temp))
				temp.sort(key=int)
				if len(temp) > 1 and temp[0] == '0':
					temp.pop(0)
				# add output state to accept states if one of nfa states is accepted
				accept = False
				for nfa_state in temp:
					if nfa_state in self._accept_states:
						accept = True
						break
				output_dfa_state = ",".join(temp)
				if accept and output_dfa_state not in dfa_accept_states:
					dfa_accept_states.append(output_dfa_state)
				# add this state to the transition table
				dfa_transition_table[dfa_entry] = output_dfa_state
				# if created output state is not in the transition table, enqueue to be handled
				if not output_dfa_state + '\'' + item + '\'' in dfa_transition_table:
					state_queue.append(output_dfa_state)
					#num_dfa_states += 1
		# write created dfa to a file in appropriate format
		num_dfa_states = int(len(dfa_transition_table)/len(self._alphabet))
		self.convertToFileFormatDFA(dfa_filename, dfa_start_state, num_dfa_states, dfa_transition_table, dfa_accept_states)


	def convertToFileFormatDFA(self, filename, start_state, num_states, transition_table, accept_states):
		"""
		Takes in a CSV-formatted DFA transition table and converts to a simple int-char mapping
		for the desired output format
		"""
		state_map = {}
		new_transition_table = {}
		cur_state = 1
		for key in transition_table:
			if key[:-3] not in state_map:
				state_map[key[:-3]] = cur_state
				cur_state += 1

		start_state = state_map[start_state]
		for val in range(len(accept_states)):
			accept_states[val] = str(state_map[accept_states[val]])

		for key in transition_table:
			new_transition_table[str(state_map[key[:-3]]) + key[-3:]] = state_map[transition_table[key]]
		
		self.writeFileDFA(filename, start_state, num_states, new_transition_table, accept_states)


	def writeFileDFA(self, filename, start_state, num_states, transition_table, accept_states):
		"""
		Takes the elements of the newly made DFA and writes it to the file "filename" in the 
		same format described in pa1"
		"""
		dfa_file = open(filename, "w+")
		dfa_file.write(str(num_states) + "\n")
		dfa_file.write(self._alphabet + "\n")

		for transition in transition_table:
			dfa_file.write(transition[:-3] + " " + transition[-3:] + " " + str(transition_table[transition]) + "\n")

		dfa_file.write(str(start_state) + "\n")
		dfa_file.write(" ".join(accept_states))


	def epsilon_transitions(self, states):
		"""
		Checks if each element in the list "states" has an epsilon transition. 
		In the case that it does, add this state to the list and continue checking recursively.
		Otherwise, return the new list of states, now accounting for epsilon transitions.
		"""
		for state in states:
			if state + '\'e\'' in self._transition_table:
				states.extend(self._transition_table[state + '\'e\''])
				states.extend(self.epsilon_transitions(self._transition_table[state + '\'e\'']))
		return states
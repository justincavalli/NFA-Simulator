# Name: pa1.py
# Author(s): Shaydon Bodemar
#			 Justin Cavalli
# Date: September 9 2020
# Description: Simulate the bahavior of a DFA to determine whether a string is in a particular language.

import sys

class DFA:
	""" Simulates a DFA """
	
	def __init__(self, filename):
		"""
		Initializes DFA from the file whose name is
		filename
		"""
		# read the input file
		file1 = open(filename, "r")
		self._num_states = file1.readline().rstrip('\n')
		file_input = file1.readline()
		self._transition_table = {}
		transition_val = True
		# loops through all transition values (lines) in file
		while(transition_val):
			file_input = file1.readline()
			if("'" in file_input):
				# set value for transition in dictionary
				tokens = file_input.split()
				self._transition_table[tokens[0] + tokens[1]] = tokens[2]
			else:
			    transition_val = False
		self._start_state = file_input.rstrip('\n')
		file_input = file1.readline()
		self._accept_states = file_input.split()

	def simulate(self, str):
		""" 
		Simulates the DFA on input str.  Returns
		True if str is in the language of the DFA,
		and False if not.
		"""
		cur_state = self._start_state
		for i in range (len(str)):
			cur_state = self._transition_table[cur_state + "\'" + str[i] + "\'"]
		return cur_state in self._accept_states
# -*- coding: utf-8 -*-

#		lsystem.py
#
#		Copyright (C) 2009  Bruno Figueira Lourenço
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
import parser
import random
import time
from genetic import GeneticOperators
""" Dummy class to hold a few variables

"""
class LRule:pass


class LSystem:
	def __init__(self,axiom,globals = {}, locals = {}, seed = None, mutation_pool = None, mutation_ignore = None):
		self.axiom = axiom
		self.var_globals = globals
		self.var_locals = locals
		self.symbols = {}
		self.rules = []
		self.genetic_operators = GeneticOperators()
		self.var_locals['crossover'] = self.__crossover
		self.var_locals['mutation'] = self.__mutation
		self.seed = time.time()
		if seed is not None:
			self.seed = seed
		self.mutation_pool = ['F','+','-']
		if mutation_pool is not None:
			self.mutation_pool = mutation_pool
		
		self.mutation_ignore = set(['(',')','[',']']),
		if mutation_ignore is not None:
			self.mutation_ignore = mutation_ignore
		random.seed(self.seed)
	""" Add a rule to the l-system

	"""
	def add_rule(self,symbol, sucessor,
					  left_context = None,
					  right_context = None,
					  condition = "True",
					  probability = 1,
					  parameters = [],
					  code = "None"):
		rule = LRule()
		rule.sucessor = sucessor
		rule.left_context = left_context
		rule.right_context = right_context
		rule.condition = condition
		rule.probability = probability
		rule.parameters = parameters
		rule.code = code
		if symbol not in self.symbols:
			self.symbols[symbol] = []
			
		
			
		self.symbols[symbol].append(rule)
		self.rules.append(rule)
	""" Try to match a rule. Return False if it doesn't find a match, 
	True otherwise.
	
	"""
	def match_rule(self,position,symbol,rule,parametric):
		#Check if the rule has a left context and if we 
		#can match the context
		#Since a symbol can be parametric we must set the position
		#argument to the beginning of the symbol
		if rule.left_context is not None: 
			match = self.match_left_context(position - (len(symbol) -1),
											rule.left_context,
											self.current_string)
			if not match:
				return False
		#Check if the rule has a right context and if we 
		#can match the context
		if rule.right_context is not None:
			match = self.match_right_context(position,
											rule.right_context,
											self.current_string)
			if not match:
				return False
				
		if parametric: 
			#if we found a parametric symbol we should only
			#consider parametric rules
			if rule.parameters == []:
				return False
			if self.check_condition(symbol,rule) is not True:
				return False
		return True		
	"""This method generates a random number and choose the successor of 
	the rule that will replace the current symbol
	
	"""
	def choose_rule(self,matched_rules,symbol):
		u  = random.random()
		aux = 0
		#if we don't find a rule to match, we rewrite 
		#the symbol to itself
		aux_str = symbol
		for rule in matched_rules:
			aux += rule.probability
			if u <= aux:
				if len(rule.parameters) == 0:
					aux_str = rule.sucessor
				else:
					aux_str = rule.aux_sucessor
				exec(rule.code,self.var_globals,self.var_locals)
				break
		return aux_str
	def __crossover(self,rule1,rule2,type = 0):
		self.rules[rule1].sucessor,self.rules[rule2].sucessor = self.genetic_operators.crossover(self.rules[rule1].sucessor,self.rules[rule2].sucessor,type)	
	
	def __mutation(self,rule,mutation_rate = 0.2):
		self.rules[rule].sucessor = self.genetic_operators.mutation(self.rules[rule].sucessor,mutation_rate,self.mutation_ignore,self.mutation_pool)
	
	def derive(self, level):
		i = 0
		random.seed(self.seed)
		self.current_string = self.axiom
		print ("0 %s") % (self.current_string)
		while i < level:
			j = 0
			string_length = len(self.current_string)
			new_string = ""
			while j < string_length:
				
				symbol = self.current_string[j]
				#check if this symbol is parametric
				parametric = False
				if j+1 < string_length and self.current_string[j+1] == '(':
					j += 1
					parametric = True
					#TODO: Check if we've reached the end of the string
					while self.current_string[j] != ')':
						symbol += self.current_string[j]
						j += 1
					symbol += self.current_string[j]
					
				#If the symbol is not in the symbols dictionary, we 
				#assume that it rewrites to itself
				if symbol[0] not in self.symbols:
					new_string += symbol
					j += 1
					continue
				
				#For each rule we have to check which rules match, then 
				#we can build a list of 'matched' rules.
				matched_rules = []
				for rule in self.symbols[symbol[0]]:
					if self.match_rule(j,symbol,rule,parametric):
						matched_rules.append(rule)			
				new_string += self.choose_rule(matched_rules,symbol)
				j += 1
			self.current_string = new_string
			print ("%d %s") % (i+1,self.current_string)
			i += 1
		return self.current_string			 
	def check_condition(self,symbol,rule): 
		formal_parameters = rule.parameters
		actual_parameters = parser.parse_parameters(symbol)
		
		if len(formal_parameters) != len(actual_parameters):
			return False
		
		#we update the value of each formal parameter
		i = 0
		for parameter in actual_parameters:
			exec(formal_parameters[i]+"="+parameter,
				 self.var_globals,
				 self.var_locals)
			i += 1
		#we check the truth value of the rule condition
		condition = eval(rule.condition,self.var_globals,self.var_locals)
		#if condition is True, substitute the parameters in the sucessor
		if condition:
			rule.aux_sucessor = self.evaluate_sucessor(rule.sucessor)
		
		#Finally, we delete the parameters from the var_locals dictionary
		#to clean the namespace.
		#TODO: Is it really necessary to do this? Maybe not...
		#for parameter in formal_parameters:
			#del self.var_locals[parameter]	
		return condition
	""" Evaluate the sucessor of a rule and replace the expressions found 
	by its values
	
	This method is called by the check_condition method if the condition 
	of a rule has a truth value of True. In this case the sucessor part 
	of the rule may contain parametric symbols and the parameters must 
	be replaced by its values.
	
	Example: if t = 1 and s = 2, evaluate_sucessor("F(t+s)G(s,t)Y") 
	returns "F(3)G(2,1)Y"
	"""	
	def evaluate_sucessor(self,string):
		i = 0
		length = len(string)
		new_string = ""
		while i < length:
			new_string += string[i]
			#if the character is '(' it means we found a parametric 
			#symbol and we must evaluate it
			if string[i] == '(':
				j = i + 1
				brackets  = 1
				#Find the expression inside the ()					
				while brackets != 0 and j < length:
					if string[j] == '(':
						brackets += 1
					elif string[j] == ')':
						brackets -= 1
					j += 1
				expressions = string[i+1:j-1].split(',')
				size = len(expressions)
				k = 0
				#For each parameter evaluate the expression and append 
				#the value to the new string
				while k < size - 1:
					value = eval(expressions[k],self.var_globals,self.var_locals)
					new_string += str(value) + ','
					k += 1
				value = eval(expressions[k],self.var_globals,self.var_locals)
				
				new_string += str(value) + ')'
				#Note to my dumb self: it's j-1 instead of j because we 
				#always add 1 to i  
				i = j - 1			
			i += 1
		return new_string
				
	def match_left_context(self,position,context,string): 
		brackets = 0
		left_part = string[:position][::-1]
		i = iter(context[::-1])
		j = iter(left_part)
		
		while True:
			#If we catch an exception it means that we've reached 
			#the end of the context and all the characters have been 
			#matched, so we return True
			try:
				context_char = i.next()
			except StopIteration:
				return True
			#If we catch an exception here, it means that we've reached 
			#the end of the string and the context was not found.
			#Example: aab and the production caa < b. We reach the end 
			#of the string but we don't match the context
			try:
				 char = j.next()
				 #Check if we have a list of ignored symbols. Those 
				 #symbols must be skipped when searching for context
				 if 'ignore' in self.var_locals:
				 	while char in self.var_locals['ignore']:
				 		char = j.next()
			except StopIteration:
				return False
			
			#if char == context_char then we have a partial match
			if char == context_char:
				#if char == ')' then we must find the parameters and 
				#check if they match.
				if char != ')':
					continue
				else:
					#find the formal parameters
					formal_parameters = ')'
					brackets = 1
					try:
						while brackets != 0:
							char = i.next()
							if char == ')':
								brackets += 1
							elif char == '(':
								brackets -= 1
							formal_parameters += char
					except StopIteration:
						return False
					#find the actual parameters
					actual_parameters = ')'
					brackets = 1
					try:
						while brackets != 0:
							char = j.next()
							if char == ')':
								brackets += 1
							elif char == '(':
								brackets -= 1
							actual_parameters += char
					except StopIteration:
						return False
					formal_parameters = parser.parse_parameters(formal_parameters[::-1])
					actual_parameters = parser.parse_parameters(actual_parameters[::-1])
					#if the number of parameters match we must evaluate
					#the expressions
					if len(formal_parameters) == len(actual_parameters):
						k = 0
						while k < len(formal_parameters):
							exec(formal_parameters[k]+"="+actual_parameters[k],
				 			self.var_globals,
				 			self.var_locals)
				 			k += 1
					else:
						return False
			#if char == ']' it means we must skip the substring between
			#brackets
			elif char == ']':
				brackets += 1
				while brackets != 0:
					try:
						char = j.next()
					except StopIteration:
						raise
					else:
						if char == '[':
							brackets -= 1
						elif char == ']':
							brackets += 1
			#TODO:check this
			elif char == '[':
				continue
			else:
				return False
		return True
	""" Check if we have a match for the right context of a symbol
	
	position = the index of the symbol
	context = the context that will be matched
	string = the string that will be matched
	
	"""	
	def match_right_context(self,position,context,string): 
		brackets = 0
		right_part = string[position+1:]
		i = iter(context)
		j = iter(right_part)
		while True:
			#Check match_left_context, the same comments apply here	
			try:
				context_char = i.next()
			except StopIteration:
				return True
			try:
				 char = j.next()
				 if 'ignore' in self.var_locals:
				 	while char in self.var_locals['ignore']:
				 		char = j.next()
			except StopIteration:
				return False
			
			
			if char == context_char:
				#if char == ')' then we must find the parameters and 
				#check if they match.
				if char != '(':
					continue
				else:
					#find the formal parameters
					formal_parameters = '('
					brackets = 1
					try:
						while brackets != 0:
							char = i.next()
							if char == '(':
								brackets += 1
							elif char == ')':
								brackets -= 1
							formal_parameters += char
					except StopIteration:
						return False
					#find the actual parameters
					actual_parameters = '('
					brackets = 1
					try:
						while brackets != 0:
							char = j.next()
							if char == '(':
								brackets += 1
							elif char == ')':
								brackets -= 1
							actual_parameters += char
					except StopIteration:
						return False
					formal_parameters = parser.parse_parameters(formal_parameters)
					actual_parameters = parser.parse_parameters(actual_parameters)
					#if the number of parameters match we must evaluate
					#the expressions
					if len(formal_parameters) == len(actual_parameters):
						k = 0
						while k < len(formal_parameters):
							exec(formal_parameters[k]+"="+actual_parameters[k],
				 			self.var_globals,
				 			self.var_locals)
				 			k += 1
					else:
						return False
			elif char == '[':
				brackets += 1
				while brackets != 0:
					try:
						char = j.next()
					except StopIteration:
						raise
					else:
						if char == ']':
							brackets -= 1
						elif char == '[':
							brackets += 1
			#TODO:check this
			elif char == ']':
				continue
			else:
				return False

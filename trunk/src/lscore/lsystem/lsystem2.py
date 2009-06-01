from lsystem import *
""" The LSystem2 class implements the syntax of Musical Grammars as 
described by Jon Mccormack


"""
class LSystem2(LSystem):
	def add_rule(self,symbol, sucessor,
					  temporal_context,
					  polyphonic_context,
					  condition = "True",
					  probability = 1,
					  parameters = [],
					  code = "None"):
		rule = LRule()
		rule.sucessor = sucessor
		rule.temporal_context = temporal_context
		rule.polyphonic_context = polyphonic_context
		rule.condition = condition
		rule.probability = probability
		rule.parameters = parameters
		rule.code = code
		if symbol not in self.symbols:
			self.symbols[symbol] = []
			
		self.symbols[symbol].append(rule)
		self.rules.append(rule)
	def match_rule(self,position,symbol,rule,parametric):pass
	
	def get_next_symbol(self,position):
		parametric= False
		string_length = len(self.current_string)
		if position+1 < string_length and self.current_string[position+1] == '(':
			position += 1
			parametric = True
			#TODO: Check if we've reached the end of the string
			while self.current_string[position] != ')':
				symbol += self.current_string[j]
				position += 1
			symbol += self.current_string[position]		
		return symbol,parametric,position


	def derive(self,level):
		i = 0
		self.current_string = self.axiom
		while i < level:
			j = 0
			string_length = len(self.current_string)
			new_string = ""
			while j < string_length:
				symbol = self.current_string[j]
				if symbol == '(':
					k = j
					while k < string_length and self.current_string[k] != ')':
						symbol,parametric,k += get_next_symbol(k)
						k += 1
				else:
					
					
				if symbol not in self.symbols:
					symbol += '('
					j += 1
					continue
				
				
		return self.current_string

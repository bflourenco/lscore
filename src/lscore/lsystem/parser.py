# -*- coding: utf-8 -*-

#		parser.py
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
from lsystem import *

def parse_parameters(string):
		left = string.find('(')
		right = string.find(')')
		parameters = []
		if left != -1 and right != -1:
			parameters = string[left+1:right].split(',')
		
		return parameters
""" A parser for L-Systems

This class implements a parser for L-Systems. The rules must follow this 
format:

<python code>
axiom = "something"
rules:
predecessor:condition:probability:sucessor
.
.
.

Examples: 
the hilbert curve:

axiom = '-X'
rules:
X:1:1:-YF+XFX+FY-
Y:1:1:+XF-YFY-FX+

context-sensitive(abop, page 35-b):
axiom = "F1F1F1"
ignore = set(['+','-','F'])
rules:
0<0>0:1:1:0
0<0>1:1:1:1[-F1F1]
0<1>0:1:1:1
0<1>1:1:1:1
1<0>0:1:1:0
1<0>1:1:1:1F1
1<1>0:1:1:1
1<1>1:1:1:0
+:1:1:-
-:1:1:+

parametric:
axiom = 'B(2)A(4,4)'
rules:
A(x,y): y <= 3 : 1 : A(x*2,x+y)
A(x,y): y  > 3 : 1 : B(x)A(x/y,0)
B(x)  : x < 1  : 1 : C
B(x)  : x >= 1 : 1 : B(x-1)

Before the 'rules:' statement you can put some python code if you want, 
for example you can write a small function and then call it inside a 
rule. Example:

def fib(n):
	i = 0
	a,b = 0,1
	while i < n:
		a,b = b,a+b
		i += 1
	return b
axiom = 'A(4)'
rules:
A(t):1:1:A(fib(t))

The result will be A(4), A(5), A(8), A(34)... 
"""
class Parser:
	def __init__(self):
		self.var_globals = {}
		self.var_locals = {}		
	
	""" Parse a string and return a LSystem object (see lsystem.py)
	
	"""
	def parse_string(self,string):
		python_code, separator, rules = string.partition("rules:")
		#If separator is '' or rules is '', it means that either
		#the statement 'rules:' was not found or there aren't 
		#any rules at all 
		if separator == '' or rules == '':
			raise NoRulesStatementError
				
		exec(python_code,self.var_globals,self.var_locals)
		
		#Check if the user declared an axiom
		if 'axiom' not in self.var_locals:
			raise AxiomNotFound
		seed = None
		#Check if the user declared a seed
		if 'seed' in self.var_locals:
			seed = self.var_locals['seed']
			
					
		lsystem = LSystem(self.var_locals['axiom'],
								  self.var_globals,
								  self.var_locals,
								  seed)
		#TODO: Instead of calling replace twice, write code to 
		#replaces both ' ' and '\t' at the same time
		rules = rules.replace(' ','')
		rules = rules.replace('\t','')
		rules = rules.splitlines()
		
		for rule in rules:
			if rule == '':
				continue
			try:
				predecessor,condition,probability,sucessor,code = rule.split(':',4)
			except ValueError:
				raise NotAWellFormedRule(rule)
			symbol, left_context, right_context = self.parse_predecessor(predecessor)
			
			#Check if the rule's probability is a well-formed float
			try:
				probability = float(probability)
			except ValueError:
				raise InvalidProbability
			
			#If condition is 1 and  since the conditions are evaluated 
			#with the built-in function eval, it's easier if we keep 
			#"True" instead of "1"
			if condition == "1":
				condition = "True"
				
			#We split the symbol the parameters and the character
			#For example: if we have F(a,b,c), symbol = 'F' 
			#and parameters = [[a,0],[b,0],[c,0]]
			parameters = parse_parameters(symbol)
			symbol = symbol[0]
			
			if code == '':
				code = 'None'
			
			#If everything went well, we are now ready to add our rule
			#to the L-System
			lsystem.add_rule(symbol,sucessor,
									left_context,
									right_context,
									condition,
									probability,
									parameters,
									code)
		
		return lsystem

	""" Parse a predecessor and return a tuple with the symbol, the left 
	context and right context
	
	This method is used by the parse_string method to find the symbol 
	of the production and the contexts. Examples: 
	parse_predecessor("0<1>2") returns ('1','0','2').
	parse_predecessor("1>0") returns ('1',None,'0')
	
	"""		
	def parse_predecessor(self,string):
		left_context_index = string.find('<')
		right_context_index = string.find('>')
		left_context = None
		right_context = None
		symbol_start,symbol_end = 0,len(string)
		#Check if we found a left context
		if left_context_index != -1:
			left_context = string[0:left_context_index]
			symbol_start = left_context_index + 1
		#Check if we found a right context
		if right_context_index != -1:
			right_context = string[right_context_index+1:]
			symbol_end = right_context_index
		
		symbol = string[symbol_start:symbol_end]
		
		return (symbol,left_context,right_context)
		
	
					
class NoRulesStatementError(Exception): pass
#	def __str__(self):
#		print "No 'rules:' statement found."
	
class NotAWellFormedRule(Exception):
	def __init__(self,rule):
		self.rule = rule
class AxiomNotFound(Exception):pass
class InvalidProbability(Exception):pass


if __name__ == "__main__":
	string = open("../tests/order.py").read()
	parser = Parser()
	l = parser.parse_string(string)
	print l.derive(4)

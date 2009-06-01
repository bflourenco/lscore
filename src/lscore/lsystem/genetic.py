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

import random

class GeneticOperators:
	def __init__(self):pass

	def crossover(self,str1,str2, type = 0):
		#We can't perform crossover on empty strings!
		if str1 == "" or str2 == "":
			return str1,str2
		
		sucessor1 = self.break_sucessor(str1)
		sucessor2 = self.break_sucessor(str2)
			
		if type == 0:
			sucessor1_len = len(sucessor1)
			sucessor2_len = len(sucessor2)
			#u1 = random.randint(0,sucessor1_len - 1)
			#u2 = random.randint(0,sucessor1_len - 1)
			
			u1 = 1
			u2 = 5
			
			v1 = 1
			v2 = 3
			
			#v1 = random.randint(0,sucessor2_len - 1)
			#v2 = random.randint(0,sucessor2_len - 1)
			
			min1 = u1
			max1 = u2
			if u2 < u1:
				min1 = u2
				max1 = u1
			
			
			min2 = v1
			max2 = v2
			if v2 < v1:
				min2 = v2
				max2 = v2	
			
			new_sucessor1 = sucessor1[0:min1] + sucessor2[min2:max2+1] + sucessor1[max1+1:]
			new_sucessor2 = sucessor2[0:min2] + sucessor1[min1:max1+1] + sucessor2[max2+1:]
		
		def __cat(s1,s2): return s1 + s2
		return reduce(__cat,new_sucessor1),reduce(__cat,new_sucessor2)
	
	def mutation(self,str,
					  mutation_rate = 0.2,
					  ignored_symbols = set(['(',')','[',']']),
					  symbol_pool = ['F','+','-']):
		new_str =  ""
		for i in str:
			if random.random() <= mutation_rate:
				j = random.choice(symbol_pool)
				new_str += j
			else:
				new_str += i
		return new_str
	""" Break a sucessor and form a list with its components so we can 
	safely perform crossover and keep the rules consistent
	
	For example, break_sucessor("F+-[FF]+A(2,3)") returns 
	['F', '+', '-', '[FF]', '+', 'A(2,3)']
	
	"""
	def break_sucessor(self,str):
		components = []
		i = iter(str)
		while True:
			try:
				char = i.next()
			except StopIteration:
				break
			if char == '(':
				components[-1] += char
				brackets = 1
				try:
					while brackets != 0:
						char = i.next()
						if char == ')':
							brackets -= 1
						elif char == '(':
							brackets += 1
						components[-1] += char
				except StopIteration:
					break
			elif char == '[':
				components.append(char)
				brackets = 1
				try:
					while brackets != 0:
						char = i.next()
						if char == ']':
							brackets -= 1
						elif char == '[':
							brackets += 1
						components[-1] += char
				except StopIteration:
					break
			else:
				components.append(char)
		return components
if __name__ == "__main__":
	g = GeneticOperators()
	#print g.break_sucessor("FF[F]F(2,3)")
	#print g.break_sucessor("FF[FF(4,5)]F(2,3)")
	#print g.break_sucessor("F+-[FF]+A(2,3)[F2]")
	#print g.crossover("FF","Xa")
	#print g.mutation("FF+-FF+-F+-")
	#print g.break_sucessor("F-[[X]+X]+F[+FX]-X")
	#print g.break_sucessor("FF+FF")
	print g.crossover("F-[[X]+X]+F[+FX]-X","FF+FF" )
	#print g.crossover("X+YF+","-FX-Y" )
	


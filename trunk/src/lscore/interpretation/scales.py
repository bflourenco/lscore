# -*- coding: utf-8 -*-

#		scales.py
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

#A few scales
#The scales are given in number of half steps from the root
MAJOR = [0,2,4,5,7,9,11]
MINOR = [0,2,3,5,7,8,10]
PENTA_MAJOR = [0,2,4,7,9]
PENTA_MINOR = [0,2,5,7,10]
HARMONIC_MINOR = [0,2,3,5,7,8,11]
JAPANESE = [0,1,5,7,8]

""" Scale - a class that represents musical scales.

"""
class Scale:
	def __init__(self,steps = MAJOR,transpose = 0,mode = 0 ): 
		self.numOfSteps = len(steps)
		self.transpose = transpose
		self.mode = mode
		self.steps = steps
		self.octave = 5
		self.octaveBounds = (0,10)
		
	def set_steps(self,steps):
		self.steps = steps
		self.numOfSteps = len(steps)
	""" Sets the octave. For example: If we are using the major scale 
	and set the octave to 5, the first note will be C5(60, MIDI 
	notation)
	
	"""
	def set_octave(self,oct):
		self.octave = oct
		
	"""Sets the bounds, so we can wrap around if the note gets too 
	high or too low.
	
	"""	
	def set_bounds(self,bounds):
		self.octaveBounds = bounds
	
	def getMIDINote(self,num):
		note =  (num+self.mode) % self.numOfSteps
		octave = self.octave + ((num+self.mode) / self.numOfSteps)

		if octave > self.octaveBounds[1]:
			octave = self.octaveBounds[1]
		elif octave < self.octaveBounds[0]:
			octave = self.octaveBounds[0]
		
		return octave*12 + self.steps[note] + self.transpose

if __name__ == "__main__":
	scale = Scale()

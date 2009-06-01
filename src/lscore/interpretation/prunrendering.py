# -*- coding: utf-8 -*-

#		prunrendering.py
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
import math

from lscore.lsystem.lsystem import *
from lscore.midi.midifile import MIDIFile
from lscore.midi.midiinstruments import *

import scales
from graphicinterpretation import GraphicInterpretation
from musicalinterpretation import MusicalInterpretation
from turtlemovements import *


""" PrunRendering - Implements the musical rendering as 
described by Prusinkiewicz on his article 'Score generation with L−systems'

"""

class PrunRendering(MusicalInterpretation):
	def __init__(self,scale,
					  tempo = 120,
					  instrument_name = DISTORTION_GUITAR,
					  multiplier = 4,
					  output_name = 'output.mid',
					  delta = math.pi/2.0):
		MusicalInterpretation.__init__(self,scale,tempo,output_name,instrument_name,multiplier)
		self.delta = delta
		
	""" Interpret a string and create a score
	
	"""	
	def create_score(self,string):
		midi = MIDIFile(self.output_name)
		midi.text(string)
		mpqn = 60000000/self.tempo
		midi.setTempo(mpqn)
		midi.timeSignature(4,2,24,8)
		midi.patchChange(0,self.instrument_name)
		
		interpretation = GraphicInterpretation(self.delta,1)
		movements = interpretation.create_movements_list(string)
		segments = self.get_segments(movements)
		
		iter_segments = iter(segments)
		
		found_note = False
		while True:
			try:
				found_note = False
				segment = iter_segments.next()
				x0 = segment[0][0]
				x1 = segment[1][0]
				y0 = segment[0][1]
				y1 = segment[1][1]
				#Holy moly we found a horizontal segment!
				if round(y0) == round(y1):
					found_note = True
					length = int(round(abs(x1-x0)))
					pitch = int(round(y0))
			except StopIteration:
				break
			finally:
				if found_note and length > 0:
					note = self.scale.getMIDINote(pitch)
					midi.noteOn(0,note,127)
					ticks = (midi.timeDivision / self.multiplier)*length
					midi.noteOff(0,note,127,ticks)
		midi.eof()
		midi.write()
	
	""" Return a list of all line segments found inside a list of 
	turtle movements
	
	"""
	def get_segments(self,movements):
		points = list()
		last_point = None
		size = len(movements)
		i = 0
		while i < size:
			if isinstance(movements[i],TurtleDrawForward):
				x0 = movements[i].x0
				x1 = movements[i].x1
								
				if len(points) > 0:
					vec1 = ( points[-1][1][0] - points[-1][0][0],
						     points[-1][1][1] - points[-1][0][1],
						     points[-1][1][2] - points[-1][0][2])
					vec2 = (x1[0] - x0[0],x1[1] - x0[1],x1[2] - x0[2])
					#Check if the new point and the last poind added 
					#to the list share the same direction				
					if self.same_direction(vec1,vec2):
						points[-1][1] = x1
					else:
						points.append([x0,x1])
				else:
					points.append([x0,x1])
			i += 1	
		return points
		
	""" Return true if the vector vec1 and vec2 have the same direction.
	Return False otherwise
	
	"""	
	def same_direction(self,vec1,vec2):
		same_direction = False
		c = None
		#we try to find non-zero vector components so we can calculate
		#the ratio
		if not self.double_equal(vec1[0],0) and not self.double_equal(vec2[0],0):
			c = vec2[0]/vec1[0]
		elif not self.double_equal(vec1[1],0) and not self.double_equal(vec2[1],0):
			c = vec2[1]/vec1[1]
		elif not self.double_equal(vec1[2],0) and not self.double_equal(vec2[2],0):
			c = vec2[2]/vec1[2]
		same_direction = False
		
		if c is not None:
			if self.double_equal(c*vec1[0], vec2[0]):
				if self.double_equal(c*vec1[1], vec2[1]):
					if self.double_equal(c*vec1[2], vec2[2]):
						same_direction = True
		return same_direction
	""" Return True if a and b are equal, return False otherwise
	
	"""
	def double_equal(self,a,b):
		if (abs(a-b) < 0.0001):
			return True
		else:
			return False	
def main():
	l = LSystem("L")
	l.addProduction("L","L+F+R-F-L+F+R-F-L-F-R+F+L-F-R-F-L+F+R-F-L-F-R-F-L+F+R+F+L+F+R-F-L+F+R+F+L-R-F+F+L+F+R-F-L+F+R-F-L")
	l.addProduction("R","R-F-L+F+R-F-L+F+R+F+L-F-R+F+L+F+R-F-L+F+R+F+L+F+R-F-L-F-R-F-L+F+R-F-L-F-R+F+L-F-R-F-L+F+R-F-L+F+R")
	major = scales.Scale(scales.PENTA_MINOR)
	major.set_octave(5)
	major.set_bounds((4,10))
	r= PrunRendering(scale = major, multiplier = 4,instrument_name = HARPSICHORD)
	r.create_score(l.generateString(3))

if __name__ == "__main__":
	main()

# -*- coding: utf-8 -*-

#		sequentialrendering.py
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

from lscore.midi.midifile import MIDIFile
from lscore.midi.midiinstruments import *
from lscore.lsystem.lsystem import *

from  musicalinterpretation import MusicalInterpretation
from  stochasticplayer import StochasticPlayer 
import scales

""" SequentialRendering - Implements the sequential rendering.
See Growing Music: musical interpretations of L-Systems by 
Peter Worth and Susan Stepney
"""
class SequentialRendering(MusicalInterpretation):
	def __init__(self,scale,
					  tempo = 120,
					  instrument_name = DISTORTION_GUITAR,
					  multiplier = 4,
					  output_name = 'output.mid'):
		MusicalInterpretation.__init__(self,scale,tempo,output_name,instrument_name,multiplier)
	
	def create_score(self,string):
		timeOffset = 0
		currentNote = 0
		#Monta pilha com a string
		#O topo da pilha é o primeiro elemento da string
		str_stack = list(string)
		note_stack = list()
		time_stack = list()
		
		midi = MIDIFile(self.output_name)
		midi.text(string)
		mpqn = 60000000/self.tempo
		midi.setTempo(mpqn)
		midi.timeSignature(4,2,24,8)
		midi.patchChange(0,self.instrument_name)
		
		player = StochasticPlayer(vibrato = 0.9)
		while True:
			try:
				tok = str_stack.pop(0)
				#Só gera código quando encontra uma sequência de pelo
				#menos 1 F
				if tok is 'F':
					noteLength = 0
					while tok is 'F':
						noteLength += 1
						tok = str_stack.pop(0)
					note = self.scale.getMIDINote(currentNote)
					midi.noteOn(0,note,127)
					ticks = (midi.timeDivision / self.multiplier)*noteLength
					midi.noteOff(0,note,127,ticks)
					#player.play(midi,note,ticks)	 	 
				if tok is '+':
					currentNote +=1
				elif tok is '-':
					currentNote -=1
				elif tok is '[':
					note_stack.append(currentNote)
				elif tok is ']':
					currentNote = note_stack.pop()	
			except IndexError:
				break
		midi.eof()
		midi.write()

def main():
	major = scales.Scale(scales.MINOR)
	major.set_bounds((0,7))
	s = SequentialRendering(major)
	
	
	l = LSystem("T")
	l.addProduction("T","TF+TF+TF+")
	l.addProduction("F","FF")
	s.create_score(l.generateString(8))
if __name__ == "__main__":
	main()

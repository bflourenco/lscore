# -*- coding: utf-8 -*-

#		schenkerianrendering.py
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
import scales


""" Schenkerian Rendering - see 
Growing Music: musical interpretations of L-Systems by 
Peter Worth and Susan Stepney

"""
class SchenkerianRendering(MusicalInterpretation):
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
		strStack = list(string)
		noteStack = list()
		timeStack = list()
		code = str()
		
		midi = MIDIFile(self.output_name)
		midi.text(string)
		mpqn = 60000000/self.tempo
		midi.setTempo(mpqn)
		midi.timeSignature(4,2,24,8)
		midi.patchChange(0,self.instrument_name)
		
		
		noteLength = 0	
		while True:
			try:
				tok = strStack.pop(0)
				if tok is 'F':
					noteLength += 1	 
				if tok is '+':
					currentNote +=1
				elif tok is '-':
					currentNote -=1
				elif tok is '[':
					noteStack.append(currentNote)
					timeStack.append(noteLength)
					noteLength = 0
				elif tok is ']':
					if noteLength is not 0:
						note = self.scale.getMIDINote(currentNote)
						midi.noteOn(0,note,127)
						ticks = (midi.timeDivision / self.multiplier)*noteLength
						midi.noteOff(0,note,127,ticks)	

					currentNote = noteStack.pop()
					noteLength = timeStack.pop()	
			except IndexError:
				note = self.scale.getMIDINote(currentNote)
				midi.noteOn(0,note,127)
				ticks = (midi.timeDivision / self.multiplier)*noteLength
				midi.noteOff(0,note,127,ticks)	
				break
		midi.eof()
		midi.write()

if __name__ == "__main__":
	major = scales.Scale(scales.MAJOR)
	s = SchenkerianRendering(major)
	l = LSystem("X")
	l.addProduction("X","F[+X][-X]FX")
	l.addProduction("F","FF")
	s.create_score(l.generateString(3))

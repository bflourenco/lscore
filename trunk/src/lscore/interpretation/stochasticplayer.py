# -*- coding: utf-8 -*-

#		stochasticplayer.py
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

class StochasticPlayer:
	def __init__(self,glissando = 0.1, 
					  pitch_bend = 0.05, 
					  vibrato = 0.1, 
					  octave = 0.05, 
					  thrill = 0.05,
					  seed = None):
		self.glissando = glissando
		self.pitch_bend = pitch_bend
		self.vibrato = vibrato
		self.octave = octave
		self.thrill = thrill
		if seed is not None:
			self.seed = seed
		self.previous = None
		
	def do_pitch_bend(self,midi_file, current_note, target_note,ticks):
		ticks_per_transition= ticks/200
		
		diff = target_note - current_note
		#Set the range of the pitch bend
		midi_file.pitchBendRange(0,abs(diff),0,0)
		midi_file.noteOn(0,current_note,127)
		
		step = 81
		if diff < 0:
			step = -81
		for i in range(0,99):
			midi_file.pitchBend(0,8192 + i*step,ticks_per_transition)
		if diff < 0:
			midi_file.pitchBend(0,0, ticks_per_transition)
		else:
			midi_file.pitchBend(0,16383, ticks_per_transition)
		midi_file.noteOff(0,current_note,127,ticks - 100*ticks_per_transition)
		#Pitch bend reset
		midi_file.pitchBend(0,8192,0)
		
	def do_vibrato(self,midi_file,note,ticks):
		midi_file.controller(0,1,127)
		midi_file.noteOn(0,note,127)
		midi_file.noteOff(0,note,127,ticks)
		#vibrato reset
		midi_file.controller(0,1,0)	
		
	def play(self, midi_file, note, ticks):
		#If we haven't played a note before, just play a note
		if self.previous is None:
			midi_file.noteOn(0,note,127)
			midi_file.noteOff(0,note,127,ticks)
			self.previous = note
		else:
			u = random.random()
			aux = 0
			#Play one octave higher if possible
			aux += self.octave
			if u <= aux:
				self.previous = note
				return
			#Do a pitch bend
			aux += self.pitch_bend
			if u <= aux:
				self.do_pitch_bend(midi_file,self.previous,note,ticks)
				self.previous = note
				return
			#Do a vibrato
			aux += self.vibrato
			if u <= aux:
				self.do_vibrato(midi_file,note,ticks)
				self.previous = note
				return
			#Do a thrill
			aux += self.thrill
			if u <= aux:
				self.previous = note
				return
			#Do a glissando
			aux += self.glissando
			if u <= aux:
				self.previous = note
				return
				
			#Play a normal note	
			midi_file.noteOn(0,note,127)
			midi_file.noteOff(0,note,127,ticks)
			self.previous = note
if __name__ == "__main__":
	midi = MIDIFile("teste.mid",0,1,480)
	midi.setTempo(750000)
	midi.timeSignature(4,2,24,8)
	midi.patchChange(0,29,0)
	player = StochasticPlayer()
	player.do_pitch_bend(midi,60,56,480)
	midi.noteOn(0,56,100,0)
	midi.noteOff(0,56,100,480)
	
	midi.eof()
	midi.write()

# -*- coding: utf-8 -*-

#		scoredialog.py
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

import gtk
import pygtk


import math
import gettext


from lscore.interpretation import scales
from lscore.interpretation.sequentialrendering import SequentialRendering
from lscore.interpretation.schenkerianrendering import SchenkerianRendering
from lscore.interpretation.prunrendering import PrunRendering


_ = gettext.gettext

class ScoreDialog(gtk.Dialog):
	def __init__(self,window,buffer):
		gtk.Dialog.__init__(self,_('Score Generation'),
								 window)
		self.set_default_size(250,300)
		self.set_destroy_with_parent(True)
		self.set_modal(True)
		self.buffer = buffer
		
		rendering_frame = self.create_rendering_frame()
		scale_frame = self.create_notes_frame()
		misc_frame = self.create_misc_frame()
		player_frame = self.create_player_frame()
		
		self.vbox.pack_start(rendering_frame,True,True,5)
		self.vbox.pack_start(scale_frame,True,True,5)
		self.vbox.pack_start(misc_frame,True,True,5)
		#self.vbox.pack_start(player_frame,True,True,5)
		
		
		
		self.add_button(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL)
		score_button = self.add_button(_("Go!"),gtk.RESPONSE_OK)
		score_image = gtk.Image()
		score_image.set_from_stock(gtk.STOCK_MEDIA_PLAY,gtk.ICON_SIZE_BUTTON)
		score_button.set_image(score_image)
	
		self.connect("response",self.response_callback)

		self.show_all()
		
	def create_label(self,str):
		label = gtk.Label(str)
		label.set_use_markup(True)
		label.set_alignment(0,0.5)	
		
		return label
		
		
	def create_empty_frame(self,str):
		label = self.create_label(str)
		
		frame = gtk.Frame()
		frame.set_label_widget(label)
		
		alignment = gtk.Alignment()
		alignment.set_padding(0,15,15,15)
		frame.alignment = alignment
		frame.add(alignment)
		return frame

	def create_rendering_frame(self):
		frame = self.create_empty_frame(_("<b>Rendering</b>"))
		

		hbox = gtk.HBox(True,15)
		vbox1 = gtk.VBox(False,0)
		vbox2 = gtk.VBox(False,0)
		
		hbox.pack_start(vbox1,True,True,0)
		hbox.pack_start(vbox2,True,True,0)
		frame.alignment.add(hbox)
		
		#Create the rendering method label and combo box
		method_label = self.create_label(_("Method"))
		self.method_combo = gtk.combo_box_new_text()
		self.method_combo.append_text("Sequential")
		self.method_combo.append_text("Schenkerian")
		self.method_combo.append_text("Prusinkiewicz")
		self.method_combo.set_active(0)
		vbox1.pack_start(method_label,False,False,0)
		vbox1.pack_start(self.method_combo,False,False,0)
		
		#Create the instrument label and button
		instrument_label = self.create_label(_("Instrument Number"))
		instrument_button_adjustment = gtk.Adjustment(0,0,127,1,5,0)
		self.instrument_button = gtk.SpinButton(instrument_button_adjustment)
		self.instrument_button.set_numeric(True)
		self.instrument_button.set_value(0)
		vbox1.pack_start(instrument_label,False,False,0)
		vbox1.pack_start(self.instrument_button,False,False,0)
		
		tempo_label = self.create_label(_("Tempo"))
		tempo_button_adjustment = gtk.Adjustment(0,30,300,1,5,0)
		self.tempo_button = gtk.SpinButton(tempo_button_adjustment)
		self.tempo_button.set_numeric(True)
		self.tempo_button.set_value(120)
		vbox2.pack_start(tempo_label,True,True,0)
		vbox2.pack_start(self.tempo_button,True,True,0)
		
		multiplier_label = self.create_label(_("Tempo Multiplier"))
		multiplier_button_adjustment = gtk.Adjustment(0,0.01,100,1,5,0)
		self.multiplier_button = gtk.SpinButton(multiplier_button_adjustment)
		self.multiplier_button.set_numeric(True)
		self.multiplier_button.set_value(4)
		self.multiplier_button.set_digits(2)
		vbox2.pack_start(multiplier_label,False,False,0)
		vbox2.pack_start(self.multiplier_button,False,False,0)
		
		
		
		return frame
	def create_player_frame(self):	
		frame = self.create_empty_frame(_("<b>Player</b>"))
		hbox = gtk.HBox(True,30)
		vbox1 = gtk.VBox(False,0)
		
		hbox.pack_start(vbox1,True,True,0)
		frame.alignment.add(hbox)
		
		stochastic_button = gtk.CheckButton(_("Stochastic"))
		vbox1.pack_start(stochastic_button,True,True,0)
		hbox2 = gtk.HBox(True,60)
		
		hbox.pack_start(hbox2,True,True,0)
		frame2 = self.create_empty_frame(_("Probabilities"))
		frame2.set_sensitive(False)
		frame2.alignment.set_padding(0,12,12,12)
		hbox2.pack_start(frame2,False,False,0)
		vbox3 = gtk.VBox(False,0)
		frame2.alignment.add(vbox3)
		
		normal_note_label = self.create_label(_("Normal Note"))
		normal_note_button_adjustment = gtk.Adjustment(0,0,1,0.1,1,0)
		self.normal_note_button = gtk.SpinButton(normal_note_button_adjustment)
		self.normal_note_button.set_numeric(True)
		self.normal_note_button.set_value(0.700)
		self.normal_note_button.set_digits(3)
		vbox3.pack_start(normal_note_label,True,True,0)
		vbox3.pack_start(self.normal_note_button,True,True,0)
		
		pitch_bend_label = self.create_label(_("Pitch Bend"))
		pitch_bend_button_adjustment = gtk.Adjustment(0,0,1,0.1,1,0)
		self.pitch_bend_button = gtk.SpinButton(pitch_bend_button_adjustment)
		self.pitch_bend_button.set_numeric(True)
		self.pitch_bend_button.set_value(0.150)
		self.pitch_bend_button.set_digits(3)
		vbox3.pack_start(pitch_bend_label,True,True,0)
		vbox3.pack_start(self.pitch_bend_button,True,True,0)
		
		vibrato_label = self.create_label(_("Vibrato"))
		vibrato_button_adjustment = gtk.Adjustment(0,0,1,0.1,1,0)
		self.vibrato_button = gtk.SpinButton(vibrato_button_adjustment)
		self.vibrato_button.set_numeric(True)
		self.vibrato_button.set_value(0.150)
		self.vibrato_button.set_digits(3)
		vbox3.pack_start(vibrato_label,True,True,0)
		vbox3.pack_start(self.vibrato_button,True,True,0)
		
		
		return frame
		
	""" Create the "notes" frame
	
	"""
	def create_notes_frame(self):
		frame = self.create_empty_frame(_("<b>Notes</b>"))
		
		hbox = gtk.HBox(True,30)
		vbox1 = gtk.VBox(False,0)
		
		hbox.pack_start(vbox1,True,True,0)
		frame.alignment.add(hbox)
		
		
		scale_label = self.create_label(_("Scale"))
		self.scale_combo = gtk.combo_box_new_text()
		self.scale_combo.append_text("Major")
		self.scale_combo.append_text("Minor")
		self.scale_combo.append_text("Penta Major")
		self.scale_combo.append_text("Penta Minor")
		self.scale_combo.append_text("Harmonic")
		self.scale_combo.append_text("Japanese")
		self.scale_combo.set_active(0)
		
		vbox1.pack_start(scale_label,False,False,0)
		vbox1.pack_start(self.scale_combo,False,False,0)
		
		
		transpose_label = self.create_label(_("Transpose"))
		transpose_button_adjustment = gtk.Adjustment(0,0,11,1,5,0)
		self.transpose_button = gtk.SpinButton(transpose_button_adjustment)
		self.transpose_button.set_value(0)
		self.transpose_button.set_numeric(True)
		vbox1.pack_start(transpose_label,False,False,0)
		vbox1.pack_start(self.transpose_button,False,False,0)
		
		mode_label = self.create_label(_("Mode"))
		mode_button_adjustment = gtk.Adjustment(0,0,11,1,5,0)
		self.mode_button = gtk.SpinButton(mode_button_adjustment)
		self.mode_button.set_value(0)
		self.mode_button.set_numeric(True)
		vbox1.pack_start(mode_label,False,False,0)
		vbox1.pack_start(self.mode_button,False,False,0)
		
		#Create the octave frame
		vbox2 = gtk.VBox(False,0)
		octave_frame = self.create_empty_frame(_("Octave"))
		octave_frame.alignment.set_padding(0,12,12,12)
		hbox.pack_start(octave_frame,False,False,0)
		octave_frame.alignment.add(vbox2)
		
		
		start_label = self.create_label(_("Start"))
		start_button_adjustment = gtk.Adjustment(0,0,10,1,5,0)
		self.start_button = gtk.SpinButton(start_button_adjustment)
		self.start_button.set_numeric(True)
		self.start_button.set_value(5)
		vbox2.pack_start(start_label,True,True,0)
		vbox2.pack_start(self.start_button,True,True,0)
		
		upper_bound_label = self.create_label(_("Upper Bound"))
		upper_bound_button_adjustment = gtk.Adjustment(0,0,10,1,5,0)
		self.upper_bound_button = gtk.SpinButton(upper_bound_button_adjustment)
		self.upper_bound_button.set_numeric(True)
		self.upper_bound_button.set_value(10)
		vbox2.pack_start(upper_bound_label,True,True,0)
		vbox2.pack_start(self.upper_bound_button,True,True,0)

		lower_bound_label = self.create_label(_("Lower Bound"))
		lower_bound_button_adjustment = gtk.Adjustment(0,0,10,1,5,0)
		self.lower_bound_button = gtk.SpinButton(lower_bound_button_adjustment)
		self.lower_bound_button.set_numeric(True)
		self.lower_bound_button.set_value(0)
		vbox2.pack_start(lower_bound_label,True,True,0)
		vbox2.pack_start(self.lower_bound_button,True,True,0)

		return frame
	""" Create the "misc" frame
	
	"""
	def create_misc_frame(self):
		frame = self.create_empty_frame(_("<b>Misc</b>"))
		hbox = gtk.HBox(False,0)		
		vbox = gtk.VBox(False,0)
		
		frame.alignment.add(hbox)
		hbox.pack_start(vbox,False,False,0)
		
		
		delta_label = self.create_label("Delta")
		delta_button_adjustment = gtk.Adjustment(0,0,360,1,5,0)
		self.delta_button = gtk.SpinButton(delta_button_adjustment)
		self.delta_button.set_numeric(True)
		self.delta_button.set_value(90)
		self.delta_button.set_digits(2)
		vbox.pack_start(delta_label,False,False,0)
		vbox.pack_start(self.delta_button,False,False,0)
		
		stochastic_button = gtk.CheckButton(_("Stochastic"))
		stochastic_button.set_sensitive(False)
		hbox.pack_start(stochastic_button,False,False,60)

		return frame
		
	""" Callback connected to the response signal.
	
	We handle the response signal here. If the response id is 
	RESPONSE_OK we try to create a score and close the score dialog.
	
	
	"""
	def response_callback(self,dialog,id):
		if id == gtk.RESPONSE_CANCEL:
			self.destroy()	
		elif id == gtk.RESPONSE_OK:
			#Get the input from the widgets
			method_name = self.method_combo.get_active_text()
			instrument = self.instrument_button.get_value_as_int()
			tempo = self.tempo_button.get_value_as_int()
			multiplier = self.multiplier_button.get_value_as_int()
			
			scale_name = self.scale_combo.get_active_text()
			transpose = self.transpose_button.get_value_as_int()
			mode = self.mode_button.get_value_as_int()
			octave = self.start_button.get_value_as_int()
			upper_bound = self.upper_bound_button.get_value_as_int()
			lower_bound = self.lower_bound_button.get_value_as_int()
			
			#Convert to rad
			delta = self.delta_button.get_value_as_int()*math.pi/180
		
			scale = scales.Scale(scales.MAJOR,transpose,mode)
			if scale_name == "Minor":
				scale.set_steps(scales.MINOR)
			elif scale_name == "Penta Major":
				scale.set_steps(scales.PENTA_MAJOR)
			elif scale_name == "Penta Minor":
				scale.set_steps(scales.PENTA_MINOR)
			elif scale_name == "Harmonic":
				scale.set_steps(scales.HARMONIC_MINOR)
			elif scale_name == "Japanese":
				scale.set_steps(scales.JAPANESE)
				
			scale.set_octave(octave)
			scale.set_bounds((lower_bound,upper_bound))
			print scale.steps
			print scale_name
			#TODO: Check if upper_bound > octave > lower_bound
			if method_name == "Sequential":
				method = SequentialRendering(scale,tempo,instrument,multiplier)
			elif method_name == "Schenkerian":
				method = SchenkerianRendering(scale,tempo,instrument,multiplier)
			elif method_name == "Prusinkiewicz":
				method = PrunRendering(scale,tempo,instrument,multiplier,delta = delta)
			method.set_note_length_multiplier(multiplier)
			
			start,end = self.buffer.get_bounds()
			text = self.buffer.get_slice(start,end,False)
			
			#If everything until now went ok, we will prompt the user 
			#to tell us the name of the file that will be created
			dialog = gtk.FileChooserDialog(action=gtk.FILE_CHOOSER_ACTION_SAVE,	
									   buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,
										gtk.STOCK_OPEN,gtk.RESPONSE_OK))
			response = dialog.run()
			if response == gtk.RESPONSE_OK:
				filename = dialog.get_filename()
				method.output_name = filename
				method.create_score(text)
				dialog.destroy()
				self.destroy()
			else:
				dialog.destroy()
			

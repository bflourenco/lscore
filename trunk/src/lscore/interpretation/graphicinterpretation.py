# -*- coding: utf-8 -*-

#		GraphicInterpretation.py
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
import cairo

from lscore.lsystem.lsystem import LSystem
from turtlemovements import *
""" The classical graphic interpretation of the L-Systems

This class implements the graphical interpretation of l-systems 
as described on the Algorithmic Beauty of the Plants. Since the 
the main purpose of the program is to create music not graphics, 
this class is very simple.

"""
class GraphicInterpretation:
	def __init__(self, delta = math.pi/2.0,
					   step_size = 1):
		self.turtle = Turtle(delta,step_size)
	
	def create_movements_list(self,str):
		str_stack = list(str)
		self.movements = list()
		while True:
			try:
				tok = str_stack.pop(0)
				movement = None
				
				found = True
				#We are going to match the token with one of the symbols
				#Idea: insert a BeginStack and EndStack
				if tok is '+':
					movement = TurtleTurn(self.turtle.delta)
				elif tok is '-':
					movement = TurtleTurn(-self.turtle.delta)
				elif tok is 'F':
					movement = TurtleDrawForward()
				elif tok is 'f':
					movement = TurtleForward()
				elif tok is '&':
					movement = TurtlePitch(self.turtle.delta)
				elif tok is '^':
					movement = TurtlePitch(-self.turtle.delta)
				elif tok is '\\':
					movement = TurtleRoll(self.turtle.delta)
				elif tok is '/':
					movement = TurtleRoll(-self.turtle.delta)
				elif tok is '|':
					movement = TurtleTurnAround()
				elif tok is '[':
					movement = TurtleBeginStack()
				elif tok is ']':
					movement = TurtleEndStack()
				#It seems we didn't find a symbol. =(
				else:
					found = False
				#Call atualize_turtle only if the the token matched 
				#one of the alphabet symbols
				if found:
					movement.atualize_turtle(self.turtle)
					self.turtle.normalize()
					self.movements.append(movement)
			except IndexError:
				break
		return self.movements
		
	""" Draw on the cairo context specified by cr. You must call 
	create_movements_list first, before calling this method.

	"""
	def draw_on_cairo(self,cr):
		cr.set_source_rgb(1.0, 1.0, 1.0)
		cr.paint()
		cr.set_source_rgb(0,0,0)
		cr.set_line_width(0.07)
		cr.translate(600,600)
		cr.scale(3,3)
		#cr.rotate(math.pi/2)
		for movement in self.movements:
			movement.draw_on_cairo(cr)
	def get_turtle(self):
		return self.turtle
	
#Test Case
def on_expose_event(widget,event):
	l = LSystem("FX")
	l.add_rule("X","X+YF+")
	l.add_rule("Y","-FX-Y")
	string = l.derive(11)
	
	turtle = GraphicInterpretation(delta = math.pi/2,step_size = 1)
	turtle.create_movements_list(string)
	cr = gtk.gdk.Drawable.cairo_create(widget.window)
	turtle.draw_on_cairo(cr)
	
	return False

def on_button_press(widget,event):
	print "%d %d\n" %(event.x,event.y)

def main():
	window = gtk.Window(gtk.WINDOW_TOPLEVEL)
	window.set_default_size(200,100)
	window.set_title('test')
	
	
	drawing_area = gtk.DrawingArea()
	drawing_area.set_size_request(200, 200)
	drawing_area.add_events(gtk.gdk.BUTTON_PRESS_MASK)
	window.add(drawing_area)
	
	drawing_area.connect("expose-event",on_expose_event)
	drawing_area.connect("destroy",gtk.main_quit)
	drawing_area.connect("button-press-event",on_button_press)
	
	window.show_all()
	gtk.main()
if __name__ == "__main__":
	main()

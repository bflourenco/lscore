# -*- coding: utf-8 -*-

#		turtlemovements.py
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

""" A Turtle as described on the The Algorithmic Beauty
of Plants

"""
class Turtle:
	def __init__(self, delta = math.pi/2,
					  step_size = 1):
		#heading vector
		self.h = [-1,0,0]
		#left vector
		self.l = [0,-1,0]
		#up vector
		self.u = [0,0,-1]
		#the initial position of the turtle
		self.position = [0,0,0]
		
		self.delta = delta
		self.step_size = step_size
		
		self.stack = []
		
	""" Pushes the current state of the turtle
	
	"""	
	def push(self):
		#For safety reasons we create a new instance of each object, this
		#way we can be sure that the turtle's state won't affect the 
		#state saved on the stack
		self.stack.append([list(self.h),list(self.l),list(self.u),list(self.position)])
	""" Pops a state from the stack
	
	"""
	def pop(self):
		self.h, self.l, self.u, self.position = self.stack.pop()
	
	def __normalize_3dvector(self,v):
		abs_v = math.sqrt(v[0]*v[0] +v[1]*v[1] + v[2]*v[2])
		return [v[0]/abs_v,v[1]/abs_v,v[2]/abs_v]
	def normalize(self):
		self.h = self.__normalize_3dvector(self.h)
		self.l = self.__normalize_3dvector(self.l)
		self.u = self.__normalize_3dvector(self.u)
		#self.position = self.__normalize_3dvector(self.position)
				
""" An interface to turtle movements.

This class is an interface that should be implemented by the classes 
that represent turtle movements. 

"""
class TurtleMovement:
	""" This method should draw on a cairo context.
	
	"""
	def draw_on_cairo(self,context):
		pass
	""" This method modify the state of the turtle(a Turtle object). 
	
	"""
	def atualize_turtle(self,turtle):
		pass
	
""" The draw forward movement

"""
class TurtleDrawForward(TurtleMovement):
	def draw_on_cairo(self,context):
		context.move_to(self.x0[0], self.x0[1])
		context.line_to(self.x1[0], self.x1[1])
		context.stroke()
	
	def atualize_turtle(self,turtle):
		self.x0 = [turtle.position[0],turtle.position[1],turtle.position[2]]
		turtle.position[0] += turtle.h[0]*turtle.step_size
		turtle.position[1] += turtle.h[1]*turtle.step_size
		turtle.position[2] += turtle.h[2]*turtle.step_size
		self.x1 = [turtle.position[0],turtle.position[1],turtle.position[2]]

""" The turtle 'forward' movement. It's the same as 
the TurtleDrawForward but we don't actually draw the 
line segment
"""
class TurtleForward(TurtleDrawForward):
	def draw_on_cairo(self,context):
		pass 

""" An abstract class for rotation movements

"""
class TurtleRotate(TurtleMovement):
	""" Create a new TurtleRotate. r is the rotation matrix
	
	"""
	def __init__(self,r):
		self.r = r
	
	def atualize_turtle(self,turtle):
		hx = turtle.h[0]*self.r[0][0] + turtle.l[0]*self.r[1][0] + turtle.u[0]*self.r[2][0]
		hy = turtle.h[1]*self.r[0][0] + turtle.l[1]*self.r[1][0] + turtle.u[1]*self.r[2][0]
		hz = turtle.h[2]*self.r[0][0] + turtle.l[2]*self.r[1][0] + turtle.u[2]*self.r[2][0]
		     
		lx = turtle.h[0]*self.r[0][1] + turtle.l[0]*self.r[1][1] + turtle.u[0]*self.r[2][1]
		ly = turtle.h[1]*self.r[0][1] + turtle.l[1]*self.r[1][1] + turtle.u[1]*self.r[2][1]
		lz = turtle.h[2]*self.r[0][1] + turtle.l[2]*self.r[1][1] + turtle.u[2]*self.r[2][1]
		     
		ux = turtle.h[0]*self.r[0][2] + turtle.l[0]*self.r[1][2] + turtle.u[0]*self.r[2][2]
		uy = turtle.h[1]*self.r[0][2] + turtle.l[1]*self.r[1][2] + turtle.u[1]*self.r[2][2]
		uz = turtle.h[2]*self.r[0][2] + turtle.l[2]*self.r[1][2] + turtle.u[2]*self.r[2][2]            
		
		turtle.h = [hx,hy,hz]
		turtle.l = [lx,ly,lz]
		turtle.u = [ux,uy,uz]
"""Turn the turtle around the u vector

"""		
class TurtleTurn(TurtleRotate):
	
	def __init__(self,delta):
		r1 = (math.cos(delta),-math.sin(delta),0)
		r2 = (math.sin(delta),math.cos(delta),0)
		r3 = (0,0,1)
		TurtleRotate.__init__(self,(r1,r2,r3))

"""Pitch the turtle around the l vector

"""				
class TurtlePitch(TurtleRotate):
	def __init__(self,delta):
		r1 = (math.cos(delta),0,math.sin(delta))
		r2 = (0,1,0)
		r3 = (-math.sin(delta),0,math.cos(delta))
		TurtleRotate.__init__(self,(r1,r2,r3))

"""Roll the turtle around the h vector

"""			
class TurtleRoll(TurtleRotate):
	def __init__(self,delta):
		r1 = (1,0,0)
		r2 = (0,math.cos(delta),math.sin(delta))
		r3 = (0,-math.sin(delta),math.cos(delta))
		TurtleRotate.__init__(self,(r1,r2,r3))
		
class TurtleTurnAround(TurtleTurn):
	def __init__(self):
		TurtleTurn.__init__(self,math.pi)

"""Dummy class to flag the beginning of a stack. Usually because 
a [ was found in the string
"""
class TurtleBeginStack(TurtleMovement):
	def atualize_turtle(self,turtle):
		turtle.push()

"""Dummy class to flag the end of stack. Usually because 
a ] was found in the string
"""	
class TurtleEndStack(TurtleMovement):
	def atualize_turtle(self,turtle):
		turtle.pop()

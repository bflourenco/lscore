# -*- coding: utf-8 -*-

#		mainwindow.py
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
import os
import gettext
import gtksourceview2

from lscore.lsystem.parser import Parser
from lscore.gui.scoredialog import ScoreDialog



_ = gettext.gettext

untitled = _("untitled")

class MainWindow:
	def __init__(self):
		#create a window
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.set_default_size(370,400)
		self.window.set_position(gtk.WIN_POS_CENTER)
		
		vbox = gtk.VBox(False,0)
		self.window.add(vbox)
		
		
		self.accel_group = gtk.AccelGroup()
		self.window.add_accel_group(self.accel_group)
		
		#Create the notebook
		notebook = gtk.Notebook()
		notebook.set_tab_pos(gtk.POS_TOP)
		notebook.set_show_border(True)
		
		#Create the L-System text view
		scrolled_window = gtk.ScrolledWindow()
		language_manager = gtksourceview2.LanguageManager()
		buffer = gtksourceview2.Buffer(language = language_manager.get_language("python"))
		self.view = gtksourceview2.View(buffer)		
		scrolled_window.add_with_viewport(self.view)
		scrolled_window.set_policy(gtk.POLICY_AUTOMATIC,gtk.POLICY_AUTOMATIC)
		scrolled_window.set_shadow_type(gtk.SHADOW_OUT)
		self.view.set_wrap_mode(gtk.WRAP_CHAR)
		page_label = gtk.Label("L-System")
		notebook.append_page(scrolled_window,page_label)
		
		#Create the Result text view
		scrolled_window = gtk.ScrolledWindow()
		self.view2 = gtk.TextView()
		scrolled_window.add_with_viewport(self.view2)
		scrolled_window.set_policy(gtk.POLICY_AUTOMATIC,gtk.POLICY_AUTOMATIC)
		scrolled_window.set_shadow_type(gtk.SHADOW_OUT)
		self.view2.set_wrap_mode(gtk.WRAP_CHAR)
		page_label = gtk.Label(_("Result"))
		notebook.append_page(scrolled_window,page_label)
		
		#Create the menu
		menubar = self.create_menu()
		vbox.pack_start(menubar,False,False,0)
		
		#Create the toolbar
		toolbar = self.create_toolbar()
		#statusbar = gtk.Statusbar()
		
		vbox.pack_start(toolbar,False,False,0)		
		vbox.pack_start(notebook,True,True,0)
		#vbox.pack_start(statusbar,False,False,0)
	
		self.filename = untitled
		self.set_title()
		
		self.window.connect("delete_event",self.quit_callback)
		self.window.show_all()
		gtk.main()
		
	"""Create the menu
	
	"""
	def create_menu(self):
		menubar = gtk.MenuBar()
		
		#The "File" item at the main menu
		file = gtk.MenuItem(_("_File"),True)
		filemenu = gtk.Menu()
		file.set_submenu(filemenu)
		
		#Create the buttons and add them to the file menu
		new_button =  gtk.ImageMenuItem(gtk.STOCK_NEW)
		open_button = gtk.ImageMenuItem(gtk.STOCK_OPEN)
		save_button = gtk.ImageMenuItem(gtk.STOCK_SAVE)
		save_as_button = gtk.ImageMenuItem(gtk.STOCK_SAVE_AS)
		
		quit_button = gtk.ImageMenuItem(gtk.STOCK_QUIT)
		
		iterate_button = gtk.ImageMenuItem(_("_Iterate"))
		iterate_image = gtk.Image()
		iterate_image.set_from_stock(gtk.STOCK_CONVERT,gtk.ICON_SIZE_MENU)
		iterate_button.set_image(iterate_image)
		
		score_button = gtk.ImageMenuItem(_("_Score"))
		score_image = gtk.Image()
		score_image.set_from_stock(gtk.STOCK_MEDIA_PLAY,gtk.ICON_SIZE_MENU)
		score_button.set_image(score_image)
		
		graphics_button = gtk.ImageMenuItem(_("_Graphics"))
		graphics_image = gtk.Image()
		graphics_image.set_from_stock(gtk.STOCK_ORIENTATION_PORTRAIT,gtk.ICON_SIZE_MENU)
		graphics_button.set_image(graphics_image)

		sep1 = gtk.SeparatorMenuItem()
		sep2 = gtk.SeparatorMenuItem()
		#Append the buttons to the file menu
		filemenu.append(new_button)
		filemenu.append(open_button)
		filemenu.append(save_button)
		filemenu.append(save_as_button)
		filemenu.append(sep1)
		filemenu.append(iterate_button)
		filemenu.append(score_button)
		filemenu.append(graphics_button)
		filemenu.append(sep2)
		filemenu.append(quit_button)
		
		#The help item at the main menu
		help = gtk.MenuItem(_("_Help"),True)
		helpmenu = gtk.Menu()
		help.set_submenu(helpmenu)
		about_button = gtk.ImageMenuItem(gtk.STOCK_ABOUT)
		helpmenu.append(about_button)
		
		menubar.append(file)
		menubar.append(help)
		
		
		#Connect the callbacks
		buffer = self.view.get_buffer()
		new_button.connect("activate",self.new_file)
		open_button.connect("activate",self.open_dialog)
		save_button.connect("activate",self.save_callback)
		save_as_button.connect("activate",self.save_as_dialog)
		quit_button.connect("activate",self.quit_callback,None)
		score_button.connect("activate",self.show_score_window)
		iterate_button.connect("activate",self.iterate_callback)
		
		about_button.connect("activate",self.about_dialog)
	
		#Connect accelerators
		save_button.add_accelerator("activate",self.accel_group,ord('s'),
											  gtk.gdk.CONTROL_MASK,
											  gtk.ACCEL_VISIBLE)
		
		return menubar
	def quit_callback(self,widget,event):
		buffer = self.view.get_buffer()
		if not buffer.get_modified():
			gtk.main_quit()
		else:
			title = _("Save changes to '%s'?") % (self.filename)
			dialog = gtk.MessageDialog(self.window,gtk.DIALOG_DESTROY_WITH_PARENT,
									   gtk.MESSAGE_QUESTION,
									   gtk.BUTTONS_NONE,
									   title)
			dialog.add_button(_("Close without saving"),1)
			dialog.add_button(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL)
			dialog.add_button(gtk.STOCK_SAVE,gtk.RESPONSE_YES)
			response = dialog.run()
			dialog.destroy()
			if response == gtk.RESPONSE_YES:
				self.save_callback(widget)
			elif response == 1:
				gtk.main_quit()
		return True
		
	def iterate_callback(self,widget):
		#get the text written on the LSystem page
		buffer = self.view.get_buffer()
		start,end = buffer.get_bounds()
		string = buffer.get_slice(start,end,False)
		#parse the text
		lsystem = Parser().parse_string(string)
		result = ""
		level = 0
		if 'level' in lsystem.var_locals:
			level = lsystem.var_locals['level']
		else:
			#In this case we ask the number of iterations
			dialog = gtk.MessageDialog(self.window,gtk.DIALOG_DESTROY_WITH_PARENT,
									  gtk.MESSAGE_QUESTION,
									  gtk.BUTTONS_OK_CANCEL,
									  _("Enter the number of iterations:"))
			
			level_button_adjustment = gtk.Adjustment(0,0,100,1,5,0)
			level_button = gtk.SpinButton(level_button_adjustment)
			level_button.set_alignment(10)
			level_button.set_numeric(True)
			dialog.vbox.pack_end(level_button,False,False,0)
			level_button.show()
			
			response = dialog.run()
			#if the user clicked on the 'ok' button we call lsystem.derive
			#otherwise we just destroy the dialog and return
			level = level_button.get_value_as_int()
			dialog.destroy()
			if response != gtk.RESPONSE_OK:
				return
		
		result = lsystem.derive(level)
		buffer = self.view2.get_buffer()
		buffer.set_text(result)
		
	"""Create the toolbar
	
	The toolbar has 4 buttons: An open button, a 
	save button, a score button and a graphics button.
	
	"""
	def create_toolbar(self):
		#create a toolbar
		toolbar = gtk.Toolbar()
		toolbar.set_style(gtk.TOOLBAR_BOTH)
		
		#The open button
		open_button = gtk.ToolButton(gtk.STOCK_OPEN)
		toolbar.insert(open_button,-1)
		#The save button
		save_button = gtk.ToolButton(gtk.STOCK_SAVE)
		toolbar.insert(save_button,-1)
		#separator
		sep = gtk.SeparatorToolItem()
		toolbar.insert(sep,-1)
		#Iterate button
		iterate_button = gtk.ToolButton(gtk.STOCK_CONVERT)
		iterate_button.set_label(_("Iterate"))
		toolbar.insert(iterate_button,-1)
		#separator
		sep = gtk.SeparatorToolItem()
		toolbar.insert(sep,-1)
		#The create score button
		score_button = gtk.ToolButton(gtk.STOCK_MEDIA_PLAY)
		score_button.set_label(_("Score"))
		toolbar.insert(score_button,-1)
		#The graphics button
		graphics_button = gtk.ToolButton(gtk.STOCK_ORIENTATION_PORTRAIT)
		graphics_button.set_label(_("Graphics"))
		toolbar.insert(graphics_button,-1)
		
		#Connect the callbacks
		buffer = self.view.get_buffer()
		iterate_button.connect("clicked",self.iterate_callback)
		open_button.connect("clicked",self.open_dialog)
		save_button.connect("clicked",self.save_callback)
		score_button.connect("clicked",self.show_score_window)
		
		#Create the tooltips
		open_button.set_tooltip_text(_("Open an existing file"))
		save_button.set_tooltip_text(_("Save the current L-System"))
		score_button.set_tooltip_text(_("Create a new score with"
										" the current file"))
		graphics_button.set_tooltip_text(_("Interpret the current file"
										   " as a turtle graphics description"))
		iterate_button.set_tooltip_text(_("Iterate the current L-System"))
		return toolbar
		
		
	"""Callback connected to the 'new file' button

	Substitute the current text buffer with an empty string 
	and call set_title to change the title of the window
	"""
	def new_file(self,widget):
		#Substitute the buffer with an empty string
		buffer = self.view.get_buffer()
		buffer.set_text("")
		buffer.set_modified(False)
		self.filename = untitled
		self.set_title()
	
	def set_title(self):
		if self.filename == untitled:
			title = untitled + ' - ' + 'LScore'
		else:
			title = os.path.basename(self.filename) + ' - ' + 'LScore'
		self.window.set_title(title)
		
	"""Callback connected to the 'open file' buttons.

	Display the file selection dialog then tries to open a file
	"""
	def open_dialog(self,widget):
		dialog = gtk.FileChooserDialog(action=gtk.FILE_CHOOSER_ACTION_OPEN,	
									   buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,
										gtk.STOCK_OPEN,gtk.RESPONSE_OK))

		while True:
			response = dialog.run()
			if response == gtk.RESPONSE_OK:
				filename = dialog.get_filename()
				try:
					buffer = self.view.get_buffer()
					#open the file
					f = open(filename)
					buffer.set_text(f.read())
					buffer.set_modified(False)
					f.close()
					
					self.filename = filename
					self.set_title()
					
					break
				except IOError, (errnum, errmsg):
					#Show the error dialog if we catch an IOError
					err =_( "Cannot open file '%s': %s" ) % (filename, errmsg)
					error_dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL,
													 gtk.MESSAGE_INFO,
													 gtk.BUTTONS_OK, err);
					error_dialog.run()
					error_dialog.destroy()
			else:
				break
		
		dialog.destroy()
	
	""" Callback connected to the 'save as' buttons.

	Display the file selection dialog then try to save the file. Display 
	an error if it fails to write the file.

	"""
	def save_as_dialog(self,widget):
		dialog = gtk.FileChooserDialog(action=gtk.FILE_CHOOSER_ACTION_SAVE,	
									   buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,
										gtk.STOCK_OPEN,gtk.RESPONSE_OK))
		while True:
			response = dialog.run()
			if response == gtk.RESPONSE_OK:
				filename = dialog.get_filename()
				try:
					#Get the current text buffer
					buffer = self.view.get_buffer()
					#Create a file with the chosen name
					f = open(filename,'w')
					#Get the beginning and the end of the buffer
					start,end = buffer.get_bounds()
					#Write the contents to the file
					f.write(buffer.get_slice(start,end,False))
					#Close the file
					f.close()			
				except IOError, (errnum, errmsg):
					#Show the error dialog if we catch an IOError
					err = _("Error writing to '%s': %s") % (filename, errmsg)
					error_dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL,
													 gtk.MESSAGE_WARNING,
													 gtk.BUTTONS_OK, err);
					error_dialog.run()
					error_dialog.destroy()
				else:
					self.filename = filename
					self.set_title()
					buffer.set_modified(False)
					break
			else:
				break
		dialog.destroy()
	""" The callback connected to the 'save' buttons
	
	If the file has not been saved at least once, it 
	call the save_as_dialog method. To check this, we check 
	if the filename is 'Untitled'
	"""
	def save_callback(self,widget):
		if self.filename == untitled:
			self.save_as_dialog(widget)
		else:
			#Get the current text buffer
			buffer = self.view.get_buffer()
			#Create a file with the chosen name
			f = open(self.filename,'w')
			#Get the beginning and the end of the buffer
			start,end = buffer.get_bounds()
			#Write the contents to the file
			f.write(buffer.get_slice(start,end,False))
			#Close the file
			f.close()
			buffer.set_modified(False)
			
	def show_score_window(self,widget):
		ScoreDialog(self.window,self.view2.get_buffer())
		pass
	"""Display the 'about' dialog of the program

	"""
	def about_dialog(self,widget):
		dialog = gtk.AboutDialog()
		dialog.set_name("LScore")
		dialog.set_version("0.1")
		dialog.set_authors(["Bruno Figueira 'Jedi' Lourenço"])
		dialog.set_comments(_("A program to create music and graphics from L-Systems."))
		dialog.set_copyright(_("Copyright © 2009 Bruno Figueira Lourenço"))
		dialog.show()
		#Close the dialog when we click on the close button
		dialog.connect("response",lambda dialog,id:dialog.hide())
	

if __name__ == "__main__":
	window = MainWindow()

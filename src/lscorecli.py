# -*- coding: utf-8 -*-
import sys
import os
import math
from optparse import OptionParser

#Check if we have lscore in sys.path
lscore_dir = os.getcwd
if lscore_dir not in sys.path:
	sys.path.append(lscore_dir)

from lscore.lsystem.parser import Parser
from lscore.interpretation.prunrendering import PrunRendering
from lscore.interpretation.schenkerianrendering import SchenkerianRendering
from lscore.interpretation.sequentialrendering import SequentialRendering
from lscore.interpretation import scales

def main():
	lscore_dir = os.getcwd
	if lscore_dir not in sys.path:
		sys.path.append(lscore_dir)
	
	parser = OptionParser(usage = "usage: %prog [options] input_file")
	parser.add_option("-l","--level",
					  default = 1, type = "int",
					  help = "recursion level")
	parser.add_option("-r","--rendering",
					 default = "spatial",
					 help = "musical rendering method: schenkerian, sequential or spatial")
	parser.add_option("-t","--tempo",
					 default = 120, type = "int",
					 help = "musical tempo for the midi output")
	parser.add_option("-s","--scale",
					 default = "major",
					 help = "musical scale: major, minor, pentatonic, "
					 "japanese or harmonic")
	parser.add_option("--octave_start",
					  default = 5, type = "int",
					  help = "octave of the first note")
	parser.add_option("--octave_upper",
					  default =  10, type = "int",
					  help = "octave upper bound")
	parser.add_option("--octave_lower",
					  default = 0, type = "int",
					  help = "octave lower bound")
	parser.add_option("--transpose",
					  default = 0, type = "int",
					  help = "transpose")
	parser.add_option("-m","--mode",
					  default = 0, type = "int",
					  help = "mode")
	parser.add_option("-d","--delta",
					  default = 90, type = "int",
					  help = "turtle's delta in degrees")
	parser.add_option("-i","--instrument_number",
					  default = 0, type = "int",metavar="NUMBER",
					  help = "midi instrument number")
	parser.add_option("-o","--output_file",
					  default = "out.mid",
					  help = "write midi output to FILE",metavar="FILE")
	parser.add_option("--tempo_multiplier",
					  default = 4, type = "int",
					  help = "tempo multiplier for the midi output")
	#Parse the arguments
	(options, args) = parser.parse_args()

	options.delta *= math.pi/180
	level = options.level
	
	#Try to open the input file
	f = None
	try:
		f = open(args[0],'r')
	except IOError as (errno, strerror):
		print "I/O error({0}): {1}".format(errno, strerror)
	except IndexError:
		print sys.argv[0] + ": No input file specified on command line"
		print "Try " + sys.argv[0] + " -h"
		sys.exit()
	input = f.read()
	
	level = options.level
	#Create the L-System
	lsystem = Parser().parse_string(input)
	if 'level' in lsystem.var_locals:
		level = lsystem.var_locals['level']
	result = lsystem.derive(level)
	
	scale = scales.Scale(scales.MAJOR,options.transpose,options.mode)
	if options.scale == "Minor":
		scale.set_steps(scales.MINOR)
	elif options.scale == "Penta Major":
		scale.set_steps(scales.PENTA_MAJOR)
	elif options.scale == "Penta Minor":
		scale.set_steps(scales.PENTA_MINOR)
	elif options.scale == "Harmonic":
		scale.set_steps(scales.HARMONIC_MINOR)
	elif options.scale == "Japanese":
		scale.set_steps(scales.JAPANESE)
		
	scale.set_octave(options.octave_start)
	scale.set_bounds((options.octave_lower,options.octave_upper))
	
	if options.rendering == "sequential":
		method = SequentialRendering(scale,options.tempo,
									options.instrument_number,
									options.tempo_multiplier)
	elif options.rendering == "schenkerian":
		method = SchenkerianRendering(scale,options.tempo,
									  options.instrument_number,
									  options.tempo_multiplier)
	else:
		method = PrunRendering(scale,options.tempo,
							   options.instrument_number,
							   options.tempo_multiplier,delta = options.delta)
	method.set_note_length_multiplier(options.tempo_multiplier)
	method.output_name = options.output_file
	method.create_score(result)
	
if __name__ == "__main__":
	main()

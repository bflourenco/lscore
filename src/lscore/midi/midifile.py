# -*- coding: utf-8 -*-
from midiconstants import *
from datatypeconverters import writeVar
from struct import pack
class MIDIFile:
	def __init__(self, outputName, 
					   format = 0, 
					   numberOfTracks = 1,
					   timeDivision = 480):
		self.outputName = outputName
		self.format = format
		self.numberOfTracks = numberOfTracks
		self.timeDivision = timeDivision
		self.tracks = []
		for i in range(0,numberOfTracks):
			self.tracks.append(MIDITrack())
	##
	##MIDI Channel Events
	##
	def noteOn(self, channel = 0,
					 note = 60,
					 velocity = 60, 
					 deltaTime = 0,
					 track = 0):
		event = MIDIEvent(deltaTime,NOTE_ON + channel,(note,velocity))
		self.tracks[track].addEvent(event)
	
	def noteOff(self,channel = 0,
					 note = 60,
					 velocity = 60, 
					 deltaTime = 0,
					 track = 0):
		event = MIDIEvent(deltaTime,NOTE_OFF + channel,(note,velocity))
		self.tracks[track].addEvent(event)
		
	def atertouch(self,
					 channel = 0,
					 note = 60,
					 amount = 60, 
					 deltaTime = 0,
					 track = 0):
		event = MIDIEvent(deltaTime,AFTERTOUCH + channel,(note,amount))
		self.tracks[track].addEvent(event)

	def controller(self, channel = 0,
						 type = 60,
						 value = 60, 
						 deltaTime = 0,
						 track = 0):
		event = MIDIEvent(deltaTime,CONTINUOUS_CONTROLLER + channel,(type,value))
		self.tracks[track].addEvent(event)
		
	def patchChange(self, channel = 0,
						  patch = 0,
						  deltaTime = 0,
						  track = 0):
		event = MIDIEvent(deltaTime,PATCH_CHANGE + channel,(patch))
		self.tracks[track].addEvent(event)
	
	def pitchBend(self, channel = 0,
						value = 8192,
						deltaTime = 0,
						track = 0):
		lsb = value & 0x7F
		msb = (value & 0x3F80) >> 7
		event = MIDIEvent(deltaTime, PITCH_BEND + channel,(lsb,msb))
		self.tracks[track].addEvent(event)				
	
	def pitchBendRange(self,channel = 0, 
							semitones = 2,
							deltaTime = 0,
							track = 0):
		rangeLSB= MIDIEvent(deltaTime,CONTINUOUS_CONTROLLER + channel,[REGISTERED_PARAMETER_NUMBER_LSB,0])
		rangeMSB = MIDIEvent(deltaTime,CONTINUOUS_CONTROLLER + channel,[REGISTERED_PARAMETER_NUMBER_MSB,0])
		rangeDataMSB = MIDIEvent(deltaTime,CONTINUOUS_CONTROLLER + channel,[DATA_ENTRY_MSB,semitones])
		rangeDataLSB = MIDIEvent(deltaTime,CONTINUOUS_CONTROLLER + channel,[DATA_ENTRY_LSB,0])
		rpnEndLSB = MIDIEvent(deltaTime,CONTINUOUS_CONTROLLER + channel,[REGISTERED_PARAMETER_NUMBER_LSB, 0x7F])
		rpnEndMSB = MIDIEvent(deltaTime,CONTINUOUS_CONTROLLER + channel,[REGISTERED_PARAMETER_NUMBER_MSB, 0x7F])
		
		self.tracks[track].addEvent(rangeLSB)
		self.tracks[track].addEvent(rangeMSB)
		self.tracks[track].addEvent(rangeDataMSB )
		self.tracks[track].addEvent(rangeDataLSB)
		self.tracks[track].addEvent(rpnEndLSB)
		self.tracks[track].addEvent(rpnEndMSB)
			
	##
	###Meta Events
	##
	##
	def sequenceNumber(self, number = 0,
							 deltaTime = 0,
							 track = 0):
		event = MIDIEvent(deltaTime,META_EVENT,(SEQUENCE_NUMBER,number))
		self.tracks[track].addEvent(event)
	
	def text(self, string,
				   deltaTime = 0,
				   track = 0):
		"""Write text to the track. 
		
		"""
		event = MIDIEvent(deltaTime,META_EVENT, (TEXT, string))
		self.tracks[track].addEvent(event)
	
	def copyright(self, string,
						deltaTime = 0,
						track = 0):
		event = MIDIEvent(deltaTime,META_EVENT, (COPYRIGHT, string))
		self.tracks[track].addEvent(event)
	
	def trackName(self,	string,
	 					deltaTime = 0,
						track = 0):
		event = MIDIEvent(deltaTime,META_EVENT, (TRACK_NAME, string))
		self.tracks[track].addEvent(event)

	def instrumentName(self, string,
							 deltaTime = 0,
							 track = 0):
		event = MIDIEvent(deltaTime,META_EVENT, (INSTRUMENT_NAME, string))
		self.tracks[track].addEvent(event)
	
	def lyric (self, string,
					 deltaTime = 0, 
					 track = 0):
		event = MIDIEvent(deltaTime,META_EVENT, (LYRIC, string))
		self.tracks[track].addEvent(event)

	def marker (self, string,
					  deltaTime = 0,
					  track = 0):
		event = MIDIEvent(deltaTime,META_EVENT, (MARKER, string))
		self.tracks[track].addEvent(event)
		
	def cuepoint (self, deltaTime = 0,
						string = "",
					    track = 0):
		event = MIDIEvent(deltaTime,META_EVENT, (CUEPOINT, string))
		self.tracks[track].addEvent(event)

	def channelPrefix (self, string,
							 deltaTime = 0,
					         track = 0):
		event = MIDIEvent(deltaTime,META_EVENT, (MIDI_CH_PREFIX, string))
		self.tracks[track].addEvent(event)

	def eof(self, track = 0):
		"""Signal the end of a track. All tracks must have this event 
		as the last event
		
		"""
		event = MIDIEvent(0,META_EVENT, (END_OF_TRACK))
		self.tracks[track].addEvent(event)

	def setTempo(self, mpqn = 750000,
					   deltaTime = 0,
					   track = 0):
		"""Change the tempo of the track. 
		
		mpqn: Microseconds per quarter note. 
		To translate from bpm to mpqn:
		bpm = 60000000/mpqn
		"""
		event = MIDIEvent(deltaTime,META_EVENT, (TEMPO,mpqn))
		self.tracks[track].addEvent(event)	
	
	def smpteOffset(self, hour, min, sec, fr, subfr,
						  deltaTime = 0,
						  track = 0):
		event = MIDIEvent(deltaTime,META_EVENT, (SMPTE_OFFSET,hour,min,sec,fr,subfr))
		self.tracks[track].addEvent(event)

	def timeSignature(self, nn, dd, cc, bb, deltaTime = 0,
											track = 0):
		"""Change the time signature of the track. 
			
		nn: The numerator of the signature
		dd: The denominator of the signature. It must be specified as 
		the number that a power of 2 must be raised. Example: 0 is a 
		whole note, 1 is a half note, 2 is a quarter note 
		cc: Number of clocks in a metronome click
		bb: The number of 32nd notes to the quarter note
		"""
		event = MIDIEvent(deltaTime,META_EVENT,(TIME_SIGNATURE,nn,dd,cc,bb))
		self.tracks[track].addEvent(event)
	
	def keySignature(self, key, isMajor = True, deltaTime = 0,
												track = 0):
		"""Change the key signature of the track. 
			
		A positive value for the key indicates the number of sharps and a
		negative value the number of flats
		"""
		event = MIDIEvent(deltaTime,META_EVENT, (KEY_SIGNATURE,(key,isMajor)))
		self.tracks[track].addEvent(event)
	
	def write(self):
		"""Write a MIDI file to the hard disk.
		
		It's a nice idea to call eof() for all tracks before calling 
		this method. 
		
		"""
		file = open(self.outputName,'w')
		#Build the file header
		header = pack('>4sihhh',FILE_HEADER,6,
								self.format,
								self.numberOfTracks,
								self.timeDivision)
		file.write(header)
		for track in self.tracks:
			trackSize = 0
			trackData = ""
			for event in track.events:
				eventBytes = event.toBytes()
				trackSize += len(eventBytes)
				trackData += eventBytes
			trackBytes = pack('>4si',TRACK_HEADER, trackSize) + trackData
			file.write(trackBytes)
		file.close()
	""" Insert a MIDI Event at 'ticks' from the beginning of the track.
	
	"""
	def insertEvent(self,ticks,event,track = 0):
		totalTicks = 0
		insertionPoint = len(self.tracks[track].events)
		entered = False
		#If ticks = 0 we probably want to play the event
		#after all meta-events with delta time equal to 0 have been read
		if ticks != 0:
			for i in range(0,len(self.tracks[track].events)):
				totalTicks += self.tracks[track].events[i].deltaTime
				#If ticks = 0 we probably want to play the event
				#after all meta-events have been read
				if totalTicks == ticks:
					entered = True
					insertionPoint = i+1
					event.deltaTime = 0
					break
				elif totalTicks > ticks:
					entered = True
					insertionPoint = i			
					event.deltaTime = ticks - tracks[track].events[i-1].deltaTime
					tracks[tracks].events[i].deltaTime -= event.deltaTime
					break
		if not entered:
			event.deltaTime = ticks - totalTicks
		self.tracks[track].events.insert(insertionPoint,event)
	
	def insertNoteOn(self,channel = 0,
					 	  note = 60,
					      velocity = 60,
					      ticks = 0,
					      track = 0):
		event = MIDIEvent(0,NOTE_ON + channel,(note,velocity))
		self.insertEvent(ticks,event,track)

	def insertNoteOff(self,channel = 0,
						   note = 60,
						   velocity = 60,
						   ticks = 0,
						   track = 0):
		event = MIDIEvent(0,NOTE_OFF + channel,(note,velocity))
		self.insertEvent(ticks,event,track)
		
class MIDITrack:
	def __init__(self,size = 0):
		self.events = []
	def addEvent(self,event):
		self.events.append(event)
		

class MIDIEvent:
	def __init__(self, deltaTime,type, eventData):
		self.deltaTime = deltaTime
		self.type = type
		self.eventData = eventData
	def toBytes(self):
		deltaTime = writeVar(self.deltaTime)
		if self.type == META_EVENT:
			#We handle here the end of track  because there are no 
			#parameters in this case and we can't obtain the type of 
			#this event with self.eventData[0], because a tuple with 
			#only one object is unsubscriptable and we are passing the 
			#parameters of the events with a tuple
			#
			#TODO: I'm so stupid. I can use a list instead of using 
			#a tuple
			if self.eventData is END_OF_TRACK:
				return pack('>BBBB',0,META_EVENT, END_OF_TRACK,0)
			else:
				metaType = self.eventData[0]
			
			bytes = deltaTime + pack('>BB',META_EVENT, metaType)
			if metaType > 0 and metaType < 8:
				metaLength = writeVar(len(self.eventData[1]))
				bytes += metaLength + self.eventData[1]
			
			elif metaType == SEQUENCE_NUMBER:
				metaLength = writeVar(2)
				bytes += metaLength + pack(">H",self.eventData[1])
	
			elif metaType == MIDI_CH_PREFIX:
				metaLength = writeVar(1)
				bytes += metaLength + pack(">B",self.eventData[1])
					
			elif metaType == TEMPO:
				metaLength = writeVar(3)
				mpqn = self.eventData[1]
				#Since we need to write 3 bytes, we break the number 
				#in 2 parts: higher byte and lower bytes.
				hb,lb = (mpqn >> 16) & 0xFF, mpqn & 0xFFFF
				bytes += metaLength + pack(">BH",hb,lb)
		
			elif metaType == SMPTE_OFFSET:
				metaLength = writeVar(5)
				h,m = self.eventData[1],self.eventData[2]
				s,fr = self.eventData[3],self.eventData[4]
				subfr = self.eventData[5]
				bytes += metaLength + pack(">BBBBB",h,m,s,fr,subfr)
			elif metaType == TIME_SIGNATURE:
				metaLength = writeVar(4)
				nn,dd = self.eventData[1],self.eventData[2]
				cc,bb = self.eventData[3],self.eventData[4]
				bytes += metaLength + pack(">BBBB",nn,dd,cc,bb)
			elif metaType == KEY_SIGNATURE:
				metaLength = writeVar(2)
				key,scale = self.eventData[1],int(self.eventData[2])
				bytes += metaLength + pack(">BB",key,scale)
			elif metaType == SPECIFIC:
				#TODO: Handle this
				pass
			return bytes
		elif self.type == SYSTEM_EXCLUSIVE:
			#TODO: Handle this
			pass
		else:
			eventType = self.type & 0xF0
			#These two events take only 1 parameter
			if eventType is PATCH_CHANGE or eventType is AFTERTOUCH:
				par1 = self.eventData
				bytes = deltaTime + pack('>BB',self.type,par1)
			else:
				par1 = self.eventData[0]
				par2 = self.eventData[1]
				bytes = deltaTime + pack('>BBB',self.type,par1,par2)
			return bytes


def pitch_bend_test(midi_file):
	#midi.pitchBendRange(0,4,0,0)
	midi_file.noteOn(0,60,100)
	for i in range(0,100):
		midi_file.pitchBend(0,8192 + i*81,2)
	midi_file.noteOff(0,60,100,480)
	#pitch bend reset
	midi_file.pitchBend(0,8192)

def note_on_test(midi_file):
	midi_file.noteOn(0,60,100)
	midi_file.noteOff(0,60,100,480)
	midi_file.noteOn(0,62,100,0)
	midi_file.noteOff(0,62,100,960)
	
def vibrato_test(midi_file):
	midi_file.controller(0,1,127)
	midi_file.noteOn(0,72,100)
	midi_file.noteOff(0,72,100,480)
	#vibrato reset
	midi_file.controller(0,1,0)
def main():
	midi = MIDIFile("teste.mid",0,1,480)
	midi.setTempo(750000)
	midi.timeSignature(4,2,24,8)
	midi.patchChange(0,29,0)
	#midi.controller(0,65,65) #slide
	#midi.controller(0,5,80) #portamento control
	
	pitch_bend_test(midi)
	#note_on_test(midi)
	#vibrato_test(midi)
	

	#midi.insertNoteOn(0,60,127)
	#midi.insertNoteOn(0,67,127)
	#midi.insertNoteOff(0,60,127,480)
	#midi.insertNoteOff(0,67,127,480)
	midi.text("Isto é um teste!")
	midi.eof()
	midi.write()
if __name__ == "__main__":
	main()

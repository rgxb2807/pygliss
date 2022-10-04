import numpy as np

class NoteSequence:
	"""
	A class to represent a sequence of single notes

	...

	Attributes
	----------
	notes : numpy.ndarray[numpy.float64]
		the notes in the sequences represented as frequency values
	time_val : numpy.ndarray[numpy.float64]
		the time value of the sequence starting at 0
	durations : numpy.ndarray[numpy.float64]
		durations of each note

	Methods
	-------

	"""

	def __init__(self, notes, time_val, durations):
		self.notes = notes
		self.time_val = time_val
		self.durations  = durations



class ChordSequence:
	"""
	A class to represent a sequence of chords
	A chord is an array of note frequencies with a duration - Not the Chord Class

	...

	Attributes
	----------
	chords : numpy.ndarray[numpy.float64]
		the notes in the sequences represented as frequency values
	time_val : numpy.ndarray[numpy.float64]
		the time value of the sequence starting at 0
	durations : numpy.ndarray[numpy.float64]
		durations of each note

	Methods
	-------

	"""
	def __init__(self, chords, time_val, durations):
		self.chords = chords
		self.time_val = time_val
		self.durations  = durations


from pygliss.sequence import NoteSequence
from pygliss.utils import NOTE_VECTOR, NOTE_VECTOR_12

import numpy as np


class Gliss(NoteSequence):
	"""
	A class to represent a glissando

	...

	Attributes
	----------
	start : numpy.float64
		the starting note of the gliss
	end : numpy.float64
		the end note of the gliss
	ascend : bool
		True if the glissando is ascending
	length:
		the number of notes in the glissando
	resolution : numpy.int
		how wide the intervals are - 1 represents 1/4 tone


	Methods
	-------

	calc_gliss(start, end):
		calculates the glissando

	"""

	def __init__(self, start, end, resolution=1):

		"""
		Contructs Glissando

		Parameters
		----------
			start : numpy.float64
				the starting note of the gliss
			end : numpy.float64
				the end note of the gliss
			resolution : numpy.int
				how wide the intervals are - 1 represents 1/4 tone
		"""

		self.start = start
		self.end = end
		self.ascend = None
		self.length = None
		self.resolution = resolution


		def calc_gliss(self):
		    """
		    Calculate glissando frequencies, time values and note durations
		    Uses attributes `start` and `end` as the starting and ending note
		    frequencies

		    time_vals are calculated with a total gliss duration of 1, each note
		    duration is equal

		    A glissando is an exponential pitch function of equal tempered notes in 
		    time. Each step increaeses NOTE * 2 **1/DIVISIONS


		    Parameters
		    ----------
		    self, uses `start` and `end`
		    
		    Returns
		    -------
		    None, Instantiates the super class NoteSequence

		    """
		    note_vector = NOTE_VECTOR
		    if self.resolution == 2:
		    	note_vector = NOTE_VECTOR_12

		    # Find high and low notes of gliss
		    high = self.end if self.end >= self.start else self.start
		    low = self.start if self.start <= self.end else self.end
		    
		    # Filter note vector by High And low 
		    low_idx = (np.abs(note_vector - low)).argmin()
		    high_idx = (np.abs(note_vector - high)).argmin()
		    notes = note_vector[low_idx:high_idx]
		    self.length = len(notes)
		    
		    # Reverse order of list if gliss descends
		    if start > end:
		        notes = note_vector[low_idx+1:high_idx+1]
		        notes = notes[::-1]
		        self.ascend = False
		    else:
		    	self.ascend = True
		        
		    time_val = (1 /  len(notes)) * np.arange(0, len(notes))
		    durations = (1 /  len(notes)) * np.ones(len(notes))
		    super().__init__(notes, time_val, durations)


		# initialize parent class
		calc_gliss(self)













## DELETE After Refactor

# from pygliss.note import Note, asc_notes_list, desc_notes_list

# # add error handling for when resolution doesn't divide evenly
# # add option  - favor end note or start note

# class Gliss:
# 	def __init__(self, start, end, resolution=1):

# 		self.start = start
# 		self.end = end
# 		self.ascend = None
# 		self.length = None
# 		self.resolution = resolution
# 		self.notes = list()

# 		def is_asc (self):
# 			if self.start.steps < self.end.steps:
# 				self.ascend = True
# 			else:
# 				self.ascend = False

# 		def set_length(self):
# 			if self.ascend:
# 				self.length = (self.end.steps - self.start.steps) / self.resolution
# 			elif (self.end.steps - self.start.steps) == 0:
# 				self.length = 1
# 			else:
# 				self.length = (self.start.steps - self.end.steps) / self.resolution

# 		def set_notes(self):
# 			idx = 0
# 			asc_list = asc_notes_list(resolution=self.resolution)
# 			desc_list = desc_notes_list(resolution=self.resolution)
# 			if self.ascend:
# 			    idx = asc_list.index(self.start)
# 			else:
# 				idx = desc_list.index(self.start)

# 			if self.length == 1:
# 				self.notes.append(self.start)
# 			else:
# 				for idx in range(idx, int(self.length) + idx):
# 					if self.ascend:
# 					    self.notes.append(asc_list[idx])
# 					else:
# 						self.notes.append(desc_list[idx])

# 		is_asc(self)
# 		set_length(self)
# 		set_notes(self)

# 	def __str__(self):
# 		s = ''
# 		for note in self.notes:
# 			s += str(note) + ", "
# 		return s

import numpy as np
from pygliss.note import freq_to_note
from pygliss.chord import Chord

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
	to_note:
		returns a list of Note objects from the note sequence
	"""

	def __init__(self, notes, time_val, durations):
		self.notes = notes
		self.time_val = time_val
		self.durations = durations
		self.length = len(notes)
		assert len(notes) == len(durations)

	def to_note(self):
		"""Returns list of Note objects from note sequence"""
		return [freq_to_note(self.notes[i]) for i in range(self.length)]

	def add_offset_at_position(self, silence_duration, durations_idx):
		"""Adds silence in seconds at specified `durations` idx """
		self.durations = np.insert(self.durations, durations_idx, silence_duration)
		self.notes = np.insert(self.notes, durations_idx, 0.0)
		self.length = len(self.notes)
		new_time_val = np.zeros(self.length)
		for i in range(len(new_time_val)):
			if i > durations_idx:
				new_time_val[i] = silence_duration + self.time_val[i-1]
			elif i <= durations_idx:
				new_time_val[i] = self.time_val[i]
		self.time_val = new_time_val


	def remove_offset_at_position(self, durations_idx):
		"""removes silence in seconds at specified `durations` idx """
		if self.notes[durations_idx] == 0.0:
			silence_duration = self.durations[durations_idx]
			self.durations = np.delete(self.durations, durations_idx)
			self.notes = np.delete(self.notes, durations_idx)
			self.length = len(self.notes)
			new_time_val = np.zeros(self.length)
			for i in range(len(new_time_val)):
				if i > durations_idx:
					new_time_val[i] = self.time_val[i+1] - silence_duration
				elif i <= durations_idx:
					new_time_val[i] = self.time_val[i]
			self.time_val = new_time_val

	def add_offset(self, offset_dur):
		"""Adds silence at the beginning of the sequence"""
		self.add_offset_at_position(offset_dur, 0)

	def add_silence(self, offset_dur):
		"""Adds silence at the end of the sequence"""
		self.durations = np.append(self.durations, offset_dur)
		self.notes = np.append(self.notes, 0.0)
		self.length = len(self.notes)
		self.time_val = np.append(self.time_val, np.sum(self.durations[:-1]))




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
	to_chord:
		returns a list of Chord objects from the Chord sequence
	"""
	def __init__(self, chords, time_val, durations):
		self.chords = chords
		self.time_val = time_val
		self.durations  = durations
		self.length = len(chords)
		assert len(chords) == len(durations)

	def __str__(self):
		s = ''
		for i in range(self.length):
			s += str(self.chords[i]) + " " + str(self.durations[i]) +"\n"
		return s

	def to_chord(self):
		"""Returns list of Chord objects from Chord sequence"""
		return [Chord(self.chords[i], self.durations[i]) for i in range(self.length)]



def make_chord_seq_from_note_seq(note_sequences):
    """
    Returns a ChordSequence all chords from overlapping note sequences

    
    Parameters
	----------
		note_sequences : list of pygliss.NoteSequence
			the starting note of the gliss

	Returns
	-------
		chord_seq : pygliss.ChordSequence
			ChordSequence generated from note_sequences

    """
    # Get time values
    time_tuple = ([seq.time_val for seq in note_sequences])
    time_vals = np.sort(np.unique(np.concatenate((time_tuple))))
    
    # create array for time, glissandi and note durations
    chords = np.zeros((time_vals.shape[0], len(note_sequences)))
    
    # calculate durations
    diff = np.diff(time_vals)
    durations = np.append(diff, [1 - np.sum(diff)])
    
    # for every timestep in a gliss, set the note value in chords
    for seq_idx, seq in enumerate(note_sequences):
        seq_time_idx = 1
        for idx, time_val in enumerate(time_vals):
        	# gliss is 1 note
            if len(seq.time_val) == 1:
                chords[idx, seq_idx] = seq.notes[0]
            # last note in sequence
            elif seq_time_idx == seq.length:
                chords[idx, seq_idx] = seq.notes[seq_time_idx - 1]
            elif seq.time_val[seq_time_idx] > time_val:
                chords[idx, seq_idx] = seq.notes[seq_time_idx - 1]
            else:
                if seq_time_idx < seq.length:
                    seq_time_idx += 1
                chords[idx, seq_idx] = seq.notes[seq_time_idx - 1]
    
    chord_seq = ChordSequence(chords, time_vals, durations)
    return chord_seq

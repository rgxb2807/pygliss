import numpy as np
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

	"""

	def __init__(self, notes, time_val, durations):
		self.notes = notes
		self.time_val = time_val
		self.durations  = durations
		self.length = len(notes)



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
		self.length = len(chords)

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
            if seq.time_val[seq_time_idx] > time_val:
                chords[idx, seq_idx] = seq.notes[seq_time_idx - 1]
            else:
                if (seq_time_idx + 1) < seq.length:
                    seq_time_idx += 1
                chords[idx, seq_idx] = seq.notes[seq_time_idx - 1]
    
    chord_seq = ChordSequence(chords, time_vals, durations)
    return chord_seq

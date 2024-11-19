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
	beats (optional) : numpy.ndarray[numpy.float64]
		the duration of each beat if a time signature/beat value is applicable


	Methods
	-------
	to_note:
		returns a list of Note objects from the note sequence
	"""

	def __init__(self, notes, time_val, durations, beats=None):
		self.notes = notes
		self.time_val = time_val
		self.durations = durations
		self.length = len(notes)
		assert len(notes) == len(durations)
		self.beats = beats

	def __iadd__(self, other):
		"""TODO"""
		pass

	def to_note(self):
		"""Returns list of Note objects from note sequence"""
		return [freq_to_note(self.notes[i]) for i in range(self.length)]

	def concat(self, other):
		"""TODO"""
		pass

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
	beats (optional) : numpy.ndarray[numpy.float64]
		the duration of each beat if a time signature/beat value is applicable

	Methods
	-------
	to_chord:
		returns a list of Chord objects from the Chord sequence
	"""
	def __init__(self, chords, time_val, durations, beats=None):
		self.chords = chords
		self.time_val = time_val
		self.durations  = durations
		self.length = len(chords)
		assert len(chords) == len(durations)
		self.beats = beats

	def __str__(self):
		s = ''
		for i in range(self.length):
			s += str(self.chords[i]) + " " + str(self.durations[i]) +"\n"
		return s

	def __iadd__(self, other):
		pass

	def to_chord(self):
		"""Returns list of Chord objects from Chord sequence"""
		return [Chord(self.chords[i], self.durations[i]) for i in range(self.length)]

	def concat(self, other):
		"""TODO"""
		pass

	def add_offset_at_position(self, silence_duration, durations_idx):
		"""Adds silence in seconds at specified `durations` idx """
		self.durations = np.insert(self.durations, durations_idx, silence_duration)
		self.chords = np.insert(self.chords, durations_idx, np.zeros(len(self.chords[0])), axis=0)
		self.length = len(self.chords)
		new_time_val = np.zeros(self.length)
		for i in range(len(new_time_val)):
			if i > durations_idx:
				new_time_val[i] = silence_duration + self.time_val[i-1]
			elif i <= durations_idx:
				new_time_val[i] = self.time_val[i]
		self.time_val = new_time_val


	def remove_offset_at_position(self, durations_idx):
		"""removes silence in seconds at specified `durations` idx """
		if np.all(self.chords[durations_idx]) == 0.0:
			silence_duration = self.durations[durations_idx]
			self.durations = np.delete(self.durations, durations_idx)
			self.chords = np.delete(self.chords, durations_idx, axis=0)
			self.length = len(self.chords)
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
		self.chords = np.append(self.chords, 0.0)
		self.length = len(self.chords)
		self.time_val = np.append(self.time_val, np.sum(self.durations[:-1]))



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


# def get_tempo_vals(start_bpm, beats, end_bpm=None):
    
#     """
#     Returns a the duration of each beat and when they occur as time values

    
#     Parameters
# 	----------
# 	start_bpm : int
# 		the starting tempo
# 	beats : int
# 		the number beat @ start_bpm
# 	end_bpm (optional): int
# 		the end bpm indicating a tempo change

# 	Returns
# 	-------
# 	time_val : numpy.ndarray[numpy.float64]
# 		the time value of the sequence starting at 0
# 	durations : numpy.ndarray[numpy.float64]
# 		durations of each beat

#     """	

#     if not end_bpm:
#         time_val = (1 /  beats) * np.arange(0, beats)
#         durations = (1 /  beats) * np.ones(beats)
#         return time_val, durations

#     tempo_diff = end_bpm - start_bpm
#     bpm_increase = tempo_diff / beats # first beat should be at start_bpm
#     time_val, durations = np.zeros(beats), np.zeros(beats) 
#     for i in range(beats):
#         durations[i] = 60 / (start_bpm + bpm_increase * i)
#         if i > 0:
#             time_val[i] = durations[i-1] + time_val[i-1]
#     return time_val, durations


def get_tempo_vals(start_bpm, beats, end_bpm=None):
    """
    Returns the duration of each beat and their corresponding time values.

    Parameters
    ----------
    start_bpm : int
        The starting tempo in beats per minute.
    beats : int
        The number of beats in the sequence.
    end_bpm : int, optional
        The ending tempo in beats per minute for a linear tempo change. 
        If not provided, the tempo remains constant.

    Returns
    -------
    time_val : numpy.ndarray
        The time values of each beat, starting at 0.
    durations : numpy.ndarray
        The durations of each beat in seconds.
    """
    if beats <= 0:
        raise ValueError("Number of beats must be greater than zero.")

    if not end_bpm:  # Constant tempo
        durations = np.full(beats, 60 / start_bpm)
        time_val = np.cumsum(np.append([0], durations[:-1]))  # Time at start of each beat
        return time_val, durations

    # Linear tempo change (accelerando or ritardando)
    tempo = np.linspace(start_bpm, end_bpm, beats, endpoint=False)  # Exclude end_bpm
    durations = 60 / tempo  # Convert tempo to beat durations
    time_val = np.cumsum(np.append([0], durations[:-1]))  # Time at start of each beat

    return time_val, durations






def transform_tempo(source_durations, source_time_val, target_beat_durations, \
	target_beat_time_val, source_beats=None):
    
    """
    Transforms the source durrations to the beat values specified in the target

    
    Parameters
	----------
	source_durations : numpy.ndarray[numpy.float64]
		durations of note/chord of the source material
	source_time_val : numpy.ndarray[numpy.float64]
		time values of the note/chord of the source material
	target_beat_durations : numpy.ndarray[numpy.float64]
		durations of the beat values of the target
	target_beat_time_val : numpy.ndarray[numpy.float64]
		time values of the beat values of the target


	Returns
	-------
	time_val : numpy.ndarray[numpy.float64]
		the time value of the sequence starting at 0
	durations : numpy.ndarray[numpy.float64]
		durations of each note/chord
    """
    source_seq_duration = np.sum(source_durations)
    target_seq_duration = np.sum(target_beat_durations)
    target_num_beats = len(target_beat_durations)

    time_val, durations = np.zeros(1), np.zeros(1)
    if source_beats is None:
    	pass
    else:
    	# divide source int chunks by target_num_beats
    	# indicate if values should be tied over
    	# multiply each chunk by time value
    	# combine chunks with ties
    	# target_beat_idx = 0

    	# multiply each chunk by factor of its corresponding beat time value
    	# if a note goes over, then you have to proportioanlly divide
    	# meaning you'll need the LCM between the source and target if beats 
    	# are present, if they're note you just have to figure out how much 
    	# they go over
    	pass








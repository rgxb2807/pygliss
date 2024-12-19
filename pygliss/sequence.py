import copy
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
	    """
	    Concat two ChordSequence sequences and returns a new instance  of 
	    ChordSequence
	    """
	    current_seq = copy.deepcopy(self)
	    other_seq = copy.deepcopy(other)

	    self_total_dur = np.sum(current_seq.durations)
	    other_total_dur = np.sum(other_seq.durations)
	    dur_diff = np.abs(self_total_dur - other_total_dur)
	    
	    # Make equation duration - add trailing silence
	    if self_total_dur > other_total_dur:
	    	other_seq.add_silence(dur_diff)
	    elif self_total_dur < other_total_dur:
	    	current_seq.add_silence(dur_diff)

	    # Get time values
	    time_tuple = ([current_seq.time_val, other_seq.time_val])
	    time_vals = np.sort(np.unique(np.concatenate((time_tuple))))
	    
	    # Create array for time, glissandi and note durations
	    self_dim, other_dim = current_seq.chords.shape[1], other_seq.chords.shape[1]
	    chords = np.zeros((time_vals.shape[0] , self_dim + other_dim))
	    
	    # Calculate durations
	    diff = np.diff(time_vals)
	    total_duration = np.maximum(np.sum(current_seq.durations), np.sum(other_seq.durations))
	    durations = np.append(diff, [total_duration - np.sum(diff)])
	    
	    chord_idx, other_idx = 0,0
	    chord_dur_time_val_start = current_seq.durations[0]
	    other_dur_time_val_start = other_seq.durations[0]

	    for idx, time_val in enumerate(time_vals):
	    	if time_val == (chord_dur_time_val_start + current_seq.time_val[chord_idx]) and chord_idx + 1 < len(current_seq.chords):
	    		chord_idx += 1
	    		chord_dur_time_val_start = current_seq.durations[chord_idx]

	    	if time_val == (other_dur_time_val_start + other_seq.time_val[other_idx]) and other_idx + 1 < len(other_seq.chords):
	    		other_idx += 1
	    		other_dur_time_val_start = other_seq.durations[other_idx]

	    	chords[idx, :self_dim] = current_seq.chords[chord_idx, :]
	    	chords[idx, self_dim:] = other_seq.chords[other_idx, :]
	    
	    chord_seq = ChordSequence(chords, time_vals, durations)

	    return chord_seq

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
				if i == durations_idx and durations_idx == len(self.time_val):
					new_time_val[i] = self.durations[i-1] + self.time_val[i-1]
				else:
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

	def add_silence(self, silence_duration):
		"""Adds silence at the end of the sequence"""
		self.add_offset_at_position(silence_duration, self.length)



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


def transform_tempo(source_durations, target_beat_durations):
    """
    Transforms the source durrations to the beat values specified in the target

    
    Parameters
    ----------
    source_durations : numpy.ndarray[numpy.float64]
        durations of note/chord of the source material
    target_beat_durations : numpy.ndarray[numpy.float64]
        durations of the beat values of the target


    Returns
    -------
    time_val : numpy.ndarray[numpy.float64]
        the time value of the sequence starting at 0
    durations : numpy.ndarray[numpy.float64]
        durations of each note/chord
    """
    len_source = len(source_durations)
    len_target = len(target_beat_durations)
    target_lcm = np.lcm(len_target, len_source)
    scaled_source_durations = np.zeros(len_source * target_lcm)
   
    for i in range(len(scaled_source_durations)):
    	target_beat_idx = int(np.floor((i * len_target) / (len_source * target_lcm)))
    	num_parts = int(len_source * target_lcm // len_target)
    	scaled_source_durations[i] = target_beat_durations[target_beat_idx] / num_parts

    transformed_durations = np.zeros(len_source)
    step_size = len_source * target_lcm // len_source 
    for j in range(len_source):
    	start_idx = j * step_size
    	end_idx = (j + 1) * step_size 
    	transformed_durations[j] = np.sum(scaled_source_durations[start_idx:end_idx])


    transformed_time_val = np.zeros(len_source)
    for i in range(len(transformed_durations)):
    	if i > 0:
    		transformed_time_val[i] = transformed_time_val[i-1] + transformed_durations[i-1]

    return transformed_time_val, transformed_durations



def calculate_beats(start_bpm, end_bpm, total_duration, bpm_step=None):
    """
    Calculate the total number of beats needed to stay under the total duration 
    while gradually increasing BPM. Optionally returns the beats where the BPM 
    changes by evenly spaced intervals.

    Args:
        start_bpm (float): The starting BPM.
        end_bpm (float): The ending BPM.
        total_duration (float): The total duration in seconds.
        bpm_step (float, optional): The step size for increasing BPM (e.g., +4 BPM).
                                    If None, no BPM changes are calculated.

    Returns:
        tuple: Total number of beats, and (if bpm_step is provided) a dictionary of
               beat numbers and their corresponding BPM.
    """
    # Initialize variables
    current_bpm = start_bpm
    beats = 0
    elapsed_time = 0
    beat_times = {}

    # Calculate total number of BPM steps
    if bpm_step:
        total_steps = int((end_bpm - start_bpm) / bpm_step)
        step_durations = [
            total_duration / (total_steps + 1) for _ in range(total_steps + 1)
        ]
    else:
        step_durations = [total_duration]

    for step_duration in step_durations:
        while elapsed_time < sum(step_durations[:step_durations.index(step_duration) + 1]):
            beat_duration = 60 / current_bpm  # Duration of a single beat in seconds

            if elapsed_time + beat_duration > total_duration:
                break  # Don't add beats that exceed the total duration

            beats += 1
            elapsed_time += beat_duration

        if bpm_step and current_bpm + bpm_step <= end_bpm:
            current_bpm += bpm_step
            beat_times[beats] = current_bpm

    return (beats, beat_times) if bpm_step else beats

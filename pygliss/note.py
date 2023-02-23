from pygliss.constants import DIVISIONS, BASE, A440, HIGH, LOW
from pygliss.utils import make_freq_vector
import numpy as np


DIV = (DIVISIONS / 12)
NOTE_NAMES = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
HIGH_OCTAVE = 10
LOW_OCTAVE = -3

NOTE_VECTOR = make_freq_vector(DIVISIONS)
NOTE_VECTOR_12 = make_freq_vector(12)


class Note:
	"""Note object represents a note with up to quarter tone divisons supported."""

	def __init__(self, note, octave, accidental=None):
		self.note = note
		self.octave = octave
		self.accidental = accidental
		self.steps = None
		self.Next = None
		self.Prev = None
		self.Midi = None
		self.Lily = None
		self.clef = None
		self.freq = None
		self.set_steps()

	def __str__(self):
		if self.accidental is not None:
		    return str(self.note) + str(self.octave) + str(self.accidental)
		else:
			return str(self.note) + str(self.octave)

	def __lt__(self, other):
		return self.frequency() < other.frequency()

	def __le__(self, other):
		return self.frequency() <= other.frequency()

	def __eq__(self,other):
		return self.frequency() == other.frequency()

	def __ne__(self, other):
		return self.frequency() != other.frequency()

	def __gt__(self, other):
		return self.frequency() > other.frequency()

	def __ge__(self, other):
		return self.frequency() >= other.frequency()

	def set_steps(self):
		"""
		Sets the number of steps for a given note based on its position in the 
		range of allowed notes.
		"""
		if self.steps is None:
			self.steps = (self.octave - 4) * DIVISIONS
			self.steps += get_note_steps(self.note)
			self.steps += get_accidental_steps(self.accidental)

	def distance(self, other_note):
		"""Returns the number of quarter tone steps between the given note."""
		return abs(self.steps - other_note.steps)

    # http://pages.mtu.edu/~suits/NoteFreqCalcs.html
	def frequency(self):
		"""Returns the frequency of a Note."""
		if self.freq is None:
			self.freq = A440 * BASE ** self.steps
		return self.freq


def get_note(note_str):
	"""format "Note Name" + "Accidental"  + "Octave"  """
	note_name = note_str[:1]
	if len (note_str) == 2:
		return Note(note_name, int(note_str[1:2]))

	if len(note_str) == 3:
		return Note(note_name, int(note_str[2:3]), note_str[1:2])

	if len(note_str) == 4:
		return Note(note_name, int(note_str[3:4]), note_str[1:3])



def get_note_steps(note):
	"""Gets associated steps for a given note."""
	steps = 0.0
	if note == 'A':
		steps += 0

	elif note == 'B':
		steps += 2 * DIV

	elif note == 'C':
		steps += -9 * DIV

	elif note == 'D':
		steps += -7 * DIV

	elif note == 'E':
		steps += -5 * DIV

	elif note == 'F':
	    steps += -4 * DIV

	elif note == 'G':
		steps += -2 * DIV

	else:
		steps += 0.0

	return steps


def get_accidental_steps(accidental):
	"""Gets associated steps for a given accidental."""
	steps = 0.0
	if accidental == '+':
		steps += 0.5 * DIV

	elif accidental == '#':
		steps += 1.0 * DIV

	elif accidental == '++':
		steps += 1.5 * DIV

	elif accidental == '-':
		steps += -0.5 * DIV

	elif accidental == 'b':
		steps += -1.0 * DIV

	elif accidental == '--':
		steps += -1.5 * DIV

	else:
		steps += 0.0

	return steps


 
def get_steps(note, octave, accidental):
	"""returns number of steps based on the number of divisions."""
	steps = (octave - 4) * DIVISIONS
	steps += get_note_steps(note)
	steps += get_accidental_steps(accidental)


def freq_to_note(freq):
	"""
	Returns a note object based on a given frequency with quartertone 
	precision.
	"""
	if freq < LOW or freq > HIGH:
		return None

	note_position = find_note_vector_position_vectorized(freq)
	octave = int(np.floor(note_position / DIVISIONS))
	note_idx = int(note_position - octave * DIVISIONS)
	
	note_names = ["C", "C", "C", "C", "D", "D", "D", "D", "E", "E", "F", "F",
	"F", "F", "G", "G", "G", "G", "A", "A", "A", "A", "B", "B"]
	accidentals = [None, "+", "#", "++", None, "+", "#", "++", None, "+", None, "+",
	"#", "++", None, "+", "#", "++", None, "+", "#", "++", None, "+"]
	
	if DIVISIONS == 12:
		note_idx = note_idx * 2

	return Note(note_names[note_idx], octave, accidentals[note_idx])

def get_partial(note, fundamental):
	return note.frequency() / fundamental.frequency()


def find_note_vector_position(note_frequency, trunc_beg=None, trunc_end=None):
    """
    Finds note position of a given frequency or array of frequencies

    Truncate note array from the begging or end by setting optional arguments

    """
    note_vector = NOTE_VECTOR
    if trunc_beg:
        note_vector = note_vector[trunc_beg:]
    if trunc_end:
        note_vector = note_vector[:trunc_end]

    note_positions = (np.abs(note_vector - note_frequency)).argmin()
    note_positions = np.where(note_positions == 0, -999999, note_positions)
    return note_positions


def find_closest_frequency(note_frequency, note_vector=NOTE_VECTOR):
    return note_vector[(np.abs(note_vector - note_frequency)).argmin()]

find_note_vector_position_vectorized = np.vectorize(find_note_vector_position)


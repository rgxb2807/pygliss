from pygliss.constants import DIVISIONS, BASE, A440

DIV = (DIVISIONS / 12)
NOTE_NAMES = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
HIGH_OCTAVE = 10
LOW_OCTAVE = -3


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


def lily(the_note):
	"""Sets Lilypond accidentals."""
	s = the_note.note.lower()
	if the_note.accidental == '+':
		s += 'qs'
	elif the_note.accidental == '#':
		s += 's'
	elif the_note.accidental == '++':
		s += 'tqs'
	elif the_note.accidental == '-':
		s += 'qf'
	elif the_note.accidental == 'b':
		s += 'b'
	elif the_note.accidental == '--':
		s += 'tqf'
	else:
		pass
	return s


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


def next_note(the_note):
	"""Returns the next note in an ascending quarter-tone scale."""
	note = the_note.note
	octave = the_note.octave
	accidental = the_note.accidental

	if accidental == None:
		if note == 'B' and DIV == 1:
			if octave < HIGH_OCTAVE:
				return Note('C', octave + 1)
			else:
				return None
		elif note == 'E' and DIV == 1:
			return Note('F', octave)
		else:
			return Note(note, octave, '+')

	elif accidental == '+':
		if note == 'B':
			if octave < HIGH_OCTAVE:
				return Note('C', octave + 1)
			else:
				return None
		elif note == 'E':
			return Note('F', octave)
		else:
			return Note(note, octave, '#')

	elif accidental == '#':
		if DIV == 1:
			idx = NOTE_NAMES.index(note)
			if idx == 6:
				return Note('A', octave)
			else:
				return Note(NOTE_NAMES[idx + 1], octave)
		elif DIV == 2:
			return Note(note, octave, '++')
		else:
			return None

	elif accidental == '++':
		idx = NOTE_NAMES.index(note)
		if idx == 6:
			return Note('A', octave)
		else:
			return Note(NOTE_NAMES[idx + 1], octave)

	elif accidental == '-':
		return None
	elif accidental == 'b':
		return None
	elif accidental == '--':
		return None
	else:
	    return None


def prev_note(the_note):
	"""Returns the previous note in an descending quarter-tone scale."""
	note = the_note.note
	octave = the_note.octave
	accidental = the_note.accidental

	if accidental == None:
		if note == 'C' and octave > LOW_OCTAVE:
			return Note('B', octave - 1, '+')
		elif note == 'F':
			return Note('E', octave, '+')
		else:
			return Note(note, octave, '-')
	elif accidental == '+':
		return Note(note, octave)
	elif accidental == '#':
		return Note(note, octave, '+')
	elif accidental == '++':
		return Note(note, octave, '#')
	elif accidental == '-':
		return Note(note, octave, 'b')
	elif accidental == 'b':
		return Note(note, octave, '--')
	elif accidental == '--':
		idx = NOTE_NAMES.index(note)
		if idx == 0:
			return Note('G', octave)
		elif idx == 2:
			return Note(NOTE_NAMES[idx - 1], octave - 1)
		else:
			return Note(NOTE_NAMES[idx - 1], octave)
	else:
		return None

 
def get_steps(note, octave, accidental):
	"""returns number of steps based on the number of divisions."""
	steps = (octave - 4) * DIVISIONS
	steps += get_note_steps(note)
	steps += get_accidental_steps(accidental)


def asc_notes_dict(low=Note('C', 0), high=Note('C', 9)):
	"""Returns a dict of ascending notes."""
	notes_dict = dict()
	current_note = low
	while(current_note.frequency() <= high.frequency()):
		current_note.Prev = current_note
		current_note.Next = next_note(current_note)
		notes_dict[str(current_note)] = current_note
		current_note = current_note.Next
	return notes_dict


def desc_notes_dict(low=Note('C', 0), high=Note('C', 9)):
	"""Returns a dict of descending notes."""
	notes_dict = dict()
	current_note = high
	while(current_note.frequency() >= low.frequency()):
		current_note.Next = current_note
		current_note.Prev = prev_note(current_note)
		notes_dict[str(current_note)] = current_note
		current_note = current_note.Prev

	return notes_dict


def freq_to_note(freq):
	"""
	Returns a note object based on a given frequency with quartertone 
	precision.
	"""
	asc_dict = asc_notes_dict()
	octave = 0
	rounded_freq = round(freq, 8)
	if rounded_freq >= round(asc_dict['C9'].frequency(), 8):
		octave = 9
	elif rounded_freq >= round(asc_dict['C8'].frequency(), 8):
		octave = 8
	elif rounded_freq >= round(asc_dict['C7'].frequency(), 8):
		octave = 7
	elif rounded_freq >= round(asc_dict['C6'].frequency(), 8):
		octave = 6
	elif rounded_freq >= round(asc_dict['C5'].frequency(), 8):
		octave = 5
	elif rounded_freq >= round(asc_dict['C4'].frequency(), 8):
		octave = 4
	elif rounded_freq >= round(asc_dict['C3'].frequency(), 8):
		octave = 3
	elif rounded_freq >= round(asc_dict['C2'].frequency(), 8):
		octave = 2
	elif rounded_freq >= round(asc_dict['C1'].frequency(), 8):
		octave = 1
	else:
		octave = 0

	diff = float('inf')
	note_str = ""
	accidental = None
	comp = freq / (2 ** octave)

	#C
	if abs(comp - asc_dict['C0'].frequency()) < diff:
		diff = abs(comp - asc_dict['C0'].frequency())
		note_str = "C"
		accidental = None
	if abs(comp - asc_dict['C0+'].frequency()) < diff:
		diff = abs(comp - asc_dict['C0+'].frequency())
		note_str = "C"
		accidental = "+"
	if abs(comp - asc_dict['C0#'].frequency()) < diff:
		diff = abs(comp - asc_dict['C0#'].frequency())
		note_str = "C"
		accidental = "#"
	if abs(comp - asc_dict['C0++'].frequency()) < diff:
		diff = abs(comp - asc_dict['C0++'].frequency())
		note_str = "C"
		accidental = "++"

	#D
	if abs(comp - asc_dict['D0'].frequency()) < diff:
		diff = abs(comp - asc_dict['D0'].frequency())
		note_str = "D"
		accidental = None
	if abs(comp - asc_dict['D0+'].frequency()) < diff:
		diff = abs(comp - asc_dict['D0+'].frequency())
		note_str = "D"
		accidental = "+"
	if abs(comp - asc_dict['D0#'].frequency()) < diff:
		diff = abs(comp - asc_dict['D0#'].frequency())
		note_str = "D"
		accidental = "#"
	if abs(comp - asc_dict['D0++'].frequency()) < diff:
		diff = abs(comp - asc_dict['D0++'].frequency())
		note_str = "D"
		accidental = "++"

	#E
	if abs(comp - asc_dict['E0'].frequency()) < diff:
		diff = abs(comp - asc_dict['E0'].frequency())
		note_str = "E"
		accidental = None
	if abs(comp - asc_dict['E0+'].frequency()) < diff:
		diff = abs(comp - asc_dict['E0+'].frequency())
		note_str = "E"
		accidental = "+"

	#F
	if abs(comp - asc_dict['F0'].frequency()) < diff:
		diff = abs(comp - asc_dict['F0'].frequency())
		note_str = "F"
		accidental = None
	if abs(comp - asc_dict['F0+'].frequency()) < diff:
		diff = abs(comp - asc_dict['F0+'].frequency())
		note_str = "F"
		accidental = "+"
	if abs(comp - asc_dict['F0#'].frequency()) < diff:
		diff = abs(comp - asc_dict['F0#'].frequency())
		note_str = "F"
		accidental = "#"
	if abs(comp - asc_dict['F0++'].frequency()) < diff:
		diff = abs(comp - asc_dict['F0++'].frequency())
		note_str = "F"
		accidental = "++"

	#G
	if abs(comp - asc_dict['G0'].frequency()) < diff:
		diff = abs(comp - asc_dict['G0'].frequency())
		note_str = "G"
		accidental = None
	if abs(comp - asc_dict['G0+'].frequency()) < diff:
		diff = abs(comp - asc_dict['G0+'].frequency())
		note_str = "G"
		accidental = "+"
	if abs(comp - asc_dict['G0#'].frequency()) < diff:
		diff = abs(comp - asc_dict['G0#'].frequency())
		note_str = "G"
		accidental = "#"
	if abs(comp - asc_dict['G0++'].frequency()) < diff:
		diff = abs(comp - asc_dict['G0++'].frequency())
		note_str = "G"
		accidental = "++"

	#A
	if abs(comp - asc_dict['A0'].frequency()) < diff:
		diff = abs(comp - asc_dict['A0'].frequency())
		note_str = "A"
		accidental = None
	if abs(comp - asc_dict['A0+'].frequency()) < diff:
		diff = abs(comp - asc_dict['A0+'].frequency())
		note_str = "A"
		accidental = "+"
	if abs(comp - asc_dict['A0#'].frequency()) < diff:
		diff = abs(comp - asc_dict['A0#'].frequency())
		note_str = "A"
		accidental = "#"
	if abs(comp - asc_dict['A0++'].frequency()) < diff:
		diff = abs(comp - asc_dict['A0++'].frequency())
		note_str = "A"
		accidental = "++"

	#B
	if abs(comp - asc_dict['B0'].frequency()) < diff:
		diff = abs(comp - asc_dict['B0'].frequency())
		note_str = "B"
		accidental = None
	if abs(comp - asc_dict['B0+'].frequency()) < diff:
		diff = abs(comp - asc_dict['B0+'].frequency())
		note_str = "B"
		accidental = "+"

	return Note(note_str, octave, accidental)


def get_partial(note, fundamental):
	return note.frequency() / fundamental.frequency()


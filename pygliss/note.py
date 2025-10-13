from pygliss.constants import DIVISIONS, BASE, A440, HIGH, LOW
from pygliss.utils import make_freq_vector
import numpy as np


DIV = (DIVISIONS / 12)
NOTE_VECTOR = make_freq_vector(DIVISIONS)
NOTE_VECTOR_12 = make_freq_vector(12)


class Note:
    """
    A class to represent a musical note
    ...
    Attributes
    ----------
        note : str
            the diatonic note represented as string
        octave : int
            the octave of the note
        accidental: str
            accidental alterations of a note in quarter tone increments.
                "+"  - quarter-tone sharp
                "#" - semi-tone sharp
                "++" - three-quarter tone sharp
                "-" - quarter-tone flat
                "b" - semi-tone flat
                "--" - three-quarter flat
        steps: int
            the number of quarter (or semi) steps away from the `BASE` note defined 
            in constants
        freq: float
            the frequency of the note

    Methods
    -------
        set_steps: 
            a helper function that sets the `steps` attribute for a given note 
            based on its position in the range of allowed notes.
        
        distance(input_note): 
            returns distance in quartertone steps between the current note and 
            the input note
        
        frequency: 
            returns the frequency value of the note
    """


    def __init__(self, note, octave, accidental=None):
        """
        Contructs Note
        Parameters
        ----------
            note : str
                the diatonic note represented as string
            octave : int
                the octave of the note
            accidental: str
                accidental alterations of a note in quarter tone increments.
        """
        self.note = note
        self.octave = octave
        self.accidental = accidental
        self.steps = None
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
    """
    Returns a note object from the input str
    The format of a string is:
        "Note Name" + "Accidental"  + "Octave" 
    
    Parameters
    ----------
        note_str : str
            the input chord
    Returns
    -------
        Note : pygliss.Note
            The note object from the string representation shorthand
    """

    note_name = note_str[:1]
    if len (note_str) == 2:
        return Note(note_name, int(note_str[1:2]))

    if len(note_str) == 3:
        return Note(note_name, int(note_str[2:3]), note_str[1:2])

    if len(note_str) == 4:
        return Note(note_name, int(note_str[3:4]), note_str[1:3])



def get_note_steps(note):
    """
    Gets associated steps for a given diatonic note.
    
    Parameters
    ----------
        note : str
            the input note str
    Returns
    -------
        steps : float
            Quarter tone sleps adjusted for the input accidental
    """
    steps = 0.0
    note_map = {"A":0, "B":2, "C":-9, "D":-7, "E":-5, "F":-4, "G":-2}
    step_val = note_map.get(note)
    if step_val:
        steps += step_val * DIV
    else:
        steps += 0
    return steps


def steps_to_note(steps):
    """
    Gets associated steps for a given diatonic note.
    
    Parameters
    ----------
        note : str
            the input note str
    Returns
    -------
        steps : float
            Quarter tone sleps adjusted for the input accidental
    """
    steps = 0.0
    note_map = {"A":0, "B":2, "C":-9, "D":-7, "E":-5, "F":-4, "G":-2}
    step_val = note_map.get(note)
    if step_val:
        steps += step_val * DIV
    else:
        steps += 0
    return steps


def get_accidental_steps(accidental):
    """
    Gets associated quarter tone steps for a given accidental.
    
    Parameters
    ----------
        accidental : str
            the input accidental
    Returns
    -------
        steps : float
            Quarter tone sleps adjusted for the input accidental
    """
    steps = 0.0
    acc_map = {"+":0.5, "#":1.0, "++":1.5, "-":-0.5, "b":-1.0, "--":-1.5}
    acc_val = acc_map.get(accidental)
    if acc_val:
        steps += acc_val * DIV
    else:
        steps += 0.0

    return steps


def freq_to_note(freq):
    """
    Returns a note object based on a given frequency with quartertone 
    precision.
    
    Parameters
    ----------
        freq : float
            the input frequency
    Returns
    -------
        Note : pygliss.Note
            The note object closest to the input frequency
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


def find_note_vector_position(note_frequency, trunc_beg=None, trunc_end=None):
    """
    Finds note position of a given frequency or array of frequencies

    Truncate note array from the begging or end by setting optional arguments

    Values below the frequency range are set to -999999
    
    Parameters
    ----------
        note_frequency : np.array[np.float]
            the input frequencies
    Returns
    -------
        note_positions : np.array[np.int]
            Array of position values for note frequency occurence in NOTE_VECTOR
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


from pygliss.sequence import ChordSequence, make_chord_seq_from_note_seq
from pygliss.gliss import Gliss
from pygliss.note import get_note
import numpy as np

class GlissCmpr(ChordSequence):
    """
    A specialized Chord Sequence generated from glissandi

    ...

    Attributes
    ----------
    glissandi : list of pygliss.gliss
        list of glissandi

    """
    def __init__(self, glissandi):
        self.glissandi = glissandi
        seq = make_chord_seq_from_note_seq(self.glissandi)
        super().__init__(seq.chords, seq.time_val, seq.durations)

    def __str__(self):
        s = ''
        for i in range(self.length):
            s += str(self.chords[i]) + " " + str(self.durations[i]) +"\n"
        return s



def make_gliss_cmpr_sequence(note_matrix):
    """
    Returns a list of GlissCmpr objects generated from the note sequences created
    from the not
    
    Parameters
    ----------
        note_matrix : 2D numpy.ndarray[numpy.float64] 
            Generates glissandi from a 2D matrix of frequency values
            
            Ex: A gliss is generated from the `note_matrix[0,0]` to 
            `note_matrix[0,1]` and then a gliss from `note_matrix[0,1]` to 
            `note_matrix[0,2]` and so on

    Returns
    -------
        chord_sequences : a list of pygliss.ChordSequence
            A list of ChordSequence objects generated from note_sequences generated
            from `note_matrix`

    """

    chord_sequences = []
    j_max, i_max = note_matrix.shape
    for i in range(i_max-1):
        glissandi = []
        for j in range(j_max):
            start = note_matrix[j,i]
            end = note_matrix[j, i+1]
            glissandi.append(Gliss(start, end))
        chord_sequences.append(GlissCmpr(glissandi))
    return chord_sequences



def get_note_mat_from_str(mat):
    """
    Returns a 2D of frequency matrix from a 2D list of note strings
    
    The format of a note string is "Bb4" or "F++4"
    
    Parameters
    ----------
        mat : 2D list of list of strings

    Returns
    -------
        freq_mat : 2D numpy.ndarray[numpy.float64] 
    """
    freq_mat = np.zeros((len(mat), len(mat[0])))
    for  i, row in enumerate(mat):
        for j, note_str in enumerate(row):
            freq_mat[i,j] = get_note(note_str).frequency()
    return freq_mat

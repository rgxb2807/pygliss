
from pygliss.sequence import NoteSequence
from pygliss.note import NOTE_VECTOR, NOTE_VECTOR_12
from pygliss.constants import LOW, HIGH

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

    def __init__(self, start, end, resolution=1, include_end=False):

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
        # Low Threshold Check
        if start < LOW:
            raise ValueError(f"Starting Note is too low - {start}")
        if end < LOW:
            raise ValueError(f"Ending Note is too low - {end}")

        # High Threshold Check
        if start > HIGH:
            raise ValueError(f"Starting Note is too high - {start}")
        if end > HIGH:
            raise ValueError(f"Ending Note is too high - {end}")
         
        self.start = start
        self.end = end
        self.ascend = None
        self.length = None
        self.resolution = resolution
        self.include_end = include_end


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
            if self.start <= self.end:
                self.ascend = True
            else:
                self.ascend = False

            
            # Filter note vector by High And low 
            low_idx = (np.abs(note_vector - low)).argmin()
            high_idx = (np.abs(note_vector - high)).argmin()
            if self.include_end and self.ascend:
                    high_idx += 1
            if not self.ascend:
                # low_idx += 1
                high_idx += 1
            if not self.ascend and not self.include_end:
                low_idx += 1



            notes = note_vector[low_idx:high_idx]
            # if self.include_end:
            #     notes = note_vector[low_idx:high_idx+1]
            if low_idx == high_idx:
                notes = [note_vector[low_idx]]
            self.length = len(notes)
            
            # Reverse order of list if gliss descends
            if start > end:
                # notes = note_vector[low_idx + 1:high_idx + 1]
                notes = notes[::-1]
                # self.ascend = False
            else:
                # self.ascend = True
                pass
                
            time_val = (1 /  len(notes)) * np.arange(0, len(notes))
            durations = (1 /  len(notes)) * np.ones(len(notes))
            super().__init__(notes, time_val, durations)


        # initialize parent class
        calc_gliss(self)

    def __str__ (self):
        return f"{self.notes}"


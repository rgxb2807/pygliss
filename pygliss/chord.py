import numpy as np
from pygliss.utils import find_note_vector_position_vectorized
from pygliss.constants import LOW

class Chord:
    """
    A class to represent a chord

    ...

    Attributes
    ----------
        notes : numpy.ndarray[numpy.float64] 
            the notes of the chord represented as frequency values
        duration : numpy.float64
            the duration of the chord


    Methods
    -------
        highest_note: 
            returns highest note in the chord
        
        lowest_note: 
            returns lowest note in the chord
        
        closest_note(note): 
            returns closest note in the chord to input note
        
        distance(in_chord): 
            returns distances between the current chord and the input chord

    """

    def __init__(self, notes, duration=1):

        """
        Contructs Chord

        Parameters
        ----------
            notes : numpy.ndarray[numpy.float64] 
                the notes of the chord represented as frequency values
            duration : numpy.float64
                the end note of the gliss
        """

        self.notes = notes
        self.duration = duration
        self.length = len(notes)
        self.steps = find_note_vector_position_vectorized(notes)

    def __str__ (self):
        return f"{self.notes} {self.duration}"

    def __eq__(self, other):
        return np.array_equal(self.notes, other)

    def __ne__(self, other):
        return np.array_equal(self.notes, other) == False

    def highest_note(self):
        return np.sort(self.notes)[-1]

    def lowest_note(self):
        return np.sort(self.notes)[0]

    def closest_note(self, note):
        return self.notes[np.abs(self.notes - note).argmin()]

    def distance(self, in_chord):
        """
        Returns stepwise distance from self to input chord `in_chord`
        Notes can be double counted, for every note, the closest is found
        
        Parameters
        ----------
            in_chord : pygliss.Chord
                the input chord

        Returns
        -------
            dist : int
                The stepwise distance between two chords

        """
        smaller, larger, dist = self.steps, in_chord.steps, 0
        if self.length > in_chord.length:
            smaller = in_chord.steps
            larger = self.steps
            
        for i in range(len(smaller)):
            dist += np.abs(larger - smaller[i]).min()
        return dist





def get_chord_distance(chord1_steps, chord2_steps, doublecount=True):
    """
    Returns stepwise distance between two chords represented as numpy arrays of
    note positions. It could also be used for arrays of frequencies but this wouldn't
    really give chordal distance.

    Notes can be double counted, for every note, the closest is found

    Parameters
    ----------
        chord1 : numpy.ndarray[numpy.int64]
            chord 1 input
        chord2 : numpy.ndarray[numpy.int64] 
            chord 2 input

    Returns
    -------
        dist : int
            The stepwise distance between two chords
    """
    if not doublecount:
        # TODO
        pass

    smaller, larger, dist = chord1_steps, chord2_steps, 0
    if len(chord1_steps) > len(chord2_steps):
        smaller = chord2_steps
        larger = chord1_steps
        
    for i in range(len(smaller)):
        dist += np.abs(larger - smaller[i]).min()
    return dist



def nearest_ot_chord(chord_freq, m, tiebreak=None):
    """
    A vectorized implementation of finding the nearest overtone chord extended 
    from Terhardt's subCoincidence algorithm for calculating virtual pitch. See
    http://jjensen.org/VirtualPitch.html

    Parameters
    ----------
        chord_freq : numpy.ndarray[numpy.float64]
            the frequencies of the input chord
        m : int
            the number of subharmonics considered
        tiebreak : str
            determines the behavior of the tiebreak. set tiebreak to `highest` 
            and the subhamonic is derived from the highest note in the chord is 
            chosen

    Returns
    -------
        chord frequencies of nearest overtone : numpy.ndarray[numpy.float64]
            the nearest overtone chord frequencies as a numpy array
    """
    chord_freq = np.sort(chord_freq)
    chord_steps = find_note_vector_position_vectorized(chord_freq)
    len_notes = len(chord_freq)
    
    # generate all possible overtone chords
    all_chord_sets = np.ones((len_notes, m, len_notes))
    for i in range(len_notes):
        subharmonics = chord_freq[i] * (1 / np.arange(1, m + 1))
        # filter values lower than human hearing
        subharmonics = np.where(subharmonics >= LOW, subharmonics, -1)
        harmonics = np.rint(chord_freq / subharmonics[:,np.newaxis])
        chords = harmonics * subharmonics[:, np.newaxis]
        all_chord_sets[i] = chords
        
    # convert frequencies to nearest step of temperment set in `DIVISIONS`
    all_chord_steps = find_note_vector_position_vectorized(all_chord_sets)
    
    # distance by summing stepwise difference along axis
    diff_from_target_chord = np.sum(np.abs(all_chord_steps - chord_steps), axis=2)

    # choose lowest subharmonic chord
    min_diff = np.where(diff_from_target_chord == diff_from_target_chord.min())
    row_idx, chord_idx = min_diff[0][0], min_diff[1][0]
    if tiebreak == "highest":
        row_idx, chord_idx = min_diff[0][-1], min_diff[1][-1]
    
    return all_chord_sets[row_idx, chord_idx]







# Delete after refactor



# from pygliss.note import Note, freq_to_note

# MAX_INHARMONIC_TONES = 200

# class Chord:

#     def __init__ (self, notes, dur=0):
#         # self.notes = sorted(list(set(notes)), key=lambda x: x.frequency())
#         self.notes = sorted(notes, key=lambda x: x.frequency())
#         self.dur = dur
#         # self.remove_duplicates()

#     def __str__ (self):
#         s = ''
#         for note in self.notes:
#             s += str(note) + ', '
#         #remove last ','
#         return s[:len(s) - 2]

#     def __eq__(self,other):
#         if len(self.notes) != len(other.notes):
#             return False
#         else:
#             for i in range(0, len(self.notes)):
#                 if self.notes[i] != other.notes[i]:
#                     return False
#             return True

#     def __ne__(self, other):
#         if other == None:
#             return False 
#         if len(self.notes) != len(other.notes):
#             return True
#         else:
#             for i in range(0, len(self.notes)):
#                 if self.notes[i] != other.notes[i]:
#                     return True
#             return False

#     def remove(self, note):
#         if note in self.notes:
#             self.notes.remove(note)

#     def distance(self, other_chord):
#         total_dist = 0
#         for i, note in enumerate(self.notes):
#             candidate_dist = float("inf")
#             for j, other_note in enumerate(other_chord.notes):
#                 temp = note.distance(other_note)
#                 if temp < candidate_dist:
#                     candidate_dist = temp
#             total_dist += candidate_dist
#         return total_dist

#     def highest_note(self):
#         highest, highest_freq = None, float("-inf")
#         for note in self.notes:
#             if note.frequency() > highest_freq:
#                 highest_freq = note.frequency()
#                 highest = note
#         return highest

#     def lowest_note(self):
#         lowest, lowest_freq = None, float("inf")
#         for note in self.notes:
#             if note.frequency() < lowest_freq:
#                 lowest_freq = note.frequency()
#                 lowest = note
#         return lowest

#     def closet_note(self, target_note):
#         #could be binary search for more efficient implmentation
#         distance = float("inf")
#         closest = None
#         for note in self.notes:
#             if note.distance(target_note) < distance:
#                 distance = note.distance(target_note)
#                 closest = note
#         return closest


# # adapted from Terhardt's subCoincidence algorithm for calculating 
# # virtual pitch. The int m is the number of fundamental candidates are 
# # allowed instead of frequency, the number of quarter tone steps is 
# # considered the distance or "closest" to avoid a a clustering of 
# # high-frequency solutions.  A frequency sensative method to be 
# # implemented 

# def nearest_ot_chord(chord, m):

#     ot_chord = list()
#     ot_chord_found = False
#     final_steps = -1
#     fundamental = Note("C", 0)

#     for i in range(0, len(chord.notes)):
#         current_freq = chord.notes[i].frequency()

#         #loop over subharmonics
#         for sub in range(1, m):
#             current_sub_harmonic = (1.0 / sub) * current_freq
#             current_steps = 0
#             temp_chord = list()

#             for j in range(0, len(chord.notes)):
#                 #if current subharmonic is lower than lowest note
#                 if current_sub_harmonic > chord.notes[0].frequency() or current_sub_harmonic < 16.3515978313:
#                     current_steps = 1000
#                     break
#                 #calculate nearest harmonic
#                 n = int(round(chord.notes[j].frequency() / current_sub_harmonic))
#                 #create temp note from nearest harmonic
#                 temp_note = freq_to_note(n * current_sub_harmonic)
#                 current_steps += abs(temp_note.steps - chord.notes[j].steps)
#                 temp_chord.append(temp_note)

#             if final_steps == -1 and current_steps > 0 or current_steps <= final_steps:
#                     if current_steps == final_steps and current_sub_harmonic < fundamental.frequency():
#                         pass
#                     else:
#                         temp_ot_chord = list()
#                         final_steps = current_steps
#                         for k in range(0, len(temp_chord)):
#                             temp_ot_chord.append(temp_chord[k])
                        
#                         ot_chord = temp_ot_chord                        
#                         fundamental = freq_to_note(current_sub_harmonic)
#                         ot_chord_found = True

#     if ot_chord_found == True:
#         return (Chord(ot_chord, 1), fundamental, final_steps)
#     else:
#         return (None, None, None)


# def diff_tones(chord, carrier=0.0):
#     diff_chord = list()
#     for i in range(0, len(chord.notes)):
#         freq = abs(chord.notes[i].frequency - carrier)
#         if freq > 16.0:
#             if freq_to_note(freq) not in diff_chord:
#                 diff_chord.append(freq_to_note(freq))
#     return Chord(diff_chord, 0)


# def sum_tones(chord, carrier=0.0):
#     diff_chord = list()
#     for i in range(0, len(chord.notes)):
#         freq = chord.notes[i].frequency + carrier
#         if freq > 16.0:
#             if freq_to_note(freq) not in diff_chord:
#                 diff_chord.append(freq_to_note(freq))
#     return Chord(diff_chord, 0)

# #made two tones side bands of a carrier frequency
# def get_carrier(note1, note2):
#     freq_diff = abs(note1.frequency - note2.frequency)
#     return freq_diff / 2


# def get_diff_tones(note, carrier, no_tones):
#     notes = []
#     freq = note.frequency
#     for i in range(no_tones):
#         if abs(i * freq - carrier) > 16.0:
#             temp_note = freq_to_note(abs(i * freq - carrier))
#             if temp_note not in notes:
#                 notes.append(temp_note)
#     return notes


# def get_sum_tones(note, carrier, no_tones):
#     notes = []
#     freq = note.frequency
#     for i in range(no_tones):
#         if i * freq + carrier > 16.0:
#             temp_note = freq_to_note(i * freq + carrier)
#             if temp_note not in notes:
#                 notes.append(temp_note)
#     return notes


# def avg_carrier(chord):
#     sum_carrier = 0.0
#     count = 0
#     for i in range(0, len(chord.notes)):
#         for j in range(i,len(chord.notes)):
#             if i != j:
#                 sum_carrier += get_carrier(chord.notes[i], chord.notes[j])
#                 count += 1
#     return sum_carrier / count


# #two implementations
# # if use_carrier = True, the carrier is included in the sounding result chord otherwise
# # it defaults to finding the carrier by averaging all tones in the chord
# # if resolution is specified, it indicates the no. of 1/4 tones the carrier should 
# # deviate from the average
# def nearest_inharmonic(chord, use_carrier=False, resolution=None):

#     if use_carrier:
#         return nearest_inharmonic_use_carrier(chord)

#     avg = avg_carrier(chord)
#     lowest = chord.lowest_note()
#     highest = chord.highest_note()

#     nearest_inharmonic, full_inharmonic_chord = None, None
#     nearest_inharmonic_distance = float("inf")

#     for note in chord.notes:
#         diff_tones_no, sum_tone_no = MAX_INHARMONIC_TONES, MAX_INHARMONIC_TONES
#         sum_tones = get_sum_tones(note, avg, sum_tone_no)
#         diff_tones = get_diff_tones(note, avg, diff_tones_no)
#         temp_inharmonic_chord = Chord(sum_tones + diff_tones)
#         temp_nearest_inharmonic = []
#         #find closest notes in temp chord to
#         for temp_note in chord.notes:
#             temp_closest = temp_inharmonic_chord.closet_note(temp_note)
#             temp_nearest_inharmonic.append(temp_closest)
#             temp_inharmonic_chord.remove(temp_closest)

#         temp_distance = chord.distance(Chord(temp_nearest_inharmonic))
#         if temp_distance < nearest_inharmonic_distance:
#             nearest_inharmonic = Chord(temp_nearest_inharmonic)
#             full_inharmonic_chord = temp_inharmonic_chord
#             nearest_inharmonic_distance = temp_distance


#     return nearest_inharmonic, nearest_inharmonic_distance



# def nearest_inharmonic_use_carrier(chord):

#     lowest = chord.lowest_note()
#     highest = chord.highest_note()

#     nearest_inharmonic, full_inharmonic_chord = None, None
#     nearest_inharmonic_distance = float("inf")
    
#     for carrier in chord.notes:
#         for modulator in chord.notes:
#             if carrier != modulator:
#                 diff_tones_no, sum_tone_no = MAX_INHARMONIC_TONES, MAX_INHARMONIC_TONES
#                 sum_tones = get_sum_tones(modulator, carrier.frequency, sum_tone_no)
#                 diff_tones = get_diff_tones(modulator, carrier.frequency, diff_tones_no)
#                 temp_inharmonic_chord = Chord(sum_tones + diff_tones)
#                 temp_nearest_inharmonic = []

#                 for temp_note in chord.notes:
#                     temp_closest = temp_inharmonic_chord.closet_note(temp_note)
#                     temp_nearest_inharmonic.append(temp_closest)
#                     temp_inharmonic_chord.remove(temp_closest)

#                 temp_distance = chord.distance(Chord(temp_nearest_inharmonic))
#                 if temp_distance < nearest_inharmonic_distance:
#                     nearest_inharmonic = Chord(temp_nearest_inharmonic)
#                     full_inharmonic_chord = temp_inharmonic_chord
#                     nearest_inharmonic_distance = temp_distance

#     return nearest_inharmonic, nearest_inharmonic_distance


# # TODO - Cluster Chords
# # def get_cluster(note, no_tones, resolution):
# #   cluster_chords = []



# # todo - check for 1/4 tone, 1/2 tone, 3/4 tone, and whole tone clusters
# # def nearest_cluster(chord, resolution=None):

# #   distance = 0
# #   if resolution is None:
# #       resolution = 0.25

# #   for note in chord.notes:


# # todo - finds chords that are combinations clusters of 1/4 tone, 
# # 1/2 tone, 3/4 tone, and whole tone clusters
# # def nearest_distorted_cluster



# # a = Chord(ASC_DICT['C5'], ASC_DICT['C3'], ASC_DICT['G4'], ASC_DICT['E3'])
# #print(a)
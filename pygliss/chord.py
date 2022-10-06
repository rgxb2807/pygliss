from pygliss.note import freq_to_note, find_note_vector_position_vectorized, NOTE_VECTOR, NOTE_VECTOR_12
from pygliss.constants import LOW, HIGH, MAX_CHORD_LENGTH

import itertools
import numpy as np


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

    def get_notes(self):
        return [freq_to_note(self.notes[i]) for i in range(self.length)]

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


class OvertoneChord(Chord):
    """
    A class to represent an Overtone chord

    ...

    Attributes
    ----------
        notes : numpy.ndarray[numpy.float64] 
            the notes of the chord represented as frequency values
        duration : numpy.float64
            the duration of the chord
        fundamental : numpy.float64
            fundamental of the overtone chord


    Methods
    -------
        fundamental_note()
            returns instance of pygliss.note.Note of the fundamental pitch

    """
    def __init__(self, notes, fundamental, duration=1):
        """
        Contructs Overtone Chord

        Parameters
        ----------
            notes : numpy.ndarray[numpy.float64] 
                the notes of the chord represented as frequency values
            duration : numpy.float64
                the end note of the gliss
            fundamental : numpy.float64
                fundamental of the overtone chord
        """
        super().__init__(notes, duration)
        self.fundamental = fundamental

    def fundamental_note(self):
        return freq_to_note(self.fundamental)



MAX_SIDEBANDS = 20
FREQ_MODULATORS = np.outer(np.arange(1, MAX_SIDEBANDS+1), NOTE_VECTOR)
SUM_TONES = np.zeros((len(NOTE_VECTOR), MAX_SIDEBANDS, len(NOTE_VECTOR)))
DIFF_TONES = np.zeros((len(NOTE_VECTOR), MAX_SIDEBANDS, len(NOTE_VECTOR)))
FM_CHORDS = np.zeros((len(NOTE_VECTOR), MAX_SIDEBANDS * 2, len(NOTE_VECTOR)))
FM_CHORDS_W_CARRIER = np.zeros((len(NOTE_VECTOR), ((MAX_SIDEBANDS * 2) + 1), len(NOTE_VECTOR)))

for i in range(len(NOTE_VECTOR)):
    SUM_TONES[i] = NOTE_VECTOR[i] + FREQ_MODULATORS
    DIFF_TONES[i] = np.abs(NOTE_VECTOR[i] - FREQ_MODULATORS)
    FM_CHORDS[i] = np.vstack((SUM_TONES[i], DIFF_TONES[i]))
    carrier = np.ones(len(NOTE_VECTOR)) * NOTE_VECTOR[i]
    FM_CHORDS_W_CARRIER[i] = np.vstack((FM_CHORDS[i], carrier))


FM_CHORDS_STEPS = find_note_vector_position_vectorized(FM_CHORDS)
FM_CHORDS_W_CARRIER_STEPS = find_note_vector_position_vectorized(FM_CHORDS_W_CARRIER)


# for use with roughness calculation
COMBOS = []
for i in range(MAX_CHORD_LENGTH):
    COMBOS.append(np.array(list(itertools.combinations(np.arange(i), 2))))


class FMChord(Chord):
    """
    A class to represent an FM chord

    The modulator and Carrier must be higher than `LOW` and lower than `HIGH`

    ...

    Attributes
    ----------
        notes : numpy.ndarray[numpy.float64] 
            the notes of the chord represented as frequency values
        duration : numpy.float64
            the duration of the chord
        carrier : numpy.float64
            carrier of the fm chord
        modulator : numpy.float64
            modulator of the fm chord


    Methods
    -------
        sum_tones(self)
            returns all sum tones associated with modulator and carrier

        roughness(only_notes=False)
            returns roughness of FM Chord
        

    """
    def __init__(self, notes, carrier, modulator, duration=1):
        """
        Contructs FM Chord

        Parameters
        ----------
            notes : numpy.ndarray[numpy.float64] 
                the notes of the chord represented as frequency values
            duration : numpy.float64
                the end note of the gliss
            carrier : numpy.float64
                carrier of the fm chord - must be 
            modulator : numpy.float64

        """
        super().__init__(notes, duration)
        self.carrier = carrier if carrier >= LOW else LOW if carrier <= HIGH else HIGH
        self.modulator = modulator if modulator >= LOW else LOW if modulator <= HIGH else HIGH 


    def __str__(self):
        return f"{self.notes} carrier:{self.carrier} modulator:{self.modulator} dur:{self.duration}"

    def sum_tones(self):
        """ Returns all sum tones from carrier and modulator"""
        indicies = find_note_vector_position_vectorized(np.array([self.carrier, self.modulator]))
        if np.isclose(self.carrier, LOW):
            indicies[0] = 0
        if np.isclose(self.modulator, LOW):
            indicies[1] = 0
        if np.isclose(self.carrier, HIGH):
            indicies[0] = -1
        if np.isclose(self.modulator, HIGH):
            indicies[1] = -1
        return FM_CHORDS[indicies[0],:sidebands,indicies[1]]


    def diff_tones(self):
        """ Returns all difference tones from carrier and modulator"""
        indicies = find_note_vector_position_vectorized(np.array([self.carrier, self.modulator]))
        if np.isclose(self.carrier, LOW):
            indicies[0] = 0
        if np.isclose(self.modulator, LOW):
            indicies[1] = 0
        if np.isclose(self.carrier, HIGH):
            indicies[0] = -1
        if np.isclose(self.modulator, HIGH):
            indicies[1] = -1
        return FM_CHORDS[indicies[0],sidebands:,indicies[1]]

    def fm_tones(self):
        """Returns all sum and difference tones from carrier and modulator"""
        indicies = find_note_vector_position_vectorized(np.array([self.carrier, self.modulator]))
        if np.isclose(self.carrier, LOW):
            indicies[0] = 0
        if np.isclose(self.modulator, LOW):
            indicies[1] = 0
        if np.isclose(self.carrier, HIGH):
            indicies[0] = -1
        if np.isclose(self.modulator, HIGH):
            indicies[1] = -1
        return FM_CHORDS[indicies[0], :, indicies[1]]


    def chord_sum_tones(self):
        """Returns chord notes that are sum tones from carrier and modulator"""
        return np.intersect1d(self.notes, self.sum_tones())

    def chord_diff_tones(self):
        """Returns chord notes that are difference tones from carrier and modulator"""
        return np.intersect1d(self.notes, self.diff_tones())

    def missing_sum_tones(self):
        """Returns sum tones from carrier and modulator not in the chord notes"""
        return np.setdiff1d(self.chord_sum_tones, self.sum_tones())

    def missing_diff_tones(self):
        """Returns difference tones from carrier and modulator not in the chord notes"""
        return np.setdiff1d(self.chord_diff_tones, self.diff_tones())

    def roughness(self, only_notes=False):
        """
        Returns roughness of the entire FM chord (Vassilakis 2001,2005)

        Set `only_notes` to True and only chord notes are calculated for roughness
        """
        if only_notes:
            return calc_roughness(self.notes)
        return calc_roughness(self.fm_tones())



def get_chord_distance(chord1_steps, chord2_steps, doublecount=True):
    """
    Returns stepwise distance between two chords represented as numpy arrays of
    note positions. It could also be used for arrays of frequencies but this 
    wouldn't really give chordal distance.

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

    ot_notes = all_chord_sets[row_idx, chord_idx]
    fundamental = chord_freq[row_idx] * (1 / (chord_idx + 1))
    
    return OvertoneChord(ot_notes, fundamental)




def calc_roughness(chord_freq):
    """
    Calculates the roughness of a chord frequencies from Vassilakis 2001,2005
    Ampltitude is set constant at 1


    Parameters
    ----------
        chord_freq : numpy.ndarray[numpy.float64]
            the frequencies of the input chord

    Returns
    -------
        roughness : numpy.float64
            roughness as defined by Vassilakis
         
    """
    c = COMBOS[len(chord_freq)]
    freq_pairs = chord_freq[c]
    amp_arr = np.ones((freq_pairs.shape))
    
    A_min, A_max = np.min(amp_arr, axis=1), np.max(amp_arr, axis=1)
    F_min, F_max = np.min(freq_pairs, axis=1), np.max(freq_pairs, axis=1)
    X = A_min * A_max
    Y = 2 * A_min / (A_min + A_max)
    b1, b2 = 3.5, 5.75
    s1, s2 = 0.0207, 18.96
    s = 0.24 / (s1 * F_min + s2)
    Z = np.exp(-1 * b1 * s *(F_max - F_min)) - np.exp(-b2 * s * (F_max - F_min))    
    R = np.power(X, 0.1) * 0.5 * np.power(Y, 3.11) * Z
    
    return np.sum(R)


def nearest_fm_chord(chord_freq, sidebands=None):
    """
    Find the nearest stepwise FM chords to the input chord 

    Parameters
    ----------
        chord_freq : numpy.ndarray[numpy.float64]
            the frequencies of the input chord
        sidebands : int
            the number of sidebands considered, uses MAX_SIDEBANDS if not
            specified

    Returns
    -------
        solutions : list of dict, each solution has 3 keys:
            `min_steps` : 
                the number of steps the solution is from the input chord
            `roughness`: numpy.float64
                roughness as defined by Vassilakis
            `fm_chord` : pygliss.FMChord
                the resultant FM chord

    """
    fm_chords_steps_w_carrier = None
    if not sidebands:
        fm_chords_steps_w_carrier = FM_CHORDS_W_CARRIER_STEPS
    elif sidebands < MAX_SIDEBANDS:
        sum_tones = FM_CHORDS_W_CARRIER_STEPS[:,:sidebands,:]
        diff_tones = FM_CHORDS_W_CARRIER_STEPS[:,sidebands:-1,:]
        carrier = FM_CHORDS_W_CARRIER_STEPS[:,MAX_SIDEBANDS * 2:,:]
        temp = np.hstack((sum_tones, diff_tones))
        fm_chords_steps_w_carrier = np.hstack((temp, carrier))

    chord_steps = np.sort(find_note_vector_position_vectorized(chord_freq))
    min_steps, candidates = float("+inf"), set()
    solutions = []
    
    #find minimium stepwise distance of each chord note to all FM CHORDS
    for i in range(len(chord_steps)):
        diff = np.abs(fm_chords_steps_w_carrier - chord_steps[i])
        min_diff = np.where(diff == diff.min())
        #add candidate chords to set
        for idx in range(len(min_diff[0])):
            candidates.add((min_diff[0][idx], min_diff[2][idx]))
    
    #find minimium stepwise distance of each candidate chord to original chord
    for candidate in candidates:
        fm_chord = fm_chords_steps_w_carrier[candidate[0],:,candidate[1]]
        dist = get_chord_distance(chord_steps, fm_chord)
        if dist < min_steps:
            min_steps = dist
            solutions = [{
                "min_steps":min_steps,
                "roughness":calc_roughness(FM_CHORDS[candidate[0],:, candidate[1]]),
                "fm_chord":FMChord(chord_freq, NOTE_VECTOR[candidate[0]], 
                    NOTE_VECTOR[candidate[1]])
            }]

        elif dist == min_steps:
            solutions.append({
                "min_steps":min_steps,
                "roughness":calc_roughness(FM_CHORDS[candidate[0],:, candidate[1]]),
                "fm_chord":FMChord(chord_freq, NOTE_VECTOR[candidate[0]], 
                    NOTE_VECTOR[candidate[1]])
            })

    return sorted(solutions, key=lambda x: (x['roughness'], x['fm_chord'].carrier, x['fm_chord'].modulator))









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
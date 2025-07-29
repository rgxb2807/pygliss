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

        self.notes = np.sort(notes)
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

    def to_notes(self):
        note_objs = []
        for i in range(len(self.notes)):
            n = freq_to_note(self.notes[i])
            if n is None:
                continue
            note_objs.append(n)
        return note_objs

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

    def get_partials(self, note=None, m=26, include_fund=False):
        """
        Returns the partials or overtone based on the specified note
        m is the number of partials
        Set `include_fund` = True to include the fundamental


        The fundamental is used when the note is note specified.

        """
        partials = self.fundamental * np.arange(1, m + 1)
        if note: 
            partials = note * np.arange(1, m + 1)
        return partials if include_fund else partials[1:]

    def chord_partials(self, m=26, return_partials=False):
        """
        Returns the partials or overtone of the chord
        Set `return_partials` = True to return the partial numbers


        The fundamental is used when the note is note specified.

        """

        note_positions = find_note_vector_position_vectorized(self.notes)
        partials = self.get_partials(m=m, include_fund=True)
        ot_positions = find_note_vector_position_vectorized(partials)
        tones, _, ot =  np.intersect1d(note_positions, ot_positions, return_indices=True)
        if return_partials:
            return ot + 1
        return NOTE_VECTOR[tones]



MAX_SIDEBANDS = 30
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
        return FM_CHORDS[indicies[0],:MAX_SIDEBANDS,indicies[1]]


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
        return FM_CHORDS[indicies[0],MAX_SIDEBANDS:,indicies[1]]

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


    def chord_sum_tones(self,return_sb=False):
        """
        Returns chord notes that are sum tones from carrier and modulator
        Set `return_sb` = True to return sideband values
        """
        note_positions = find_note_vector_position_vectorized(self.notes)
        sum_tone_positions = find_note_vector_position_vectorized(self.sum_tones())
        tones, _, sb =  np.intersect1d(note_positions, sum_tone_positions, return_indices=True)
        if return_sb:
            return sb + 1
        return NOTE_VECTOR[tones]

    def chord_diff_tones(self, return_sb=False):
        """
        Returns chord notes that are difference tones from carrier and modulator
        Set `return_sb` = True to return sideband values
        """
        note_positions = find_note_vector_position_vectorized(self.notes)
        diff_tone_positions = find_note_vector_position_vectorized(self.diff_tones())
        # return np.intersect1d(self.notes, self.sum_tones())
        tones, _, sb =  np.intersect1d(note_positions, diff_tone_positions, return_indices=True)
        if return_sb:
            return sb + 1
        return NOTE_VECTOR[tones]

    def missing_sum_tones(self):
        """Returns sum tones from carrier and modulator not in the chord notes"""
        return np.setdiff1d(self.chord_sum_tones(), self.sum_tones())

    def missing_diff_tones(self):
        """Returns difference tones from carrier and modulator not in the chord notes"""
        return np.setdiff1d(self.chord_diff_tones(), self.diff_tones())

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
    chord_freq = chord_freq[chord_freq >= NOTE_VECTOR[0]]
    chord_freq = np.sort(chord_freq)
    chord_steps = find_note_vector_position_vectorized(chord_freq)
    len_notes = len(chord_freq)
    
    # generate all possible overtone chords
    all_chord_sets = np.ones((len_notes, m, len_notes))
    for i in range(len_notes):
        subharmonics = chord_freq[i] * (1 / np.arange(1, m + 1))
        # filter values lower than human hearing
        # subharmonics = np.where(subharmonics >= LOW, subharmonics, -1)

        # TEMP FIX - because the low value is zeroed out in find_note_vector_position_vectorized
        # we have to use 1 value above the lowest to avoid the index out of range issue
        subharmonics = np.where(subharmonics >= NOTE_VECTOR[1], subharmonics, np.inf)
        # # replace +inf values with min hearable value
        # # TODO - remove duplicates 
        subharmonics = np.where(subharmonics == np.inf, np.min(subharmonics), subharmonics)
        # adjust subharmonics for equal temperament note values
        subharmonics = NOTE_VECTOR[find_note_vector_position_vectorized(subharmonics)]
        harmonics = np.rint(chord_freq / subharmonics[:,np.newaxis]) # should this be chord_freq[i] ?????
        chords = harmonics * subharmonics[:, np.newaxis]
        all_chord_sets[i] = chords
        
    # convert frequencies to nearest step of temperment set in `DIVISIONS`
    all_chord_steps = find_note_vector_position_vectorized(all_chord_sets)
    
    # distance by summing stepwise difference along axis
    diff_from_target_chord = np.sum(np.abs(all_chord_steps - chord_steps), axis=2)

    # choose subharmonic chord with highest fundamental
    min_diff = np.where(diff_from_target_chord == diff_from_target_chord.min())
    row_idx, chord_idx = min_diff[0][-1], min_diff[1][-1]
    if tiebreak == "lowest":
        row_idx, chord_idx = min_diff[0][0], min_diff[1][0]

    ot_notes = all_chord_sets[row_idx, chord_idx]
    fundamental = chord_freq[row_idx] * (1 / (chord_idx + 1))
    
    return OvertoneChord(ot_notes, fundamental)




def calc_roughness(chord_freq):
    """
    Calculates the roughness of a chord frequencies from Vassilakis 2001,2005
    Ampltitude is set constant at 1

    http://www.acousticslab.org/learnmoresra/moremodel.html


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



def filter_fm_ot_chords(chords, ot_subharm=12, ot_dist=0, fm_roughness=10):
    """
    Given a list of chord obects, it returns candidates of nearest overtone chord 
    and nearest fm chords based on specified parameters

    Returns dictionary of solutions

    """
    solutions = []
    for idx, chord in enumerate(chords):
        candidate_chords = []
        fm_solutions = nearest_fm_chord(chord.notes)
        for sol in fm_solutions:
            if sol['roughness'] <= fm_roughness:
                candidate_chords.append({
                    "type":"fm",
                    "full_roughness":sol['roughness'],
                    "roughness":calc_roughness(sol['fm_chord'].notes),
                    "chord":sol['fm_chord']
                })           
        ot = nearest_ot_chord(chord.notes, ot_subharm)
        cur_ot_dist = ot.distance(chord)
        if cur_ot_dist <= ot_dist:
            
            # include original chord
            if cur_ot_dist != 0:
                candidate_chords.append({
                    "type":f"ot_dist_{cur_ot_dist}_fund_{ot.fundamental_note()}",
                    "roughness":None,
                    "chord":chord,
                    "full_roughness":None
                })
            candidate_chords.append({
                "type":"ot",
                "roughness":None,
                "chord":ot,
                "full_roughness":None
            })
        if len(candidate_chords) > 0:
            solutions.append({
                "candidates":candidate_chords,
                "idx":idx
            })
    return solutions


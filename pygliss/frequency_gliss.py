import numpy as np
from collections import OrderedDict
from pygliss.utils import make_freq_vector, make_freq_to_steps_map, find_note_vector_position_vectorized

NOTE_VECTOR = make_freq_vector()


def calc_gliss(start, end):
    """
    Calculate gliss frequencies and when they occur 
    with note values specified in the note_vector.  time_vals are when the note 
    starts based on a total gliss duration of 1.
    
    A glissando is an exponential pitch function of 
    equal tempered notes in time. Each step 
    increaeses NOTE * 2 **1/DIVISIONS
    
    Each note duration is equal 
    """ 
    # Find high and low notes of gliss
    high = end if end >= start else start
    low = start if start <= end else end
    
    # Filter note vector by High And low 
    low_idx = (np.abs(NOTE_VECTOR - low)).argmin()
    high_idx = (np.abs(NOTE_VECTOR - high)).argmin()
    notes = NOTE_VECTOR[low_idx:high_idx]
    
    # Reverse order of list if gliss descends
    if start > end:
        notes = notes[::-1]
        
    time_val = (1 /  len(notes)) * np.arange(0, len(notes))
    durations = (1 /  len(notes)) * np.ones(len(notes))
    return np.vstack((time_val, notes, durations)) 


def make_chords_from_note_sequences(sequences):
    """
    Returns all unique chords from overlapping glissandi
    
    The First row is time
    The last row is the duration of each note
    Each gliss has a frequency row and a note duration row
    
    """
    # Get time values
    time_tuple = ([seq[0] for seq in sequences])
    time_vals = np.sort(np.unique(np.concatenate((time_tuple))))
    
    # create array for time, glissandi and note durations
    chords = np.zeros(((len(sequences) + 2), time_vals.shape[0]))
    chords[0] = time_vals
    
    # calculate durations
    diff = np.diff(time_vals)
    chords[-1] = np.append(diff, [1 - np.sum(diff)])
    
    # for every timestep in a gliss, set the note value in chords
    for seq_idx, seq in enumerate(sequences):
        g_time_idx = 1
        for idx, time_val in enumerate(time_vals):
            if seq[0, g_time_idx] > time_val:
                chords[seq_idx + 1, idx] = seq[1, g_time_idx - 1]
            else:
                if (g_time_idx + 1) < seq.shape[1]:
                    g_time_idx += 1
                chords[seq_idx + 1,idx] = seq[1, g_time_idx - 1]
    return chords

    
def approximate_equal_note_durations(durations, beats, subdivisons=4):
    """
    Returns the nearest equal  
    
    Let the number of durations in the sequence be the lcm.
    Let beats be the "a" value for the lcm arg. Find the b value.  
    Increase the lcm to get the lowest integer value.
    """
    note_count = len(durations)
    tuple_val = note_count / beats
    print(f"note count:{note_count} tuple:{tuple_val}")
    
    while not tuple_val.is_integer():
        note_count += 1
        tuple_val = note_count / beats
        print(f"note count:{note_count} tuple:{tuple_val}")
        
    # needs to be adjusted to handle tied tuple values
    # 391.99543598 to 440 is five steps
    # this can be repesented as a 3 values of quintuplets 
    # 3 + 2 | 1 + 3 + 1 | 2 + 3
    # what about adding 3 quintuplet rest to this example were 4 steps

    

def approximate_note_durations(durations, beats, subdivisons=4):
    """
    Given a set of time_values over 
    """
    if np.all(durations):
        return approximate_equal_note_durations(durations, beats, subdivisons)



def tiebreak_chord(chord, minimum_values_idx, tiebreak=None):
	"""
	Breaks a tie when multiple target chords have the same number of steps from
	the original chord and the subharmonics are the same

	The default is to choose the subharmonic who is derived from the lowest note 
	in the chord.

	set tiebreak to `highest` and the subhamonic is derived from the highest 
	note in the chord is chosen

	"""
    row_idx, chord_idx = 0,0
    if tiebreak =="highest":
        row_idx = minimum_values_idx[np.argmax(chord[minimum_values_idx])]
        chord_idx = min_subharm_idx[row_idx]
    else:
        row_idx = minimum_values_idx[np.argmin(chord[minimum_values_idx])]
        chord_idx = min_subharm_idx[row_idx]
    return row_idx, chord_idx


def vectorized_nearest_ot(chord, m, tiebreak=None):
    """
    A vectorized implementation of finding the nearest overtone chord extended 
    fromTerhardt's subCoincidence algorithm for calculating virtual pitch
    
    m is the number of subharmonics considered
    
    tiebreak defaults to selecting the lowest note to generate from an  overtone 
    chord. Enter `highest` to choose which tied chords are selected
    """

    chord_steps = find_note_vector_position_vectorized(chord)
    no_notes = len(chord)
    # generate all possible overtone chords
    all_chord_sets = np.ones((no_notes, m, no_notes))
    for i in range(no_notes):
        subharmonics = chord[i] * (1 / np.arange(1, m + 1))
        # filter values lower than human hearing
        subharmonics = np.where(subharmonics >= MIN_LOW, subharmonics, -1)
        harmonics = np.rint(chord / subharmonics[:,np.newaxis])
        chords = harmonics * subharmonics[:, np.newaxis]
        all_chord_sets[i] = chords
        
    # convert frequencies to nearest step of temperment set in `DIVISIONS`
    all_chord_steps = find_note_vector_position_vectorized(all_chord_sets)
    
    # right now we'll do pure summing, but you may want to consider
    # different methods, what if all notes were exact but one was way off.
    # another chord might have a bunch of tones that are close, but the distance
    # is a little bit more
    diff_from_target_chord = np.sum(np.abs(all_chord_steps - chord_steps), axis=2)
    
    ## find the chord with least number of steps and the lowest subharmonic
    # get the idx of the minimum number of steps of the subharmonics for each 
    # note of the input chord
    min_subharm_idx = np.argmin(diff_from_target_chord, axis=1)
    min_subharm_values = np.take_along_axis(diff_from_target_chord, 
    	min_subharm_idx[:, np.newaxis], axis=1).T[0]

    #find the minimum of every chord
    minimum_values_idx = np.argwhere(min_subharm_values == np.amin(
    	min_subharm_values)).T[0]

    row_idx, chord_idx = 0, 0
    if minimum_values_idx.size == 1: # if only 1 value exists
        row_idx = minimum_values_idx[0]
        chord_idx = min_subharm_idx[row_idx]
    else:
        # take value with lower subharmonic
        # tiebreak - both have same subharmonic value, choose lowest default
        if np.all(min_subharm_idx[minimum_values_idx]):
            row_idx, chord_idx = tiebreak_chord(chord, minimum_values_idx, tiebreak)
                
        row_idx = np.min(min_subharm_idx[minimum_values_idx])
        chord_idx = min_subharm_idx[row_idx]
    
    return all_chord_sets[row_idx, chord_idx]


import numpy as np
from collections import OrderedDict
from pygliss.utils import make_freq_vector, make_freq_to_steps_map, find_note_vector_position_vectorized
import time

NOTE_VECTOR = make_freq_vector()
MIN_LOW = 16.3515978313

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


##### Nearest FM Chords


# chord 1 - fm chord - A carrier, mod 110
# chord 2 - fm chord C carrier, mod 110
# chord 3 - modified chord 1 - diff distorted by 1 quarter tone
# chord 4 - modified chord 2 - both distorted

test_chords = np.array([
    [110.0, 220.0,  330.0],
    [151.6255653, 261.6255653,  371.6255653],
    [113.22324603, 220.0,  330.0],
    [146.83238396, 261.6255653,  380.83608684],
])


NOTE_VECTOR = make_freq_vector()
TRUNC_BEG = None
TRUNC_END = None
NOTE_VECTOR = NOTE_VECTOR[TRUNC_BEG:TRUNC_END]

MAX_SIDEBANDS = 20
freq_modulators = np.outer(np.arange(1, MAX_SIDEBANDS+1), NOTE_VECTOR)
SUM_TONES = np.zeros((len(NOTE_VECTOR), MAX_SIDEBANDS, len(NOTE_VECTOR)))
DIFF_TONES = np.zeros((len(NOTE_VECTOR), MAX_SIDEBANDS, len(NOTE_VECTOR)))
FM_CHORDS = np.zeros((len(NOTE_VECTOR), MAX_SIDEBANDS * 2, len(NOTE_VECTOR)))
FM_CHORDS_W_CARRIER = np.zeros((len(NOTE_VECTOR), ((MAX_SIDEBANDS * 2) + 1), len(NOTE_VECTOR)))

for i in range(len(NOTE_VECTOR)):
    SUM_TONES[i] = NOTE_VECTOR[i] + freq_modulators
    DIFF_TONES[i] = np.abs(NOTE_VECTOR[i] - freq_modulators)
    FM_CHORDS[i] = np.vstack((SUM_TONES[i], DIFF_TONES[i]))
    carrier = np.ones(len(NOTE_VECTOR)) * NOTE_VECTOR[i]
    FM_CHORDS_W_CARRIER[i] = np.vstack((FM_CHORDS[i], carrier))


FM_CHORDS_STEPS = find_note_vector_position_vectorized(FM_CHORDS, TRUNC_BEG, TRUNC_END)
FM_CHORDS_W_CARRIER_STEPS = find_note_vector_position_vectorized(FM_CHORDS_W_CARRIER, TRUNC_BEG, TRUNC_END)




def closet_fm_chord(chord):
    """
    find the closest FM chord to the input chord 
    when a tie is found give priority to the carrier of the found chord 
    that is closest to the lowest note of the input chord
    """
    
    chord_steps = np.sort(find_note_vector_position_vectorized(chord, TRUNC_BEG, TRUNC_END))
    solutions = []
    min_steps, best_i,best_j, best_carrier, best_mod = float("+inf"), 0, 0, 0.0, 0.0
    for i in range(len(NOTE_VECTOR)):
        cur_carrier = NOTE_VECTOR[i]
        for j in range(len(NOTE_VECTOR)):
            cur_mod = NOTE_VECTOR[j]
            current_fm_chord = FM_CHORDS[i,:,j]
            current_fm_chord_steps = find_note_vector_position_vectorized(current_fm_chord, TRUNC_BEG, TRUNC_END)
            #add carrier
            current_fm_chord_steps = np.append(current_fm_chord_steps, i)
            temp_min_steps = 0
            
            # find closet note in each chord
            for k in range(len(chord_steps)):
                # for each not of the input chord, find the closet
                # tone in the current FM chord
                min_note_dist = np.abs(current_fm_chord_steps - chord_steps[k]).min()
                temp_min_steps += min_note_dist

            if temp_min_steps < min_steps:
                min_steps = temp_min_steps
                best_i, best_j = i,j
                best_carrier = NOTE_VECTOR[i]
                best_mod = NOTE_VECTOR[j]
                solutions = [{
                    "min_steps":min_steps,
                    "carrier":best_carrier,
                    "modulator":best_mod,
                    "i":i,
                    "j":j
                }]
                
                
            # prioritize carrier closest to lowest note in chord
            elif temp_min_steps == min_steps:
                min_steps = temp_min_steps
                best_i, best_j = i,j
                best_carrier = NOTE_VECTOR[i]
                best_mod = NOTE_VECTOR[j]
                solutions.append({
                    "min_steps":min_steps,
                    "carrier":NOTE_VECTOR[i],
                    "modulator":cur_mod,
                    "i":i,
                    "j":j
                })
    return solutions


def verify_solutions(chord, solutions):
    chord = np.sort(chord)
    for idx, solution in enumerate(solutions):
        print(f"solution {idx+1}")
        print(solution)
        found_chord = FM_CHORDS[solution['i'],:,solution['j']]
        print(chord)
        print(found_chord, NOTE_VECTOR[solution['i']])
        print()
        chord_steps = find_note_vector_position_vectorized(chord, TRUNC_BEG, TRUNC_END)
        print(chord_steps)
        found_chord_steps = np.append(FM_CHORDS_STEPS[solution['i'],:,solution['j']], solution['i'])
        print(found_chord_steps)
        print()
        intersection = np.intersect1d(chord_steps, found_chord_steps)
        print(f"intersection:{intersection}")
        
        diff = len(chord) - len(intersection)
        if diff == solution['min_steps']:
            print(f"==> Solution verified <==")
        else:
            print("**** INCORRECT Solution ****")
        print("----\n")


def get_chord_distance(chord1, chord2):
    """
    Find Min distance between two chords (chord be stepwise or frequency)
    notes should be able to doublecount, thus why the vectorized implementation is more difficult
    
    """
    smaller, larger, dist = chord1, chord2, 0
    if len(chord1) > len(chord2):
        smaller = chord2
        larger = chord1
        
    for i in range(len(smaller)):
        dist += np.abs(larger - smaller[i]).min()
    return dist



def closet_fm_chord_vectorized(chord, sidebands=None):
    """
    find the closest FM chord to the input chord 
    when a tie is found give priority to the carrier of the found chord 
    that is closest to the lowest note of the input chord
    """
    fm_chords_steps_w_carrier = None
    if not sidebands:
        fm_chords_steps_w_carrier = FM_CHORDS_W_CARRIER_STEPS
    elif sidebands < MAX_SIDEBANDS:
        sum_tones = FM_CHORDS_W_CARRIER_STEPS[:,:sidebands,:]
        diff_tones = FM_CHORDS_W_CARRIER_STEPS[:,:sidebands,:]
        carrier = FM_CHORDS_W_CARRIER_STEPS[:,MAX_SIDEBANDS * 2:,:]
        temp = np.hstack((sum_tones, diff_tones))
        fm_chords_steps_w_carrier = np.hstack((temp, carrier))

    chord_steps = np.sort(find_note_vector_position_vectorized(chord, TRUNC_BEG, TRUNC_END))
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
                "carrier":NOTE_VECTOR[candidate[0]],
                "modulator":NOTE_VECTOR[candidate[1]],
                "i":candidate[0],
                "j":candidate[1]
            }]
        elif dist == min_steps:
            solutions.append({
                "min_steps":min_steps,
                "carrier":NOTE_VECTOR[candidate[0]],
                "modulator":NOTE_VECTOR[candidate[1]],
                "i":candidate[0],
                "j":candidate[1]
            })

    return sorted(solutions, key=lambda x: (x['carrier'], x['modulator']))


# # testing - nearest FM
# start = time.time()
# # closet_fm_chord(chords[:,10])
# test_idx = 0
# solutions = closet_fm_chord(test_chords[test_idx])
# print(len(solutions))
# verify_solutions(test_chords[test_idx], solutions)
# print(time.time() - start)



# start = time.time()
# # closet_fm_chord_vectorized(chords[:,10])
# # test_idx = 0
# solutions_v = closet_fm_chord_vectorized(test_chords[test_idx])
# print(len(solutions_v))
# verify_solutions(test_chords[test_idx], solutions_v)
# print(time.time() - start)
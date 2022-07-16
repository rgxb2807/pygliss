import numpy as np
from collections import OrderedDict
from pygliss.utils import make_freq_vector, make_freq_to_steps_map


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
    notes = NOTE_VECTOR[NOTE_VECTOR >= low]
    notes = notes[notes <= high]
    
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


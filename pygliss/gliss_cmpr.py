from pygliss.sequence import ChordSequence, make_chord_seq_from_note_seq
from pygliss.gliss import Gliss


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
    i_max, j_max = note_matrix.shape
    for i in range(i_max):
        glissandi = []
        for j in range(j_max-1):
            start = note_matrix[i,j]
            end = note_matrix[i,j+1]
            glissandi.append(Gliss(start, end)) 
        chord_sequences.append(GlissCmpr(glissandi))
    return chord_sequences














### delete after refactor

# # from pygliss.note import Note
# from pygliss.chord import Chord
# from pygliss.gliss import Gliss
# from pygliss.utils import lcm


# class Gliss_Cmpr:

#     def __init__(self, glissandi):
#         self.glissandi = list()
#         self.lcm = None
#         self.chord_arr = list()
#         self.glissandi_len = list()
#         self.chords = list()
#         self.chords_dups = list()

#         self.glissandi = glissandi
#         self.glissandi_len = set_gliss_len(self.glissandi, self.glissandi_len)
#         self.lcm = lcm(self.glissandi_len)
#         self = set_chords(self)
#         self.all_chords = set_dur(self.chords)
#         self.chords = unique(self.all_chords)


#     def __str__(self):
#         s = ''
#         for chord in self.chords:
#             s += str(chord) + " " + str(chord.dur) +"\n"
#         return s


# def set_gliss_len(glissandi, glissandi_len):
# 	for gliss in glissandi:
# 		glissandi_len.append(gliss.length)
# 	return glissandi_len


# def set_chords(comp):
# 	for i in range(0, int(comp.lcm)):
# 		note_list = list()
# 		for j in range(0, len(comp.glissandi_len)):
# 			step_len = int(comp.lcm) / comp.glissandi[j].length
# 			note_list.append(comp.glissandi[j].notes[i // int(step_len)])
# 		comp.chords.append(Chord(note_list))
# 	return comp


# def set_dur(chords):
# 	count = 1
# 	for i in range(0, len(chords)):
# 		if i != 0:
# 			if chords[i].notes == chords[i - 1].notes:
# 				count += 1
# 			else:
# 				for j in range(0, count):
# 					chords[i - j - 1].dur = count
# 				count = 1

# 	#set last chord
# 	for k in range((len(chords) - count), len(chords)):
# 		chords[k].dur = count

# 	return chords

# def unique(chords):
# 	unique = list()
# 	for chord in chords:
# 		if chord not in unique:
# 			unique.append(chord)
# 	return unique


# def gliss_cmpr_seq(note_matrix):
#     glissandi = list()
#     for i in range(0, len(note_matrix)):
#         gliss_list = list()
#         for j in range(0, len(note_matrix[i]) - 1):
#             temp = Gliss(note_matrix[i][j], note_matrix[i][j + 1])
#             gliss_list.append(temp)
#         glissandi.append(gliss_list)
    
#     Comp_List = list()
#     for i in range(0, len(note_matrix[0]) - 1):
#         if len(note_matrix) == 2:
#             temp = Gliss_Cmpr(
#                 glissandi[0][i],
#                 glissandi[1][i]
#             )
#             Comp_List.append(temp)
#         elif len(note_matrix) == 3:
#             temp = Gliss_Cmpr(
#                 glissandi[0][i],
#                 glissandi[1][i],
#                 glissandi[2][i]
#             )
#             Comp_List.append(temp)
#         elif len(note_matrix) == 4:
#             temp = Gliss_Cmpr(
#                 glissandi[0][i],
#                 glissandi[1][i],
#                 glissandi[2][i],
#                 glissandi[3][i]
#             )
#             Comp_List.append(temp)
#         elif len(note_matrix) == 5:
#             temp = Gliss_Cmpr(
#                 glissandi[0][i],
#                 glissandi[1][i],
#                 glissandi[2][i],
#                 glissandi[3][i],
#                 glissandi[4][i],
                
#             )
#             Comp_List.append(temp)
#         elif len(note_matrix) == 6:
#             temp = Gliss_Cmpr(
#                 glissandi[0][i],
#                 glissandi[1][i],
#                 glissandi[2][i],
#                 glissandi[3][i],
#                 glissandi[4][i],
#                 glissandi[5][i],
#             )
#             Comp_List.append(temp)
#         elif len(note_matrix) == 7:
#             temp = Gliss_Cmpr(
#                 glissandi[0][i],
#                 glissandi[1][i],
#                 glissandi[2][i],
#                 glissandi[3][i],
#                 glissandi[4][i],
#                 glissandi[5][i],
#                 glissandi[6][i]
#             )
#             Comp_List.append(temp)
#         elif len(note_matrix) == 8:
#             temp = Gliss_Cmpr(
#                 glissandi[0][i],
#                 glissandi[1][i],
#                 glissandi[2][i],
#                 glissandi[3][i],
#                 glissandi[4][i],
#                 glissandi[5][i],
#                 glissandi[6][i],
#                 glissandi[7][i]
#             )
#             Comp_List.append(temp)
#         elif len(note_matrix) == 9:
#             temp = Gliss_Cmpr(
#                 glissandi[0][i],
#                 glissandi[1][i],
#                 glissandi[2][i],
#                 glissandi[3][i],
#                 glissandi[4][i],
#                 glissandi[5][i],
#                 glissandi[6][i],
#                 glissandi[7][i],
#                 glissandi[8][i],  
#             )
#             Comp_List.append(temp)
#         elif len(note_matrix) == 10:
#             temp = Gliss_Cmpr(
#                 glissandi[0][i],
#                 glissandi[1][i],
#                 glissandi[2][i],
#                 glissandi[3][i],
#                 glissandi[4][i],
#                 glissandi[5][i],
#                 glissandi[6][i],
#                 glissandi[7][i],
#                 glissandi[8][i],
#                 glissandi[9][i],
#             )
#             Comp_List.append(temp)
#         else:
#             print("Comparisson Depth > 10 Not supported")
        
#     return Comp_List





from pygliss.note import *
from pygliss.chord import *
from pygliss.gliss import *


# TODO - Redo Constructors in pythonic way

# ASC_LIST2, ASC_DICT2 = keyboard_asc()
# DESC_LIST2, DESC_DICT2 = keyboard_desc()

class Gliss_Cmpr:

	def __init__(self, *args):
		self.glissandi = list()
		self.lcm = None
		self.chord_arr = list()
		self.glissandi_len = list()
		self.chords = list()
		self.chords_dups = list()

		self.glissandi = set_gliss(self.glissandi, *args)
		self.glissandi_len = set_gliss_len(self.glissandi, self.glissandi_len)
		self.lcm = lcm(self.glissandi_len)
		self = set_chords(self)
		self.chords = set_dur(self.chords)
		self.chords = unique(self.chords)


	def __str__(self):
		s = ''
		for chord in self.chords:
			s += str(chord) + " " + str(chord.dur) +"\n"
		return s


def set_gliss(glissandi, *args):
	for gliss in args:
		glissandi.append(gliss)
	return glissandi



def set_gliss_len(glissandi, glissandi_len):
	for gliss in glissandi:
		glissandi_len.append(gliss.length)
	return glissandi_len



def set_chords(comp):
	for i in range(0, int(comp.lcm)):
		note_list = list()
		for j in range(0, len(comp.glissandi_len)):
			step_len = int(comp.lcm) / comp.glissandi[j].length
			note_list.append(comp.glissandi[j].notes[i // int(step_len)])
		comp.chords.append(Chord(note_list))

	return comp


def set_dur(chords):
	count = 1
	for i in range(0, len(chords)):
		if i != 0:
			if chords[i].notes == chords[i - 1].notes:
				count += 1
			else:
				for j in range(0, count):
					chords[i - j - 1].dur = count
				count = 1

	#set last chord
	for k in range((len(chords) - count), len(chords)):
		chords[k].dur = count

	return chords

def unique(chords):
	unique = list()
	for chord in chords:
		if chord not in unique:
			unique.append(chord)

	return unique


#Euclid's Algorithm via StackOverFlow
def the_gcd(a, b):
	while (b > 0):
		temp = b
		b = a % b
		a = temp

	return a

def gcd(*args):
	result = args[0]
	for i in range(0, len(args)):
		result = the_gcd(result, args[i])

	return result

def the_lcm(a, b):
	return a * (b / gcd(a, b))

def lcm(num_list):
	result = num_list[0]
	for i in range(0, len(num_list)):
		result = the_lcm(result, num_list[i])

	return result



def gliss_cmpr_seq(note_matrix):
    glissandi = list()
    for i in range(0, len(note_matrix)):
        gliss_list = list()
        for j in range(0, len(note_matrix[i]) - 1):
            temp = Gliss(note_matrix[i][j], note_matrix[i][j + 1])
            gliss_list.append(temp)
        glissandi.append(gliss_list)
    
    Comp_List = list()
    for i in range(0, len(note_matrix[0]) - 1):
        if len(note_matrix) == 2:
            temp = Gliss_Cmpr(
                glissandi[0][i],
                glissandi[1][i]
            )
            Comp_List.append(temp)
        elif len(note_matrix) == 3:
            temp = Gliss_Cmpr(
                glissandi[0][i],
                glissandi[1][i],
                glissandi[2][i]
            )
            Comp_List.append(temp)
        elif len(note_matrix) == 4:
            temp = Gliss_Cmpr(
                glissandi[0][i],
                glissandi[1][i],
                glissandi[2][i],
                glissandi[3][i]
            )
            Comp_List.append(temp)
        elif len(note_matrix) == 5:
            temp = Gliss_Cmpr(
                glissandi[0][i],
                glissandi[1][i],
                glissandi[2][i],
                glissandi[3][i],
                glissandi[4][i],
                
            )
            Comp_List.append(temp)
        elif len(note_matrix) == 6:
            temp = Gliss_Cmpr(
                glissandi[0][i],
                glissandi[1][i],
                glissandi[2][i],
                glissandi[3][i],
                glissandi[4][i],
                glissandi[5][i],
            )
            Comp_List.append(temp)
        elif len(note_matrix) == 7:
            temp = Gliss_Cmpr(
                glissandi[0][i],
                glissandi[1][i],
                glissandi[2][i],
                glissandi[3][i],
                glissandi[4][i],
                glissandi[5][i],
                glissandi[6][i]
            )
            Comp_List.append(temp)
        elif len(note_matrix) == 8:
            temp = Gliss_Cmpr(
                glissandi[0][i],
                glissandi[1][i],
                glissandi[2][i],
                glissandi[3][i],
                glissandi[4][i],
                glissandi[5][i],
                glissandi[6][i],
                glissandi[7][i]
            )
            Comp_List.append(temp)
        elif len(note_matrix) == 9:
            temp = Gliss_Cmpr(
                glissandi[0][i],
                glissandi[1][i],
                glissandi[2][i],
                glissandi[3][i],
                glissandi[4][i],
                glissandi[5][i],
                glissandi[6][i],
                glissandi[7][i],
                glissandi[8][i],  
            )
            Comp_List.append(temp)
        elif len(note_matrix) == 10:
            temp = Gliss_Cmpr(
                glissandi[0][i],
                glissandi[1][i],
                glissandi[2][i],
                glissandi[3][i],
                glissandi[4][i],
                glissandi[5][i],
                glissandi[6][i],
                glissandi[7][i],
                glissandi[8][i],
                glissandi[9][i],
            )
            Comp_List.append(temp)
        else:
            print("Comparisson Depth > 10 Not supported")
        
    return Comp_List


# a = Gliss(ASC_DICT['C3'], ASC_DICT['C5'])
# b = Gliss(ASC_DICT['C4'], ASC_DICT['G5'])
# c = Gliss(ASC_DICT['E3'], ASC_DICT['G3'])

# x = Gliss_Cmpr(a, b, c)
#print(x)





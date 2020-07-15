import unittest
import pygliss
from music21 import pitch

class TestNoteMethods(unittest.TestCase):

    def test_distance(self):
        self.assertEqual(pygliss.note.Note('A', 4).distance(pygliss.note.Note('A', 5)), 24)

    def test_freq_to_note_1(self):
        self.assertEqual(pygliss.note.freq_to_note(440.0), pygliss.note.Note('A', 4))

    def test_freq_to_note_2(self):
        self.assertEqual(pygliss.note.freq_to_note(133.0), pygliss.note.Note('C', 3, "+"))


class TestChordMethods(unittest.TestCase):

	def test_chord_distance_1(self):
		C_maj = pygliss.chord.Chord([
			pygliss.note.Note('C', 4),
			pygliss.note.Note('E', 4),
			pygliss.note.Note('G', 4),
			])
		
		C_min = pygliss.chord.Chord([
			pygliss.note.Note('C', 4),
			pygliss.note.Note('E', 4, "b"),
			pygliss.note.Note('G', 4)
			])
		self.assertEqual(C_maj.distance(C_min), 2)

	def test_chord_distance_1(self):
		C_maj = pygliss.chord.Chord([
			pygliss.note.Note('C', 4),
			pygliss.note.Note('E', 4),
			pygliss.note.Note('G', 4),
			])
		
		C_min_7 = pygliss.chord.Chord([
			pygliss.note.Note('C', 4),
			pygliss.note.Note('E', 4, "b"),
			pygliss.note.Note('G', 4),
			pygliss.note.Note('B', 4, "b")
			])
		self.assertEqual(C_maj.distance(C_min_7), 2)

	def test_highest(self):
		C_maj = pygliss.chord.Chord([
			pygliss.note.Note('C', 4),
			pygliss.note.Note('E', 4),
			pygliss.note.Note('G', 4),
			])
		self.assertEqual(C_maj.highest_note(), pygliss.note.Note('G', 4))

	def test_lowest(self):
		C_maj = pygliss.chord.Chord([
			pygliss.note.Note('C', 4),
			pygliss.note.Note('E', 4),
			pygliss.note.Note('G', 4),
			])
		self.assertEqual(C_maj.lowest_note(), pygliss.note.Note('C', 4))

	def test_closest(self):
		C_maj = pygliss.chord.Chord([
			pygliss.note.Note('C', 4),
			pygliss.note.Note('E', 4),
			pygliss.note.Note('G', 4),
			])
		self.assertEqual(C_maj.closet_note(pygliss.note.Note('C', 4, "#")), pygliss.note.Note('C', 4))

	def test_ot_1(self):
		C_maj = pygliss.chord.Chord([
			pygliss.note.Note('C', 4),
			pygliss.note.Note('E', 4),
			pygliss.note.Note('G', 4),
			])
		ot = pygliss.chord.nearest_ot_chord(C_maj, 10)
		print()
		print("** Nearest Overtone Chord Test 1 **")
		print(f"found chord:{ot[0]}")
		print(f"fundamental:{ot[1]}")
		print(f"steps:{ot[2]}")
		print()
		self.assertEqual(C_maj,ot[0])
	
	def test_ot_2(self):
		C_wt_clus_ot = pygliss.chord.Chord([
			pygliss.note.Note('C', 4),
			pygliss.note.Note('D', 4),
			pygliss.note.Note('E', 4),
			pygliss.note.Note('F', 4, "+")
			])
		ot = pygliss.chord.nearest_ot_chord(C_wt_clus_ot, 10)
		print("** Nearest Overtone Chord Test 2 **")
		print(f"found chord:{ot[0]}")
		print(f"fundamental:{ot[1]}")
		print(f"steps:{ot[2]}")
		print()
		self.assertEqual(C_wt_clus_ot, ot[0])

	def test_ot_3(self):
		C_wt_clus = pygliss.chord.Chord([
			pygliss.note.Note('C', 4),
			pygliss.note.Note('D', 4),
			pygliss.note.Note('E', 4),
			pygliss.note.Note('F', 4, "#")
			])

		Nearest_ot = pygliss.chord.Chord([
			pygliss.note.Note('B', 3, "+"),
			pygliss.note.Note('D', 4),
			pygliss.note.Note('E', 4),
			pygliss.note.Note('F', 4, "#")
			])
		ot = pygliss.chord.nearest_ot_chord(C_wt_clus, 10)
		print("** Nearest Overtone Chord Test 3 **")
		print(f"found chord:{ot[0]}")
		print(f"fundamental:{ot[1]}")
		print(f"steps:{ot[2]}")
		print()
		self.assertEqual(Nearest_ot, ot[0])


class TestGlissMethods(unittest.TestCase):
	def test_gliss_1(self):
		g = pygliss.gliss.Gliss(
			pygliss.note.Note('C', 4),
			pygliss.note.Note('C', 5)
			)
		self.assertEqual(len(g.notes), 24)

	def test_gliss_2(self):
		g = pygliss.gliss.Gliss(
			pygliss.note.Note('C', 4),
			pygliss.note.Note('C', 5, "+")
			)
		self.assertEqual(g.length, 25)

	def test_gliss_3(self):
		g = pygliss.gliss.Gliss(
			pygliss.note.Note('C', 4),
			pygliss.note.Note('C', 5),
			resolution=2
			)
		self.assertEqual(g.length, 12)

	# add case to favor end note when resolution doesn't divide evenly
	# add case to favor start note

class TestGlissMethods(unittest.TestCase):
	def test_gliss_cmpr(self):
		g1 = pygliss.gliss.Gliss(
			pygliss.note.Note('C', 4),
			pygliss.note.Note('C', 5)
			)
		g2 = pygliss.gliss.Gliss(
			pygliss.note.Note('C', 4),
			pygliss.note.Note('C', 3)
			)
		g3 = pygliss.gliss.Gliss(
			pygliss.note.Note('C', 4),
			pygliss.note.Note('G', 4)
			)
		comp = pygliss.gliss_cmpr.Gliss_Cmpr([g1, g2, g3])
		self.assertEqual(comp.lcm, 168)

	def test_gliss_cmpr(self):
		g1 = pygliss.gliss.Gliss(
			pygliss.note.Note('C', 4),
			pygliss.note.Note('C', 5),
			resolution=3
			)
		g2 = pygliss.gliss.Gliss(
			pygliss.note.Note('C', 4),
			pygliss.note.Note('C', 3),
			resolution=2
			)
		g3 = pygliss.gliss.Gliss(
			pygliss.note.Note('C', 4),
			pygliss.note.Note('G', 4)
			)
		comp = pygliss.gliss_cmpr.Gliss_Cmpr([g1, g2, g3])
		self.assertEqual(comp.lcm, 168)


class TestMus21Methods(unittest.TestCase):
	

	def test_pitch_conversion_1(self):
		n = pygliss.note.Note('C', 4)
		self.assertEqual(pygliss.mus21.get_mus21_pitch(n), pitch.Pitch("C4"))

	def test_pitch_conversion_2(self):
		n = pygliss.note.Note('C', 4, "+")
		self.assertEqual(pygliss.mus21.get_mus21_pitch(n), pitch.Pitch("C4~"))

	def test_pitch_conversion_3(self):
		n = pygliss.note.Note('C', 4, "#")
		self.assertEqual(pygliss.mus21.get_mus21_pitch(n), pitch.Pitch("C4#"))

	def test_pitch_conversion_4(self):
		n = pygliss.note.Note('C', 4, "++")
		self.assertEqual(pygliss.mus21.get_mus21_pitch(n), pitch.Pitch("C4#~"))

	def test_pitch_conversion_5(self):
		n = pygliss.note.Note('D', 4, "-")
		self.assertEqual(pygliss.mus21.get_mus21_pitch(n), pitch.Pitch("D`4"))

	def test_pitch_conversion_6(self):
		n = pygliss.note.Note('D', 4, "b")
		self.assertEqual(pygliss.mus21.get_mus21_pitch(n), pitch.Pitch("D-4"))

	def test_pitch_conversion_7(self):
		n = pygliss.note.Note('D', 4, "--")
		self.assertEqual(
			pygliss.mus21.get_mus21_pitch(n), 
			pitch.Pitch(name="D", accidental="one-and-a-half-flat", octave="4"))




	def test_seq(self):
		self.assertEqual(pygliss.mus21.seq("test"), True)
		

	# def test_playbach(self):
	# 	self.assertEqual(pygliss.mus21.playbach(), True)



if __name__ == '__main__':
    unittest.main()
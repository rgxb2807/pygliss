import unittest
import pygliss
from music21 import pitch

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

if __name__ == '__main__':
    unittest.main()
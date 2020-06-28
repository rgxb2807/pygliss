import unittest
import pygliss

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





if __name__ == '__main__':
    unittest.main()
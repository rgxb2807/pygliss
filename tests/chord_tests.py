import unittest
import pygliss
from music21 import pitch
import numpy as np

class TestChordMethods(unittest.TestCase):

	def test_chord_distance_1(self):
		C_maj = pygliss.chord.Chord(np.array([
			pygliss.note.Note('C', 4).frequency(),
			pygliss.note.Note('E', 4).frequency(),
			pygliss.note.Note('G', 4).frequency()
			]))
		
		C_min = pygliss.chord.Chord(np.array([
			pygliss.note.Note('C', 4).frequency(),
			pygliss.note.Note('E', 4, "b").frequency(),
			pygliss.note.Note('G', 4).frequency()
			]))
		self.assertEqual(C_maj.distance(C_min), 2)

	def test_chord_distance_1(self):
		C_maj = pygliss.chord.Chord(np.array([
			pygliss.note.Note('C', 4).frequency(),
			pygliss.note.Note('E', 4).frequency(),
			pygliss.note.Note('G', 4).frequency()
			]))
		
		C_min_7 = pygliss.chord.Chord(np.array([
			pygliss.note.Note('C', 4).frequency(),
			pygliss.note.Note('E', 4, "b").frequency(),
			pygliss.note.Note('G', 4).frequency(),
			pygliss.note.Note('B', 4, "b").frequency()
			]))
		self.assertEqual(C_maj.distance(C_min_7), 2)

	def test_highest(self):
		C_maj = pygliss.chord.Chord(np.array([
			pygliss.note.Note('C', 4).frequency(),
			pygliss.note.Note('E', 4).frequency(),
			pygliss.note.Note('G', 4).frequency()
			]))
		self.assertEqual(C_maj.highest_note(), pygliss.note.Note('G', 4).frequency())

	def test_lowest(self):
		C_maj = pygliss.chord.Chord(np.array([
			pygliss.note.Note('C', 4).frequency(),
			pygliss.note.Note('E', 4).frequency(),
			pygliss.note.Note('G', 4).frequency()
			]))
		self.assertEqual(C_maj.lowest_note(), pygliss.note.Note('C', 4).frequency())

	def test_closest(self):
		C_maj = pygliss.chord.Chord(np.array([
			pygliss.note.Note('C', 4).frequency(),
			pygliss.note.Note('E', 4).frequency(),
			pygliss.note.Note('G', 4).frequency()
			]))
		self.assertEqual(C_maj.closest_note(pygliss.note.Note('C', 4, "#").frequency()), pygliss.note.Note('C', 4).frequency())


	def test_ot_1(self):
		C_maj = pygliss.chord.Chord(np.array([
			pygliss.note.Note('C', 4).frequency(),
			pygliss.note.Note('E', 4).frequency(),
			pygliss.note.Note('G', 4).frequency()
			]))
		ot = pygliss.chord.nearest_ot_chord(C_maj.notes, 10)

		self.assertEqual(C_maj.notes[0], pygliss.note.freq_to_note(ot.notes[0]).frequency())
		self.assertEqual(C_maj.notes[1], pygliss.note.freq_to_note(ot.notes[1]).frequency())
		self.assertEqual(C_maj.notes[2], pygliss.note.freq_to_note(ot.notes[2]).frequency())

		self.assertEqual(pygliss.note.Note('C', 2).frequency(), ot.fundamental_note().frequency())

	
	def test_ot_2(self):
		C_wt_clus_ot = pygliss.chord.Chord(np.array([
			pygliss.note.Note('C', 4).frequency(),
			pygliss.note.Note('D', 4).frequency(),
			pygliss.note.Note('E', 4).frequency(),
			pygliss.note.Note('F', 4, "+").frequency()
			]))
		ot = pygliss.chord.nearest_ot_chord(C_wt_clus_ot.notes, 10)

		self.assertEqual(C_wt_clus_ot.notes[0], pygliss.note.freq_to_note(ot.notes[0]).frequency())
		self.assertEqual(C_wt_clus_ot.notes[1], pygliss.note.freq_to_note(ot.notes[1]).frequency())
		self.assertEqual(C_wt_clus_ot.notes[2], pygliss.note.freq_to_note(ot.notes[2]).frequency())
		self.assertEqual(C_wt_clus_ot.notes[3], pygliss.note.freq_to_note(ot.notes[3]).frequency())

		self.assertEqual(pygliss.note.Note('C', 1).frequency(), ot.fundamental_note().frequency())


	def test_ot_3(self):
		C_wt_clus = pygliss.chord.Chord(np.array([
			pygliss.note.Note('C', 4).frequency(),
			pygliss.note.Note('D', 4).frequency(),
			pygliss.note.Note('E', 4).frequency(),
			pygliss.note.Note('F', 4, "#").frequency()
			]))

		Nearest_ot = pygliss.chord.Chord(np.array([
			pygliss.note.Note('B', 3, "+").frequency(),
			pygliss.note.Note('D', 4).frequency(),
			pygliss.note.Note('E', 4).frequency(),
			pygliss.note.Note('F', 4, "#").frequency()
			]))


		ot = pygliss.chord.nearest_ot_chord(C_wt_clus.notes, 10)

		self.assertEqual(Nearest_ot.notes[0], pygliss.note.freq_to_note(ot.notes[0]).frequency())
		self.assertEqual(Nearest_ot.notes[1], pygliss.note.freq_to_note(ot.notes[1]).frequency())
		self.assertEqual(Nearest_ot.notes[2], pygliss.note.freq_to_note(ot.notes[2]).frequency())
		self.assertEqual(Nearest_ot.notes[3], pygliss.note.freq_to_note(ot.notes[3]).frequency())

		self.assertEqual(pygliss.note.Note('D', 1).frequency(), ot.fundamental_note().frequency())


if __name__ == '__main__':
    unittest.main()
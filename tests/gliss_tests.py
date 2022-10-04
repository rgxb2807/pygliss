import unittest
import pygliss
import numpy as np
# from music21 import pitch

class TestGlissMethods(unittest.TestCase):
	def test_gliss_1(self):
		g = pygliss.gliss.Gliss(
			pygliss.note.Note('C', 4).frequency(),
			pygliss.note.Note('C', 5).frequency()
			)
		self.assertEqual(len(g.notes), 24)

	def test_gliss_2(self):
		g = pygliss.gliss.Gliss(
			pygliss.note.Note('C', 4).frequency(),
			pygliss.note.Note('C', 5, "+").frequency()
			)
		self.assertEqual(g.length, 25)

	def test_gliss_3(self):
		g = pygliss.gliss.Gliss(
			pygliss.note.Note('A', 3).frequency(),
			pygliss.note.Note('A', 4).frequency()
			)
		self.assertEqual(g.notes[0], 220.0)
		self.assertEqual(g.time_val[0], 0)
		self.assertEqual(g.durations[0], 1/24)

		self.assertTrue(np.isclose(g.notes[1], pygliss.note.Note('A', 3, "+").frequency()))
		self.assertTrue(np.isclose(g.notes[2], pygliss.note.Note('A', 3, "#").frequency()))
		self.assertTrue(np.isclose(g.notes[3], pygliss.note.Note('A', 3, "++").frequency()))
		self.assertTrue(np.isclose(g.notes[4], pygliss.note.Note('B', 3).frequency()))
		self.assertTrue(np.isclose(g.notes[5], pygliss.note.Note('B', 3, "+").frequency()))
		self.assertTrue(np.isclose(g.notes[6], pygliss.note.Note('C', 4).frequency()))
		self.assertTrue(np.isclose(g.notes[7], pygliss.note.Note('C', 4, "+").frequency()))
		self.assertTrue(np.isclose(g.notes[8], pygliss.note.Note('C', 4, "#").frequency()))


	def test_gliss_resolution(self):
		g = pygliss.gliss.Gliss(
			pygliss.note.Note('A', 3).frequency(),
			pygliss.note.Note('A', 4).frequency(),
			resolution=2
			)
		self.assertEqual(g.length, 12)

		self.assertEqual(g.notes[0], 220.0)
		self.assertEqual(g.time_val[0], 0)
		self.assertEqual(g.durations[0], 1/12)

		self.assertTrue(np.isclose(g.notes[1], pygliss.note.Note('A', 3, "#").frequency()))
		self.assertTrue(np.isclose(g.notes[2], pygliss.note.Note('B', 3).frequency()))
		self.assertTrue(np.isclose(g.notes[3], pygliss.note.Note('C', 4).frequency()))
		self.assertTrue(np.isclose(g.notes[4], pygliss.note.Note('C', 4, "#").frequency()))


	# add case to favor end note when resolution doesn't divide evenly
	# add case to favor start note
if __name__ == '__main__':
    unittest.main()
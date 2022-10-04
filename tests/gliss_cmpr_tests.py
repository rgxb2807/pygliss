import unittest
import pygliss
from music21 import pitch
import numpy as np

class TestGlissCmprMethods(unittest.TestCase):
	def test_gliss_cmpr_1(self):
		g1 = pygliss.gliss.Gliss(
			pygliss.note.Note('C', 4).frequency(),
			pygliss.note.Note('C', 5).frequency()
			)
		g2 = pygliss.gliss.Gliss(
			pygliss.note.Note('C', 4).frequency(),
			pygliss.note.Note('C', 3).frequency()
			)
		g3 = pygliss.gliss.Gliss(
			pygliss.note.Note('C', 4).frequency(),
			pygliss.note.Note('G', 4).frequency()
			)
		comp = pygliss.gliss_cmpr.GlissCmpr([g1, g2, g3])


		self.assertEqual(g1.length, 24)
		self.assertEqual(g2.length, 24)
		self.assertEqual(g3.length, 14)
		self.assertEqual(comp.length, 36)

		self.assertTrue(np.isclose(comp.chords[0][0], pygliss.note.Note('C', 4).frequency()))
		self.assertTrue(np.isclose(comp.chords[0][1], pygliss.note.Note('C', 4).frequency()))
		self.assertTrue(np.isclose(comp.chords[0][2], pygliss.note.Note('C', 4).frequency()))

		self.assertTrue(np.isclose(comp.chords[1][0], pygliss.note.Note('C', 4, "+").frequency()))
		self.assertTrue(np.isclose(comp.chords[1][1], pygliss.note.Note('B', 3, "+").frequency()))
		self.assertTrue(np.isclose(comp.chords[1][2], pygliss.note.Note('C', 4).frequency()))

		self.assertTrue(np.isclose(comp.chords[2][0], pygliss.note.Note('C', 4, "+").frequency()))
		self.assertTrue(np.isclose(comp.chords[2][1], pygliss.note.Note('B', 3, "+").frequency()))
		self.assertTrue(np.isclose(comp.chords[2][2], pygliss.note.Note('C', 4, "+").frequency()))

		self.assertTrue(np.isclose(comp.chords[3][0], pygliss.note.Note('C', 4, "#").frequency()))
		self.assertTrue(np.isclose(comp.chords[3][1], pygliss.note.Note('B', 3).frequency()))
		self.assertTrue(np.isclose(comp.chords[3][2], pygliss.note.Note('C', 4, "+").frequency()))

		self.assertTrue(np.isclose(comp.chords[4][0], pygliss.note.Note('C', 4, "++").frequency()))
		self.assertTrue(np.isclose(comp.chords[4][1], pygliss.note.Note('A', 3, "++").frequency()))
		self.assertTrue(np.isclose(comp.chords[4][2], pygliss.note.Note('C', 4, "+").frequency()))


	def test_gliss_cmpr_2(self):
		g1 = pygliss.gliss.Gliss(
			pygliss.note.Note('C', 4).frequency(),
			pygliss.note.Note('C', 5).frequency()
			)
		g2 = pygliss.gliss.Gliss(
			pygliss.note.Note('C', 4).frequency(),
			pygliss.note.Note('C', 3).frequency()
			)
		g3 = pygliss.gliss.Gliss(
			pygliss.note.Note('C', 4).frequency(),
			pygliss.note.Note('F', 4, "#").frequency()
			)
		comp = pygliss.gliss_cmpr.GlissCmpr([g1, g2, g3])


		self.assertEqual(g1.length, 24)
		self.assertEqual(g2.length, 24)
		self.assertEqual(g3.length, 12)
		self.assertEqual(comp.length, 24)


		self.assertTrue(np.isclose(comp.chords[0][0], pygliss.note.Note('C', 4).frequency()))
		self.assertTrue(np.isclose(comp.chords[0][1], pygliss.note.Note('C', 4).frequency()))
		self.assertTrue(np.isclose(comp.chords[0][2], pygliss.note.Note('C', 4).frequency()))

		self.assertTrue(np.isclose(comp.chords[1][0], pygliss.note.Note('C', 4, "+").frequency()))
		self.assertTrue(np.isclose(comp.chords[1][1], pygliss.note.Note('B', 3, "+").frequency()))
		self.assertTrue(np.isclose(comp.chords[1][2], pygliss.note.Note('C', 4).frequency()))

		self.assertTrue(np.isclose(comp.chords[2][0], pygliss.note.Note('C', 4, "#").frequency()))
		self.assertTrue(np.isclose(comp.chords[2][1], pygliss.note.Note('B', 3).frequency()))
		self.assertTrue(np.isclose(comp.chords[2][2], pygliss.note.Note('C', 4, "+").frequency()))

		self.assertTrue(np.isclose(comp.chords[3][0], pygliss.note.Note('C', 4, "++").frequency()))
		self.assertTrue(np.isclose(comp.chords[3][1], pygliss.note.Note('A', 3, "++").frequency()))
		self.assertTrue(np.isclose(comp.chords[3][2], pygliss.note.Note('C', 4, "+").frequency()))

		self.assertTrue(np.isclose(comp.chords[4][0], pygliss.note.Note('D', 4).frequency()))
		self.assertTrue(np.isclose(comp.chords[4][1], pygliss.note.Note('A', 3, "#").frequency()))
		self.assertTrue(np.isclose(comp.chords[4][2], pygliss.note.Note('C', 4, "#").frequency()))



	def test_gliss_cmpr_2(self):
		g1 = pygliss.gliss.Gliss(
			pygliss.note.Note('C', 4).frequency(),
			pygliss.note.Note('C', 5).frequency(),
			resolution=2
			)
		g2 = pygliss.gliss.Gliss(
			pygliss.note.Note('C', 4).frequency(),
			pygliss.note.Note('C', 3).frequency(),
			resolution=2
			)
		g3 = pygliss.gliss.Gliss(
			pygliss.note.Note('C', 4).frequency(),
			pygliss.note.Note('F', 4, "#").frequency(),
			resolution=2
			)
		comp = pygliss.gliss_cmpr.GlissCmpr([g1, g2, g3])

		self.assertEqual(g1.length, 12)
		self.assertEqual(g2.length, 12)
		self.assertEqual(g3.length, 6)
		self.assertEqual(comp.length, 12)

		self.assertTrue(np.isclose(comp.chords[0][0], pygliss.note.Note('C', 4).frequency()))
		self.assertTrue(np.isclose(comp.chords[0][1], pygliss.note.Note('C', 4).frequency()))
		self.assertTrue(np.isclose(comp.chords[0][2], pygliss.note.Note('C', 4).frequency()))

		self.assertTrue(np.isclose(comp.chords[1][0], pygliss.note.Note('C', 4, "#").frequency()))
		self.assertTrue(np.isclose(comp.chords[1][1], pygliss.note.Note('B', 3).frequency()))
		self.assertTrue(np.isclose(comp.chords[1][2], pygliss.note.Note('C', 4).frequency()))

		self.assertTrue(np.isclose(comp.chords[2][0], pygliss.note.Note('D', 4).frequency()))
		self.assertTrue(np.isclose(comp.chords[2][1], pygliss.note.Note('A', 3, "#").frequency()))
		self.assertTrue(np.isclose(comp.chords[2][2], pygliss.note.Note('C', 4, "#").frequency()))

		self.assertTrue(np.isclose(comp.chords[3][0], pygliss.note.Note('D', 4, "#").frequency()))
		self.assertTrue(np.isclose(comp.chords[3][1], pygliss.note.Note('A', 3).frequency()))
		self.assertTrue(np.isclose(comp.chords[3][2], pygliss.note.Note('C', 4, "#").frequency()))

		self.assertTrue(np.isclose(comp.chords[4][0], pygliss.note.Note('E', 4).frequency()))
		self.assertTrue(np.isclose(comp.chords[4][1], pygliss.note.Note('G', 3, "#").frequency()))
		self.assertTrue(np.isclose(comp.chords[4][2], pygliss.note.Note('D', 4).frequency()))

if __name__ == '__main__':
    unittest.main()
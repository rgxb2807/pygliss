import unittest
import pygliss
from music21 import pitch

class TestGlissCmprMethods(unittest.TestCase):
	def test_gliss_cmpr_1(self):
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

	def test_gliss_cmpr_2(self):
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

if __name__ == '__main__':
    unittest.main()
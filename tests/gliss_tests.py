import unittest
import pygliss
from music21 import pitch

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
if __name__ == '__main__':
    unittest.main()
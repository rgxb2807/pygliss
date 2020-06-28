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

	def test_chord(self):
		self.assertEqual(1,1)


if __name__ == '__main__':
    unittest.main()
import unittest
import pygliss
from music21 import pitch


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
			pitch.Pitch("D-`4"))

	def test_comp_stream(self):
		g1 = pygliss.gliss.Gliss(
			pygliss.note.Note('C', 5).frequency(),
			pygliss.note.Note('C', 4).frequency()
			)
		g2 = pygliss.gliss.Gliss(
			pygliss.note.Note('C', 4).frequency(),
			pygliss.note.Note('G', 4).frequency()
			)

		g3 = pygliss.gliss.Gliss(
			pygliss.note.Note('C', 3).frequency(),
			pygliss.note.Note('C', 5).frequency()
			)
		comp = pygliss.gliss_cmpr.GlissCmpr([g1, g2, g3])
		cs  = pygliss.mus21.comp_stream(comp)

		self.assertEqual(pygliss.mus21.write_stream(cs, "testing_file"), True)
		
	def test_gliss_ratio_1(self):
		g1 = pygliss.gliss.Gliss(
			pygliss.note.Note('C', 5).frequency(),
			pygliss.note.Note('C', 4).frequency()
			)
		g2 = pygliss.gliss.Gliss(
			pygliss.note.Note('C', 4).frequency(),
			pygliss.note.Note('G', 4).frequency()
			)

		g3 = pygliss.gliss.Gliss(
			pygliss.note.Note('C', 3).frequency(),
			pygliss.note.Note('C', 5).frequency()
			)

		s  = pygliss.mus21.gliss_ratio([g1, g2, g3])
		# pygliss.mus21.play_stream(s)

		self.assertEqual(pygliss.mus21.write_stream(s, "testing_file_ratio_1"), True)

	def test_gliss_ratio_2(self):
		g1 = pygliss.gliss.Gliss(
			pygliss.note.Note('C', 5).frequency(),
			pygliss.note.Note('C', 4).frequency()
			)
		g2 = pygliss.gliss.Gliss(
			pygliss.note.Note('C', 4).frequency(),
			pygliss.note.Note('D', 4).frequency()
			)

		g3 = pygliss.gliss.Gliss(
			pygliss.note.Note('C', 3).frequency(),
			pygliss.note.Note('C', 5).frequency()
			)

		s  = pygliss.mus21.gliss_ratio([g1, g2, g3])
		pygliss.mus21.play_stream(s)

		self.assertEqual(pygliss.mus21.write_stream(s, "testing_file_ratio_2"), True)

	def test_gliss_ratio_3(self):
		g1 = pygliss.gliss.Gliss(
			pygliss.note.Note('C', 5).frequency(),
			pygliss.note.Note('C', 4).frequency()
			)
		g2 = pygliss.gliss.Gliss(
			pygliss.note.Note('C', 4).frequency(),
			pygliss.note.Note('D', 4, "+").frequency()
			)

		g3 = pygliss.gliss.Gliss(
			pygliss.note.Note('C', 3).frequency(),
			pygliss.note.Note('C', 5).frequency()
			)

		s  = pygliss.mus21.gliss_ratio([g1, g2, g3])
		pygliss.mus21.play_stream(s)
		pygliss.mus21.play_stream(s)

		self.assertEqual(pygliss.mus21.write_stream(s, "testing_file_ratio_3"), True)

	def test_gliss_ratio_4(self):
		g1 = pygliss.gliss.Gliss(
			pygliss.note.Note('C', 5).frequency(),
			pygliss.note.Note('E', 3).frequency()
			)
		g2 = pygliss.gliss.Gliss(
			pygliss.note.Note('C', 4).frequency(),
			pygliss.note.Note('G', 4).frequency()
			)

		g3 = pygliss.gliss.Gliss(
			pygliss.note.Note('C', 3).frequency(),
			pygliss.note.Note('C', 5).frequency()
			)

		# s  = pygliss.mus21.gliss_ratio([g1, g2, g3], length=0.142857)
		s  = pygliss.mus21.gliss_ratio([g1, g2, g3], length=0.2, bpm=60)
		pygliss.mus21.write_stream(s, "testing_file_ratio_4")
		# pygliss.mus21.play_stream(s)


		self.assertEqual(True, True)


	def test_gliss_ratio_5(self):
		g1 = pygliss.gliss.Gliss(
			pygliss.note.Note('C', 5).frequency(),
			pygliss.note.Note('E', 3).frequency()
			)
		g2 = pygliss.gliss.Gliss(
			pygliss.note.Note('C', 4).frequency(),
			pygliss.note.Note('G', 4).frequency()
			)

		g3 = pygliss.gliss.Gliss(
			pygliss.note.Note('C', 3).frequency(),
			pygliss.note.Note('C', 5).frequency()
			)

		# s  = pygliss.mus21.gliss_ratio([g1, g2, g3], length=0.142857)
		s  = pygliss.mus21.gliss_ratio([g1, g2, g3], length=0.2, bpm=60)
		pygliss.mus21.write_stream(s, "testing_file_ratio_5")
		pygliss.mus21.play_stream(s)


		self.assertEqual(True, True)

	# def test_playbach(self):
	# 	self.assertEqual(pygliss.mus21.playbach(), True)
	def test_dur(self):
		self.assertEqual(pygliss.mus21.test_note(), True)


if __name__ == '__main__':
    unittest.main()
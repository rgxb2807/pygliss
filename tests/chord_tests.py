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

		nearest_ot = pygliss.chord.Chord(np.array([
			pygliss.note.Note('B', 3, "+").frequency(),
			pygliss.note.Note('D', 4).frequency(),
			pygliss.note.Note('E', 4).frequency(),
			pygliss.note.Note('F', 4, "#").frequency()
			]))


		ot = pygliss.chord.nearest_ot_chord(C_wt_clus.notes, 12)
	

		# self.assertEqual(nearest_ot.notes[0], pygliss.note.freq_to_note(ot.notes[0]).frequency())
		self.assertEqual(nearest_ot.notes[1], pygliss.note.freq_to_note(ot.notes[1]).frequency())
		self.assertEqual(nearest_ot.notes[2], pygliss.note.freq_to_note(ot.notes[2]).frequency())
		self.assertEqual(nearest_ot.notes[3], pygliss.note.freq_to_note(ot.notes[3]).frequency())

		self.assertEqual(pygliss.note.Note('D', 1).frequency(), ot.fundamental_note().frequency())

	def test_fm_1(self):
		
		note_1 = pygliss.note.freq_to_note(110.0)
		note_2 = pygliss.note.freq_to_note(220.0)
		note_3 = pygliss.note.freq_to_note(330.0)
		carrier = 880.0
		modulator = 110.0

		test_chord = pygliss.chord.Chord(np.array([note_1.frequency(), note_2.frequency(),
			note_3.frequency()]))
		
		fm_test_chord = pygliss.chord.FMChord(test_chord.notes, carrier, modulator)
		diff_tones = [abs(carrier - i * modulator) for i in range(1, 31)]
		sum_tones = [carrier + i * modulator for i in range(1, 31)]
		self.assertTrue(np.array_equiv(fm_test_chord.diff_tones(), diff_tones))
		self.assertTrue(np.array_equiv(fm_test_chord.sum_tones(), sum_tones))

		fm_solutions = pygliss.chord.nearest_fm_chord(test_chord.notes)
		self.assertEqual(fm_solutions[3]['fm_chord'].carrier, carrier)
		self.assertEqual(fm_solutions[3]['fm_chord'].modulator, modulator)
		self.assertEqual(fm_solutions[3]['roughness'], fm_test_chord.roughness())




	def test_fm_2(self):

		note_1 = pygliss.note.freq_to_note(151.6255653)
		note_2 = pygliss.note.freq_to_note(261.6255653)
		note_3 = pygliss.note.freq_to_note(371.6255653)
		carrier = 880.0
		modulator = 103.82617439498628

		test_chord = pygliss.chord.Chord(np.array([note_1.frequency(), note_2.frequency(), 
			note_3.frequency()]))
		
		fm_test_chord = pygliss.chord.FMChord(test_chord.notes, carrier, modulator)
		diff_tones = [abs(carrier - i * modulator) for i in range(1, 31)]
		sum_tones = [carrier + i * modulator for i in range(1, 31)]
		self.assertTrue(np.array_equiv(fm_test_chord.diff_tones(), diff_tones))
		self.assertTrue(np.array_equiv(fm_test_chord.sum_tones(), sum_tones))

		fm_solutions = pygliss.chord.nearest_fm_chord(test_chord.notes)
		self.assertEqual(fm_solutions[7]['fm_chord'].carrier, carrier)
		self.assertEqual(fm_solutions[7]['fm_chord'].modulator, modulator)
		self.assertEqual(fm_solutions[7]['roughness'], fm_test_chord.roughness())

	def test_fm_3(self):

		note_1 = pygliss.note.freq_to_note(113.22324603)
		note_2 = pygliss.note.freq_to_note(220.0)
		note_3 = pygliss.note.freq_to_note(330.0)
		carrier = 987.7666025122483
		modulator = 110.0

		test_chord = pygliss.chord.Chord(np.array([note_1.frequency(), note_2.frequency(),
			note_3.frequency()]))
		
		fm_test_chord = pygliss.chord.FMChord(test_chord.notes, carrier, modulator)
		diff_tones = [abs(carrier - i * modulator) for i in range(1, 31)]
		sum_tones = [carrier + i * modulator for i in range(1, 31)]
		self.assertTrue(np.array_equiv(fm_test_chord.diff_tones(), diff_tones))
		self.assertTrue(np.array_equiv(fm_test_chord.sum_tones(), sum_tones))

		fm_solutions = pygliss.chord.nearest_fm_chord(test_chord.notes)
		self.assertEqual(fm_solutions[2]['fm_chord'].carrier, carrier)
		self.assertEqual(fm_solutions[2]['fm_chord'].modulator, modulator)
		self.assertEqual(fm_solutions[2]['roughness'], fm_test_chord.roughness())

	def test_fm_4(self):

		note_1 = pygliss.note.freq_to_note(146.83238396)
		note_2 = pygliss.note.freq_to_note(261.6255653)
		note_3 = pygliss.note.freq_to_note(380.83608684)
		carrier = 1661.2187903197805
		modulator = 116.5409403795224

		test_chord = pygliss.chord.Chord(np.array([note_1.frequency(), note_2.frequency(), note_3.frequency()]))
		
		fm_test_chord = pygliss.chord.FMChord(test_chord.notes, carrier, modulator)
		diff_tones = [abs(carrier - i * modulator) for i in range(1, 31)]
		sum_tones = [carrier + i * modulator for i in range(1, 31)]
		for val in zip(diff_tones, fm_test_chord.diff_tones()):
			self.assertTrue(np.isclose(val[0], val[1]))

		for val in zip(sum_tones, fm_test_chord.sum_tones()):
			self.assertTrue(np.isclose(val[0], val[1]))

		fm_solutions = pygliss.chord.nearest_fm_chord(test_chord.notes)
		self.assertEqual(fm_solutions[1]['fm_chord'].carrier, carrier)
		# self.assertEqual(fm_solutions[1]['fm_chord'].modulator, modulator)
		self.assertTrue(np.isclose(fm_solutions[1]['fm_chord'].modulator, modulator))
		self.assertEqual(fm_solutions[1]['roughness'], fm_test_chord.roughness())

	def test_fm_5(self):

		note_1 = pygliss.note.freq_to_note(3737.213936077532)
		note_2 = pygliss.note.freq_to_note(3407.5863791646616)
		note_3 = pygliss.note.freq_to_note(3077.958822251792)
		carrier = 4066.8414929904015
		modulator = 329.6275569128699


		test_chord = pygliss.chord.Chord(np.array([note_1.frequency(), note_2.frequency(),
			note_3.frequency()]))

		fm_test_chord = pygliss.chord.FMChord(test_chord.notes, carrier, modulator)
		diff_tones = [abs(carrier - i * modulator) for i in range(1, 31)]
		sum_tones = [carrier + i * modulator for i in range(1, 31)]
		self.assertTrue(np.array_equiv(fm_test_chord.diff_tones(), diff_tones))
		self.assertTrue(np.array_equiv(fm_test_chord.sum_tones(), sum_tones))

		fm_solutions = pygliss.chord.nearest_fm_chord(test_chord.notes)
		self.assertEqual(fm_solutions[31]['fm_chord'].carrier, carrier)
		self.assertEqual(fm_solutions[31]['fm_chord'].modulator, modulator)
		self.assertEqual(fm_solutions[31]['roughness'], fm_test_chord.roughness())






if __name__ == '__main__':
    unittest.main()
import unittest
import pygliss
from music21 import pitch
import numpy as np

class TestSequenceMethods(unittest.TestCase):
	def test_note_seq_offset(self):
		notes = np.array([
			pygliss.note.Note('C', 4).frequency(),
			pygliss.note.Note('D', 4).frequency(),
			pygliss.note.Note('E', 4).frequency(),
			pygliss.note.Note('F', 4).frequency(),
			pygliss.note.Note('G', 4).frequency(),
			pygliss.note.Note('A', 4).frequency(),
			pygliss.note.Note('B', 4).frequency(),
			pygliss.note.Note('C', 5).frequency(),
			])
		durations = np.ones(len(notes)) / len(notes)
		time_val = np.arange(len(notes)) / len(notes)
		note_seq = pygliss.sequence.NoteSequence(notes, time_val, durations)
		note_seq.add_offset(10)
		assert note_seq.notes[0] == 0.0
		assert note_seq.durations[0] == 10
		assert note_seq.time_val[0] == 0.0
		assert note_seq.time_val[1] == 10.0


	def test_note_seq_add_silence(self):
		notes = np.array([
			pygliss.note.Note('C', 4).frequency(),
			pygliss.note.Note('D', 4).frequency(),
			pygliss.note.Note('E', 4).frequency(),
			pygliss.note.Note('F', 4).frequency(),
			pygliss.note.Note('G', 4).frequency(),
			pygliss.note.Note('A', 4).frequency(),
			pygliss.note.Note('B', 4).frequency(),
			pygliss.note.Note('C', 5).frequency(),
			])
		durations = np.ones(len(notes)) / len(notes)
		time_val = np.arange(len(notes)) / len(notes)
		note_seq = pygliss.sequence.NoteSequence(notes, time_val, durations)
		note_seq.add_silence(10)
		assert note_seq.notes[-1] == 0.0
		assert note_seq.durations[-1] == 10.0
		assert note_seq.time_val[-1] == 1.0

	def test_note_seq_add_offset_at_idx(self):
		notes = np.array([
			pygliss.note.Note('C', 4).frequency(),
			pygliss.note.Note('D', 4).frequency(),
			pygliss.note.Note('E', 4).frequency(),
			pygliss.note.Note('F', 4).frequency(),
			pygliss.note.Note('G', 4).frequency(),
			pygliss.note.Note('A', 4).frequency(),
			pygliss.note.Note('B', 4).frequency(),
			pygliss.note.Note('C', 5).frequency(),
			])
		durations = np.ones(len(notes)) / len(notes)
		time_val = np.arange(len(notes)) / len(notes)
		note_seq = pygliss.sequence.NoteSequence(notes, time_val, durations)
		note_seq.add_offset_at_position(10, 3)
		assert note_seq.notes[3] == 0.0
		assert note_seq.durations[3] == 10
		assert note_seq.time_val[3] == 0.375
		assert note_seq.time_val[4] == 10.375

	def test_note_seq_remove_offset_at_idx(self):
		notes = np.array([
			pygliss.note.Note('C', 4).frequency(),
			pygliss.note.Note('D', 4).frequency(),
			pygliss.note.Note('E', 4).frequency(),
			pygliss.note.Note('F', 4).frequency(),
			pygliss.note.Note('G', 4).frequency(),
			pygliss.note.Note('A', 4).frequency(),
			pygliss.note.Note('B', 4).frequency(),
			pygliss.note.Note('C', 5).frequency(),
			])
		durations = np.ones(len(notes)) / len(notes)
		time_val = np.arange(len(notes)) / len(notes)
		note_seq = pygliss.sequence.NoteSequence(notes, time_val, durations)
		note_seq.add_offset_at_position(10, 3)
		assert note_seq.notes[3] == 0.0
		assert note_seq.durations[3] == 10
		assert note_seq.time_val[3] == 0.375
		assert note_seq.time_val[4] == 10.375

		note_seq.remove_offset_at_position(3)
		assert note_seq.notes[3] != 0.0
		assert note_seq.durations[3] == 0.125
		assert note_seq.time_val[3] == 0.375
		assert note_seq.time_val[4] == 0.5



	def test_chord_seq_offset(self):
		chords = np.array([
				[pygliss.note.Note('C', 4).frequency(),
				pygliss.note.Note('E', 4).frequency(),
				pygliss.note.Note('G', 4).frequency()],
				[pygliss.note.Note('C', 4).frequency(),
				pygliss.note.Note('E', 4).frequency(),
				pygliss.note.Note('G', 4).frequency()],
				[pygliss.note.Note('C', 4).frequency(),
				pygliss.note.Note('E', 4).frequency(),
				pygliss.note.Note('G', 4).frequency()],
				[pygliss.note.Note('C', 4).frequency(),
				pygliss.note.Note('E', 4).frequency(),
				pygliss.note.Note('G', 4).frequency()]
			])
		durations = np.ones(len(chords)) / len(chords)
		time_val = np.arange(len(chords)) / len(chords)
		
		chords_seq = pygliss.sequence.ChordSequence(chords, time_val, durations)
		chords_seq.add_offset(10)
		assert np.all(chords_seq.chords[0]) == 0.0
		assert chords_seq.durations[0] == 10
		assert chords_seq.time_val[0] == 0.0
		assert chords_seq.time_val[1] == 10.0

	def test_chord_seq_add_silence(self):
		chords = np.array([
				[pygliss.note.Note('C', 4).frequency(),
				pygliss.note.Note('E', 4).frequency(),
				pygliss.note.Note('G', 4).frequency()],
				[pygliss.note.Note('C', 4).frequency(),
				pygliss.note.Note('E', 4).frequency(),
				pygliss.note.Note('G', 4).frequency()],
				[pygliss.note.Note('C', 4).frequency(),
				pygliss.note.Note('E', 4).frequency(),
				pygliss.note.Note('G', 4).frequency()],
				[pygliss.note.Note('C', 4).frequency(),
				pygliss.note.Note('E', 4).frequency(),
				pygliss.note.Note('G', 4).frequency()]
			])
		durations = np.ones(len(chords)) / len(chords)
		time_val = np.arange(len(chords)) / len(chords)
		
		chords_seq = pygliss.sequence.ChordSequence(chords, time_val, durations)
		chords_seq.add_silence(10)
		assert np.all(chords_seq.chords[-1]) == 0.0
		assert chords_seq.durations[-1] == 10.0
		assert chords_seq.time_val[-1] == 1.0

	def test_chord_seq_add_offset_at_idx(self):
		chords = np.array([
				[pygliss.note.Note('C', 4).frequency(),
				pygliss.note.Note('E', 4).frequency(),
				pygliss.note.Note('G', 4).frequency()],
				[pygliss.note.Note('C', 4).frequency(),
				pygliss.note.Note('E', 4).frequency(),
				pygliss.note.Note('G', 4).frequency()],
				[pygliss.note.Note('C', 4).frequency(),
				pygliss.note.Note('E', 4).frequency(),
				pygliss.note.Note('G', 4).frequency()],
				[pygliss.note.Note('C', 4).frequency(),
				pygliss.note.Note('E', 4).frequency(),
				pygliss.note.Note('G', 4).frequency()]
			])
		durations = np.ones(len(chords)) / len(chords)
		time_val = np.arange(len(chords)) / len(chords)
		
		chords_seq = pygliss.sequence.ChordSequence(chords, time_val, durations)
		chords_seq.add_offset_at_position(10, 2)
		assert np.all(chords_seq.chords[2]) == 0.0
		assert chords_seq.durations[2] == 10
		assert chords_seq.time_val[2] == 0.5
		assert chords_seq.time_val[3] == 10.5

	def test_chord_seq_remove_offset_at_idx(self):
		chords = np.array([
				[pygliss.note.Note('C', 4).frequency(),
				pygliss.note.Note('E', 4).frequency(),
				pygliss.note.Note('G', 4).frequency()],
				[pygliss.note.Note('C', 4).frequency(),
				pygliss.note.Note('E', 4).frequency(),
				pygliss.note.Note('G', 4).frequency()],
				[pygliss.note.Note('C', 4).frequency(),
				pygliss.note.Note('E', 4).frequency(),
				pygliss.note.Note('G', 4).frequency()],
				[pygliss.note.Note('C', 4).frequency(),
				pygliss.note.Note('E', 4).frequency(),
				pygliss.note.Note('G', 4).frequency()]
			])
		durations = np.ones(len(chords)) / len(chords)
		time_val = np.arange(len(chords)) / len(chords)
		
		chords_seq = pygliss.sequence.ChordSequence(chords, time_val, durations)
		chords_seq.add_offset_at_position(10, 2)
		assert np.all(chords_seq.chords[2]) == 0.0
		assert chords_seq.durations[2] == 10
		assert chords_seq.time_val[2] == 0.5
		assert chords_seq.time_val[3] == 10.5

		chords_seq.remove_offset_at_position(2)
		assert np.all(chords_seq.chords[2]) != 0.0
		assert chords_seq.durations[2] == 0.25
		assert chords_seq.time_val[2] == 0.5
		assert chords_seq.time_val[3] == 0.75

	def test_get_tempo_vals_1(self):
		start_bpm = 60
		beats = 4
		test_time_vals = np.array([0.0, 1.0, 2.0, 3.0])
		test_durations = np.array([1.0, 1.0, 1.0, 1.0])
		time_val, durations = pygliss.sequence.get_tempo_vals(start_bpm, beats)
		assert np.array_equal(test_time_vals, time_val)
		assert np.array_equal(test_durations, durations)


	def test_get_tempo_vals_2(self):
		# 60 | 70 | 80 | 90 | 100 | 110
		start_bpm = 60
		end_bpm = 120
		beats = 6

		test_time_vals = np.zeros(beats)
		test_durations = np.array([60 / val for val in [60.0, 70.0, 80.0, 90.0, 100.0, 110.0]])
		for i, val in enumerate(test_durations):
			if i > 0:
				test_time_vals[i] = test_time_vals[i-1] + test_durations[i-1]

		time_val, durations = pygliss.sequence.get_tempo_vals(start_bpm, beats, end_bpm=end_bpm)
		assert np.array_equal(test_time_vals, time_val)
		assert np.array_equal(test_durations, durations)

	def test_transform_tempo_1(self):
		# 4 beats @ 60bpm
		source_time_val = np.array([0.0, 1.0, 2.0, 3.0])
		source_durations = np.array([1.0, 1.0, 1.0, 1.0])

		# 8 beats @ 120bpm
		target_beat_time_val = np.array([0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5])
		target_beat_durations = np.array([0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5])

		time_val, durations = pygliss.sequence.transform_tempo(source_durations, 
			target_beat_durations)

		# transform_tempo
		test_time_val = np.array([0.0, 1.0, 2.0, 3.0])
		test_durations = np.array([1.0, 1.0, 1.0, 1.0])
		assert np.array_equal(time_val, test_time_val)
		assert np.array_equal(durations, test_durations)

	
	def test_transform_tempo_2(self):
		# no beats octave gliss
		source_time_val = np.array([i / 12 for i in range(12)])
		source_durations = np.array([1/12]*12)

		# 4 beats @ 60bpm
		target_beat_time_val = np.array([0.0, 1.0, 2.0, 3.0])
		target_beat_durations = np.array([1.0, 1.0, 1.0, 1.0])


		# time_val, durations = pygliss.sequence.transform_tempo(source_durations, source_time_val, 
		# 	target_beat_durations, target_beat_time_val)
		time_val, durations = pygliss.sequence.transform_tempo(source_durations, 
			target_beat_durations)

		# transform_tempo
		test_time_val = source_time_val * 4
		test_durations = source_durations * 4

		assert np.allclose(time_val, test_time_val)
		assert np.allclose(durations, test_durations)

	def test_transform_tempo_3(self):
		# no beats octave gliss
		source_time_val = np.array([i / 12 for i in range(12)])
		source_durations = np.array([1/12]*12)

		# 6 beats @ 60bpm -> 120bpm
		target_beat_durations = np.array([60 / val for val in [60.0, 70.0, 80.0, 90.0, 100.0, 110.0]])
		target_beat_time_val = np.zeros(len(target_beat_durations))
		for i in range(len(target_beat_durations)):
			if i > 0:
				target_beat_time_val[i] = target_beat_time_val[i-1] + target_beat_durations[i-1]


		# time_val, durations = pygliss.sequence.transform_tempo(source_durations, source_time_val, 
		# 	target_beat_durations, target_beat_time_val)

		time_val, durations = pygliss.sequence.transform_tempo(source_durations, 
			target_beat_durations)

		# transform_tempo
		test_durations = []
		for i in range(len(target_beat_durations)):
			test_durations.append(target_beat_durations[i]/2)
			test_durations.append(target_beat_durations[i]/2)
		
		test_durations = np.array(test_durations)
		test_time_val = np.zeros(len(test_durations))
		for i in range(len(test_durations)):
			if i > 0:
				test_time_val[i] = test_time_val[i-1] + test_durations[i-1]

		assert np.allclose(time_val, test_time_val)
		assert np.allclose(durations, test_durations)

	def test_transform_tempo_4(self):
		# no beats octave gliss
		gliss_len = 18
		source_time_val = np.array([i / gliss_len for i in range(gliss_len)])
		source_durations = np.array([1/gliss_len]*gliss_len)

		# 6 beats @ 60bpm -> 120bpm
		target_beat_durations = np.array([60 / val for val in [60.0, 70.0, 80.0, 90.0, 100.0, 110.0]])
		target_beat_time_val = np.zeros(len(target_beat_durations))
		for i in range(len(target_beat_durations)):
			if i > 0:
				target_beat_time_val[i] = target_beat_time_val[i-1] + target_beat_durations[i-1]

		time_val, durations = pygliss.sequence.transform_tempo(source_durations, 
			target_beat_durations)

		# transform_tempo
		target_lcm = 42 # lcm(18, 6) = 18
		test_durations = []
		for i in range(len(target_beat_durations)):
			test_durations.append(target_beat_durations[i]/3)
			test_durations.append(target_beat_durations[i]/3)
			test_durations.append(target_beat_durations[i]/3)
		
		test_durations = np.array(test_durations)
		test_time_val = np.zeros(len(test_durations))
		for i in range(len(test_durations)):
			if i > 0:
				test_time_val[i] = test_time_val[i-1] + test_durations[i-1]


		assert np.allclose(time_val, test_time_val)
		assert np.allclose(durations, test_durations)

	def test_transform_tempo_5(self):
		# no beats octave gliss
		gliss_len = 14
		source_time_val = np.array([i / gliss_len for i in range(gliss_len)])
		source_durations = np.array([1/gliss_len]*gliss_len)

		# 6 beats @ 60bpm -> 120bpm
		target_beat_durations = np.array([60 / val for val in [60.0, 70.0, 80.0, 90.0, 100.0, 110.0]])
		target_beat_time_val = np.zeros(len(target_beat_durations))
		for i in range(len(target_beat_durations)):
			if i > 0:
				target_beat_time_val[i] = target_beat_time_val[i-1] + target_beat_durations[i-1]

		time_val, durations = pygliss.sequence.transform_tempo(source_durations, 
			target_beat_durations)

		# transform_tempo
		# lcm(14, 6) = 42, 42 / 14 = 3, 42 / 6 = 7
		test_durations = [
			(target_beat_durations[0] / 7) * 3,
			(target_beat_durations[0] / 7) * 3,
			(target_beat_durations[0] / 7) + (target_beat_durations[1] / 7) * 2,
			(target_beat_durations[1] / 7) * 3,
			(target_beat_durations[1] / 7) * 2 + (target_beat_durations[2] / 7),
			(target_beat_durations[2] / 7) * 3,
			(target_beat_durations[2] / 7) * 3,
			(target_beat_durations[3] / 7) * 3,
			(target_beat_durations[3] / 7) * 3,
			(target_beat_durations[3] / 7) + (target_beat_durations[4] / 7) * 2,
			(target_beat_durations[4] / 7) * 3,
			(target_beat_durations[4] / 7) * 2 + (target_beat_durations[5] / 7),
			(target_beat_durations[5] / 7) * 3,
			(target_beat_durations[5] / 7) * 3
		]
		
		test_durations = np.array(test_durations)
		test_time_val = np.zeros(len(test_durations))
		for i in range(len(test_durations)):
			if i > 0:
				test_time_val[i] = test_time_val[i-1] + test_durations[i-1]

		assert np.allclose(time_val, test_time_val)
		assert np.allclose(durations, test_durations)

	def test_concat_seq_1(self):
		chords_1 = np.array([
				[pygliss.note.Note('C', 4).frequency(),
				pygliss.note.Note('E', 4).frequency(),
				pygliss.note.Note('G', 4).frequency(),
				pygliss.note.Note('C', 5).frequency()],
				[pygliss.note.Note('C', 4).frequency(),
				pygliss.note.Note('E', 4).frequency(),
				pygliss.note.Note('G', 4).frequency(),
				pygliss.note.Note('C', 5).frequency()],
				[pygliss.note.Note('C', 4).frequency(),
				pygliss.note.Note('E', 4).frequency(),
				pygliss.note.Note('G', 4).frequency(),
				pygliss.note.Note('C', 5).frequency()],
				[pygliss.note.Note('C', 4).frequency(),
				pygliss.note.Note('E', 4).frequency(),
				pygliss.note.Note('G', 4).frequency(),
				pygliss.note.Note('C', 5).frequency()]
			])
		durations_1 = np.ones(len(chords_1)) / len(chords_1)
		time_val_1 = np.arange(len(chords_1)) / len(chords_1)
		
		chords_seq_1 = pygliss.sequence.ChordSequence(chords_1, time_val_1, durations_1)
		# chords_seq_1.add_offset(10)

		chords_2 = np.array([
				[pygliss.note.Note('D', 5).frequency(),
				pygliss.note.Note('F', 5).frequency(),
				pygliss.note.Note('A', 5).frequency()],
				[pygliss.note.Note('D', 5).frequency(),
				pygliss.note.Note('F', 5).frequency(),
				pygliss.note.Note('A', 5).frequency()],
				[pygliss.note.Note('D', 5).frequency(),
				pygliss.note.Note('F', 5).frequency(),
				pygliss.note.Note('A', 5).frequency()]
			])
		durations_2 = np.ones(len(chords_2)) / len(chords_2)
		time_val_2 = np.arange(len(chords_2)) / len(chords_2)
		
		chords_seq_2 = pygliss.sequence.ChordSequence(chords_2, time_val_2, durations_2)
		# chords_seq_2.add_offset(10)

		comb_seq = chords_seq_1.concat(chords_seq_2)
		test_time_val = [0.0, 0.25, 0.333333, 0.5, 0.6666666, 0.75]
		test_chords = np.array([
			[pygliss.note.Note('C', 4).frequency(),
			pygliss.note.Note('E', 4).frequency(),
			pygliss.note.Note('G', 4).frequency(),
			pygliss.note.Note('C', 5).frequency(),
			pygliss.note.Note('D', 5).frequency(),
			pygliss.note.Note('F', 5).frequency(),
			pygliss.note.Note('A', 5).frequency()],
			[pygliss.note.Note('C', 4).frequency(),
			pygliss.note.Note('E', 4).frequency(),
			pygliss.note.Note('G', 4).frequency(),
			pygliss.note.Note('C', 5).frequency(),
			pygliss.note.Note('D', 5).frequency(),
			pygliss.note.Note('F', 5).frequency(),
			pygliss.note.Note('A', 5).frequency()],
			[pygliss.note.Note('C', 4).frequency(),
			pygliss.note.Note('E', 4).frequency(),
			pygliss.note.Note('G', 4).frequency(),
			pygliss.note.Note('C', 5).frequency(),
			pygliss.note.Note('D', 5).frequency(),
			pygliss.note.Note('F', 5).frequency(),
			pygliss.note.Note('A', 5).frequency()],
			[pygliss.note.Note('C', 4).frequency(),
			pygliss.note.Note('E', 4).frequency(),
			pygliss.note.Note('G', 4).frequency(),
			pygliss.note.Note('C', 5).frequency(),
			pygliss.note.Note('D', 5).frequency(),
			pygliss.note.Note('F', 5).frequency(),
			pygliss.note.Note('A', 5).frequency()],
			[pygliss.note.Note('C', 4).frequency(),
			pygliss.note.Note('E', 4).frequency(),
			pygliss.note.Note('G', 4).frequency(),
			pygliss.note.Note('C', 5).frequency(),
			pygliss.note.Note('D', 5).frequency(),
			pygliss.note.Note('F', 5).frequency(),
			pygliss.note.Note('A', 5).frequency()],
			[pygliss.note.Note('C', 4).frequency(),
			pygliss.note.Note('E', 4).frequency(),
			pygliss.note.Note('G', 4).frequency(),
			pygliss.note.Note('C', 5).frequency(),
			pygliss.note.Note('D', 5).frequency(),
			pygliss.note.Note('F', 5).frequency(),
			pygliss.note.Note('A', 5).frequency()]
			])

		assert np.allclose(comb_seq.time_val, np.array(test_time_val))
		assert np.array_equal(test_chords, comb_seq.chords)

	def test_concat_seq_2(self):
		chords_1 = np.array([
				[pygliss.note.Note('C', 4).frequency(),
				pygliss.note.Note('E', 4).frequency(),
				pygliss.note.Note('G', 4).frequency(),
				pygliss.note.Note('C', 5).frequency()],
				[pygliss.note.Note('C', 4).frequency(),
				pygliss.note.Note('E', 4).frequency(),
				pygliss.note.Note('G', 4).frequency(),
				pygliss.note.Note('C', 5).frequency()],
				[pygliss.note.Note('C', 4).frequency(),
				pygliss.note.Note('E', 4).frequency(),
				pygliss.note.Note('G', 4).frequency(),
				pygliss.note.Note('C', 5).frequency()],
				[pygliss.note.Note('C', 4).frequency(),
				pygliss.note.Note('E', 4).frequency(),
				pygliss.note.Note('G', 4).frequency(),
				pygliss.note.Note('C', 5).frequency()]
			])
		durations_1 = np.ones(len(chords_1)) / len(chords_1)
		time_val_1 = np.arange(len(chords_1)) / len(chords_1)

		durations_1 = durations_1 * 5
		time_val_1 = time_val_1 * 5
		
		chords_seq_1 = pygliss.sequence.ChordSequence(chords_1, time_val_1, durations_1)
		# chords_seq_1.add_offset(10)

		chords_2 = np.array([
				[pygliss.note.Note('D', 5).frequency(),
				pygliss.note.Note('F', 5).frequency(),
				pygliss.note.Note('A', 5).frequency()],
				[pygliss.note.Note('D', 5).frequency(),
				pygliss.note.Note('F', 5).frequency(),
				pygliss.note.Note('A', 5).frequency()],
				[pygliss.note.Note('D', 5).frequency(),
				pygliss.note.Note('F', 5).frequency(),
				pygliss.note.Note('A', 5).frequency()]
			])
		durations_2 = np.ones(len(chords_2)) / len(chords_2)
		time_val_2 = np.arange(len(chords_2)) / len(chords_2)
		
		chords_seq_2 = pygliss.sequence.ChordSequence(chords_2, time_val_2, durations_2)

		comb_seq = chords_seq_1.concat(chords_seq_2)
		test_time_val = [0.0, 0.333333, 0.6666666, 1.25, 2.5, 3.75]
		test_chords = np.array([
			[pygliss.note.Note('C', 4).frequency(),
			pygliss.note.Note('E', 4).frequency(),
			pygliss.note.Note('G', 4).frequency(),
			pygliss.note.Note('C', 5).frequency(),
			pygliss.note.Note('D', 5).frequency(),
			pygliss.note.Note('F', 5).frequency(),
			pygliss.note.Note('A', 5).frequency()],
			[pygliss.note.Note('C', 4).frequency(),
			pygliss.note.Note('E', 4).frequency(),
			pygliss.note.Note('G', 4).frequency(),
			pygliss.note.Note('C', 5).frequency(),
			pygliss.note.Note('D', 5).frequency(),
			pygliss.note.Note('F', 5).frequency(),
			pygliss.note.Note('A', 5).frequency()],
			[pygliss.note.Note('C', 4).frequency(),
			pygliss.note.Note('E', 4).frequency(),
			pygliss.note.Note('G', 4).frequency(),
			pygliss.note.Note('C', 5).frequency(),
			pygliss.note.Note('D', 5).frequency(),
			pygliss.note.Note('F', 5).frequency(),
			pygliss.note.Note('A', 5).frequency()],
			[pygliss.note.Note('C', 4).frequency(),
			pygliss.note.Note('E', 4).frequency(),
			pygliss.note.Note('G', 4).frequency(),
			pygliss.note.Note('C', 5).frequency(),
			0, 0, 0],
			[pygliss.note.Note('C', 4).frequency(),
			pygliss.note.Note('E', 4).frequency(),
			pygliss.note.Note('G', 4).frequency(),
			pygliss.note.Note('C', 5).frequency(),
			0, 0, 0],
			[pygliss.note.Note('C', 4).frequency(),
			pygliss.note.Note('E', 4).frequency(),
			pygliss.note.Note('G', 4).frequency(),
			pygliss.note.Note('C', 5).frequency(),
			0, 0, 0]
			])

		assert np.array_equal(test_chords, comb_seq.chords)
		assert np.allclose(comb_seq.time_val, np.array(test_time_val))


	def test_concat_seq_3(self):
		chords_1 = np.array([
				[pygliss.note.Note('C', 4).frequency(),
				pygliss.note.Note('E', 4).frequency(),
				pygliss.note.Note('G', 4).frequency(),
				pygliss.note.Note('C', 5).frequency()],
				[pygliss.note.Note('C', 4).frequency(),
				pygliss.note.Note('E', 4).frequency(),
				pygliss.note.Note('G', 4).frequency(),
				pygliss.note.Note('C', 5).frequency()],
				[pygliss.note.Note('C', 4).frequency(),
				pygliss.note.Note('E', 4).frequency(),
				pygliss.note.Note('G', 4).frequency(),
				pygliss.note.Note('C', 5).frequency()],
				[pygliss.note.Note('C', 4).frequency(),
				pygliss.note.Note('E', 4).frequency(),
				pygliss.note.Note('G', 4).frequency(),
				pygliss.note.Note('C', 5).frequency()]
			])
		durations_1 = np.ones(len(chords_1)) / len(chords_1)
		time_val_1 = np.arange(len(chords_1)) / len(chords_1)

		durations_1 = durations_1
		time_val_1 = time_val_1
		
		chords_seq_1 = pygliss.sequence.ChordSequence(chords_1, time_val_1, durations_1)
		chords_seq_1.add_offset(4)

		chords_2 = np.array([
				[pygliss.note.Note('D', 5).frequency(),
				pygliss.note.Note('F', 5).frequency(),
				pygliss.note.Note('A', 5).frequency()],
				[pygliss.note.Note('D', 5).frequency(),
				pygliss.note.Note('F', 5).frequency(),
				pygliss.note.Note('A', 5).frequency()],
				[pygliss.note.Note('D', 5).frequency(),
				pygliss.note.Note('F', 5).frequency(),
				pygliss.note.Note('A', 5).frequency()]
			])
		durations_2 = np.ones(len(chords_2)) / len(chords_2) * 3
		time_val_2 = np.arange(len(chords_2)) / len(chords_2) * 3
		chords_seq_2 = pygliss.sequence.ChordSequence(chords_2, time_val_2, durations_2)


		comb_seq = chords_seq_1.concat(chords_seq_2)
		test_time_val = [0.0, 1.0, 2.0, 4.0, 4.25, 4.5, 4.75]
		test_chords = np.array([
			[0.0, 0.0, 0.0, 0.0,
			pygliss.note.Note('D', 5).frequency(),
			pygliss.note.Note('F', 5).frequency(),
			pygliss.note.Note('A', 5).frequency()],
			[0.0, 0.0, 0.0, 0.0,
			pygliss.note.Note('D', 5).frequency(),
			pygliss.note.Note('F', 5).frequency(),
			pygliss.note.Note('A', 5).frequency()],
			[0.0, 0.0, 0.0, 0.0,
			pygliss.note.Note('D', 5).frequency(),
			pygliss.note.Note('F', 5).frequency(),
			pygliss.note.Note('A', 5).frequency()],
			[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
			[pygliss.note.Note('C', 4).frequency(),
			pygliss.note.Note('E', 4).frequency(),
			pygliss.note.Note('G', 4).frequency(),
			pygliss.note.Note('C', 5).frequency(),
			0.0, 0.0, 0.0],
			[pygliss.note.Note('C', 4).frequency(),
			pygliss.note.Note('E', 4).frequency(),
			pygliss.note.Note('G', 4).frequency(),
			pygliss.note.Note('C', 5).frequency(),
			0.0, 0.0, 0.0],
			[pygliss.note.Note('C', 4).frequency(),
			pygliss.note.Note('E', 4).frequency(),
			pygliss.note.Note('G', 4).frequency(),
			pygliss.note.Note('C', 5).frequency(),
			0.0, 0.0, 0.0]
			])

		print(f"test 3")
		print("chords_seq_1.durations", chords_seq_1.durations)
		print("chords_seq_1.time_val", chords_seq_1.time_val)
		print("chords_seq_2.durations", chords_seq_2.durations)
		print("chords_seq_2.time_val", chords_seq_2.time_val)
		print(f"comb_seq.time_val", comb_seq.time_val)
		print(f"comb_seq.durations", comb_seq.durations)
		print(f"test_time_val", test_time_val)
		print("\n\ncomb_seq.chords\n\n", comb_seq.chords, "\n\n\n")
		print("\n\ntest_chords\n\n", test_chords, "\n\n\n")

		assert np.array_equal(test_chords, comb_seq.chords)
		assert np.array_equal(comb_seq.time_val, np.array(test_time_val))

	def test_concat_seq_4(self):

		chords_1 = np.array([
				[pygliss.note.Note('C', 4).frequency(),
				pygliss.note.Note('E', 4).frequency(),
				pygliss.note.Note('G', 4).frequency(),
				pygliss.note.Note('C', 5).frequency()],
				[pygliss.note.Note('C', 4).frequency(),
				pygliss.note.Note('E', 4).frequency(),
				pygliss.note.Note('G', 4).frequency(),
				pygliss.note.Note('C', 5).frequency()],
				[pygliss.note.Note('C', 4).frequency(),
				pygliss.note.Note('E', 4).frequency(),
				pygliss.note.Note('G', 4).frequency(),
				pygliss.note.Note('C', 5).frequency()],
				[pygliss.note.Note('C', 4).frequency(),
				pygliss.note.Note('E', 4).frequency(),
				pygliss.note.Note('G', 4).frequency(),
				pygliss.note.Note('C', 5).frequency()]
			])
		durations_1 = np.ones(len(chords_1)) / len(chords_1)
		time_val_1 = np.arange(len(chords_1)) / len(chords_1)

		durations_1 = durations_1 * 4
		time_val_1 = time_val_1 * 4
		chords_seq_1 = pygliss.sequence.ChordSequence(chords_1, time_val_1, durations_1)


		chords_2 = np.array([
				[pygliss.note.Note('D', 5).frequency(),
				pygliss.note.Note('F', 5).frequency(),
				pygliss.note.Note('A', 5).frequency()],
				[pygliss.note.Note('D', 5).frequency(),
				pygliss.note.Note('F', 5).frequency(),
				pygliss.note.Note('A', 5).frequency()],
				[pygliss.note.Note('D', 5).frequency(),
				pygliss.note.Note('F', 5).frequency(),
				pygliss.note.Note('A', 5).frequency()]
			])
		durations_2 = np.ones(len(chords_2)) / len(chords_2)
		time_val_2 = np.arange(len(chords_2)) / len(chords_2)
		
		chords_seq_2 = pygliss.sequence.ChordSequence(chords_2, time_val_2, durations_2)
		chords_seq_2.add_offset(3)

		comb_seq = chords_seq_1.concat(chords_seq_2)
		test_time_val = [0.0, 0.333333, 0.6666666, 1.0, 2, 3.0]
		test_time_val = np.array([0.0, 1.0, 2.0, 3.0, 3.33333333, 3.66666667])
		test_chords = np.array([
			[pygliss.note.Note('C', 4).frequency(),
			pygliss.note.Note('E', 4).frequency(),
			pygliss.note.Note('G', 4).frequency(),
			pygliss.note.Note('C', 5).frequency(),
			0.0, 0.0, 0.0],
			[pygliss.note.Note('C', 4).frequency(),
			pygliss.note.Note('E', 4).frequency(),
			pygliss.note.Note('G', 4).frequency(),
			pygliss.note.Note('C', 5).frequency(),
			0.0, 0.0, 0.0],
			[pygliss.note.Note('C', 4).frequency(),
			pygliss.note.Note('E', 4).frequency(),
			pygliss.note.Note('G', 4).frequency(),
			pygliss.note.Note('C', 5).frequency(),
			0.0, 0.0, 0.0],
			[pygliss.note.Note('C', 4).frequency(),
			pygliss.note.Note('E', 4).frequency(),
			pygliss.note.Note('G', 4).frequency(),
			pygliss.note.Note('C', 5).frequency(),
			pygliss.note.Note('D', 5).frequency(),
			pygliss.note.Note('F', 5).frequency(),
			pygliss.note.Note('A', 5).frequency()],
			[pygliss.note.Note('C', 4).frequency(),
			pygliss.note.Note('E', 4).frequency(),
			pygliss.note.Note('G', 4).frequency(),
			pygliss.note.Note('C', 5).frequency(),
			pygliss.note.Note('D', 5).frequency(),
			pygliss.note.Note('F', 5).frequency(),
			pygliss.note.Note('A', 5).frequency()],
			[pygliss.note.Note('C', 4).frequency(),
			pygliss.note.Note('E', 4).frequency(),
			pygliss.note.Note('G', 4).frequency(),
			pygliss.note.Note('C', 5).frequency(),
			pygliss.note.Note('D', 5).frequency(),
			pygliss.note.Note('F', 5).frequency(),
			pygliss.note.Note('A', 5).frequency()]
			])

		# print(f"test 4")
		# print("chords_seq_1.durations", chords_seq_1.durations)
		# print("chords_seq_1.time_val", chords_seq_1.time_val)
		# print("chords_seq_2.durations", chords_seq_2.durations)
		# print("chords_seq_2.time_val", chords_seq_2.time_val)
		# print(f"comb_seq.time_val", comb_seq.time_val)
		# print(f"comb_seq.durations", comb_seq.durations)
		# print(f"test_time_val", test_time_val)
		# print("\n\ncomb_seq.chords\n\n", comb_seq.chords, "\n\n\n")
		assert np.allclose(test_chords, comb_seq.chords)
		assert np.allclose(comb_seq.time_val, test_time_val)





if __name__ == '__main__':
    unittest.main()

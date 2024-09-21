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



if __name__ == '__main__':
    unittest.main()

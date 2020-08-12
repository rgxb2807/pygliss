import numpy as np
import math
from pygliss.note import Note
from music21 import pitch, corpus, midi, stream, tempo, duration, note as m21note


def get_mus21_pitch(note):
	"""Convert pygliss.note to music21.pitch."""
	if note.accidental == '+':
		return pitch.Pitch(name=note.note + "~" + str(note.octave))
	elif note.accidental == '#':
		return pitch.Pitch(name=note.note + "#" + str(note.octave))
	elif note.accidental == '++':
		return pitch.Pitch(name=note.note + "#~" + str(note.octave))
	elif note.accidental == '-':
		return pitch.Pitch(name=note.note + "`" + str(note.octave))
	elif note.accidental == 'b':
		return pitch.Pitch(name=note.note + "-" + str(note.octave))
	elif note.accidental == '--':
		return pitch.Pitch(name=note.note + "-`" + str(note.octave))
	else:
		return pitch.Pitch(note.note + str(note.octave))


def playbach():
	"""Playback Test - Play Bach bwv66.6 from Corpus."""
	b = corpus.parse('bach/bwv66.6')
	print(b)
	sp = midi.realtime.StreamPlayer(b)
	sp.play()
	return True


def comp_stream(comp, bpm=60, length=0.25):
	"""."""
	parts = [stream.Part() for i in range(len(comp.chords[0].notes))]
	parts.append(tempo.MetronomeMark(number=bpm))
	for chord in comp.all_chords:
		for idx, note in enumerate(chord.notes):
			parts[idx].append(m21note.Note(get_mus21_pitch(note), 
				quarterLength=length))
	
	s = stream.Stream(parts)
	return s

def get_note_length(ratio):
	lengths = [1,2,3,4,5,6,7,8,9]
	floor = math.floor(ratio)
	ratio =  ratio - floor
	closest = 0
	denom = 1
	distance = float("inf")
	if ratio != 0:
		for i in lengths:
			for j in lengths:
				if j > i:
					temp_ratio = i / j
					temp_diff = abs(temp_ratio - ratio)
					if temp_diff < distance:
						distance = temp_diff
						closest = temp_ratio
						denom = j
	return closest + floor, denom


def longest_gliss(glissandi):
	longest, longest_idx = None, None
	longest_length = 0
	for i, gliss in enumerate(glissandi):
		if gliss.length > longest_length:
			longest_length = gliss.length
			longest = gliss
			longest_idx = i
	return longest

def get_note_duration(pitch, note_length, denom):
	dur = None
	#3/2
	if denom == 3:
		if math.isclose(note_length, (1/3)):
			dur = duration.Duration(type='eighth')
		elif math.isclose(note_length, (2/3)):
			dur = duration.Duration(type='quarter')
		dur.appendTuplet(duration.Tuplet(3,2, 'eighth'))
	
	#5/4
	elif denom == 5:
		if math.isclose(note_length, (1/5)):
			dur = duration.Duration(type='16th')
		elif math.isclose(note_length, (2/5)):
			dur = duration.Duration(type='eighth')
		elif math.isclose(note_length, (3/5)):
			dur = duration.Duration(type='eighth', dots=1)
		elif math.isclose(note_length, (4/5)):
			dur = duration.Duration(type='quarter')
		dur.appendTuplet(duration.Tuplet(5,4, '16th'))

	#6/4
	elif denom == 6:
		if math.isclose(note_length, (1/6)):
			dur = duration.Duration(type='16th')
		elif math.isclose(note_length, (2/6)):
			dur = duration.Duration(type='eighth')
		elif math.isclose(note_length, (3/6)):
			dur = duration.Duration(type='eighth', dots=1)
		elif math.isclose(note_length, (4/6)):
			dur = duration.Duration(type='quarter')
		elif math.isclose(note_length, (5/6)):
			note1 = m21note.Note(pitch)
			note1.duration = duration.Duration(type='eighth', dots=1)
			note1.duration.appendTuplet(duration.Tuplet(6,4, '16th'))
			note2 = m21note.Note(pitch)
			note2.duration = duration.Duration(type='eighth')
			note2.duration.appendTuplet(duration.Tuplet(6,4, '16th'))
			return [note1, note2]
		dur.appendTuplet(duration.Tuplet(6,4, '16th'))
	
	#7/4
	elif denom == 7:
		if math.isclose(note_length, (1/7)):
			dur = duration.Duration(type='16th')
		elif math.isclose(note_length, (2/7)):
			dur = duration.Duration(type='eighth')
		elif math.isclose(note_length, (3/7)):
			dur = duration.Duration(type='eighth', dots=1)
		elif math.isclose(note_length, (4/7)):
			dur = duration.Duration(type='quarter')
		elif math.isclose(note_length, (5/7)):
			note1 = m21note.Note(pitch)
			note1.duration = duration.Duration(type='eighth', dots=1)
			note1.duration.appendTuplet(duration.Tuplet(7,4, '16th'))
			note2 = m21note.Note(pitch)
			note2.duration = duration.Duration(type='eighth')
			note2.duration.appendTuplet(duration.Tuplet(7,4, '16th'))
			return [note1, note2]
		elif math.isclose(note_length, (6/7)):
			dur = duration.Duration(type='quarter', dots=1)
		dur.appendTuplet(duration.Tuplet(7,4, '16th'))

	#9/8
	elif denom == 9:
		if math.isclose(note_length, (1/9)):
			dur = duration.Duration(type='32nd')
		elif math.isclose(note_length, (2/9)):
			dur = duration.Duration(type='16th')
		elif math.isclose(note_length, (3/9)):
			dur = duration.Duration(type='16th', dots=1)
		elif math.isclose(note_length, (4/9)):
			dur = duration.Duration(type='eighth')
		elif math.isclose(note_length, (5/9)):
			note1 = m21note.Note(pitch)
			note1.duration = duration.Duration(type='16th', dots=1)
			note1.duration.appendTuplet(duration.Tuplet(9,8, '32nd'))
			note2 = m21note.Note(pitch)
			note2.duration = duration.Duration(type='16th')
			note2.duration.appendTuplet(duration.Tuplet(9,8, '32nd'))
			return [note1, note2]
		elif math.isclose(note_length, (6/9)):
			dur = duration.Duration(type='eighth', dots=1)
		elif math.isclose(note_length, (7/9)):
			dur = duration.Duration(type='eighth', dots=2)
		elif math.isclose(note_length, (8/9)):
			dur = duration.Duration(type='quarter')
		dur.appendTuplet(duration.Tuplet(9,8, '32nd'))
	
	note = m21note.Note(pitch)
	note.duration = dur
	return [note]


def build_note_sequence(gliss, longest, length=0.25):
	"""."""
	part = stream.Part()
	note_length_ratio = (longest.length / gliss.length) * length
	note_length, denom = get_note_length(note_length_ratio)
	
	# add rests to offset
	offset = note_length_ratio - note_length * gliss.length
	if offset > 0:
		#add rests - todo
		pass

	prev = 0
	for i, note in enumerate(gliss.notes):
		pitch = get_mus21_pitch(note)
		# check if note length is a tuple 
		if note_length % (length / 4) == 0:	
			note = m21note.Note(pitch, quarterLength=note_length)
			part.append(note)
		else:
			#if tied from previous note
			if prev > 0:
				if math.isclose((note_length + prev), 1):
					notes = get_note_duration(pitch, note_length, denom)
					for n in notes:
						part.append(n)
					prev = 0
				elif (note_length + prev) < 1:
					notes = get_note_duration(pitch, note_length, denom)
					for n in notes:
						part.append(n)
					prev += note_length
				else:
					first_length, _ = get_note_length(1-prev)
					first_notes = get_note_duration(pitch, first_length, denom)
					for n in first_notes:
						part.append(n)
					
					# check for middle note
					middle_length = (note_length - first_length) // 1
					if middle_length > 0:
						middle_note = m21note.Note(pitch, quarterLength=middle_length)
						part.append(middle_note)
					
					# end note
					end_length = (note_length - middle_length - first_length)
					if math.isclose(end_length, 0) or end_length < 0:
						end_length = 0
					if end_length != 0:
						end_notes = get_note_duration(pitch, end_length, denom)
						for n in end_notes:
							part.append(n)
					prev = end_length

			else:
				if note_length < 1:
					notes = get_note_duration(pitch, note_length, denom)
					for n in notes:
						part.append(n)
					prev = note_length
				
				else:
					first_length = note_length // 1
					if first_length > 0:
						first_note = m21note.Note(pitch, quarterLength=first_length)
						part.append(first_note)
					end_length = (note_length - first_length)
					end_notes = get_note_duration(pitch, end_length, denom)
					for n in end_notes:
						part.append(n)
					prev = end_length
	return part
		
 
def gliss_ratio(glissandi, length=0.25, bpm=60):
	"""."""
	parts = []
	longest = longest_gliss(glissandi)
	total_length = longest.length * length
	for i, gliss in enumerate(glissandi):
		part = build_note_sequence(gliss, longest, length)
		parts.append(part)

	# for part in parts:
	# 	print(part.notes)
	# 	for note in part.notes:
	# 		print(note)
	# 		print(note.duration)
	# 		print()

	s = stream.Stream(parts)
	return s

def test_note():
	parts = [stream.Part() for i in range(3)]
	# note1 = m21note.Note(pitch.Pitch("C4"), quarterLength=3/7)
	# note2 = m21note.Note(pitch.Pitch("C4"), quarterLength=3/7)
	# note3 = m21note.Note(pitch.Pitch("C4"), quarterLength=1/7)
	note1 = m21note.Note(pitch.Pitch("C4"))
	note2 = m21note.Note(pitch.Pitch("C4"))
	note3 = m21note.Note(pitch.Pitch("C4"))

	# sep = duration.Tuplet(7,4)
	# sep.setDurationType('16th')
	print(f"type !! {note1.duration.type}")

	# note1.duration.appendTuplet(duration.Tuplet(7,4, '16th'))
	note1.duration = duration.Duration(type='eighth', dots=1)
	note1.duration.appendTuplet(duration.Tuplet(7,4, '16th'))

	# note2.duration.appendTuplet(duration.Tuplet(7,4, '16th'))
	note2.duration = duration.Duration(type='eighth', dots=1)
	note2.duration.appendTuplet(duration.Tuplet(7,4, '16th'))

	# note3.duration.appendTuplet(duration.Tuplet(7,4, '16th'))
	note3.duration = duration.Duration(type='16th')
	note3.duration.appendTuplet(duration.Tuplet(7,4, '16th'))


	# note2.duration.Tuplet(7,4)
	# note3.duration.Tuplet()
	parts[0].append(note1)
	parts[0].append(note2)
	parts[0].append(note3)
	parts.append(tempo.MetronomeMark(number=60))
	s = stream.Stream(parts)
	s.write("musicxml", "dur_test" + ".musicxml")
	return True


def play_stream(s):
	sp = midi.realtime.StreamPlayer(s)
	sp.play()
	return True


def write_stream(s, filename):
	s.write("musicxml", filename + ".musicxml")
	return True


from pygliss.note import Note
from music21 import pitch, corpus, midi, stream, tempo, note as m21note


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


def comp_stream(comp, bpm=60, length=0.25, constrain=False):
	"""."""
	parts = [stream.Part() for i in range(len(comp.chords[0].notes))]
	parts.append(tempo.MetronomeMark(number=bpm))

	if constrain:
		# find the longest gliss
		longest = max(comp.glissandi_len)
		# set the reosolution of that gliss to be duration of the specified length
		for chord in comp.all_chords:
			for idx, note in enumerate(chord.notes):
				if comp.glissandi_len[idx] == longest:
					parts[idx].append(m21note.Note(get_mus21_pitch(note), quarterLength=length))
				else:
					#ratio should round to the nearest 2,3,4,5,6,7,8,9
					# temporarily just end ratio as is
					# gliss 1 is 12
					# gliss 2 is 6

					ratio = longest / comp.glissandi_len[idx]
					parts[idx].append(m21note.Note(get_mus21_pitch(note), quarterLength=ratio * length))


		# build the other voices as ratios of to that gliss
		# omit the starting notes at first if the ratios don't map perfectly

	else:
		for chord in comp.all_chords:
			for idx, note in enumerate(chord.notes):
				parts[idx].append(m21note.Note(get_mus21_pitch(note), quarterLength=length))

		
	s = stream.Stream(parts)
	return s

def play_stream(s):
	sp = midi.realtime.StreamPlayer(s)
	sp.play()
	return True


def write_stream(s, filename):
	s.write("musicxml", filename + ".musicxml")
	return True


from pygliss.note import Note
from music21 import pitch, corpus, midi, stream, tempo, note as m21note


def get_mus21_pitch(note):
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
		return pitch.Pitch(name=note.note, accidental="one-and-a-half-flat", octave=str(note.octave))
	else:
		return pitch.Pitch(note.note + str(note.octave))


def playbach():
	b = corpus.parse('bach/bwv66.6')
	print(b)
	sp = midi.realtime.StreamPlayer(b)
	sp.play()
	return True

def seq(filename):

	p1 = stream.Part()
	n1 = m21note.Note('D', quarterLength=0.25)
	p1.append(n1)
	n2 = m21note.Note('D', quarterLength=0.25)
	p1.append(n2)
	n3 = m21note.Note('E', quarterLength=0.25)
	p1.append(n3)
	n4 = m21note.Note('D', quarterLength=0.25)
	p1.append(n4)

	p2 = stream.Part()
	n1 = m21note.Note('F', quarterLength=0.25)
	p2.append(n1)
	n2 = m21note.Note('F', quarterLength=0.25)
	p2.append(n2)
	n3 = m21note.Note('G', quarterLength=0.25)
	p2.append(n3)
	n4 = m21note.Note('F~', quarterLength=0.25)
	p2.append(n4)

	p3 = stream.Part()
	n1 = m21note.Note('A', quarterLength=0.25)
	p3.append(n1)
	n2 = m21note.Note('A', quarterLength=0.25)
	p3.append(n2)
	n3 = m21note.Note('C', quarterLength=0.25)
	p3.append(n3)
	n4 = m21note.Note('C', quarterLength=0.25)
	p3.append(n4)

	mm1 = tempo.MetronomeMark(number=30)
	s2 = stream.Stream([p1, p2, p3, mm1])

	sp = midi.realtime.StreamPlayer(s2)
	sp.play()
	s2.write("musicxml", filename + ".musicxml")
	s2.write("midi", filename + ".midi")
	return True




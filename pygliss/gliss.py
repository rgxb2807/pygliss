from pygliss.note import Note, asc_notes_list, desc_notes_dict

ASC_LIST = asc_notes_list()
DESC_LIST = desc_notes_dict()

class Gliss:
	def __init__(self, start, end):

		self.start = start
		self.end = end
		self.ascend = None
		self.length = None
		self.notes = list()

		def is_asc (self):
			if self.start.steps < self.end.steps:
				self.ascend = True
			else:
				self.ascend = False

		def set_length(self):
			if self.ascend:
				self.length = self.end.steps - self.start.steps
			elif (self.end.steps - self.start.steps) == 0:
				self.length = 1
			else:
				self.length = self.start.steps - self.end.steps

		def set_notes(self):
			idx = 0
			if self.ascend:
			    idx = ASC_LIST.index(self.start)
			else:
				idx = DESC_LIST.index(self.start)

			if self.length == 1:
				self.notes.append(self.start)
			else:
				for idx in range(idx, int(self.length) + idx):
					if self.ascend:
					    self.notes.append(ASC_LIST[idx])
					else:
						self.notes.append(DESC_LIST[idx])

		is_asc(self)
		set_length(self)
		set_notes(self)

	def __str__(self):
		s = ''
		for note in self.notes:
			s += str(note) + ", "
		return s

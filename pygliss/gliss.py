from pygliss.note import Note, asc_notes_list, desc_notes_list

# add error handling for when resolution doesn't divide evening
# add option  - favor end note or start note

class Gliss:
	def __init__(self, start, end, resolution=1):

		self.start = start
		self.end = end
		self.ascend = None
		self.length = None
		self.resolution = resolution
		self.notes = list()

		def is_asc (self):
			if self.start.steps < self.end.steps:
				self.ascend = True
			else:
				self.ascend = False

		def set_length(self):
			if self.ascend:
				self.length = (self.end.steps - self.start.steps) / self.resolution
			elif (self.end.steps - self.start.steps) == 0:
				self.length = 1
			else:
				self.length = (self.start.steps - self.end.steps) / self.resolution

		def set_notes(self):
			idx = 0
			asc_list = asc_notes_list(resolution=self.resolution)
			desc_list = desc_notes_list(resolution=self.resolution)
			if self.ascend:
			    idx = asc_list.index(self.start)
			else:
				idx = desc_list.index(self.start)

			if self.length == 1:
				self.notes.append(self.start)
			else:
				for idx in range(idx, int(self.length) + idx):
					if self.ascend:
					    self.notes.append(asc_list[idx])
					else:
						self.notes.append(desc_list[idx])

		is_asc(self)
		set_length(self)
		set_notes(self)

	def __str__(self):
		s = ''
		for note in self.notes:
			s += str(note) + ", "
		return s

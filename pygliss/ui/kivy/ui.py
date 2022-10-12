from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.core.window import Window




import sys
import os
sys.path.append('/Users/rgxb2807/Music/pygliss_package')
import pygliss.mus21 as mus21
from music21 import pitch, corpus, midi, stream, tempo, duration, note as m21note, tie


####

from pygliss.utils import make_freq_vector, make_freq_to_steps_map
from pygliss.constants import DIVISIONS
from pygliss.note import Note, freq_to_note, find_note_vector_position_vectorized, find_note_vector_position
from pygliss.chord import Chord, nearest_ot_chord, nearest_fm_chord, FM_CHORDS, FMChord, calc_roughness
from pygliss.sequence import make_chord_seq_from_note_seq
from pygliss.gliss import Gliss
from pygliss.gliss_cmpr import make_gliss_cmpr_sequence

import numpy as np


###
test_chords = np.array([
    [110.0, 220.0,  330.0],
    [151.6255653, 261.6255653,  371.6255653],
    [113.22324603, 220.0,  330.0],
    [146.83238396, 261.6255653,  380.83608684],
])



g1 = Gliss(220.0, 110.0)
g2 = Gliss(220.0, 330.0)
g3 = Gliss(440.0, 330.0)
g4 = Gliss(440.0, 660.0)
g5 = Gliss(440.0, 2000.0)

glissandi = [g1, g2, g3, g4, g5]


t = make_chord_seq_from_note_seq(glissandi)

chords = t.to_chord()

def get_chord_stream(chords, bpm=60, length=0.25):
    parts = [stream.Part() for i in range(len(chords[0].notes))]
    parts.append(tempo.MetronomeMark(number=bpm))
    for chord in chords:
        notes = chord.to_notes()            
        for idx, note in enumerate(notes):
            parts[idx].append(m21note.Note(mus21.get_mus21_pitch(note), quarterLength=length))
    s = stream.Stream(parts)
    return s



# s = get_chord_stream(chords)

def write_stream_png(s, filename):
   s.write("musicxml.png", filename + ".musicxml.png")
   return True



###






Builder.load_file("layout.kv")
class AnnotatorLayout(Widget):

    def __init__(self, **kwargs):
        super(AnnotatorLayout, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self.current_page = 1

    def on_open(self, *args):
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
      if keycode[1] == 'd':
         main_input = "HEY"
         self.ids.main_text.text = main_input
      elif keycode[1] == '0':
         # title = df.iloc[self.current_idx]["LinkText"]
         title = "HIIIIII 0"
         self.ids.main_text.text = self.adjust_newline(title)
         # print(title)
         # print(len(title))
         # print(df.iloc[self.current_idx]["ToLinkURL"])
         # self.current_idx += 1
      elif keycode[1] == "left":
         if os.path.exists(f"temp_seq.musicxml-{self.current_page - 1}.png"):
            self.current_page -= 1
            self.ids.main_image.source = f"temp_seq.musicxml-{self.current_page}.png"
            self.ids.main_image.reload()
      elif keycode[1] == "right":
         if os.path.exists(f"temp_seq.musicxml-{self.current_page + 1}.png"):
            self.current_page += 1
            self.ids.main_image.source = f"temp_seq.musicxml-{self.current_page}.png"
            self.ids.main_image.reload()


      return True

    def press(self):
      # update label
      s = get_chord_stream(chords)
      write_stream_png(s, "temp_seq")
      file = f"temp_seq.musicxml-{self.current_page}.png"
      self.ids.main_image.source = "temp_seq.musicxml-1.png"
      self.ids.main_image.reload()
    
    def press_next(self):
      # update label

      if os.path.exists(f"temp_seq.musicxml-{self.current_page + 1}.png"):
         self.current_page += 1
         self.ids.main_image.source = f"temp_seq.musicxml-{self.current_page}.png"
         self.ids.main_image.reload()
    
    def press_prev(self):
      # update label

      if os.path.exists(f"temp_seq.musicxml-{self.current_page - 1}.png"):
         self.current_page -= 1
         self.ids.main_image.source = f"temp_seq.musicxml-{self.current_page}.png"
         self.ids.main_image.reload()






      # print(title)
      # print(len(title))
      # print(df.iloc[self.current_idx]["ToLinkURL"])
      # self.current_idx += 1

    def adjust_newline(self, text):
      if len(text) > 70:
         words = text.split(" ")
         half = int(len(words) / 2)
         return " ".join(words[:half]) + "\n" + " ".join(words[half:])
      return text


class AnnotatorApp(App):
   def build(self):
      return AnnotatorLayout()

if __name__ == '__main__':
   AnnotatorApp().run()

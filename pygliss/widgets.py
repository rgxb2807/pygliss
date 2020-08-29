from IPython.display import display, clear_output
from pygliss.chord import Chord
from pygliss.mus21 import play_stream, chord_stream
import ipywidgets as widgets

class ChordToggle:
    
    def __init__(self, chords, length=1.0):
        self.chords = chords
        self.length = 1.0
        self.streams = [chord_stream([chord], length=1.0) for chord in self.chords ]
        self.count = 0
        
    def play_next(self):
        if self.count < len(self.chords) - 1:
            self.count += 1
            play_stream(self.streams[self.count])
    
    def play_prev(self):
        if self.count > 0:
            self.count -=1
            play_stream(self.streams[self.count])
    
    def play_cur(self):
        play_stream(self.streams[self.count])
    
    def chord_info(self):
        return f"{self.count}: {self.chords[self.count]}"
    
    def reset(self):
        self.count = 0
        
    def goto(self, n):
        self.count = n
    

class ToggleChordButtons:
    def __init__(self, chords, length=1.0):
        chord_toggle = ChordToggle(chords, length=1.0)
        prev_button = widgets.Button(description="Previous")
        cur_button = widgets.Button(description="Current")
        next_button = widgets.Button(description="Next")
        reset_button = widgets.Button(description="Reset")
        goto_slider = widgets.IntSlider(min=0, max=len(chord_toggle.chords)-1, value=0, description='Slider')
        output = widgets.Output()

        display(reset_button)
        display(prev_button)
        display(cur_button)
        display(next_button, output)
        display(goto_slider)
        
        def on_click_prev(b):
            chord_toggle.play_prev()
            with output:
                clear_output()
                info = chord_toggle.chord_info()
                print(info)

        def on_click_cur(b):
            chord_toggle.play_cur()
            with output:
                clear_output()
                info = chord_toggle.chord_info()
                print(info)

        def on_click_next(b):
            chord_toggle.play_next()
            with output:
                clear_output()
                info = chord_toggle.chord_info()
                print(info)
        
        def on_click_reset(b):
            chord_toggle.reset()
            with output:
                clear_output()
                info = chord_toggle.chord_info()
                print(info)
                
        def goto_slider_handler(change):
            chord_toggle.goto(change.new)
            with output:
                clear_output()
                info = chord_toggle.chord_info()
        
        reset_button.on_click(on_click_reset)
        prev_button.on_click(on_click_prev)
        cur_button.on_click(on_click_cur)
        next_button.on_click(on_click_next)
        goto_slider.observe(goto_slider_handler, names='value')
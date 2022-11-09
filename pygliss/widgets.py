from pygliss.note import Note, freq_to_note
from pygliss.chord import Chord
from pygliss.mus21 import play_stream, chord_stream
from music21 import pitch, corpus, midi, stream, tempo, duration, note as m21note, tie


from IPython.display import display, clear_output
import ipywidgets as widgets
import numpy as np
import pygame
import scipy
import copy

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






pygame.mixer.init(size=32)


def play_sin_freq(freq, dur=1000):
    buffer = np.sin(2 * np.pi * np.arange(44100) * freq / 44100).astype(np.float32)
    sound = pygame.mixer.Sound(buffer)
    sound.play(0)
    pygame.time.wait(int(sound.get_length() * dur))


def play_square_freq(freq, dur=1000):
    buffer = scipy.signal.square(2 * np.pi * np.arange(44100) * freq / 44100).astype(np.float32)
    sound = pygame.mixer.Sound(buffer)
    sound.play(0)
    pygame.time.wait(int(sound.get_length() * dur))





class FilteredChordsToggle:
    
    def __init__(self, candidates, saved,length=1.0):

        self.cand_idx = 0
        self.seq_idx = 0
        self.sol_idx = 0

        self.candidates = candidates
        self.reset_candidates  = copy.deepcopy(candidates)
        self.cand_type = self.candidates[self.cand_idx]["candidates"][self.sol_idx]['type']
        self.length = len(candidates)
        self.streams = [chord_stream([c["candidates"][0]['chord']], length=0.75) for c in candidates]
        self.sequence = saved

        self.mode = "only_play"
        self.playback_type = 'sin'
        self.current_chord = candidates[self.cand_idx]["candidates"][self.sol_idx]['chord']
        self.current_note = candidates[self.cand_idx]['candidates'][self.sol_idx]['chord'].notes[0]
        # self.temp_chord_stream = chord_stream([self.temp_chord], length=0.25)
        # self.temp_note_stream = stream.Part() 


    def chord_info(self):
        note_strs = [str(freq_to_note(n)) for n in self.current_chord.notes]
        return f"{' '.join(note_strs)} type:{self.cand_type} idx:{self.cand_idx}"

    def solution_info(self):
        t = self.candidates[self.cand_idx]["candidates"][self.sol_idx]['type']
        c = self.candidates[self.cand_idx]["candidates"][self.sol_idx]['chord']
        sol_len = len(self.candidates[self.cand_idx]["candidates"])
        note_s = ' '.join([str(freq_to_note(n)) for n in c.notes])
        s = ""

        if t == "fm":
            carrier = self.candidates[self.cand_idx]["candidates"][self.sol_idx]['chord'].carrier
            mod = self.candidates[self.cand_idx]["candidates"][self.sol_idx]['chord'].modulator
            sum_tones = self.candidates[self.cand_idx]["candidates"][self.sol_idx]['chord'].chord_sum_tones(return_sb=True)
            diff_tones = self.candidates[self.cand_idx]["candidates"][self.sol_idx]['chord'].chord_diff_tones(return_sb=True)
            s += f"{c.notes} type:{t} carrier:{np.around(carrier,3)} mod:{np.around(mod,3)} sol:{self.sol_idx + 1} of {sol_len}\n"
            if len(sum_tones) > 0:
                s += f"sum sidebands:{sum_tones}\n"
            if len(diff_tones) > 0:
                s += f"diff sidebands:{diff_tones}\n"
        elif t =="ot":
            fund = self.candidates[self.cand_idx]["candidates"][self.sol_idx]['chord'].fundamental
            partials = self.candidates[self.cand_idx]["candidates"][self.sol_idx]['chord'].chord_partials(m=50, return_partials=True)
            s += f"{c.notes} type:{t} fund:{freq_to_note(fund)} sol:{self.sol_idx + 1} of {sol_len}\n"
            s += f"partials:{partials}"

        
        return s + note_s

    def next_solution(self):
        if self.sol_idx < len(self.candidates[self.cand_idx]["candidates"]) - 1:
            self.sol_idx += 1
            self.cand_type = self.candidates[self.cand_idx]["candidates"][self.sol_idx]['type']
            self.current_chord = self.candidates[self.cand_idx]["candidates"][self.sol_idx]['chord']
        return self.solution_info()

    def prev_solution(self):
        if self.sol_idx > 0:
            self.sol_idx -= 1
            self.cand_type = self.candidates[self.cand_idx]["candidates"][self.sol_idx]['type']
            self.current_chord = self.candidates[self.cand_idx]["candidates"][self.sol_idx]['chord']
        return self.solution_info()

    def play_current(self):
        play_stream(self.streams[self.cand_idx])

    def next_chord(self):
        if self.cand_idx  < self.length - 1:
            self.cand_idx  += 1
            self.sol_idx = 0
            self.current_chord = self.candidates[self.cand_idx]["candidates"][self.sol_idx]['chord']
            self.cand_type = self.candidates[self.cand_idx]["candidates"][self.sol_idx]['type']
            play_stream(self.streams[self.cand_idx])


    def prev_chord(self):
        if self.cand_idx  > 0:
            self.cand_idx -= 1
            self.sol_idx = 0
            self.current_chord = self.candidates[self.cand_idx]["candidates"][self.sol_idx]['chord']
            self.cand_type = self.candidates[self.cand_idx]["candidates"][self.sol_idx]['type']
            play_stream(self.streams[self.cand_idx])


    def toggle_note(self):
        if self.mode != "only_play":
            # add note to chord
            # should you be able to toggle notes that are in the chord itself?
            # sum or diff tones are already in there
            contains_idx = np.argwhere(np.isin(self.current_chord.notes, self.current_note)).ravel()
            if len(contains_idx) == 0:
                self.current_chord.notes = np.append(self.current_chord.notes, self.current_note)
            else:
                self.current_chord.notes = np.delete(self.current_chord.notes, contains_idx[0])

    def toggle_mode(self):
        if self.mode == "note":
            self.mode = "only_play"
        else:
            self.mode = "note"
        return self.mode

    def insert_chord(self):
        self.sequence.append(self.current_chord)
        if len(self.sequence) > 1:
            self.seq_idx += 1

    def remove_chord(self):
        if len(self.sequence) > 0:
            self.sequence.pop(self.seq_idx)
            self.seq_idx -= 1

    def reset_chord(self):
        c = copy.deepcopy(self.reset_candidates[self.cand_idx]["candidates"][self.sol_idx]['chord'])
        self.current_chord = c
        self.candidates[self.cand_idx]["candidates"][self.sol_idx]['chord'] = c


    def seq_info(self):
        return " ".join([str(c) for c in self.sequence])

    def seq_chord_info(self):
        return f"{self.sequence[self.seq_idx]}"



    def play_sum_tone(self, sb=1):
        if self.cand_type == 'fm':
            freq = self.current_chord.sum_tones()[sb-1]
            self.current_note = freq
            self.toggle_note()
            if self.playback_type == "sin":
                play_sin_freq(freq)
            else:
                play_square_freq(freq)

    def play_diff_tone(self, sb=1):
        if self.cand_type == 'fm':
            freq = self.current_chord.diff_tones()[sb-1]
            self.current_note = freq
            self.toggle_note()
            if self.playback_type == "sin":
                play_sin_freq(freq)
            else:
                play_square_freq(freq)

    def play_ot_tone(self, ot=1):
        if self.cand_type == 'ot':
            freq = self.current_chord.get_partials(include_fund=True)[ot-1]
            self.current_note = freq
            self.toggle_note()
            if self.playback_type == "sin":
                play_sin_freq(freq)
            else:
                play_square_freq(freq)

    def play_carrier(self):
        if self.cand_type == 'fm':
            freq = self.current_chord.carrier
            self.current_note = freq
            self.toggle_note()
            if self.playback_type == "sin":
                play_sin_freq(freq)
            else:
                play_square_freq(freq)

    # sum tones
    def play_sum_sb1(self):
        self.play_sum_tone(1)
    def play_sum_sb2(self):
        self.play_sum_tone(2)
    def play_sum_sb3(self):
        self.play_sum_tone(3)
    def play_sum_sb4(self):
        self.play_sum_tone(4)
    def play_sum_sb5(self):
        self.play_sum_tone(5)

    def play_sum_sb6(self):
        self.play_sum_tone(6)
    def play_sum_sb7(self):
        self.play_sum_tone(7)
    def play_sum_sb8(self):
        self.play_sum_tone(8)
    def play_sum_sb9(self):
        self.play_sum_tone(9)
    def play_sum_sb10(self):
        self.play_sum_tone(10)

    def play_sum_sb11(self):
        self.play_sum_tone(11)
    def play_sum_sb12(self):
        self.play_sum_tone(12)
    def play_sum_sb13(self):
        self.play_sum_tone(13)
    def play_sum_sb14(self):
        self.play_sum_tone(14)
    def play_sum_sb15(self):
        self.play_sum_tone(15)

    def play_sum_sb16(self):
        self.play_sum_tone(16)
    def play_sum_sb17(self):
        self.play_sum_tone(17)
    def play_sum_sb18(self):
        self.play_sum_tone(18)
    def play_sum_sb19(self):
        self.play_sum_tone(19)
    def play_sum_sb20(self):
        self.play_sum_tone(20)

    def play_sum_sb21(self):
        self.play_sum_tone(21)
    def play_sum_sb22(self):
        self.play_sum_tone(22)
    def play_sum_sb23(self):
        self.play_sum_tone(23)
    def play_sum_sb24(self):
        self.play_sum_tone(24)
    def play_sum_sb25(self):
        self.play_sum_tone(25)


    #diff tones
    def play_diff_sb1(self):
        self.play_diff_tone(1)
    def play_diff_sb2(self):
        self.play_diff_tone(2)
    def play_diff_sb3(self):
        self.play_diff_tone(3)
    def play_diff_sb4(self):
        self.play_diff_tone(4)
    def play_diff_sb5(self):
        self.play_diff_tone(5)

    def play_diff_sb6(self):
        self.play_diff_tone(6)
    def play_diff_sb7(self):
        self.play_diff_tone(7)
    def play_diff_sb8(self):
        self.play_diff_tone(8)
    def play_diff_sb9(self):
        self.play_diff_tone(9)
    def play_diff_sb10(self):
        self.play_diff_tone(10)

    def play_diff_sb11(self):
        self.play_diff_tone(11)
    def play_diff_sb12(self):
        self.play_diff_tone(12)
    def play_diff_sb13(self):
        self.play_diff_tone(13)
    def play_diff_sb14(self):
        self.play_diff_tone(14)
    def play_diff_sb15(self):
        self.play_diff_tone(15)

    def play_diff_sb16(self):
        self.play_diff_tone(16)
    def play_diff_sb17(self):
        self.play_diff_tone(17)
    def play_diff_sb18(self):
        self.play_diff_tone(18)
    def play_diff_sb19(self):
        self.play_diff_tone(19)
    def play_diff_sb20(self):
        self.play_diff_tone(20)

    def play_diff_sb21(self):
        self.play_diff_tone(21)
    def play_diff_sb22(self):
        self.play_diff_tone(22)
    def play_diff_sb23(self):
        self.play_diff_tone(23)
    def play_diff_sb24(self):
        self.play_diff_tone(24)
    def play_diff_sb25(self):
        self.play_diff_tone(25)


    #OT
    def play_ot_part1(self):
        self.play_ot_tone(1)
    def play_ot_part2(self):
        self.play_ot_tone(2)
    def play_ot_part3(self):
        self.play_ot_tone(3)
    def play_ot_part4(self):
        self.play_ot_tone(4)
    def play_ot_part5(self):
        self.play_ot_tone(5)

    def play_ot_part6(self):
        self.play_ot_tone(6)
    def play_ot_part7(self):
        self.play_ot_tone(7)
    def play_ot_part8(self):
        self.play_ot_tone(8)
    def play_ot_part9(self):
        self.play_ot_tone(9)
    def play_ot_part10(self):
        self.play_ot_tone(10)

    def play_ot_part11(self):
        self.play_ot_tone(11)
    def play_ot_part12(self):
        self.play_ot_tone(12)
    def play_ot_part13(self):
        self.play_ot_tone(13)
    def play_ot_part14(self):
        self.play_ot_tone(14)
    def play_ot_part15(self):
        self.play_ot_tone(15)

    def play_ot_part16(self):
        self.play_ot_tone(16)
    def play_ot_part17(self):
        self.play_ot_tone(17)
    def play_ot_part18(self):
        self.play_ot_tone(18)
    def play_ot_part19(self):
        self.play_ot_tone(19)
    def play_ot_part20(self):
        self.play_ot_tone(20)

    def play_ot_part21(self):
        self.play_ot_tone(21)
    def play_ot_part22(self):
        self.play_ot_tone(22)
    def play_ot_part23(self):
        self.play_ot_tone(23)
    def play_ot_part24(self):
        self.play_ot_tone(24)
    def play_ot_part25(self):
        self.play_ot_tone(25)

        

class FilteredChordsToggleButtons:
    
    def __init__(self, candidates, saved,length=1.0):
        self.toggle = FilteredChordsToggle(candidates, saved, length)
        self.grid = widgets.GridspecLayout(20, 6)
        self.output = widgets.Output()


        def create_button(desc, style):
            return widgets.Button(description=desc, button_style=style, 
                layout=widgets.Layout(height='auto', width='auto'))


        # candidate controls
        self.grid[-5,-1] = create_button('Mode: Note/Only Play'.format(""), 'danger')
        def toggle_mode(b):
            mode = self.toggle.toggle_mode()
            with self.output:
                clear_output()
                print(mode)
        self.grid[-5,-1].on_click(toggle_mode)



        self.grid[-5,-2] = create_button('Chord Info'.format(""), 'info')
        def chord_info(b):
            with self.output:
                clear_output()
                info = self.toggle.chord_info()
                print(info)
        self.grid[-5,-2].on_click(chord_info)


        self.grid[-4,-1] = create_button('- Play Chord - '.format(""), 'primary')
        def play_current(b):
            self.toggle.play_current()
        self.grid[-4,-1].on_click(play_current)

        
        # next candidate
        self.grid[-4,-2] = create_button('Next'.format(""), 'danger')
        def next_chord(b):
            self.toggle.next_chord()
            with self.output:
                clear_output()
                print(self.toggle.chord_info())
        self.grid[-4,-2].on_click(next_chord)


        # previous candidate
        self.grid[-4,-3] = create_button('Prev'.format(""), 'danger')
        def prev_chord(b):
            self.toggle.prev_chord()
            with self.output:
                clear_output()
                print(self.toggle.chord_info())
        self.grid[-4,-3].on_click(prev_chord)


        # solution toggle
        self.grid[5,-1] = create_button('Prev Solution'.format(""), 'danger')
        def prev_solution(b):
            with self.output:
                clear_output()
                print(self.toggle.prev_solution())
        self.grid[5,-1].on_click(prev_solution)

        self.grid[6,-1] = create_button('Next Solution'.format(""), 'danger')
        def next_solution(b):
            with self.output:
                clear_output()
                print(self.toggle.next_solution())
        self.grid[6,-1].on_click(next_solution)

        self.grid[7,-1] = create_button('Solution Info'.format(""), 'primary')
        def solution_info(b):
            with self.output:
                clear_output()
                print(self.toggle.solution_info())
        self.grid[7,-1].on_click(solution_info)


        #Chord Sequence
        self.grid[-5,0] = create_button('Insert Chord'.format(""), 'danger')
        def insert_chord(b):
            self.toggle.insert_chord()
        self.grid[-5,0].on_click(insert_chord)

        self.grid[-4,0] = create_button('Remove'.format(""), 'warning')
        def reset_chord(b):
            self.toggle.remove_chord()
        self.grid[-4,0].on_click(reset_chord)
        
        self.grid[-3,0] = create_button('Reset'.format(""), 'danger')
        def reset_chord(b):
            self.toggle.reset_chord()
        self.grid[-3,0].on_click(reset_chord)


        self.grid[-1,-2] = create_button('Sequence Info'.format(""), 'info')
        def seq_info(b):
            with self.output:
                clear_output()
                print(self.toggle.seq_info())
        self.grid[-1,-2].on_click(seq_info)
        
        self.grid[-1,-3] = create_button('Seq Chord Info'.format(""), 'info')
        def seq_chord_info(b):
            with self.output:
                clear_output()
                print(self.toggle.seq_chord_info())


        self.grid[-1,-3].on_click(seq_chord_info)


        self.grid[-2,-1] = create_button('- Play Seq Chord - '.format(""), 'info')
        self.grid[-1,-1] = create_button('- Play Sequence - '.format(""), 'primary')
        self.grid[-2,-2] = create_button('Next'.format(""), 'success')
        self.grid[-2,-3] = create_button('Prev'.format(""), 'success')



        tone_idx = 1
        #FM tones
        for i in range(10):
            for j in range(5):
                if tone_idx <= 25:
                    self.tone_type = "fm_sum"
                    b = create_button('Sum - sb {}'.format(tone_idx), 'info')
                    self.grid[i, j] = b
                else:
                    self.tone_type = "fm_diff"
                    b = create_button('Diff - sb {}'.format(tone_idx-25), 'success')
                    self.grid[i, j] = b
                tone_idx += 1
        
        #OT tones
        tone_idx = 1
        self.tone_type = "ot_par"
        for i in range(10, 15):
            for j in range(5):
                b = create_button('OT - Partial {}'.format(tone_idx), 'primary')
                if tone_idx == 1:
                    b = create_button('- Fundamental - '.format(""), 'warning')
                self.grid[i, j] = b
                tone_idx += 1


    
        display(self.grid)
        display(self.output)


        self.grid[0,-1] = create_button('- Carrier - '.format(""), 'warning')
        def play_carrier(b):
            self.toggle.play_carrier()
        self.grid[0,-1].on_click(play_carrier)

        ## Sum tones
        def play_sb1_sum(b):
            self.toggle.play_sum_sb1()
        self.grid[0,0].on_click(play_sb1_sum)

        def play_sb2_sum(b):
            self.toggle.play_sum_sb2()
        self.grid[0,1].on_click(play_sb2_sum)

        def play_sb3_sum(b):
            self.toggle.play_sum_sb3()
        self.grid[0,2].on_click(play_sb3_sum)

        def play_sb4_sum(b):
            self.toggle.play_sum_sb4()
        self.grid[0,3].on_click(play_sb4_sum)

        def play_sb5_sum(b):
            self.toggle.play_sum_sb5()
        self.grid[0,4].on_click(play_sb5_sum)


        def play_sb6_sum(b):
            self.toggle.play_sum_sb6()
        self.grid[1,0].on_click(play_sb6_sum)

        def play_sb7_sum(b):
            self.toggle.play_sum_sb7()
        self.grid[1,1].on_click(play_sb7_sum)

        def play_sb8_sum(b):
            self.toggle.play_sum_sb8()
        self.grid[1,2].on_click(play_sb8_sum)

        def play_sb9_sum(b):
            self.toggle.play_sum_sb9()
        self.grid[1,3].on_click(play_sb9_sum)

        def play_sb10_sum(b):
            self.toggle.play_sum_sb10()
        self.grid[1,4].on_click(play_sb10_sum)


        def play_sb11_sum(b):
            self.toggle.play_sum_sb11()
        self.grid[2,0].on_click(play_sb11_sum)

        def play_sb12_sum(b):
            self.toggle.play_sum_sb12()
        self.grid[2,1].on_click(play_sb12_sum)

        def play_sb13_sum(b):
            self.toggle.play_sum_sb13()
        self.grid[2,2].on_click(play_sb13_sum)

        def play_sb14_sum(b):
            self.toggle.play_sum_sb14()
        self.grid[2,3].on_click(play_sb14_sum)

        def play_sb15_sum(b):
            self.toggle.play_sum_sb15()
        self.grid[2,4].on_click(play_sb15_sum)


        def play_sb16_sum(b):
            self.toggle.play_sum_sb16()
        self.grid[2,0].on_click(play_sb16_sum)

        def play_sb17_sum(b):
            self.toggle.play_sum_sb17()
        self.grid[2,1].on_click(play_sb17_sum)

        def play_sb18_sum(b):
            self.toggle.play_sum_sb18()
        self.grid[2,2].on_click(play_sb18_sum)

        def play_sb19_sum(b):
            self.toggle.play_sum_sb19()
        self.grid[2,3].on_click(play_sb19_sum)

        def play_sb20_sum(b):
            self.toggle.play_sum_sb20()
        self.grid[2,4].on_click(play_sb20_sum)


        def play_sb21_sum(b):
            self.toggle.play_sum_sb21()
        self.grid[3,0].on_click(play_sb21_sum)

        def play_sb22_sum(b):
            self.toggle.play_sum_sb22()
        self.grid[3,1].on_click(play_sb22_sum)

        def play_sb23_sum(b):
            self.toggle.play_sum_sb23()
        self.grid[3,2].on_click(play_sb23_sum)

        def play_sb24_sum(b):
            self.toggle.play_sum_sb24()
        self.grid[3,3].on_click(play_sb24_sum)

        def play_sb25_sum(b):
            self.toggle.play_sum_sb25()
        self.grid[3,4].on_click(play_sb25_sum)


        # diff tones
        def play_sb1_diff(b):
            self.toggle.play_diff_sb1()
        self.grid[5,0].on_click(play_sb1_diff)

        def play_sb2_diff(b):
            self.toggle.play_diff_sb2()
        self.grid[5,1].on_click(play_sb2_diff)

        def play_sb3_diff(b):
            self.toggle.play_diff_sb3()
        self.grid[5,2].on_click(play_sb3_diff)

        def play_sb4_diff(b):
            self.toggle.play_diff_sb4()
        self.grid[5,3].on_click(play_sb4_diff)

        def play_sb5_diff(b):
            self.toggle.play_diff_sb5()
        self.grid[5,4].on_click(play_sb5_diff)


        def play_sb6_diff(b):
            self.toggle.play_diff_sb6()
        self.grid[6,0].on_click(play_sb6_diff)

        def play_sb7_diff(b):
            self.toggle.play_diff_sb7()
        self.grid[6,1].on_click(play_sb7_diff)

        def play_sb8_diff(b):
            self.toggle.play_diff_sb8()
        self.grid[6,2].on_click(play_sb8_diff)

        def play_sb9_diff(b):
            self.toggle.play_diff_sb9()
        self.grid[6,3].on_click(play_sb9_diff)

        def play_sb10_diff(b):
            self.toggle.play_diff_sb10()
        self.grid[6,4].on_click(play_sb10_diff)


        def play_sb11_diff(b):
            self.toggle.play_diff_sb11()
        self.grid[7,0].on_click(play_sb11_diff)

        def play_sb12_diff(b):
            self.toggle.play_diff_sb12()
        self.grid[7,1].on_click(play_sb12_diff)

        def play_sb13_diff(b):
            self.toggle.play_diff_sb13()
        self.grid[7,2].on_click(play_sb13_diff)

        def play_sb14_diff(b):
            self.toggle.play_diff_sb14()
        self.grid[7,3].on_click(play_sb14_diff)

        def play_sb15_diff(b):
            self.toggle.play_diff_sb15()
        self.grid[7,4].on_click(play_sb15_diff)


        def play_sb16_diff(b):
            self.toggle.play_diff_sb16()
        self.grid[8,0].on_click(play_sb16_diff)

        def play_sb17_diff(b):
            self.toggle.play_diff_sb17()
        self.grid[8,1].on_click(play_sb17_diff)

        def play_sb18_diff(b):
            self.toggle.play_diff_sb18()
        self.grid[8,2].on_click(play_sb18_diff)

        def play_sb19_diff(b):
            self.toggle.play_diff_sb19()
        self.grid[8,3].on_click(play_sb19_diff)

        def play_sb20_diff(b):
            self.toggle.play_diff_sb20()
        self.grid[8,4].on_click(play_sb20_diff)


        def play_sb21_diff(b):
            self.toggle.play_diff_sb21()
        self.grid[9,0].on_click(play_sb21_diff)

        def play_sb22_diff(b):
            self.toggle.play_diff_sb22()
        self.grid[9,1].on_click(play_sb22_diff)

        def play_sb23_diff(b):
            self.toggle.play_diff_sb23()
        self.grid[9,2].on_click(play_sb23_diff)

        def play_sb24_diff(b):
            self.toggle.play_diff_sb24()
        self.grid[9,3].on_click(play_sb24_diff)

        def play_sb25_diff(b):
            self.toggle.play_diff_sb25()
        self.grid[9,4].on_click(play_sb25_diff)

        #OT
        def play_ot_fund(b):
            self.toggle.play_ot_part1()
        self.grid[10,0].on_click(play_ot_fund)

        def play_ot_part2(b):
            self.toggle.play_ot_part2()
        self.grid[10,1].on_click(play_ot_part2)

        def play_ot_part3(b):
            self.toggle.play_ot_part3()
        self.grid[10,2].on_click(play_ot_part3)

        def play_ot_part4(b):
            self.toggle.play_ot_part4()
        self.grid[10,3].on_click(play_ot_part4)

        def play_ot_part5(b):
            self.toggle.play_ot_part5()
        self.grid[10,4].on_click(play_ot_part5)


        def play_ot_part6(b):
            self.toggle.play_ot_part6()
        self.grid[11,0].on_click(play_ot_part6)

        def play_ot_part7(b):
            self.toggle.play_ot_part7()
        self.grid[11,1].on_click(play_ot_part7)

        def play_ot_part8(b):
            self.toggle.play_ot_part8()
        self.grid[11,2].on_click(play_ot_part8)

        def play_ot_part9(b):
            self.toggle.play_ot_part9()
        self.grid[11,3].on_click(play_ot_part9)

        def play_ot_part10(b):
            self.toggle.play_ot_part10()
        self.grid[11,4].on_click(play_ot_part10)


        def play_ot_part11(b):
            self.toggle.play_ot_part11()
        self.grid[12,0].on_click(play_ot_part11)

        def play_ot_part12(b):
            self.toggle.play_ot_part12()
        self.grid[12,1].on_click(play_ot_part12)

        def play_ot_part13(b):
            self.toggle.play_ot_part13()
        self.grid[12,2].on_click(play_ot_part13)

        def play_ot_part14(b):
            self.toggle.play_ot_part14()
        self.grid[12,3].on_click(play_ot_part14)

        def play_ot_part15(b):
            self.toggle.play_ot_part15()
        self.grid[12,4].on_click(play_ot_part15)


        def play_ot_part16(b):
            self.toggle.play_ot_part16()
        self.grid[13,0].on_click(play_ot_part16)

        def play_ot_part17(b):
            self.toggle.play_ot_part17()
        self.grid[13,1].on_click(play_ot_part17)

        def play_ot_part18(b):
            self.toggle.play_ot_part18()
        self.grid[13,2].on_click(play_ot_part18)

        def play_ot_part19(b):
            self.toggle.play_ot_part19()
        self.grid[13,3].on_click(play_ot_part19)

        def play_ot_part20(b):
            self.toggle.play_ot_part20()
        self.grid[13,4].on_click(play_ot_part20)


        def play_ot_part21(b):
            self.toggle.play_ot_part21()
        self.grid[14,0].on_click(play_ot_part21)

        def play_ot_part22(b):
            self.toggle.play_ot_part22()
        self.grid[14,1].on_click(play_ot_part22)

        def play_ot_part23(b):
            self.toggle.play_ot_part23()
        self.grid[14,2].on_click(play_ot_part23)

        def play_ot_part24(b):
            self.toggle.play_ot_part24()
        self.grid[14,3].on_click(play_ot_part24)

        def play_ot_part25(b):
            self.toggle.play_ot_part25()
        self.grid[14,4].on_click(play_ot_part25)






#######################################






# class FilteredChordsToggle:
    
#     def __init__(self, candidates, saved,length=1.0):

#         self.cand_idx = 0
#         self.seq_idx = 0
#         self.fm_idx = 0
#         self.sol_idx = 0

#         self.candidates = candidates
#         self.cand_type = self.candidates[self.cand_idx][self.sol_idx]['type']
#         self.length = 1.0
#         self.streams = [chord_stream([v[0]['chord']], length=1.0) for k, v in candidates.items()]
#         self.sequence = []

#         self.mode = "chord"
#         self.playback_type = 'sin'
#         self.current_chord = candidates[self.cand_idx][self.sol_idx]['chord']
#         self.current_note = candidates[0][0]['chord'].notes[0]
#         # self.temp_chord_stream = chord_stream([self.temp_chord], length=0.25)
#         # self.temp_note_stream = stream.Part() 




#     def play_toggle_note(self, idx, tone_type="fm_sum"):
#         """
#         Plays specified tone - FM or Overtones

#         """
#         cand_type = self.candidates[self.cand_idx][self.sol_idx]['type']

#         # Find Note Frequency
#         if tone_type == "fm_sum":
#             if cand_type != "fm":
#                 print("Not an FM Chord")
#                 return
#             self.current_note = self.candidates[self.cand_idx][self.sol_idx]['chord'].sum_tones()[idx-1]
        
#         elif tone_type == "fm_diff":
#             if cand_type != "fm":
#                 print("Not an FM Chord")
#                 return
#             self.current_note = self.candidates[self.cand_idx][self.sol_idx]['chord'].diff_tones()[idx-1]
        
#         elif tone_type == "fm_car":
#             if cand_type != "fm":
#                 print("Not an FM Chord")
#                 return
#             self.current_note = self.candidates[self.cand_idx][self.sol_idx]['chord'].carrier
        
#         elif tone_type == "ot_par":
#             if cand_type != "ot":
#                 print("Not an OT Chord")
#                 return
#             self.current_note = self.candidates[self.cand_idx][self.sol_idx]['chord'].get_partials()[idx-1]


#         elif tone_type == "ot_fund":
#             if cand_type != "ot":
#                 print("Not an OT Chord")
#                 return
#             self.current_note = self.candidates[self.cand_idx][self.sol_idx]['chord'].fundamental


#         if self.mode != "only_play":
#             # add note to chord
#             # should you be able to toggle notes that are in the chord itself?
#             # sum or diff tones are already in there
#             contains_idx = np.argwhere(np.isin(self.temp_chord.notes, self.current_note)).ravel()
#             if len(contains_idx) == 0:
#                 self.temp_chord.notes = np.append(self.temp_chord.notes, self.current_note)
#             else:
#                 self.temp_chord.notes = np.delete(self.temp_chord.notes, contains_idx[0])


#         if self.playback_type == "sin":
#             play_sin_freq(self.current_note)
#         else:
#             play_square_freq(self.current_note)


#     def play_sum_sb1(self):
#         if self.cand_type == 'fm':
#             freq = self.current_chord.sum_tones()[0]
#             if self.playback_type == "sin":
#                 play_sin_freq(freq)
#             else:
#                 play_square_freq(freq)
        
            

#     def play_diff_sb1(self):
#         if self.cand_type == 'fm':
#             freq = self.current_chord.diff_tones()[0]
#             if self.playback_type == "sin":
#                 play_sin_freq(freq)
#             else:
#                 play_square_freq(freq)

            


#     # def play_note(self):
#     #     if self.mode == 'chord':
#     #         self.temp_chord_stream = chord_stream([self.temp_chord], length=0.25)
#     #         play_stream(self.temp_chord_stream)
        
#     #     else:

#     #         self.temp_note_stream[0] = m21note.Note(get_mus21_pitch(freq_to_note(self.current_note)), 
#     #             quarterLength=0.25)

#     #         play_stream(self.temp_note_stream[0])



#         # ## 
#         # def play_next_chord(b):
#         #     if self.count < len(self.chords) - 1:
#         #         self.count += 1
#         #         play_stream(self.streams[self.count])
        
#         # def play_prev_chord(b):
#         #     if self.count > 0:
#         #         self.count -=1
#         #         play_stream(self.streams[self.count])
        
#         # def play_cur_chord(b):
#         #     play_stream(self.streams[self.count])

#         # def chord_info(b):
#         #     return f"{self.count}: {self.chords[self.count]}"


#         # ## FM
#         # def next_fm(b):
#         #     pass

#         # def prev_fm(b):
#         #     pass


#         # def fm_info(b):
#         #     pass


#         # #sequnce
#         # def next_seq_chord(b):
#         #     pass

#         # def prev_seq_chord(b):
#         #     pass

#         # def seq_chord_info(b):
#         #     pass

#         # def seq_info(b):
#         #     pass

#         # def play_cur_seq_chord(b):
#         #     pass

#         # def play_sequence(b):
#         #     pass


# class FilteredChordsToggleButtons:
    
#     def __init__(self, candidates, saved,length=1.0):
#         self.toggle = FilteredChordsToggle(candidates, saved, length)
#         self.candidates = candidates
#         self.length = 1.0
#         self.grid = widgets.GridspecLayout(20, 6)
#         self.mode = "chord"
#         self.temp_chord = None
#         self.tone_idx = 1
#         self.tone_type = "fm_sum"


#         def create_tone_button(desc, style):
#             return widgets.Button(description=desc, button_style=style, 
#                 layout=widgets.Layout(height='auto', width='auto'))


#         def play_toggle_note_button(b):
#             self.toggle.play_toggle_note(self.tone_idx, self.tone_type)

#         #FM tones
#         for i in range(10):
#             for j in range(5):
#                 if self.tone_idx <= 25:
#                     self.tone_type = "fm_sum"
#                     b = create_tone_button('Sum - sb {}'.format(self.tone_idx), 'info')
#                     b.on_click(play_toggle_note_button)
#                     self.grid[i, j] = b
#                 else:
#                     self.tone_type = "fm_diff"
#                     b = create_tone_button('Diff - sb {}'.format(self.tone_idx-25), 'success')
#                     b.on_click(play_toggle_note_button)
#                     self.grid[i, j] = b
#                 self.tone_idx += 1
        
#         #OT tones
#         self.tone_idx = 1
#         self.tone_type = "ot_par"
#         for i in range(10, 15):
#             for j in range(5):
#                 b = create_tone_button('OT - Partial {}'.format(self.tone_idx), 'primary')
#                 # b.on_click(play_toggle_note_button)
#                 self.grid[i, j] = b
#                 self.tone_idx += 1


    
#         display(self.grid)


#         ##
#         def play_sb1_sum(b):
#             self.toggle.play_sum_sb1()

#         def play_sb1_diff(b):
#             self.toggle.play_diff_sb1()

#         # self.grid[0,0].on_click(play_sb1_sum)
#         # self.grid[5,0].on_click(play_sb1_diff)



#         def play_next_chord(b):
#             if self.count < len(self.chords) - 1:
#                 self.count += 1
#                 play_stream(self.streams[self.count])
        
#         def play_prev_chord(b):
#             if self.count > 0:
#                 self.count -=1
#                 play_stream(self.streams[self.count])
        
#         def play_cur_chord(b):
#             play_stream(self.streams[self.count])

#         def chord_info(b):
#             return f"{self.count}: {self.chords[self.count]}"


#         ## FM
#         def next_fm(b):
#             pass

#         def prev_fm(b):
#             pass


#         def fm_info(b):
#             pass


#         #sequnce
#         def next_seq_chord(b):
#             pass

#         def prev_seq_chord(b):
#             pass

#         def seq_chord_info(b):
#             pass

#         def seq_info(b):
#             pass

#         def play_cur_seq_chord(b):
#             pass

#         def play_sequence(b):
#             pass





    
    
#     def reset(self):
#         self.count = 0
        
#     def goto(self, n):
#         self.count = n


# class NoteGridButton:
#     pass


# # class NoteToggleButton:
# #     __init__ self():
# #         pass


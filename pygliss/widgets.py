from pygliss.constants import LOW, HIGH
from pygliss.note import Note, freq_to_note
from pygliss.chord import Chord
from pygliss.mus21 import play_stream, chord_stream, get_chord_stream, get_chord_arp_stream
from music21 import pitch, corpus, midi, stream, tempo, duration, note as m21note, tie



from IPython.display import display, clear_output
import ipywidgets as widgets
import numpy as np
import pygame
import scipy
import copy

import simpleaudio as sa
import time


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



def play_sampled_notes(notes, mode=None, pause=0.0, bass_first=False):
    """
    Mode can be `med` or `short`
    """
    path = "/Users/rgxb2807/Music/pygliss_package/pygliss/samples/"
    if bass_first:
        notes.reverse()
    
    for note in notes:
        if mode == 'med':
            filename = f"{path}{str(note)}_med.wav"
        elif mode == 'short':
            filename = f"{path}{str(note)}_short.wav"
        else:
            filename = f"{path}{str(note)}.wav"

        wave_obj = sa.WaveObject.from_wave_file(filename)
        play_obj = wave_obj.play()
        if pause > 0:
            time.sleep(pause)
            

class FilteredChordsToggle:
    
    def __init__(self, candidates, saved,length=1.0):

        self.cand_idx = 0
        self.seq_idx = 0
        self.sol_idx = 0

        self.candidates = candidates
        self.reset_candidates  = copy.deepcopy(candidates)
        self.cand_type = self.candidates[self.cand_idx]["candidates"][self.sol_idx]['type']
        self.length = len(candidates)
        self.sequence = saved

        self.mode = "only_play"
        self.arp = "chord"
        self.playback_type = 'samples'
        self.current_chord = candidates[self.cand_idx]["candidates"][self.sol_idx]['chord']
        self.current_note = candidates[self.cand_idx]['candidates'][self.sol_idx]['chord'].notes[0]


    def chord_info(self):
        note_strs = [str(freq_to_note(n)) for n in self.current_chord.notes]
        return f"{' '.join(note_strs)} type:{self.cand_type} idx:{self.cand_idx}"

    def chord_score(self):
        if self.arp == 'arp':
            s = get_chord_arp_stream([self.current_chord])
        else:
            s = get_chord_stream([self.current_chord])
        return s

    def chord_seq_score(self):
        if self.arp == 'arp':
            s = get_chord_arp_stream(self.sequence)
        else:
            s = get_chord_stream(self.sequence)
        return s


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

        else:
            s += f"{c.notes} type:{t} sol:{self.sol_idx + 1} of {sol_len}\n"


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
        # play_stream(self.streams[self.cand_idx])
        pause = 0.0 if self.arp  != "arp" else 0.2
        play_sampled_notes(self.current_chord.to_notes(), pause=pause)

    def playback_arp_mode(self):
        # play_stream(self.streams[self.cand_idx])
        # play_sampled_notes(self.current_chord.to_notes(), pause=0.2)
        if self.arp == "chord":
            self.arp = "arp"
        else:
            self.arp = "chord"

    def next_chord(self):
        if self.cand_idx  < self.length - 1:
            self.cand_idx  += 1
            self.sol_idx = 0
            self.current_chord = self.candidates[self.cand_idx]["candidates"][self.sol_idx]['chord']
            self.cand_type = self.candidates[self.cand_idx]["candidates"][self.sol_idx]['type']
            # play_stream(self.streams[self.cand_idx])
            play_sampled_notes(self.current_chord.to_notes())


    def prev_chord(self):
        if self.cand_idx  > 0:
            self.cand_idx -= 1
            self.sol_idx = 0
            self.current_chord = self.candidates[self.cand_idx]["candidates"][self.sol_idx]['chord']
            self.cand_type = self.candidates[self.cand_idx]["candidates"][self.sol_idx]['type']
            # play_stream(self.streams[self.cand_idx])
            play_sampled_notes(self.current_chord.to_notes())


    def next_seq_chord(self):
        if self.seq_idx  < len(self.sequence) - 1:
            self.seq_idx += 1
            # play_sampled_notes(self.current_chord.to_notes())


    def prev_seq_chord(self):
        if self.seq_idx  > 0:
            self.seq_idx -= 1
            # play_sampled_notes(self.current_chord.to_notes())


    def toggle_note(self):
        if self.mode != "only_play":
            # add note to chord
            # should you be able to toggle notes that are in the chord itself?
            # sum or diff tones are already in there
            contains_idx = np.argwhere(np.isin(self.current_chord.notes, self.current_note)).ravel()
            if len(contains_idx) == 0:
                self.current_chord.notes = np.sort(np.append(self.current_chord.notes, self.current_note))

            else:
                self.current_chord.notes = np.sort(np.delete(self.current_chord.notes, contains_idx[0]))

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
        if len(self.sequence) > 0:
            return " ".join([str(c) for c in self.sequence])

    def seq_chord_info(self):
        if len(self.sequence) > 0:
            return f"{self.sequence[self.seq_idx]}"

    def play_current_seq(self):
        if len(self.sequence) > 0:
            pause = 0.0 if self.arp  != "arp" else 0.2
            play_sampled_notes(self.sequence[self.seq_idx].to_notes(), pause=pause)

    def play_sequence(self,wait=1.0):

        for c in self.sequence:
            pause = 0.0 if self.arp  != "arp" else 0.2
            play_sampled_notes(c.to_notes(), pause=pause)
            time.sleep(wait)



    def play_sum_tone(self, sb=1):
        if self.cand_type == 'fm':
            freq = self.current_chord.sum_tones()[sb-1]
            self.current_note = freq
            self.toggle_note()
            if self.playback_type == "sin":
                play_sin_freq(freq)
            else:
                if freq >= LOW and freq <= HIGH:
                    play_sampled_notes([freq_to_note(freq)])

    def play_diff_tone(self, sb=1):
        if self.cand_type == 'fm':
            freq = self.current_chord.diff_tones()[sb-1]
            self.current_note = freq
            self.toggle_note()
            if self.playback_type == "sin":
                play_sin_freq(freq)
            else:
                if freq >= LOW and freq <= HIGH:
                    play_sampled_notes([freq_to_note(freq)])

    def play_ot_tone(self, ot=1):
        if self.cand_type == 'ot':
            freq = self.current_chord.get_partials(m=30, include_fund=True)[ot-1]
            self.current_note = freq
            self.toggle_note()
            if self.playback_type == "sin":
                play_sin_freq(freq)
            else:
                if freq >= LOW and freq <= HIGH:
                    play_sampled_notes([freq_to_note(freq)])

    def play_carrier(self):
        if self.cand_type == 'fm':
            freq = self.current_chord.carrier
            self.current_note = freq
            self.toggle_note()
            if self.playback_type == "sin":
                play_sin_freq(freq)
            else:
                if freq >= LOW and freq <= HIGH:
                    play_sampled_notes([freq_to_note(freq)])

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

    def play_sum_sb26(self):
        self.play_sum_tone(26)
    def play_sum_sb27(self):
        self.play_sum_tone(27)
    def play_sum_sb28(self):
        self.play_sum_tone(28)
    def play_sum_sb29(self):
        self.play_sum_tone(29)
    def play_sum_sb30(self):
        self.play_sum_tone(30)


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

    def play_diff_sb26(self):
        self.play_diff_tone(26)
    def play_diff_sb27(self):
        self.play_diff_tone(27)
    def play_diff_sb28(self):
        self.play_diff_tone(28)
    def play_diff_sb29(self):
        self.play_diff_tone(29)
    def play_diff_sb30(self):
        self.play_diff_tone(30)


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

    def play_ot_part26(self):
        self.play_ot_tone(26)
    def play_ot_part27(self):
        self.play_ot_tone(27)
    def play_ot_part28(self):
        self.play_ot_tone(28)
    def play_ot_part29(self):
        self.play_ot_tone(29)
    def play_ot_part30(self):
        self.play_ot_tone(30)

        

class FilteredChordsToggleButtons:
    
    def __init__(self, candidates, saved,length=1.0):
        self.toggle = FilteredChordsToggle(candidates, saved, length)
        self.grid = widgets.GridspecLayout(14, 10)
        self.output = widgets.Output()


        def create_button(desc, style):
            return widgets.Button(description=desc, button_style=style, 
                layout=widgets.Layout(height='auto', width='auto'))


        # candidate controls
        self.grid[11,8] = create_button('Mode: Note/Only Play'.format(""), 'danger')
        def toggle_mode(b):
            mode = self.toggle.toggle_mode()
            with self.output:
                clear_output()
                print(mode)
        self.grid[11,8].on_click(toggle_mode)



        self.grid[10,9] = create_button('Chord Info'.format(""), 'primary')
        def chord_info(b):
            with self.output:
                clear_output()
                info = self.toggle.chord_info()
                print(info)
        self.grid[10,9].on_click(chord_info)


        self.grid[10,6] = create_button('Chord Score'.format(""), 'primary')
        def chord_score(b):
            with self.output:
                clear_output()
                s = self.toggle.chord_score()
                s.show()
        self.grid[10,6].on_click(chord_score)


        self.grid[11,9] = create_button('Play Chord'.format(""), 'success')
        def play_current(b):
            self.toggle.play_current()
        self.grid[11,9].on_click(play_current)

        self.grid[11,7] = create_button('Arp'.format(""), 'info')
        def playback_arp_mode(b):
            self.toggle.playback_arp_mode()
        self.grid[11,7].on_click(playback_arp_mode)

        self.grid[12,9] = create_button('Play Seq Chord'.format(""), 'warning')
        def play_current_seq(b):
            self.toggle.play_current_seq()
        self.grid[12,9].on_click(play_current_seq)

        
        # next candidate
        self.grid[10,8] = create_button('Next'.format(""), 'warning')
        def next_chord(b):
            self.toggle.next_chord()
            with self.output:
                clear_output()
                print(self.toggle.chord_info())
        self.grid[10,8].on_click(next_chord)


        # previous candidate
        self.grid[10,7] = create_button('Prev'.format(""), 'warning')
        def prev_chord(b):
            self.toggle.prev_chord()
            with self.output:
                clear_output()
                print(self.toggle.chord_info())
        self.grid[10,7].on_click(prev_chord)


        # solution toggle
        self.grid[9,7] = create_button('Prev'.format(""), 'danger')
        def prev_solution(b):
            with self.output:
                clear_output()
                print(self.toggle.prev_solution())
        self.grid[9,7].on_click(prev_solution)

        self.grid[9,8] = create_button('Next'.format(""), 'danger')
        def next_solution(b):
            with self.output:
                clear_output()
                print(self.toggle.next_solution())
        self.grid[9,8].on_click(next_solution)

        self.grid[9,9] = create_button('Solution Info'.format(""), 'info')
        def solution_info(b):
            with self.output:
                clear_output()
                print(self.toggle.solution_info())
        self.grid[9, 9].on_click(solution_info)

        #Chord Sequence
        self.grid[9,0] = create_button('Insert Chord'.format(""), 'danger')
        def insert_chord(b):
            self.toggle.insert_chord()
        self.grid[9,0].on_click(insert_chord)

        self.grid[10,0] = create_button('Remove'.format(""), 'warning')
        def reset_chord(b):
            self.toggle.remove_chord()
        self.grid[10,0].on_click(reset_chord)
        
        self.grid[11,0] = create_button('Reset'.format(""), 'danger')
        def reset_chord(b):
            self.toggle.reset_chord()
        self.grid[11,0].on_click(reset_chord)


        self.grid[13,8] = create_button('Seq Info'.format(""), 'info')
        def seq_info(b):
            with self.output:
                clear_output()
                print(self.toggle.seq_info())
        self.grid[13,8].on_click(seq_info)
        
        self.grid[13,7] = create_button('Seq Chord'.format(""), 'info')
        def seq_chord_info(b):
            with self.output:
                clear_output()
                print(self.toggle.seq_chord_info())


        self.grid[13,7].on_click(seq_chord_info)


        self.grid[13,6] = create_button('Seq Score'.format(""), 'primary')
        def chord_seq_score(b):
            with self.output:
                clear_output()
                s = self.toggle.chord_seq_score()
                s.show()
        self.grid[13,6].on_click(chord_seq_score)


        # self.grid[12,9] = create_button('Play Cur'.format(""), 'info')
        # def play_current(b):
        #     with self.output:
        #         clear_output()
        #         print(self.toggle.seq_chord_info())
        #         self.toggle.play_current()




        self.grid[13,9] = create_button('Play Seq'.format(""), 'primary')
        def play_sequence(b):
            with self.output:
                self.toggle.play_sequence()
        self.grid[13,9].on_click(play_sequence)


        self.grid[12,8] = create_button('Next'.format(""), 'success')
        def next_seq_chord(b):
            self.toggle.next_seq_chord()
            with self.output:
                clear_output()
                print(self.toggle.seq_chord_info())
        self.grid[12,8].on_click(next_seq_chord)


        # previous candidate
        self.grid[12,7] = create_button('Prev'.format(""), 'success')
        def prev_seq_chord(b):
            self.toggle.prev_seq_chord()
            with self.output:
                clear_output()
                print(self.toggle.seq_chord_info())
        self.grid[12,7].on_click(prev_seq_chord)



        tone_idx = 1
        #FM tones
        for i in range(6):
            for j in range(10):
                if tone_idx <= 25:
                    self.tone_type = "fm_sum"
                    b = create_button('Sum {}'.format(tone_idx), 'info')
                    self.grid[i, j] = b
                elif tone_idx > 30:
                    self.tone_type = "fm_diff"
                    b = create_button('Diff {}'.format(tone_idx-30), 'success')
                    self.grid[i, j] = b
                tone_idx += 1
        
        #OT tones
        tone_idx = 1
        self.tone_type = "ot_par"
        for i in range(6, 9):
            for j in range(10):
                b = create_button('Partial {}'.format(tone_idx), 'primary')
                if tone_idx == 1:
                    b = create_button('Fund'.format(""), 'warning')
                self.grid[i, j] = b
                tone_idx += 1


    
        display(self.grid)
        display(self.output)


        self.grid[2,5] = create_button('- Carrier - '.format(""), 'warning')
        def play_carrier(b):
            self.toggle.play_carrier()
        self.grid[2,5].on_click(play_carrier)

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
        self.grid[0,5].on_click(play_sb6_sum)

        def play_sb7_sum(b):
            self.toggle.play_sum_sb7()
        self.grid[0,6].on_click(play_sb7_sum)

        def play_sb8_sum(b):
            self.toggle.play_sum_sb8()
        self.grid[0,7].on_click(play_sb8_sum)

        def play_sb9_sum(b):
            self.toggle.play_sum_sb9()
        self.grid[0,8].on_click(play_sb9_sum)

        def play_sb10_sum(b):
            self.toggle.play_sum_sb10()
        self.grid[0,9].on_click(play_sb10_sum)


        def play_sb11_sum(b):
            self.toggle.play_sum_sb11()
        self.grid[1,0].on_click(play_sb11_sum)

        def play_sb12_sum(b):
            self.toggle.play_sum_sb12()
        self.grid[1,1].on_click(play_sb12_sum)

        def play_sb13_sum(b):
            self.toggle.play_sum_sb13()
        self.grid[1,2].on_click(play_sb13_sum)

        def play_sb14_sum(b):
            self.toggle.play_sum_sb14()
        self.grid[1,3].on_click(play_sb14_sum)

        def play_sb15_sum(b):
            self.toggle.play_sum_sb15()
        self.grid[1,4].on_click(play_sb15_sum)


        def play_sb16_sum(b):
            self.toggle.play_sum_sb16()
        self.grid[1,5].on_click(play_sb16_sum)

        def play_sb17_sum(b):
            self.toggle.play_sum_sb17()
        self.grid[1,6].on_click(play_sb17_sum)

        def play_sb18_sum(b):
            self.toggle.play_sum_sb18()
        self.grid[1,7].on_click(play_sb18_sum)

        def play_sb19_sum(b):
            self.toggle.play_sum_sb19()
        self.grid[1,8].on_click(play_sb19_sum)

        def play_sb20_sum(b):
            self.toggle.play_sum_sb20()
        self.grid[1,9].on_click(play_sb20_sum)


        def play_sb21_sum(b):
            self.toggle.play_sum_sb21()
        self.grid[2,0].on_click(play_sb21_sum)

        def play_sb22_sum(b):
            self.toggle.play_sum_sb22()
        self.grid[2,1].on_click(play_sb22_sum)

        def play_sb23_sum(b):
            self.toggle.play_sum_sb23()
        self.grid[2,2].on_click(play_sb23_sum)

        def play_sb24_sum(b):
            self.toggle.play_sum_sb24()
        self.grid[2,3].on_click(play_sb24_sum)

        def play_sb25_sum(b):
            self.toggle.play_sum_sb25()
        self.grid[2,4].on_click(play_sb25_sum)


        # diff tones
        def play_sb1_diff(b):
            self.toggle.play_diff_sb1()
        self.grid[3,0].on_click(play_sb1_diff)

        def play_sb2_diff(b):
            self.toggle.play_diff_sb2()
        self.grid[3,1].on_click(play_sb2_diff)

        def play_sb3_diff(b):
            self.toggle.play_diff_sb3()
        self.grid[3,2].on_click(play_sb3_diff)

        def play_sb4_diff(b):
            self.toggle.play_diff_sb4()
        self.grid[3,3].on_click(play_sb4_diff)

        def play_sb5_diff(b):
            self.toggle.play_diff_sb5()
        self.grid[3,4].on_click(play_sb5_diff)


        def play_sb6_diff(b):
            self.toggle.play_diff_sb6()
        self.grid[3,5].on_click(play_sb6_diff)

        def play_sb7_diff(b):
            self.toggle.play_diff_sb7()
        self.grid[3,6].on_click(play_sb7_diff)

        def play_sb8_diff(b):
            self.toggle.play_diff_sb8()
        self.grid[3,7].on_click(play_sb8_diff)

        def play_sb9_diff(b):
            self.toggle.play_diff_sb9()
        self.grid[3,8].on_click(play_sb9_diff)

        def play_sb10_diff(b):
            self.toggle.play_diff_sb10()
        self.grid[3,9].on_click(play_sb10_diff)


        def play_sb11_diff(b):
            self.toggle.play_diff_sb11()
        self.grid[4,0].on_click(play_sb11_diff)

        def play_sb12_diff(b):
            self.toggle.play_diff_sb12()
        self.grid[4,1].on_click(play_sb12_diff)

        def play_sb13_diff(b):
            self.toggle.play_diff_sb13()
        self.grid[4,2].on_click(play_sb13_diff)

        def play_sb14_diff(b):
            self.toggle.play_diff_sb14()
        self.grid[4,3].on_click(play_sb14_diff)

        def play_sb15_diff(b):
            self.toggle.play_diff_sb15()
        self.grid[4,4].on_click(play_sb15_diff)


        def play_sb16_diff(b):
            self.toggle.play_diff_sb16()
        self.grid[4,5].on_click(play_sb16_diff)

        def play_sb17_diff(b):
            self.toggle.play_diff_sb17()
        self.grid[4,6].on_click(play_sb17_diff)

        def play_sb18_diff(b):
            self.toggle.play_diff_sb18()
        self.grid[4,7].on_click(play_sb18_diff)

        def play_sb19_diff(b):
            self.toggle.play_diff_sb19()
        self.grid[4,8].on_click(play_sb19_diff)

        def play_sb20_diff(b):
            self.toggle.play_diff_sb20()
        self.grid[4,9].on_click(play_sb20_diff)


        def play_sb21_diff(b):
            self.toggle.play_diff_sb21()
        self.grid[5,0].on_click(play_sb21_diff)

        def play_sb22_diff(b):
            self.toggle.play_diff_sb22()
        self.grid[5,1].on_click(play_sb22_diff)

        def play_sb23_diff(b):
            self.toggle.play_diff_sb23()
        self.grid[5,2].on_click(play_sb23_diff)

        def play_sb24_diff(b):
            self.toggle.play_diff_sb24()
        self.grid[5,3].on_click(play_sb24_diff)

        def play_sb25_diff(b):
            self.toggle.play_diff_sb25()
        self.grid[5,4].on_click(play_sb25_diff)


        def play_sb26_diff(b):
            self.toggle.play_diff_sb26()
        self.grid[5,5].on_click(play_sb26_diff)

        def play_sb27_diff(b):
            self.toggle.play_diff_sb27()
        self.grid[5,6].on_click(play_sb27_diff)

        def play_sb28_diff(b):
            self.toggle.play_diff_sb28()
        self.grid[5,7].on_click(play_sb28_diff)

        def play_sb29_diff(b):
            self.toggle.play_diff_sb29()
        self.grid[5,8].on_click(play_sb29_diff)

        def play_sb30_diff(b):
            self.toggle.play_diff_sb30()
        self.grid[5,9].on_click(play_sb30_diff)


        #OT
        def play_ot_fund(b):
            self.toggle.play_ot_part1()
        self.grid[6,0].on_click(play_ot_fund)

        def play_ot_part2(b):
            self.toggle.play_ot_part2()
        self.grid[6,1].on_click(play_ot_part2)

        def play_ot_part3(b):
            self.toggle.play_ot_part3()
        self.grid[6,2].on_click(play_ot_part3)

        def play_ot_part4(b):
            self.toggle.play_ot_part4()
        self.grid[6,3].on_click(play_ot_part4)

        def play_ot_part5(b):
            self.toggle.play_ot_part5()
        self.grid[6,4].on_click(play_ot_part5)


        def play_ot_part6(b):
            self.toggle.play_ot_part6()
        self.grid[6,5].on_click(play_ot_part6)

        def play_ot_part7(b):
            self.toggle.play_ot_part7()
        self.grid[6,6].on_click(play_ot_part7)

        def play_ot_part8(b):
            self.toggle.play_ot_part8()
        self.grid[6,7].on_click(play_ot_part8)

        def play_ot_part9(b):
            self.toggle.play_ot_part9()
        self.grid[6,8].on_click(play_ot_part9)

        def play_ot_part10(b):
            self.toggle.play_ot_part10()
        self.grid[6,9].on_click(play_ot_part10)


        def play_ot_part11(b):
            self.toggle.play_ot_part11()
        self.grid[7,0].on_click(play_ot_part11)

        def play_ot_part12(b):
            self.toggle.play_ot_part12()
        self.grid[7,1].on_click(play_ot_part12)

        def play_ot_part13(b):
            self.toggle.play_ot_part13()
        self.grid[7,2].on_click(play_ot_part13)

        def play_ot_part14(b):
            self.toggle.play_ot_part14()
        self.grid[7,3].on_click(play_ot_part14)

        def play_ot_part15(b):
            self.toggle.play_ot_part15()
        self.grid[7,4].on_click(play_ot_part15)


        def play_ot_part16(b):
            self.toggle.play_ot_part16()
        self.grid[7,5].on_click(play_ot_part16)

        def play_ot_part17(b):
            self.toggle.play_ot_part17()
        self.grid[7,6].on_click(play_ot_part17)

        def play_ot_part18(b):
            self.toggle.play_ot_part18()
        self.grid[7,7].on_click(play_ot_part18)

        def play_ot_part19(b):
            self.toggle.play_ot_part19()
        self.grid[7,8].on_click(play_ot_part19)

        def play_ot_part20(b):
            self.toggle.play_ot_part20()
        self.grid[7,9].on_click(play_ot_part20)


        def play_ot_part21(b):
            self.toggle.play_ot_part21()
        self.grid[8,0].on_click(play_ot_part21)

        def play_ot_part22(b):
            self.toggle.play_ot_part22()
        self.grid[8,1].on_click(play_ot_part22)

        def play_ot_part23(b):
            self.toggle.play_ot_part23()
        self.grid[8,2].on_click(play_ot_part23)

        def play_ot_part24(b):
            self.toggle.play_ot_part24()
        self.grid[8,3].on_click(play_ot_part24)

        def play_ot_part25(b):
            self.toggle.play_ot_part25()
        self.grid[8,4].on_click(play_ot_part25)


        def play_ot_part26(b):
            self.toggle.play_ot_part26()
        self.grid[8,5].on_click(play_ot_part26)

        def play_ot_part27(b):
            self.toggle.play_ot_part27()
        self.grid[8,6].on_click(play_ot_part27)

        def play_ot_part28(b):
            self.toggle.play_ot_part28()
        self.grid[8,7].on_click(play_ot_part28)

        def play_ot_part29(b):
            self.toggle.play_ot_part29()
        self.grid[8,8].on_click(play_ot_part29)

        def play_ot_part30(b):
            self.toggle.play_ot_part30()
        self.grid[8,9].on_click(play_ot_part30)



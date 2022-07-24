init:
	pip install -r requirements.txt

test: test_note test_chord test_gliss test_gliss_cmpr test_music21

test_note:
	python -m unittest tests/note_tests.py

test_chord:
	python -m unittest tests/chord_tests.py

test_gliss:
	python -m unittest tests/gliss_tests.py

test_gliss_cmpr:
	python -m unittest tests/gliss_cmpr_tests.py

test_music21:
	python -m unittest tests/music21_tests.py
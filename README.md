# Glissandi Harmonic Relations Calculator in Python
Calculates the chordal relationship between two or more independent glissandi.  Lilypond integration to display score instead of text representation, not yet implemented 

## Table of Contents

- [Introduction](#introduction)
- [Useful Music Links](#useful-music-links)
- [Getting Started](#getting-started)
- [Class List](#class-list)
- [Authors](#authors)
- [License](#license)
- [Acknowledgments](#acknowledgments)




## Introduction
The motivation for this project started out of a desire to move beyond the vertically structured harmonic tendencies of the Spectral Music school.  I greatly admire the work of Gerard Grisey and Tristan Murail and wanted to see if a more horizontal approach to frequency based composition was possible.  Mass structure composers like Ligeti and Cerha and more recently Jay Schwartz and Georg Friedrich Haas employ various polyphonic structures, one of which is the slowly evolving glissandi structure. 

The goal of this program is to allow the user to calculate these structures quickly and isolate important harmonic moments.  Once moments are isolated the user will be able to perform various operations on a a given chord:nearest overtone chord, sum and difference tone calculations.  

## Useful Music Links

### Music Theory
- [Glissando (Wikipedia)](https://en.wikipedia.org/wiki/Glissando)
- [Harmony (Wikipedia)](https://en.wikipedia.org/wiki/Harmony)
- [Counterpoint (Wikipedia)](https://en.wikipedia.org/wiki/Counterpoint)
- [Spectral Music (Wikipedia)](https://en.wikipedia.org/wiki/Spectral_music)
- [Shepard Tone (Wikipedia)](https://en.wikipedia.org/wiki/Shepard_tone)
- [Shepard Tone Sound Example](https://www.youtube.com/watch?v=T-A0gg1kVrg)


### Composers

- [Jean-Claude Risset (Wikipedia)](https://en.wikipedia.org/wiki/Jean-Claude_Risset)
- [Gérard Grisey (Wikipedia)](https://en.wikipedia.org/wiki/Gérard_Grisey)
- [Tristan Murail (Wikipedia)](https://en.wikipedia.org/wiki/Tristan_Murail)
- [György Ligeti (Wikipedia)](https://en.wikipedia.org/wiki/György_Ligeti)
- [Friedrich Cerha (Wikipedia)](https://en.wikipedia.org/wiki/Friedrich_Cerha)
- [Georg Friedrich Haas (Wikipedia)](https://en.wikipedia.org/wiki/Georg_Friedrich_Haas)
- [Jay Schwartz (Wikipedia)](https://en.wikipedia.org/wiki/Jay_Schwartz)


### Musical Examples

- [Grisey: Partiels](https://www.youtube.com/watch?v=GRRwk3hwrDI)
- [Murail: Les courants de l'espace](https://www.youtube.com/watch?v=e5tOhMPqmQo)
- [Ligeti: Atmospheres](https://www.youtube.com/watch?v=9XfefKJRoSA)
- [Cerha: Spiegel II](https://www.youtube.com/watch?v=ZJxIWmYiHPc)
- [Haas: Limited Approximations](https://www.youtube.com/watch?v=BoqvGLdjUhE&t=1309s)
- [Schwartz: Music for Orchestra](https://www.youtube.com/watch?v=WuogXAgt2u4)


## Getting Started
- Clone the repository. 
- Create at least two gliddandi objects and use the GlissCmpr object to create a comparison. 


## Class List

### Note.py
Notes are divided into 24 steps rather than 12 to allow a quarter tone equally tempered scale


### Chord.py
Accepts Arrays of Notes as an argument


### Gliss.py
Accepts a start note and an end note as arguments.  Creates an array of notes with quarter note resolution between the two notes

### GlissCmpr.py
Takes a variable number of glissandi as arguments and calculates the chordal relationship between them.


## Authors

* **Ryan Beppel** - *Initial work* - [rgxb2807](https://github.com/rgxb2807)


## License

see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

A big thank you to the composers listed above for inspiring this project.

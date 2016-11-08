# Language-Creator

This is an interactive Python script.

This script creates a randoly-generated laguage, and then pdf's a randomly-generated story from it.

It should work on linux with any tex interpreter which can pdflatex.

It still makes semi-gibberish, but we switched to creating words based on a syllable schema, with a prebuilt matrix of allowed sound transitions.


ChangeLog:

update 2: changed the way words are constructed again, based on syllables and allowed sound transitions.  Soundspaces are now freq for start/ed on vowel/consonant and indiv. sound frequencies, which is manageable for someone to create.

update 1: changed the way words are constructed to flow more naturally between vowels and consonants.  Still work to be done on, i.e., starting words with 'rs' or other equivalent weirdnessess.

#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende

"""This module contains rules taken
from http://openmusictheory.com/cantusFirmus.html
to compose a good cantus firmus"""

import error
import note
import stave

def rule_1(s: stave.Stave): # TEST
    """Length of about 8 - 16 notes"""
    if not (8 <= len(s) <= 16):
        raise error.CompositionError("Length of the cantus firmus should be between 8 and 16.",s)

def rule_2(s: stave.Stave):
    """
    arhythmic (all whole notes; no long or short notes)
    """
    for n in s:
        if n.duration != note.Duration.SEMIBREVE:
            raise error.CompositionError("Whole notes only are permitted",n)

def rule_3(s: stave.Stave):
    """
    begin and end on do
    """
    pass

def rule_4(s: stave.Stave):
    """
    approach final tonic by step (usually re - do, sometimes ti - do
    """
    pass

def rule_5(s: stave.Stave):
    """
    all note-to-note progressions are melodic consonances
    """
    pass

def rule_6(s: stave.Stave):
    """
    range (interval between lowest and highest notes) of no more than a tenth, usually less than an octave
    """
    pass

def rule_7(s: stave.Stave):
    """
    a single climax (high point) that appears only once in the melody
    """
    pass

def rule_8(s: stave.Stave):
    """
    clear logical connection and smooth shape from beginning to climax to ending
    """
    pass

def rule_9(s: stave.Stave):
    """
    mostly stepwise motion, but with some leaps (mostly small leaps
    """
    pass

def rule_10(s: stave.Stave):
    """
    no repetition of "motives" or "licks"
    """
    pass

def rule_11(s: stave.Stave):
    """
    any large leaps (fourth or larger) are followed by step in opposite direction
    """
    pass

def rule_12(s: stave.Stave):
    """
    no more than two leaps in a row; no consecutive leaps in the same direction
    """
    pass

def rule_13(s: stave.Stave):
    """
    the leading tone progresses to the tonic
    """
    pass

def rule_14(s: stave.Stave):
    """
    in minor, the leading tone only appears in the penultimate bar; the raised submediant is only used when progressing to that leading tone
    """
    pass

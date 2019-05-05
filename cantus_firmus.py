#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende

"""This module contains rules taken
from http://openmusictheory.com/cantusFirmus.html
to compose a good cantus firmus"""

import error
import note
import stave
from scalenote import NoteScale as NS

def rule_1(s: stave.Stave): # TEST
    """Length of about 8 - 16 notes"""
    if not (8 <= len(s) <= 16):
        raise error.CompositionError("Length of the cantus firmus should be between 8 and 16.",s)

def rule_2(s: stave.Stave): # TEST
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
    if not (s.scale.isTonic(s.notes[0].pitch) and s.scale.isTonic(s.notes[-1].pitch)):
        raise error.CompositionError("The first and the last note must be a do",s[0],s[-1])

def rule_4(s: stave.Stave):
    """
    approach final tonic by step (usually re - do, sometimes ti - do
    """
    penultimate = NS(s.scale,s.notes[-2])
    if not (penultimate.isSupertonic or penultimate.isLeading):
            raise error.CompositionError("The penultimate note should be a re or a ti",penultimate)

    last = NS(s.scale, s.notes[-1])
    if abs(penultimate.distanceWith(last)) != 1:
        raise error.CompositionError("The penultimate note should be at one step of the lst one",penultimate, last)

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

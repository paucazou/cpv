#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende

"""This module contains rules taken
from http://openmusictheory.com/cantusFirmus.html
to compose a good cantus firmus"""

import error
import note
import scale
import stave
import tools
from scalenote import NoteScale as NS

def __extract_data(fun):
    def wrapper(data):
        return fun(data[0])
    return wrapper


@__extract_data
def rule_1(s: stave.Stave): # TEST
    """Length of about 8 - 16 notes"""
    if not (8 <= len(s) <= 16):
        raise error.CompositionError(f"Length of the cantus firmus should be between 8 and 16. Current length: {len(s)}",s)

@__extract_data
def rule_2(s: stave.Stave): # TEST
    """
    arhythmic (all whole notes; no long or short notes)
    """
    for n in s:
        if n.duration != note.Duration.SEMIBREVE.value:
            raise error.CompositionError("Whole notes only are permitted",n)

@__extract_data
def rule_3(s: stave.Stave):
    """
    begin and end on do
    """
    if not (s.scale.isTonic(s.notes[0].pitch) and s.scale.isTonic(s.notes[-1].pitch)):
        raise error.CompositionError("The first and the last note must be a do",s[0],s[-1])

@__extract_data
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

@__extract_data
def rule_5(s: stave.Stave):
    """
    all note-to-note progressions are melodic consonances
    """
    previous = None
    for n in s.notes:
        n = n.pitch
        if previous is not None and (not previous.isMelodicConsonantWith(n)):
            raise error.CompositionError("Melodic consonances only",previous,n)
        previous = n

@__extract_data
def rule_6(s: stave.Stave):
    """
    range (interval between lowest and highest notes) of no more than a tenth, usually less than an octave
    """
    min, max = tools.min_max(s)
    if min.intervalWith(max) > 10:
        raise error.CompositionError("The range should be no more than a tenth",min,max)
    if min.intervalWith(max) > 8:
        error.warn("It is a good thing to keep the range in an octave",min,max)

@__extract_data
def rule_7(s: stave.Stave): # TEST
    """
    a single climax (high point) that appears only once in the melody
    """
    max = tools.min_max(s).max
    nb = 0
    for n in s:
        if n.pitch == max:
            nb += 1

    if nb > 1:
        raise error.CompositionError(f"There should be only one climax. Here, {max} is found {nb} time{s if nb > 1 else ''}")

@__extract_data
def rule_8(s: stave.Stave):
    """
    clear logical connection and smooth shape from beginning to climax to ending
    """
    # WARNING This rule can be considered too vague to be implemented

@__extract_data
def rule_9(s: stave.Stave):
    """
    mostly stepwise motion, but with some leaps (mostly small leaps)
    """
    previous = None
    steps = {}

    for n in s.notes:
        p = n.pitch
        if previous is not None:
            interval = p.intervalWith(previous)
            val = steps.get(interval,0)
            val += 1
            steps[interval] = val
        previous = p

    stepwise = steps.get(1,0) + steps.get(2,0)
    if  stepwise < (len(s) / 2):
        raise error.CompositionError(f"The cantus firmus must be mostly stepwise motion. Number of steps of 2 or 1: {stepwise}")

    if max(steps.keys()) > 4:
        error.warn("The cantus firmus must be with mostly small leaps.",steps)

    if max(steps.keys()) <= 2:
        error.warn("The cantus firmus should contain at least some (small) leaps")



@__extract_data
def rule_10(s: stave.Stave):
    """
    no repetition of "motives" or "licks"
    """
    from cp2_note_against_note import _Rule_10
    _Rule_10(s)

@__extract_data
def rule_11(s: stave.Stave):
    """
    any large leaps (fourth or larger) are followed by step in opposite direction
    """
    previous = None
    for i,n in enumerate(s):
        p = n.pitch
        if previous is not None and previous.intervalWith(p) > 4:
            if i + 1 == len(s) or tools.is_same_direction(previous,p,s.notes[i+1].pitch):
                raise error.CompositionError("A large leap must be followed by a step in another direction",previous,p,s.notes[i+1].pitch)


@__extract_data
def rule_12(s: stave.Stave):
    """
    no more than two leaps in a row; no consecutive leaps in the same direction
    """
    previous = None
    leap_nb = 0
    leaps = []

    for n in s.notes:
        p = n.pitch
        if previous is not None:
            if previous.intervalWith(p) > 2:
                leap_nb += 1
                leaps.append((previous,p))
                if len(leaps) == 2 and tools.is_same_direction(*leaps[0],p):
                    raise error.CompositionError("No consecutive leaps in the same direction",leaps)
            else:
                leap_nb = 0
                leaps = []

            if leap_nb > 2:
                raise error.CompositionError("No more than two leaps in a row",leaps)


        previous = p

@__extract_data
def rule_13(s: stave.Stave):
    """
    the leading tone progresses to the tonic
    """
    for i,n in enumerate(s.notes):
        ns = NS(s.scale,n)
        if ns.isLeading and ((i == len(s) -1) or (not NS(s.scale,s.notes[i+1]).isTonic)):
            raise error.CompositionError("The leading should progress to the tonic",ns)


@__extract_data
def rule_14(s: stave.Stave):
    """
    in minor, the leading tone only appears in the penultimate bar;
    the raised submediant is only used when progressing to that leading tone
    """
    # minor?
    if s.scale.mode not in (scale.Mode.m,scale.Mode.m_full,scale.Mode.m_rising,scale.Mode.m_full):
        return

    # minor: the leading at the end
    for i,n in enumerate(s.notes):
        ns = NS(s.scale,n)
        if ns.isLeading and i != len(s) -2:
            raise error.CompositionError("In minor, the leading tone must be at the penultimate bar only",n)

    # minor: the raised submediant used when progressing to leading
    for i,n in enumerate(s.notes):
        ns = NS(s.scale,n)
        if ns.isRaisedSubmediant and ((i + 1 == len(s)) or not NS(s.notes[i+1]).isLeading):
            raise error.CompositionError("Raised submediant should be used before leadingtone only",ns)

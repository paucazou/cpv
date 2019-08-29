#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende
"""This module contains only melodic rules.
Errors are reported as warnings"""
import error
import note
import rest
import re
import scale
import stave
import tessitura
import tools
import util

def no_more_than(s : stave.Stave, x:int) -> bool:
    """s is a pure melody. 
    Warn if one note is used more
    than x times in a row
    """
    nb = 0
    previous = None
    for i, n in enumerate(s.notes):
        pn = util.to_pitch(n)
        if i != 0 and pn == previous:
            nb += 1
        else:
            nb = 0
        if nb >= x:
            error.warn(f"It is forbidden to use the same note more than {x} times if a row",n,s.findBarOf(n))
        previous = pn


def allowed_intervals(s : stave.Stave, *intervals):
    """Checks that only allowed intervals are used
    in s. Warn if not true.
    Intervals are entered as a sequence of pairs:
    (interval,qualification) = (3,"minor")
    See pitch.py for exact syntax.
    """
    for n1, n2 in util.pairwise(s):
        if not n1.pitch.isQualifiedInterval(*intervals).With(n2.pitch):
            error.warn(f"Interval forbidden: {n1.qualifiedIntervalWith(n2)}",n1,n2)

def forbidden_intervals(s : stave.Stave, *intervals):
    """Same as allowed_intervals, but for forbidden
    ones"""
    for n1, n2 in util.pairwise(s):
        if n1.pitch.isQualifiedInterval(*intervals).With(n2.pitch):
            error.warn(f"Following intervals are forbidden: {intervals}.",n1, n2)

def allow_under_major_sixth(s : stave.Stave):
    """Wrapper of allowed_intervals.
    Allow under major sixth and octaves
    """
    allow_under_minor_sixth(s,(6,"major"))

def allow_under_minor_sixth(s : stave.Stave,*intervals):
    """Wrapper of allowed_intervals.
    Allow under minor sixth, + octaves, + intervals.
    Only major, minor and perfect
    """
    allowed_intervals(s,*intervals,
            (2,"minor"),
            (2,"major"),
            (3,"minor"),
            (3,"major"),
            (4,"perfect"),
            (5,"perfect"),
            (6,"minor"),
            (8,"perfect"))

def forbid_augmented_and_seventh(s : stave.Stave, *intervals):
    """Forbid sevenths, fourth and fifth augmented or diminished
    and intervals"""
    forbidden_intervals(s,
            (7,"minor"),
            (7,"major"),
            (4,"augmented"),
            (5,"diminished"))

def forbid_chromatism(s : stave.Stave):
    """Warn if chromatic motion is used in s"""
    for n1, n2 in util.pairwise(s):
        if n1.pitch.isChromaticInflectionWith(n2.pitch):
            error.warn(f"Chromatic inflection is forbidden",n1,n2)

def max_interval(s : stave.Stave, maximum, tolerance=[]):
    """Warn if the melody has gap over maximum.
    tolerance is the intervals tolerated only.
    User is warned of that thing
    """
    res = tools.min_max(s)
    min = res.min
    max = res.max
    if max.intervalWith(min) in tolerance:
        error.warn(f"The melody can exceed {tolerance} by tolerance only", s)
    if max.intervalWith(min) > maximum:
        error.warn(f"The melody can not exceed {maximum} gap",s)

def better_conjunct(s : stave.Stave):
    """Warn when disjunct movement is used"""
    for n1, n2 in util.pairwise(s):
        if n1.pitch.intervalWith(n2.pitch) > 2:
            error.warn("It is better to avoid disjunct motion",n1,n2, f"in {s.title}")

def transposition(source : stave.Stave, target : stave.Stave):
    """Transposition is allowed if not outside a voice
    """
    T = tessitura

    valid_tessitura = False
    for tess in (T.soprano,T.tenor,T.bass,T.alto):
        if target in tess:
            valid_tessitura = True
            break

    if not valid_tessitura:
        error.warn("The melody transposed is too high or too low",target)

    # check the transposition is correct
    def _semitone_sum(n,n2):
        return n.pitch.value.semitone - n2.pitch.value.semitone

    for i, (b1, b2) in enumerate(zip(target,source)):
        if i + 1 == len(target):
            break
        if _semitone_sum(b1,target[i+1]) != _semitone_sum(b2,source[i+1]):
            error.warn("Melody transposed doesn't match with original melody",b1,b2)

def relative_modulation(s : stave.Stave):
    """Modulation allowed only if it is the relative one"""
    sc = scale.Scale(s.keynote,s.mode)
    relative = sc.relative(scale.Mode.m_full)
    for n in s:
        if n.pitch not in sc and n.pitch not in relative:
            error.warn("It is forbidden to modulate outside the relative key",n)

def rythmic_pattern(s : stave.Stave, pattern : str):
    """True if it matches the pattern
    How it works:
    s is changed to a string with duration only. See rests and notes
    for names. Rests are preceded by 'R', notes by 'N'.
    pattern must be a regex that match s.
    see tools.get_rythmic_string for more details
    """
    string = tools.get_rythmic_string(s)
    return re.fullmatch(pattern,string)


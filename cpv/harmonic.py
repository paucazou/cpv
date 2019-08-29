#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende
"""Harmonic rules. Warn only"""

import error
import motion
import pitch
import re
import tools
import util

def perfect_at_pos(pos, s1, s2):
    """True if s1 and s2 form a perfect consonance
    at position pos.
    Warn if not"""
    n1, n2 = s1[pos], s2[pos]
    return util.to_pitch(n1).isPerfectlyConsonantWith(util.to_pitch(n2))

def perfect_start(s1, s2):
    """Wrapper of perfect_at_pos for the first notes."""
    return perfect_at_pos(0,s1,s2)

def perfect_end(s1, s2):
    """Wrapper of perfect_at_pos for the last notes"""
    return perfect_at_pos(-1,s1,s2)

def intersection(s1, s2):
    """True if the two melodies intersect.
    Warn at every point intersection is found"""
    state = None
    for notes in tools.iter_melodies(s1,s2):
        pnotes = [util.to_pitch(n) for n in notes]
        if len(notes) == 1 or pnotes[0] == pnotes[1]:
            continue
        new_state = pnotes[0] < pnotes[1]
        if state is not None and new_state is not state:
            error.warn(f"Melodies intersect.",*notes)
        state = new_state

def forbid_consecutive_interval(s1, s2, interval):
    """Warn if two intervals of the same type are consecutive
    Interval must be qualified"""
    for (na,n1), (nb, n2) in zip(util.pairwise(s1), util.pairwise(s2)):
        nap, nbp, n1p, n2p = [util.to_pitch(x) for x in (na, nb, n1, n2)]
        if nap.isQualifiedInterval(interval).With(n1p) and nbp.isQualifiedInterval(interval).With(n2p):
            error.warn(f"Two {interval} in a row are forbidden",na,nb,n1,n2,f"in {s1.title} and {s2.title}")

def forbid_consecutive_octaves(s1,s2):
    return forbid_consecutive_interval(s1,s2,(8,"perfect"))

def forbid_consecutive_fifths(s1,s2):
    return forbid_consecutive_interval(s1,s2,(5,"perfect"))

def forbid_direct_interval(s1, s2, *intervals):
    """Warns if interval occured by direct motion
    intervals must be qualified or not """
    for (na,n1), (nb, n2) in util.pairwise(tools.iter_melodies(s1,s2,all=True)):
        nap, nbp, n1p, n2p = [util.to_pitch(x) for x in (na, nb, n1, n2)]

        answer = nbp.isQualifiedInterval(*intervals).With(n2p) if not isinstance(intervals[0],int) else nbp.isInterval(*intervals,True).With(n2p)

        if answer and (motion.MotionType.motion(na,n1,nb,n2) == motion.MotionType.direct):
            error.warn(f"It is forbidden to go to direct {intervals}",na,nb,n1,n2,f"in {s1.title} and {s2.title}")

def calculate_motion_types(s1, s2):
    """Finds the number of motion type: direct, contrary
    and oblique"""
    movs = { motion.MotionType.direct : 0,
            motion.MotionType.contrary : 0,
            motion.MotionType.oblique : 0}

    for (na,n1), (nb, n2) in util.pairwise(tools.iter_melodies(s1,s2,alone=False)):
        nap, nbp, n1p, n2p = [util.to_pitch(x) for x in (na, nb, n1, n2)]
        movs[motion.MotionType.motion(nap,n1p,nbp,n2p)] += 1

    return movs

def forbid_false_relation_tritone(s1,s2,allow_in_minor=False):
    """
    Warn if tritone false relation is found
    """
    msg = f"False relation of tritone is forbidden. In {s1.title} and {s2.title}"
    def __fun(n1, n2):
        n1p, n2 = [util.to_pitch(x) for x in (n1,n2)]
        def __is_VI_VII_minor():
            if allow_in_minor is not True:
                return False
            if s1.scale.mode == scale.Mode.m_rising:
                _scale = s1.scale.mode
            elif s1.scale.mode == scale.Mode.m_full:
                _scale = s1.scale.mode.minor_scales[scale.Mode.m_rising]
            elif s1.scale.mode == scale.Mode.M:
                _scale = s1.scale.mode.relative(scale.Mode.m_rising)
            else:
                return False 
            return _scale.isDegree(n1,6) or _scale.isDegree(n1,7) or _scale.isDegree(n2,6) or _scale.isDegree(n2,7)

        if n1p.isTritoneWith(n2p) and not __is_VI_VII_minor():
            error.warn(msg,n1,n2)

    for (na, n1), (nb, n2) in util.pairwise(tools.iter_melodies(s1,s2,all=True)):
        nap, nbp, n1p, n2p = [util.to_pitch(x) for x in (na, nb, n1, n2)]
        __fun(na,n2)
        __fun(n1,nb)

def distance_between_intervals(s1,s2,interval):
    """Generator that yields the distance between two identical intervals.
    interval can be qualified or not. If it is not, a compound interval is reduced."""
    class __distance_interval:
        def __init__(self,first_pos, last_pos, first, second):
            self.distance = last_pos - first_pos
            self.first = first
            self.second = second

    for first, second in by_two_intervals(s1,s2,interval):
        # yield pos
        f1,f2 = first
        first_pos = f1.last_pos if f1.last_pos < f2.last_pos else f2.last_pos
        l1, l2 = second
        last_pos = l1.pos if l1.pos > l2.pos else l2.pos
        yield __distance_interval(first_pos,last_pos,first,second)

def by_two_intervals(s1,s2,interval):
    """Similar to distance_between_intervals,
    but yield only the two intervals
    """
    def fun(x,y):
        if isinstance(interval,int):
            return x.pitch.isInterval(interval,True).With(y.pitch)
        return x.pitch.isQualifiedInterval(interval).With(y.pitch)

    previous_interval = None
    for n1, n2 in tools.iter_melodies(s1,s2,alone=False):
        if fun(n1,n2):
            if previous_interval is None:
                previous_interval = n1,n2
                continue
            yield previous_interval, (n1,n2)
            previous_interval = n1,n2

def interval_pattern(s1, s2, pattern : str):
    """True if it matches the pattern.
    See tools.get_interval_string for more details
    """
    string = tools.get_interval_string(s1,s2)
    return re.fullmatch(pattern,string)

def forbid_sequence(*s,min_len=2):
    """Forbids sequences in staves s.
    There must be at least one stave
    """
    assert len(s) >= 1
    notes = [part for part in tools.iter_melodies(*s)]

    for start in range(len(notes)):
        for end in range(start,len(notes)):
            if end - start < min_len:
                continue

            # try a motif
            motif = []
            for i in range(start,end+1):
                motif.extend(notes[i])

            # try a following
            part_nb = end - start + 1
            try:
                following = []
                for i in range(end+1, part_nb + end + 1):
                    following.extend(notes[i])
            except IndexError:
                break

            # is there a sequence?
            try:
                if tools.matchSequence(motif, following, s[0].scale):
                    warn(f"Sequence in {(s.title for s in s)}.",motif,following)
            except ValueError:
                continue

            










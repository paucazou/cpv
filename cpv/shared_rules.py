#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende

import error
import stave
import util

def no_more_than(s : stave.Stave, x:int) -> bool:
    """s is a pure melody. Return True if no problem.
    Raise CompositionError if one note is used more
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
            raise error.CompositionError(f"It is forbidden to use the same note more than {x} times if a row",n,s.findBarOf(n))
        previous = pn

    return True

def no_consecutive(interval : int, s1 : stave.Stave, s2 : stave.Stave) -> bool:
    """Raise error if two interval in a row
    between s1 and s2"""
    nb = 0
    for n1, n2 in zip(s1,s2):
        p1, p2 = [util.to_pitch(n) for n in (n1,n2)]
        if p1.isInterval(interval,True).With(p2):
            nb += 1
        else:
            nb = 0

        if nb >= 2:
            raise error.CompositionError(f"It is forbidden to have two {interval} in a row",n1,n2,s1.findBarOf(n1));

    return True




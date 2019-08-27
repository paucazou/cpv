#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende
import itertools

def list_finder(l, res, fall_back=None, fun=lambda x: x):
    """Find elements into the list l
    matching with result res
    following fun procedure
    If no elt can be found,
    return fall_back or, if fall_back
    is None, raise a ValueError
    """
    for elt in l:
        if fun(elt) == res:
            return elt
    if fall_back is not None:
        return fall_back
    raise ValueError("No value matchs the result expected")

def to_pitch(n):
    """Transforms a note into a pitch
    """
    try:
        return n.pitch
    except AttributeError:
        try:
            return to_pitch(n.note)
        except AttributeError:
            return n

def push_to_end(l: list) -> list: # TEST
    """Takes a list and return a new list
    with the first elemtn of l at the end
    l must contain at least one element
    """
    assert len(l) > 0
    return l[1:] + [l[0]]

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)
    

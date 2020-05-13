#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende
import itertools
import collections

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
    If it's an iterable, return an iterable
    of pitches in the same order.
    """
    if isinstance(n,collections.abc.Iterable):
        return (to_pitch(elt) for elt in n)
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

def nwise(iterable, n):
    """Same as pairwise but with n elements
    >>> for elt in nwise(range(10),3):
    ...     a,b,c = elt
    ...     print(a,b,c)
    ... 
    0 1 2
    1 2 3
    2 3 4
    3 4 5
    4 5 6
    5 6 7
    6 7 8
    7 8 9
    >>> for elt in nwise(range(15),4):
    ...     print(*elt)
    ... 
    0 1 2 3
    1 2 3 4
    2 3 4 5
    3 4 5 6
    4 5 6 7
    5 6 7 8
    6 7 8 9
    7 8 9 10
    8 9 10 11
    9 10 11 12
    10 11 12 13
    11 12 13 14
    """
    # https://stackoverflow.com/questions/54280228/how-to-iterate-n-wise-over-an-iterator-efficiently
    deq = collections.deque((),n)
    for elt in iterable:
        deq.append(elt)
        if len(deq) == n:
            yield deq
    

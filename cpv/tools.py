import scalenote
import util
from collections import namedtuple

NS = scalenote.NoteScale

def matchSequence(motif, part, scale) -> bool:
    """True if part matches the motif
    Each arg is an iterable of Note"""
    motif_ns = [ NS(scale,n.pitch) for n in motif]
    part_ns = [ NS(scale,n.pitch) for n in part]

    distance = part_ns[0].distanceWith(motif_ns[0])
    NS.moveSequence(distance, part_ns)
    return motif_ns == part_ns

def min_max(s): # TEST
    """Return the highest and the lowest
    pitch of s, which must be an iterable
    as a namedtuple of pitchs
    """
    __min_max = namedtuple("MIN_MAX",("min","max"))

    min = max = None
    for n in s:
        p = util.to_pitch(n)
        if min is None:
            min = max = p
            continue
        if p.value.step > max.value.step:
            max = p
        elif p.value.step < min.value.step:
            min = p

    return __min_max(min,max)


def is_same_direction(n1,n2,n3) -> bool: # TEST
    """
    True if the melodic direction is the same
    from n1 to n3
    """
    return n1 < n2 < n3 or n1 > n2 > n3



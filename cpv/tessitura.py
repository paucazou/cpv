#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende

import pitch
import util

class Tessitura:
    """Represents a tessitura.
    The min and max can be used
    in that tessitura.
    condoned are notes tolerated
    """
    def __init__(self,min: pitch.Pitch, max: pitch.Pitch, condoned=[]):
        self.min = min
        self.max = max
        self.condoned = condoned

    def __contains__(self, arg) -> bool: #TEST
        """True if arg is
        above min and beyond max
        condoned are not used here
        arg may be an iterable
        """

        try:
            for n in arg:
                if n not in self:
                    return False
                return True
        except TypeError:
            n = util.to_pitch(arg)
            return self.min.value.semitone <= n.value.semitone <= self.max.value.semitone

    def isCondoned(self, n: pitch.Pitch) -> bool: # TEST
        """True if in the tessitura or
        in condoned notes"""
        n = util.to_pitch(n)
        return self.__contains__(n) or n in self.condoned

    def areCondoned(self, args) -> bool:
        """Same as condoned, with
        an iterable as argument"""
        for elt in args:
            if not elt in self.isCondoned(elt):
                return False
        return True


p = pitch.Pitch

soprano = Tessitura(
        p.C4,
        p.A5,
        [p.Bb5]
            )

alto = Tessitura(
        p.F3,
        p.D5
        )

tenor = Tessitura(
        p.C3,
        p.A4,
        [p.Bb4]
        )

bass = Tessitura(
        p.F2,
        p.D4,
        [p.E2]
        )



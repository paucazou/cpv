#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende

import pitch

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

    def __contains__(self, n: pitch.Pitch) -> bool:
        """True if n is
        above min and beyond max
        condoned are not used here
        """
        return self.min.value.semitone <= n.value.semitone <= self.max.value.semitone

    def isCondoned(self, n: pitch.Pitch) -> bool:
        """True if in the tessitura or
        in condoned notes"""
        return self.__contains__(n) or n in self.condoned


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



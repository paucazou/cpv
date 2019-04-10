#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende

import note

class Tessitura:
    """Represents a tessitura.
    The min and max can be used
    in that tessitura.
    condoned are notes tolerated
    """
    def __init__(self,min: note.Note, max: note.Note, condoned=[]):
        self.min = min
        self.max = max
        self.condoned = condoned

    def __contain__(self, n: note.Note) -> bool:
        """True if n is
        above min and beyond max
        condoned are not used here
        """
        return min <= n <= max

    def isCondoned(self, n: note.Note) -> bool:
        """True if in the tessitura or
        in condoned notes"""
        return self.__contain__(n) or n in self.condoned


f_str = note.Note.fromString
soprano = Tessitura(
        f_str("C4 1 0"),
        f_str("A5 1 0"),
        [f_str("Bb5 1 0")
            )

alto = Tessitura(
        f_str("F3 1 0"),
        f_str("D5 1 0")
        )

tenor = Tessitura(
        f_str("C3 1 0"),
        f_str("A4 1 0"),
        [f_str("Bb4 1 0")]
        )

bass = Tessitura(
        f_str("F2 1 0"),
        f_str("D4 1 0"),
        [f_str("E2 1 0")]
        )



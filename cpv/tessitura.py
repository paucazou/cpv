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
        f_str("C 0 1 0"),
        f_str("A 1 1 0"),
        [f_str("B 1 1 0 b")
            )

alto = Tessitura(
        f_str("F -1 1 0"),
        f_str("D 1 1 0")
        )

tenor = Tessitura(
        f_str("C -1 1 0"),
        f_str("A 0 1 0"),
        [f_str("B 0 1 0 b")]
        )

bass = Tessitura(
        f_str("F -2 1 0"),
        f_str("D 0 1 0"),
        [f_str("E -2 1 0")]
        )



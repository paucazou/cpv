#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende

import enum
from fractions import Fraction as F
from pitch import Pitch

class Note:
    """Represents a single note"""

    @enum.unique
    class Duration(enum.Enum):
        """Represents the duration
        of the note"""
        MAXIMA = 32
        LONGA  = 16
        BREVE  = 8
        SEMIBREVE = 4
        MINIM  = 2
        CROTCHET = 1
        QUAVER = F('1/2')
        SEMIQUAVER = F('1/4')
        DEMISEMIQUAVER = F('1/8')
        HEMIDEMISEQUAVER = F('1/16')
        SEMIHEMIDEMISEMIQUAVER = F('1/32')
        DEMISEMIHEMIDEMISEMIQUAVER = F('1/64')

    @staticmethod
    def fromString(string : str):
        """Takes a string and return Note.
        Syntax is the following:
            - each element is separated by a space
            - the order is the following:
                1 - Note: A to G, followed by optional accidental:
                    b = flat, bb = double flat, s = sharp, ss = double sharp
                    Followed by the relative position to initial C.
                    Central C is C4
                2 - Duration (Crotchet=1)
                3 - Position in the stave (first=0)

            For the duration and the position,
            if they can't be expressed as an integer,
            the first part is an integral part followed
            by a fraction:
                1+1/2 -> a dotted crotchet / a note starting one time and a half after the starting of the stave

            !!!Note that withespaces are not allowed !!!
        """
        try:
            values = string.split()

            pitch = Pitch.__members__.get(values[0])

            duration = Note.__to_fraction(values[1])
            pos = Note.__to_fraction(values[2])

            return Note(pitch,pos,duration)

        except (NameError, IndexError, ValueError):
            raise SyntaxError(f"Impossible to parse string {string}")

    def __init__(self,
            pitch: Pitch,
            pos: F,
            duration: F,
            ):
        """
        pos is the position in the stave,
        which starts with 0. Each step is equal to 1,
        but we can define steps under one,
        following the duration of the previous note.
        """
        self.pitch = pitch
        self.pos = pos
        self.duration = duration

    def __repr__(self):
        return f"{self.pitch.name} {self.duration} {self.pos}"

    def _get_last_pos(self):
        """Return the last position
        of the note, including
        the starting of the following one"""
        return self.pos + self.duration

    last_pos = property(_get_last_pos)

    def __eq__(self, other):
        return self.pitch == other.pitch and self.pos == other.pos and self.duration == other.duration

    @staticmethod
    def __to_fraction(string: str) -> F:
        if '+' not in string:
            return F(string)

        elts = string.split('+')
        return F(elts[0]) + F(elts[1])


Duration = Note.Duration

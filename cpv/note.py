#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende

import enum
from pitch import Pitch

class Note:
    """Represents a single note"""

    @enum.unique
    class Duration(enum.Enum):
        """Represents the duration
        of the note"""
        #MAXIMA = 32
        #LONGA  = 16
        BREVE  = 8
        SEMIBREVE = 4
        MINIM  = 2
        CROTCHET = 1
        QUAVER = 1/2
        SEMIQUAVER = 1/4
        DEMISEMIQUAVER = 1/8
        HEMIDEMISEQUAVER = 1/16
        SEMIHEMIDEMISEMIQUAVER = 1/32
        DEMISEMIHEMIDEMISEMIQUAVER = 1/64

    Duration.symbols = {
            member : chr(value)
            for member, value in zip(list(Duration),range(119132,119141))
            }

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
        """
        try:
            values = string.split()

            pitch = Pitch.__members__.get(values[0])
            duration = eval(values[1])
            for elt in Duration.__members__.values():
                if elt.value == duration:
                    duration = elt
                    break
            else:
                raise ValueError

            pos = eval(values[2])

            return Note(pitch,pos,duration)

        except (NameError, IndexError, ValueError):
            raise SyntaxError(f"Impossible to parse string {string}")

    def __init__(self,
            pitch: Pitch,
            pos: float,
            duration: Duration,
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
        return f"{self.Duration.symbols[self.duration]}{self.pitch.name}. Stave pos: {self.pos}"

    def _get_last_pos(self):
        """Return the last position
        of the note, excluding
        the starting of the following one"""
        return self.pos + self.duration.value - 1/50

    last_pos = property(_get_last_pos)

    def __eq__(self, other):
        return self.pitch == other.pitch and self.pos == other.pos and self.duration == other.duration

    """
    def is(interval).with():
    def intervalWith() -> int;
    """

Duration = Note.Duration

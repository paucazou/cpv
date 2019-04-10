#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende

import enum

class Note:
    """Represents a single note"""
    class Pitch(enum.Enum):
        """Represents the pitch
        of the Note
        """
        C = 0
        D = 1
        E = 2
        F = 3
        G = 4
        A = 5
        B = 6

    class Accidental(enum.Enum):
        """Represents the
        accidentals of the Note"""
        NONE = "" 
        FLAT = "♭" 
        SHARP = "#"
        DOUBLE_FLAT = "♭♭"
        DOUBLE_SHARP = "##"

    class Duration(enum.Enum):
        """Represents the duration
        of the note"""
        MAXIMA = 32
        LONGA  = 16
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
        symbols = {

    def __init__(self,
            pitch: Pitch,
            height: int,
            pos: float,
            duration: Duration,
            accidental=Accidental.NONE
            ):
        """Height reprents the position
        relative to the central C, which is 0.
        -1 is the C under, +1 above.
        pos is the position in the stave,
        which starts with 0. Each step is equal to 1,
        but we can define steps under one,
        following the duration of the previous note.
        """
        self.pitch = pitch
        self.height = height
        self.pos = pos
        self.duration = duration
        self.accidental = accidental

    def __repr__(self):
        return f"{self.pitch.name}{self.accidental.value}{self.height}. Pos: {self.pos}"

    def is(interval).with():
    def intervalWith() -> int;

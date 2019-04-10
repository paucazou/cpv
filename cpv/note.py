#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende

import enum

class Note:
    """Represents a single note"""
    @enum.unique
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

        def intervalWith(self,other,negative=True) -> int:
            """Return the interval between
            self and other
            if negative is set, return the correct
            interval if other is lower pitched than self
            (ex: self=E, other=C)
            """
            if self == other:
                return 1 #unison
            if self < other or negative is False:
                return other.value - self.value + 1
            if negative is True:
                return abs(other.value + 8 - self.value)

        def __equal__(self,other):
            """True if self.value == other.value"""
            return self.value == other.value
        
        def __lt__(self,other):
            """True if self.value < other.value"""
            return self.value < other.value

    @enum.unique
    class Accidental(enum.Enum):
        """Represents the
        accidentals of the Note"""
        NONE = "" 
        FLAT = "b" 
        SHARP = "#"
        DOUBLE_FLAT = "bb"
        DOUBLE_SHARP = "x"

    Accidental.symbols = {
            member : val
            for member,val in zip(list(Accidental),['','♭','#','♭♭','𝄪'])
            }

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
                1 - Note: A to G
                2 - Relative position to central C(=0)
                3 - Duration (Crotchet=1)
                4 - Position in the stave (first=0)
                5 - Optional: Accidental (b=flat,# for sharp,x for double sharp)
        """
        try:
            values = string.split()

            pitch = Pitch.__members__.get(values[0])
            height = int(values[1])
            duration = eval(values[2])
            for elt in Duration.__members__.values():
                if elt.value == duration:
                    duration = elt
                    break
            else:
                raise ValueError

            pos = eval(values[3])
            if len(values) == 5:
                for elt in Accidental.__members__.values():
                    if elt.value == values[4]:
                        accidental = elt
            else:
                accidental = Accidental.NONE

            return Note(pitch,height,pos,duration,accidental)
        except (NameError, IndexError, ValueError):
            raise SyntaxError(f"Impossible to parse string {string}")

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
        return f"{self.Duration.symbols[self.duration]}{self.pitch.name}{self.Accidental.symbols[self.accidental]}{self.height}. Stave pos: {self.pos}"

    def _get_last_pos(self):
        """Return the last position
        of the note, excluding
        the starting of the following one"""
        return self.pos + self.duration.value - 1/50

    last_pos = property(_get_last_pos)

    """
    def is(interval).with():
    def intervalWith() -> int;
    """

Pitch, Accidental, Duration = Note.Pitch, Note.Accidental, Note.Duration

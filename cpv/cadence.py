#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende
"""Represents candences"""

import chord
import enum
from collections.abc import Iterable

class Cadence:
    class Type(enum.Enum):
        PerfectAuthentic = enum.auto()
        ImperfectAuthenticRoot = enum.auto()
        ImperfectAuthenticInverted = enum.auto()
        ImperfectAuthenticLeading = enum.auto()
        Evaded = enum.auto()
        Half = enum.auto()
        PhrygianHalf = enum.auto()
        Lydian = enum.auto()
        Burgundian = enum.auto()
        PlagalHalf = enum.auto()
        Plagal = enum.auto()
        Deceptive = enum.auto()

    def __init__(self,chords):
        self.chords = chords
        self.type = self.getType(chords)

    @classmethod
    def getType(cls,*chords):
        """Return the type of cadence
        with the chords
        Raise ValueError if the type can't be found
        """
        # TODO WARNING method unfinished
        # is iterable
        if len(chords) == 1 and isinstance(chords[0],Iterable):
            chords = list(chords[0])

        inversions = [ c.inversion for c in chords ]
        degrees = [ c.abstract.degree for c in chords]
        highests_roots = [ c.isHighestRoot for c in chords]

        if degrees == [5,1]:
            if inversions == [0,0]: # root position
                if chords[1].isHighestRoot: # check highest pitch
                    return cls.Type.PerfectAuthentic # TEST
                return cls.Type.ImperfectAuthenticRoot # TEST
            else: # inversions
                return cls.Type.ImperfectAuthenticInverted
        if degrees == [7,1] and chords[0].abstract.isQuality("diminished","minor"):
            return cls.ImperfectAuthenticLeading

        raise ValueError(f"No cadence found for {chords}")




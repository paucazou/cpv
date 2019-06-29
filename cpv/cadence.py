#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende
"""Represents candences"""

import chord
import enum

class Cadence:
    class Type(enum.Enum):
        PerfectAuthentic = enum.auto()
        ImperfectAuthenc = enum.auto()
        Evaded = enum.auto()
        Half = enum.auto()
        PhrygianHalf = enum.auto()
        Lydian = enum.auto()
        Burgundian = enum.auto()
        PlagalHalf = enum.auto()
        Plagal = enum.auto()
        Deceptive = enum.auto()


#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende
"""Describes rest names"""

import enum
from fractions import Fraction as F

class Rest(enum.Enum):
    """Rests are silences
    in music"""
    LONGA = F(4)
    BREVE = F(2)
    SEMIBREVE = F(1)
    MINIM = F('1/2')
    CROTCHET = F('1/4')
    QUAVER = F('1/8')
    SEMIQUAVER = F('1/16')
    DEMISEMIQUAVER = F('1/32')
    HEMIDEMISEMIQUAVER = F('1/64')


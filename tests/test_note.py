#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende

import sys
sys.path.append('./cpv/')
print(sys.path)

import note
import pitch

N = note.Note
P = pitch.Pitch

def test_equal():
    assert(N(P.C4, 0, note.Duration.CROTCHET).__eq__( N(P.C4, 0, note.Duration.CROTCHET)))

def test_from_String():
    func = note.Note.fromString
    assert( func('A1 2 0') == N(P.A1, 0, note.Duration.MINIM))


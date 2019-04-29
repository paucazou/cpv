#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende

import sys
sys.path.append('./cpv/')

import chord
import pitch
import pytest
import scale



Chord = chord.Chord
P = pitch.Pitch

scale0 = scale.Scale(P.C0, scale.Mode.M)
chord0 = Chord(1,scale0)
chord07 = Chord(1,scale0,seventh=True)

generate_notes=lambda s : [P[val] for val in s.split()]

def test_contains():
    assert chord0.__contains__(P.C4)
    assert chord0.__contains__((P.C4,P.E4,P.G4))
    assert not chord0.__contains__(P.B3)
    assert not chord0.__contains__((P.C4,P.B3))
    assert chord07.__contains__(P.B2)

def test_is_position():
    def func(n,i):
        assert chord07.isPosition(n,i)
    func(P.E5,3)
    func(P.G4,5)
    func(P.C0,1)
    func(P.B2,7)

def test_find_position():
    def func(n,i):
        assert chord07.findPosition(n) == i

    func(P.C2,1)
    func(P.E3,3)
    func(P.G5,5)
    func(P.B4,7)
    with pytest.raises(ValueError):
        func(P.D4,2)

def test_is_inversion():
    def func(c, i,b=True):
        assert chord07.isInversion(c,i) is b
    root = generate_notes ("C4 E4 G4")
    first = generate_notes("E3 G3 C4")
    second = generate_notes("G2 C4 E4 G3")
    third = root + [P.B3]
    outside = first + [P.A2]

    func(root,0)
    func(first,1)
    func(second,2)
    func(third,3)

def test_find_inversion():
    def func(c, i):
        assert chord07.findInversion(c) == i
    root = generate_notes ("C4 E4 G4")
    first = generate_notes("E3 G3 C4")
    second = generate_notes("G2 C4 E4 G3")
    third = root + [P.B3]
    outside = first + [P.A2]
    
    func(root,0)
    func(first,1)
    func(second,2)
    func(third,3)
    with pytest.raises(ValueError):
        func(outside,0)

def test_find_chord():
    def func(r,n,s,**kw):
        assert Chord.findChord(n,s,**kw) == r


def test_is_chord():
    pass

def test_is_full_chord():
    def func7(n,b=True,c=chord07):
        assert c.isFullChord(n) is b

    def func(n,b=True):
        func7(n,b,chord0)

    func7(generate_notes("C4 C3 E4 G4 B3"))
    func(generate_notes("C3 E4 G4 B3"),False)
    func(generate_notes("C3 E4"),False)











#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende

import sys
sys.path.append('./cpv/')
print(sys.path)

import note


def test_intervalWith():
    p = note.Note.Pitch
    assert(p.A.intervalWith(p.A) == 1)
    assert(p.A.intervalWith(p.B) == 2)
    assert(p.A.intervalWith(p.C) == 3)
    assert(p.A.intervalWith(p.D) == 4)
    assert(p.A.intervalWith(p.E) == 5)
    assert(p.A.intervalWith(p.F) == 6)
    assert(p.A.intervalWith(p.G) == 7)
    assert(p.B.intervalWith(p.A) == 7)
    assert(p.B.intervalWith(p.B) == 1)
    assert(p.B.intervalWith(p.C) == 2)
    assert(p.B.intervalWith(p.D) == 3)
    assert(p.B.intervalWith(p.E) == 4)
    assert(p.B.intervalWith(p.F) == 5)
    assert(p.B.intervalWith(p.G) == 6)
    assert(p.C.intervalWith(p.A) == 6)
    assert(p.C.intervalWith(p.B) == 7)
    assert(p.C.intervalWith(p.C) == 1)
    assert(p.C.intervalWith(p.D) == 2)
    assert(p.C.intervalWith(p.E) == 3)
    assert(p.C.intervalWith(p.F) == 4)
    assert(p.C.intervalWith(p.G) == 5)
    assert(p.D.intervalWith(p.A) == 5)
    assert(p.D.intervalWith(p.B) == 6)
    assert(p.D.intervalWith(p.C) == 7)
    assert(p.D.intervalWith(p.D) == 1)
    assert(p.D.intervalWith(p.E) == 2)
    assert(p.D.intervalWith(p.F) == 3)
    assert(p.D.intervalWith(p.G) == 4)
    assert(p.E.intervalWith(p.A) == 4)
    assert(p.E.intervalWith(p.B) == 5)
    assert(p.E.intervalWith(p.C) == 6)
    assert(p.E.intervalWith(p.D) == 7)
    assert(p.E.intervalWith(p.E) == 1)
    assert(p.E.intervalWith(p.F) == 2)
    assert(p.E.intervalWith(p.G) == 3)
    assert(p.F.intervalWith(p.A) == 3)
    assert(p.F.intervalWith(p.B) == 4)
    assert(p.F.intervalWith(p.C) == 5)
    assert(p.F.intervalWith(p.D) == 6)
    assert(p.F.intervalWith(p.E) == 7)
    assert(p.F.intervalWith(p.F) == 1)
    assert(p.F.intervalWith(p.G) == 2)
    assert(p.G.intervalWith(p.A) == 2)
    assert(p.G.intervalWith(p.B) == 3)
    assert(p.G.intervalWith(p.C) == 4)
    assert(p.G.intervalWith(p.D) == 5)
    assert(p.G.intervalWith(p.E) == 6)
    assert(p.G.intervalWith(p.F) == 7)
    assert(p.G.intervalWith(p.G) == 1)


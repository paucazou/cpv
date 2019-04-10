#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende

import sys
sys.path.append('./cpv/')


import pitch
p = pitch.Pitch

def test_interval_With():
    def func(f, s):
        return f.intervalWith(s)

    assert(func(p.C5, p.E4) == 6)
    assert(func(p.C5, p.E3) == 13)
    assert(func(p.C5, p.C5) == 1)
    assert(func(p.E4, p.E5) == 8)
    assert(func(p.D3, p.D5) == 15 == func(p.Dss3, p.D5) == func(p.Db3, p.Dss5))

def test_interval_With_Min():
    def func(f, s):
        return f.intervalWith(s,True)

    assert(func(p.C4,p.C5) == 1)
    assert(func(p.C5,p.C4) == 1)
    assert(func(p.C4,p.E5) == 3)

    assert(func(p.Cs4,p.E2) == 6)

def test_semitone_with():
    def func(f, s):
        return f.semitoneWith(s)

    assert(func(p.C4, p.D4) == 2)
    assert(func(p.C4, p.Db4) == 1)
    assert(func(p.C4, p.E4) == 4)
    assert(func(p.F4, p.B4) == 6)
    assert(func(p.B4, p.F5) == 6)
    assert(func(p.G4, p.Gs4) == 1)
    assert(func(p.C4, p.C5) == 12)

    
def test_semitone_with_min():
    def func(f, s):
        return f.semitoneWith(s,True)

    assert(func(p.C4, p.C5) == 0)
    assert(func(p.B2, p.F6) == 6)




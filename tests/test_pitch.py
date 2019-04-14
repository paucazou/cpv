#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende

import sys
sys.path.append('./cpv/')
import pytest


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

    assert(func(p.C4,p.C5) == 8)
    assert(func(p.C5,p.C4) == 8)
    assert(func(p.D4,p.D4) == 1)
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

    assert(func(p.C4, p.C5) == 12)
    assert(func(p.C4, p.C4) == 0)
    assert(func(p.B2, p.F6) == 6)

def test_is_perfectly_consonant_with():
    def func(f, s):
        return f.isPerfectlyConsonantWith(s)

    assert(func(p.C4,p.G4))
    assert(func(p.C4,p.G5))
    assert(func(p.C4,p.C5))
    assert(func(p.C4,p.C4))
    assert(func(p.C4,p.C0))
    assert(not func(p.C4,p.E4))
    assert(not func(p.Cb4,p.G4))
    assert(func(p.D3,p.A3))
    assert(func(p.B3,p.Fs4))


def test_is_interval_without_min():
    assert(p.C4.isInterval(8).With(p.C5))
    assert(p.Gb4.isInterval(4).With(p.C5))

def test_is_interval_with_min():
    assert(p.C4.isInterval(8,True).With(p.C5))
    assert(p.Bb3.isInterval(2,True).With(p.C6))

def test_qualify_interval():
    func = p.qualifyInterval
    perfect, minor, major, diminished, augmented = "perfect minor major diminished augmented".split()

    assert(func(3,4) == major)
    assert(func(2,1) == minor)
    assert(func(8,12) == perfect)
    assert(func(1,0) == perfect)
    assert(func(5,6) == diminished)
    with pytest.raises(ValueError):
        func(9,3)

def test_qualified_interval_with():
    def func(f, s, i, q):
        res = f.qualifiedIntervalWith(s)
        assert(res.interval == i)
        assert(res.quality == q)
    perfect, minor, major, diminished, augmented = "perfect minor major diminished augmented".split()

    func(p.C4,p.C5,8,perfect)
    func(p.F4,p.B4,4,augmented)
    func(p.A3,p.F4,6,minor)
    func(p.B2,p.Fs3,5,perfect)

def test_is_qualified_interval_with():
    def ass_true(f, s, *args):
        assert(f.isQualifiedInterval(*args).With(s) is True)
    def ass_false(f, s, *args):
        assert(f.isQualifiedInterval(*args).With(s) is False)

    ass_true(p.C4,p.C5,(8,"perfect"))
    ass_true(p.F4,p.B4,(4,"augmented"))
    ass_true(p.B4,p.F5,(5,"diminished"),(3,"minor"))

def test_is_imperfectly_consonant_with():
    def func(f, s, b=True):
        assert(f.isImperfectlyConsonantWith(s) is b)

    func(p.C4,p.E4)
    func(p.C4,p.Eb4)
    func(p.G4,p.E3)
    func(p.G4,p.Eb3)
    func(p.B2,p.B3,False)

def test_lower_higher_degree():
    assert(p.lowerDegree().value.step == min(p,key=lambda x : x.value.step).value.step)

    assert(p.higherDegree().value.step == max(p,key=lambda x : x.value.step).value.step)






#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende
import sys
sys.path.append('./cpv/')

import scale as S
import pitch
import pytest
P = pitch.Pitch

def test_init():
    s = S.Scale(P.C4,S.Mode.M)
    assert(s.notes[0] == P.C0)
    assert(s.mode == S.Mode.M)

    minor_full = S.Scale(P.C4, S.Mode.m_full)
    for note in (P.Eb4, P.A4, P.Ab4, P.B4, P.Bb4):
        assert(note in minor_full.notes)

def test_relative():
    major = S.Scale(P.C0, S.Mode.M)
    minor = S.Scale(P.A0, S.Mode.m)
    m_har = S.Scale(P.A0, S.Mode.m_harmonic)
    m_ris = S.Scale(P.A0, S.Mode.m_rising)
    m_ful = S.Scale(P.A0, S.Mode.m_full)

    assert(major.relative() == minor)
    assert(major.relative(S.Mode.m_harmonic) == m_har)
    assert(major.relative(S.Mode.m_rising) == m_ris)
    assert(minor.relative() == m_har.relative() == m_ris.relative() == m_ful.relative() == major)

def test_adjacent_scales():
    s = S.Scale(P.C4,S.Mode.M)
    F_scale, G_scale = s.adjacentScales()
    assert(F_scale == S.Scale(P.F3,S.Mode.M))
    assert(G_scale == S.Scale(P.G0,S.Mode.M))

def test_contains():
    major = S.Scale(P.G4, S.Mode.M)
    assert(P.Fs3 in major)
    assert((P.Fs3, P.G4) in major)
    assert(not P.F3 in major)
    assert(not (P.F3,P.G4) in major)

def test_is_degree():
    def func(s, n, i, b=True):
        assert s.isDegree(n, i) is b

    cmajor = S.Scale(P.C4, S.Mode.M)
    func(cmajor, P.C2, 1)
    func(cmajor, P.G5, 5)
    func(cmajor, P.B1, 7)

    with pytest.raises(ValueError):
        func(cmajor, P.Cb4, 1)

def test_is_leading():
    def func(s, n, b=True):
        assert s.isLeading(n) is b

    func(S.Scale(P.C4,S.Mode.M),P.B3)
    func(S.Scale(P.C4,S.Mode.m_harmonic),P.B3)
    func(S.Scale(P.C4,S.Mode.m_rising),P.B3)
    func(S.Scale(P.C4,S.Mode.m_full),P.B3)

    func(S.Scale(P.C4,S.Mode.m),P.B3,False)
    func(S.Scale(P.C4,S.Mode.m_full),P.Bb3,False)

def test_is_subtonic():
    def func(s, n, b=True):
        assert s.isSubtonic(n) is b

    func(S.Scale(P.C4,S.Mode.m),P.Bb3)
    func(S.Scale(P.C4,S.Mode.m_full),P.Bb3)

    func(S.Scale(P.C4,S.Mode.m_harmonic),P.B3,False)
    func(S.Scale(P.C4,S.Mode.m_rising),P.B3,False)
    func(S.Scale(P.C4,S.Mode.M),P.B3,False)

def test_is_raised_submediant():
    def func(s, n, b=True):
        assert s.isRaisedSubmediant(n) is b

    func(S.Scale(P.C4,S.Mode.m_rising),P.A3)
    func(S.Scale(P.C4,S.Mode.m_full),P.A3)

    func(S.Scale(P.C4,S.Mode.m),P.A3,False)
    func(S.Scale(P.C4,S.Mode.m_harmonic),P.A3,False)
    func(S.Scale(P.C4,S.Mode.M),P.A3,False)

def test_from_string():

    def func(s, k, m):
        assert S.Scale.fromString(s) == S.Scale(k,m)

    func("CM",P.C0,S.Mode.M)
    func("Cm",P.C0,S.Mode.m_full)

    with pytest.raises(SyntaxError):
        func("Cg",P.C0,S.Mode.m)


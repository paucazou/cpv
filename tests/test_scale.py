#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende
import sys
sys.path.append('./cpv/')

import scale as S
import pitch
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



#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende

import sys
sys.path.append('./cpv')

import note
import pitch
import pytest
import scalenote
import scale

NS = scalenote.NoteScale
P = pitch.Pitch
Mode = scale.Mode

scale0 = scale.Scale(P.C0,Mode.M)
scale1 = scale.Scale(P.A0,Mode.m)
scale2 = scale.Scale(P.A0,Mode.m_full)

def test_new():
    assert isinstance(NS(scale2, P.A4), scalenote._minor__note_scale)

def test_moveBy():
    ns = NS(scale0,P.D4)
    assert ns.note == P.D4
    ns.moveBy(1)
    assert ns.note == P.E4
    ns.moveBy(-2)
    assert ns.note == P.C4
    with pytest.raises(ValueError):
        ns.moveBy(100)

def test_distanceWith():
    ns1 = NS(scale0,P.C4)
    ns2 = NS(scale0,P.E4)
    ns3 = NS(scale0,P.C4) # same as ns1
    assert ns1.distanceWith(ns2) == 2
    assert ns2.distanceWith(ns1) == -2
    assert ns1.distanceWith(ns3) == 0

def test_eq():
    ns1 = NS(scale0,P.A3)
    ns2 = NS(scale0,P.A3)
    assert ns1.__eq__(ns2)
    ns3 = NS(scale0, P.A4)
    assert not ns3.__eq__(ns2)

    with pytest.raises(ValueError):
        other_scale_ns = NS(scale.Scale(P.A5,Mode.m),P.A3)
        ns1 == other_scale_ns

def test_lt():
    ns1 = NS(scale0, P.C4)
    ns2 = NS(scale0, P.D4)
    assert ns1.__lt__(ns2)
    assert ns2.__gt__(ns1)

def test_moveSequence():
    def func(string):
        return [ NS(scale0,P[val]) for val in string.split() ]
    base = "A4 B4 D5 C5 C4"
    seq = func(base)
    NS.moveSequence(1,seq)
    assert seq == func("B4 C5 E5 D5 D4")

    seq = func(base)
    NS.moveSequence(-1,seq)
    assert seq == func("G4 A4 C5 B4 B3")

def test_functions_chord():
    assert NS(scale0, P.C4).isTonic

def test_moveBy_minor():

    def func(n,i,n2,m=Mode.m):
        ns = NS(scale2, n)
        ns.moveBy(i,m)
        assert ns.note == n2

    func(P.C4,1,P.D4)
    func(P.Gs4,1,P.A4)
    func(P.Gs4,2,P.B4)
    func(P.Fs4,1,P.Gs4)
    func(P.G4,1,P.A4)
    func(P.A3,-1,P.G3)
    func(P.A3,-1,P.Gs3,Mode.m_harmonic)
    func(P.A3,-2,P.Fs3,Mode.m_rising)


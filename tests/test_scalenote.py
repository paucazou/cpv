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
    seq = func("A4 B4 D5 C5 C4")
    NS.moveSequence(1,seq)
    assert seq == func("B4 C5 E5 D5 D4")

def test_functions_chord():
    assert NS(scale0, P.C4).isTonic

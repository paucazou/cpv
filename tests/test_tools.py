#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende

import sys
sys.path.append('./cpv')

import tools
import pitch

P = pitch.Pitch

def test_min_max():
    def func(i,a,*notes):
        res = tools.min_max(notes)
        assert res.min == i
        assert res.max == a

    func(P.C4,P.C5,P.B4,P.G4,P.C4, P.C5)

def test_is_same_direction():
    def func(b,*args):
        assert tools.is_same_direction(*args) is b

    func(True,P.C4,P.D4,P.E4)
    func(True,P.C4,P.B3,P.A3)

    func(False,P.C4,P.D4,P.C4)

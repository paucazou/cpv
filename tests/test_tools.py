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

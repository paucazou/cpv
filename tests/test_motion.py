#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende

import sys
import unittest.mock as mock
sys.path.append('./cpv/')

import motion
mt = motion.MotionType

class FakePitch:
    def __init__(self,s : int):
        self.value = mock.Mock()
        self.value.semitone = s

    def __eq__(self,other):
        return self.value.semitone == other.value.semitone

C, D, E, F, G, A, B = [FakePitch(i*2) for i in range(7)]

def test_motion():
    def func(a,b,c,d,result):
        assert(mt.motion(a,b,c,d) == result)

    func(C,A,C,A,mt.direct)
    func(C,E,D,F,mt.direct)
    func(F,B,C,A, mt.direct)

    func(A,F,B,F, mt.oblique)
    func(A,F,A,E, mt.oblique)

    func(G,E, B,D, mt.contrary)
    func(A,C, G,E, mt.contrary)

def test_match():
    def func(a,b,c,d, result):
        assert(result.match(a,b,c,d))
    func(C,A,C,A,mt.direct)
    func(C,E,D,F,mt.direct)
    func(F,B,C,A, mt.direct)

    func(A,F,B,F, mt.oblique)
    func(A,F,A,E, mt.oblique)

    func(G,E, B,D, mt.contrary)
    func(A,C, G,E, mt.contrary)



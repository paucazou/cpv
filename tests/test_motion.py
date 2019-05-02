#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende

import sys
sys.path.append('./cpv')
import motion
import pitch

P = pitch.Pitch
M = motion.MotionType

pitcher = lambda x : [ P[elt] for elt in x.split() ]

def test_motion():
    def func(n,r):
        assert motion.MotionType.motion(pitcher(n)) == r

    func("C4 C3 G3 E3",M.contrary)
    func("G3 E3 C4 C3",M.contrary)
    func("C4 G4 E4 G4",M.oblique)
    func("C3 G3 C3 D3",M.oblique)
    func("E3 G3 C3 E3",M.direct)
    func("E3 G3 G3 B3",M.direct)
    func("E3 G3 E3 G3",M.direct)

    func("G3 E3 E3 G3",M.direct)





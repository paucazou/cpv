#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende

import sys
sys.path.append('./cpv/')

from pitch import Pitch as P
from tessitura import *


def test_contains():
    assert(P.E4 in soprano)
    assert(P.Bb5 not in soprano)
    assert(P.Bs3 in soprano)
    assert(P.B3 not in soprano)

def test_is_condoned():
    assert(soprano.isCondoned(P.Bb5))
    assert(soprano.isCondoned(P.E4))



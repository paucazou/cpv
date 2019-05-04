#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende

import pytest
import sys
import unittest.mock as mock
sys.path.append('./cpv/')

import cantus_firmus
import error
import note

def test_rule_1():
    f = [ i for i in range(7) ]
    s = [i for i in range(12) ]
    t = [ i for i in range(30) ]
    with pytest.raises(error.CompositionError):
        cantus_firmus.rule_1(f)
    with pytest.raises(error.CompositionError):
        cantus_firmus.rule_1(t)
    cantus_firmus.rule_1(s)

def test_rule_2():
    class FakeNote:
        def __init__(self,duration):
            self.duration = duration

    FK = FakeNote
    
    errors = [FK(4)] * 10
    errors.append(FK(2))
    with pytest.raises(error.CompositionError):
        cantus_firmus.rule_2(errors)

    no_errors = [FK(note.Duration.SEMIBREVE)] * 14
    cantus_firmus.rule_2(no_errors)


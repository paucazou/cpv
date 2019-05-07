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
import scale
import stave

def raises_composition_error(func):
    with pytest.raises(error.CompositionError):
        func()

def test_rule_1():
    f = [ i for i in range(7) ]
    s = [i for i in range(12) ]
    t = [ i for i in range(30) ]
    with pytest.raises(error.CompositionError):
        cantus_firmus.rule_1([f])
    with pytest.raises(error.CompositionError):
        cantus_firmus.rule_1([t])
    cantus_firmus.rule_1([s])

def test_rule_2():
    class FakeNote:
        def __init__(self,duration):
            self.duration = duration

    FK = FakeNote
    
    errors = [FK(4)] * 10
    errors.append(FK(2))
    with pytest.raises(error.CompositionError):
        cantus_firmus.rule_2([errors])

    no_errors = [FK(note.Duration.SEMIBREVE)] * 14
    cantus_firmus.rule_2([no_errors])

def test_rule_3():
    staves = stave.Stave.fromString("""4/4\nCM\n* first\nC4 4 0\nC3 4 4\n* second\nC5 4 0\nB2 4 4\n* last\nG4 4 0\nC3 4 4""")
    cantus_firmus.rule_3([staves[0]])

    with pytest.raises(error.CompositionError):
        cantus_firmus.rule_3([staves[1]])
    with pytest.raises(error.CompositionError):
        cantus_firmus.rule_3([staves[2]])

def test_rule_4():
    staves = stave.Stave.fromString("""4/4\nCM\n
* first\nC4 4 0\nB2 4 4\nC3 4 8\n
* second\nD5 4 0\nC5 4 4\n

* third\nD5 4 0\nC3 4 4\n
* last\nG4 4 0\nC3 4 4""")

    cantus_firmus.rule_4([staves[0]])
    cantus_firmus.rule_4([staves[1]])

    raises_composition_error(lambda : cantus_firmus.rule_4([staves[2]]))
    raises_composition_error(lambda : cantus_firmus.rule_4([staves[3]]))

def test_rule_7():
    staves = stave.Stave.fromString("""4/4\nCM\n
* correct
C4 4 0
D4 4 4
E4 4 8
D4 4 12
C4 4 16
* incorrect
C4 4 0
D4 4 4
D4 4 8
C4 4 12
""")
    cantus_firmus.rule_7([staves[0]])
    raises_composition_error(lambda : cantus_firmus.rule_7([staves[1]]))






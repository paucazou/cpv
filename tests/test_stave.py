#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende

import sys
sys.path.append('./cpv/')
import unittest.mock as mock
import pytest

import note
import stave
class N:
    """A mock of Note"""
    def __init__(self,pos,duration):
        self.pos = pos
        self.duration = mock.Mock()
        self.duration.value = duration
        self.last_pos = pos + duration - 0.0001

    def __equal__(self,other):
        return self.pos == other.pos and self.duration.value == other.duration.value

    def __repr__(self):
        return f"N({self.pos},{self.duration.value})"

@mock.patch('note.Note')
def test_fromString(note_):
    note_.fromString.return_value = 'N'
    from_str = stave.Stave.fromString

    first = from_str("""4/4\n# comment\nA 0 1 0""")[0]
    assert(first.rythm == 4 == first.breve_value)
    assert(len(first._stave) == 1)
    assert(first._stave == ['N'])

    title2 = "A title"
    second = from_str(f"""3/4\n* {title2}\nA 0 1 0""")[0]
    assert(second.rythm == 3)
    assert(second.breve_value == 4)
    assert(second.title == title2)
    assert(second._stave == ["N"])

def test_bar_number():

    s = stave.Stave()
    s._stave = [ N(0,4),
                 N(4,4),
                 N(8,1)]
    assert(isinstance(s._stave[0].duration.value,int))
    assert(s.barNumber == 3)


def test_get_bar():
    s = stave.Stave()
    s._stave = [ N(0,4),
                 N(4,4),
                 N(8,1)]
    bar1 = s.getBar(0)
    bar1 = bar1.elts
    assert(len(bar1) == 1)
    assert(bar1[0] is s._stave[0])

    bar2 = s.getBar(1)
    bar2 = bar2.elts
    assert(len(bar2) == 1)
    assert(bar2[0] is s._stave[1])




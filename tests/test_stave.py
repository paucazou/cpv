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
        self.duration= duration
        self.last_pos = pos + duration 

    def __equal__(self,other):
        return self.pos == other.pos and self.duration == other.duration

    def __repr__(self):
        return f"N({self.pos},{self.duration})"

@mock.patch('note.Note')
def test_fromString(note_):
    note_.fromString.return_value = 'N'
    from_str = stave.Stave.fromString

    first = from_str("""4/4\nCM\n# comment\nA 0 1 0""")[0]
    assert(first.rythm == 4 == first.breve_value)
    assert(len(first._stave) == 1)
    assert(first._stave == ['N'])

    title2 = "A title"
    second = from_str(f"""3/4\nCM\n* {title2}\nA 0 1 0""")[0]
    assert(second.rythm == 3)
    assert(second.breve_value == 4)
    assert(second.title == title2)
    assert(second._stave == ["N"])

def test_bar_number():

    s = stave.Stave()
    s._stave = [ N(0,4),
                 N(4,4),
                 N(8,1)]
    assert(isinstance(s._stave[0].duration,int))
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
    assert s.getBar(-1)[0] == s.getBar(2)[0]

def test_copy():
    s = stave.Stave()
    copy = s.copy()

    assert s is not copy
    assert s._stave is not copy._stave

    s._stave.append('ok')
    assert len(s._stave) != len(copy._stave)

def test_find_bar_of():
    s = stave.Stave()
    s._stave =  notes = [
            N(0,4),
            N(4,4),
            N(8,4),
            ]
    def func(i):
        res = s.findBarOf(notes[i])
        assert res.elts == [notes[i]]
        assert res.pos == i 

    func(0)
    func(1)
    func(2)

    with pytest.raises(AssertionError):
        s.findBarOf(N(14,2))








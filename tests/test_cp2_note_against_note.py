#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende

import sys
sys.path.append('./cpv/')

import cp2_note_against_note
import stave


def test_first_rule():
    stave_list= stave.Stave.fromFile("./tests/examples/1")
    s = stave_list[0]
    cp2_note_against_note._first_rule(s)

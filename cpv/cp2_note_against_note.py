#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende
"""Defines the 22 rules defined
by Andre Geldage in his Traité de
Contrepoint"""

import error
import note
import stave
import util


def first_rule(parts: list):
    """Wrapper of the first rule.
    Each part in parts is a Stave
    """
    rythm, brev_val = parts[0].rythm, parts[0].breve_value
    by_title = lambda x : x.title
    main_cf = util.list_finder(parts,'cantus firmus',by_title)

    for i in range(1,7):
        s = stave.Stave(rythm,brev_val)
        cp = util.list_finder(parts,f'{i}cp',fun=by_title)
        cf = util.list_finder(parts,f'{i}cf',main_cf,by_title)

        s.extend(cp)
        s.extend(cf)

        _first_rule(s)


def _first_rule(s : stave.Stave):
    """
    s is the main stave
    1 - Le contrepoint se compose d'une partie en rondes combinée avec le Chant donné (en rondes)

    """
    for nb,bar in enumerate(s.barIter()):

        # check that each bar contains only two notes
        if len(bar.elts) != 2:
            raise error.CompositionError("Number of breve should be two",bar)

        # check that each note is a breve
        if bar.elts[0].duration != bar.elts[1].duration != note.Duration.BREVE:
            raise error.CompositionError("The notes are not breves",bar)

def second_rule(staves: list, c: stave.Stave):
    """
    2 - Le chant donné servira trois fois de partie inférieure et trois de partie supérieure. Les trois parties combinées sur le chant donné devront être entièrement différentes - de même pour celles formées sur le chant donné.
    """
    pass

def third_rule():
    """
    3 - Le chant donné (ou plain-chant) peut être transposé toutes les fois qu'il ne dépassera pas l'étendue ordinaire, au grave ou à l'aigu, de la voix pour laquelle on le transposera.
    """
    pass


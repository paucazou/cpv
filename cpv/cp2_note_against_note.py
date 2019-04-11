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


def rule_1(parts: list):
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

def rule_2(staves: list, c: stave.Stave):
    """
    2 - Le chant donné servira trois fois de partie inférieure et trois de partie supérieure. Les trois parties combinées sur le chant donné devront être entièrement différentes - de même pour celles formées sur le chant donné.
    """
    pass

def rule_3():
    """
    3 - Le chant donné (ou plain-chant) peut être transposé toutes les fois qu'il ne dépassera pas l'étendue ordinaire, au grave ou à l'aigu, de la voix pour laquelle on le transposera.
    """
    # check the tessitura
    # check the transposition is correct
    pass

def _fourth_rule(s: stave.Stave):
    """On doit commencer par une consonance parfaite (unisson, quinte ou douzième, octave ou quinzième) et finir par l'octave ou l'unisson
    """
    def nb_error(poss, posi):
        if len(notes) != 2:
            raise error.CompositionError(f"Two notes are expected at the {poss} of the track",s.getBar(posi))

    # start
    notes = s.atFirstPos(0)
    nb_error("start",0)

    if not notes[0].pitch.isPerfectlyConsonantWith(notes[1].pitch):
        raise error.CompositionError("The first two notes are not fully consonant.",s.getBar(0))

    # end
    notes = s.atFirstPos(s.lastFirstPos)
    nb_error("end",s.getBar(s.barNumber-1))

    if not notes[0].pitch.isInterval(1,True).With(notes[1].pitch):
        raise error.CompositionError("The last interval must be an unison or an octave.",s.getBar(s.barNumber-1))

def _fifth_rule(s : stave.Stave):
    """L'unisson est défendu dans le courant du contrepoint"""

    for elt in s.barIter():

        if elt.pos == 0 or elt.pos == s.lastFirstPos:
            # first and last interval can be unisons.
            continue

        if len(elt) != 2:
            raise error.CompositionError("Two notes are expected.",elt)

        if elt[0].pitch == elt[1].pitch:
            raise error.CompositionError("Unison is forbidden insided the couterpoint",elt)

def _ninth_rule(s : stave.Stave):
    """Les notes ne peuvent pas êtres répétées plus d'une fois - on ne peut les faire entendre plus de deux fois de suite."""
    nb = 0
    previous = None
    for elt in s.barIter():
        if elt.pos != 0 and elt[0].pitch == previous.pitch:
            nb += 1
        else:
            nb = 0

        if nb >= 2:
            raise error.CompositionError("It is forbidden to use the same note more than two times in a row",elt)

        previous = elt[0]







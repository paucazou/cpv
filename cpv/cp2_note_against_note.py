#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende
"""Defines the 22 rules defined
by Andre Geldage in his Traité de
Contrepoint"""

import error
import motion
import note
import stave
import util

_semitone = lambda x : x.value.semitone


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

def _seventh_rule(s : stave.Stave):
    """Les intervalles formant consonance parfaites ou imparfaites avec le chant donné sont seuls employés"""
    for bar in s.barIter():
        if len(bar) != 2:
            raise error.CompositionError("Two notes expected",bar)
        f, s = bar[0].pitch, bar[1].pitch
        if not f.isConsonantWith(s):
            raise error.CompositionError("The notes must be consonant",bar)

def _eighth_rule(s : stave.Stave):
    """On ne doit pas entendre plus de trois tierces ou trois sixtes de suite"""
    _6, _3 = 0
    intervals = {3:0,6:0}

    for bar in s.barIter():
        if len(bar) != 2:
            raise error.CompositionError("Two notes expected",bar)
        f, s = bar[0].pitch, bar[1].pitch
        int_ = f.intervalWith(s)
        if int_ == 3:
            _3 += 1
            _6 = 0
        elif int_ == 6:
            _6 += 1
            _3 = 0
        else:
            _6 = _3 = 0

        if 4 in (_6,_3):
            raise error.CompositionError("It is forbidden to use more than three sixths or thirds in a row", bar)

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

def _eleventh_rule(cp : stave.Stave, cd : stave.Stave):
    """Les croisements sont tolérés, employés avec une grande réserve"""
    cp_high_part = None

    for cp_n, cd_n in zip(cp.barIter(),cd.barIter()):

        if not (len(cp_n) == len(cd_n) == 1):
            raise error.CompositionError("Two notes are expected",cp_n,cd_n)

        cdn, cpn = cd_n[0], cp_n[0]

        if cp_n.pos is None:
            cp_high_part = cpn.semitone > cdn.semitone if cpn.semitone != cdn.semitone else None
        else:
            if cp_high_part is True:
                if cdn.semitone > cpn.semitone:
                    error.warn("The melodies intersect",cp_n,cd_n)
                cp_high_part = False
            else:
                if cpn.semitone > cdn.semitone:
                    error.warn("The melodies interset",cp_n,cd_n)
                cp_high_part = True

def _fourteenth_rule(s : stave.Stave):
    """Pour la fausse relation de triton, la règle est la même qu'en harmonie : la fausse relation de triton est défendue."""
    for bar in s.barIter():
        if len(bar) != 2:
            raise error.CompositionError("Two notes expected",bar)
        if abs(bar[0].pitch.semitoneWith(bar[1].pitch) == 6):
            raise error.CompositionError("Tritone is forbidden",bar)

def _fifteenth_rule(s : stave.Stave):
    """Le contrepoint ne doit pas parcourir une étendue plus grande que la dixième et par exception la onzième."""
    min = pitch.higherDegree()
    max = pitch.lowerDegree()
    for n in s:
        if n.intervalWith(min) > max.intervalWith(min):
            max = n
        if n.intervalWith(max) < min.interval(max):
            min = n

    if max.intervalWith(min) == 11:
        error.warn("The counterpoint can exceed the 11th by tolerance only.",*s.iterBar())
    if max.intervalWith(min) > 11:
        raise error.CompositionError("It is strictly forbidden to exceed the 11th.",*s.iterBar())

def _sixteenth_rule(s : stave.Stave):
    """Le mouvement conjoint est celui qui convient le mieux au style du Contrepoint rigoureux. Employer le mouvement disjoint très discrètement."""
    previous = None
    for bar in s.barIter():
        if previous is not None and bar[0].intervalWith(previous[0]) != 2:
            error.warn("It is better to avoid disjunct motion",previous, bar)
        previous = bar

def _seventeenth_rule(s : stave.Stave):
    """Les mouvements de quarte augmentée (triton), quinte dimininuée, de septième majeure et mineure sont défendus"""
    previous = None
    for bar in s.barIter():
        if previous is not None and bar[0].isQualifiedInterval(
                (5,"diminished"),
                (4,"augmented"),
                (7,"minor"),
                (7,"major")
                ).With(previous[0]):
            raise error.CompositionError("Melodic motion can't be a 4th augmented, 5th diminished, 7th minor or major",previous, bar)
        previous = bar

def _eighteenth_rule(s: stave.Stave):
    """Comme pour l'harmonie, le mouvement contraire est préférable à l'oblique, et ce dernier au direct"""
    movs = {motion.MotionType.direct : 0,
            motion.MotionType.contrary : 0,
            motion.MotionType.oblique : 0
            }
    previous_bar = None

    for bar in s.barIter():
        notes = [*bar]
        notes.sort(key=lambda x : x.value.semitone]
        if previous_bar is not None:
            movs[motion.MotionType.motion(previous_bar,*notes)] += 1
        previous_bar = [*notes]


    error.warn(f"Number of contrary movements: {movs[motion.MotionType.direct]}; oblique movements: {movs[motion.MotionType.oblique]}; direct movements: {movs[motion.MotionType.direct]}")
    error.warn("Prefer the contrary movement to the oblique, and the oblique to the direct")

def _nineteenth_rule(s : stave.Stave):
    """Ne jamais arriver sur une quinte ou une octave par mouvement direct. A priori, deux quintes ou deux octaves sont défendues."""
    # 2 5th/8ve in a row
    previous = None
    for bar in s.barIter():
        interval = bar[0].intervalWith(bar[1])
        if previous is not None and interval in (8,5):
            if interval == previous:
                raise error.CompositionError("Two 5th or two 8ve in a row is forbidden",previous_bar, bar)
            # direct motion?
            previous_notes = [*previous]
            notes = [*bar]
            previous_notes.sort(key=_semitone)
            notes.sort(key=_semitone)
            if motion.MotionType.motion(*previous_notes,*notes) == motion.MotionType.direct:
                raise error.CompositionError("It is forbidden to go to a 5th or an 8ve by direct motion",previous,bar)

        previous_bar = bar
        previous = interval

def _twentieth_rule(cd : stave.Stave, max_size = 20):
    """Prendre de préférence des chants donnés courts, en majeur et en mineur."""
    if len(s) > max_size:
        error.warn(f"Be careful to take shorts canti firmi. Recommanded size is {max_size}. This cantus firmus is {len(cd)}.",*s.barIter())

def _twentyfirst_rule(s : stave.Stave, ratio = 5/20):
    """Employer de préférence les consonances imparfaites"""
    bars = []
    for bar in s.barIter():
        f, s = bar
        if f.isPerfectlyConsonantWith(s):
            bars.append(bar)
        

    if len(perfect) / len(s) > ratio:
        error.warn("The number of perfect consonances is possibly higher than requested",*bars)
















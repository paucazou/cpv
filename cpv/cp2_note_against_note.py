#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende
"""Defines the 22 rules defined
by Andre Geldage in his Traité de
Contrepoint"""

import chord
import error
import motion
import note
import pitch
import scale
import scalenote
import stave
import tessitura
import tools
import util

_semitone = lambda x : util.to_pitch(x).value.semitone

def get_matching_cf(s,data):
    """For a stave s, with a title
    like 'cp1', return the matching
    cantus firmus"""
    return next((x for x in data if x.title == f'{s.title[0]}cf'),
            next((y for y in data if y.title == "cantus firmus")))


# decorators
def __counterpoint_only(func):
    """Extracts only the counterpoints
    parts and pass them to func"""
    def __wrapper(data):
        for s in data:
            if 'cp' in s.title:
                func(s)

    return __wrapper

def __mix_cp_cf(func):
    """Mix the counterpoints parts and
    the cantus firmus"""
    def __wrapper(data):
        for s in data:
            if 'cp' in s.title:
                cf = get_matching_cf(s,data)
                new_s = s.copy()
                new_s.extend(cf)

                func(new_s)

    return __wrapper

def __cp_cf(func):
    """Return the counterpoint and
    the cantus firmus
    as two parts
    """
    def __wrapper(data):
        for s in data:
            if not ('cp' in s.title):
                continue
            cf = get_matching_cf(s,data)
            func(s, cf)
    
    return __wrapper


def __cantus_firmus_only(func):
    """When the canti firmi
    only are expected
    """
    def __wrapper(data):
        cf = next(x for x in data if x.title == "cantus firmus")
        for s in data:
            if 'cf' in s.title:
                func(s, cf)

    return __wrapper
            

# rules



def oldRULE1(parts: list):
    """Wrapper of the first rule.
    Each part in parts is a Stave
    """
    rythm, brev_val = parts[0].rythm, parts[0].breve_value
    by_title = lambda x : x.title
    main_cf = util.list_finder(parts,'cantus firmus',fun=by_title)

    for i in range(1,7):
        s = stave.Stave(rythm,brev_val)
        cp = util.list_finder(parts,f'{i}cp',fun=by_title)
        cf = util.list_finder(parts,f'{i}cf',main_cf,by_title)

        s.extend(cp)
        s.extend(cf)

        _first_rule(s)


@__mix_cp_cf
def rule_1(s : stave.Stave):
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

def rule_2(staves: list):
    """
    2 - Le chant donné servira trois fois de partie inférieure et trois de partie supérieure. Les trois parties combinées sur le chant donné devront être entièrement différentes - de même pour celles formées sur le chant donné.
    """
    #is every part present?
    parts = {f"{n}cp":False for n in range(1,7)}
    for s in staves:
        parts[s.title] = True
    for val in parts.values():
        if val is False:
            raise error.CompositionError("Six parts are expected in the counterpoint")

    # is every part different?
    for cp_name, cp in parts.items():
        if not ('cp' in cp_name):
            continue
        for other_cp in parts.values():
            if cp is other_cp:
                continue
            if cp == other_cp:
                raise error.CompositionError("The parts in the counterpoint must be totally different",cp,other_cp)


@__cantus_firmus_only
def rule_3(cf : stave.Stave, base_cf : stave.Stave):
    """
    3 - Le chant donné (ou plain-chant) peut être transposé toutes les fois qu'il ne dépassera pas l'étendue ordinaire, au grave ou à l'aigu, de la voix pour laquelle on le transposera.
    """
    # check the tessitura
    T = tessitura

    valid_tessitura = False
    for tess in (T.soprano,T.tenor,T.bass,T.alto):
        if cf in tess:
            valid_tessitura = True
            break

    if not valid_tessitura:
        raise error.CompositionError("The cantus firmus transposed is too high or too low",cf)
    
    # check the transposition is correct
    def _semitone_sum(n,n2):
        return n.pitch.value.semitone - n2.pitch.value.semitone

    for i, (b1, b2) in enumerate(zip(cf,base_cf)):
        if i + 1 == len(cf):
            break
        if _semitone_sum(b1,cf[i+1]) != _semitone_sum(b2,base_cf[i+1]):
            raise error.CompositionError("Cantus firmus transposed doesn't match with original cantus firmus",b1,b2)



@__mix_cp_cf
def rule_4(s: stave.Stave):
    """On doit commencer par une consonance parfaite (unisson, quinte ou douzième, octave ou quinzième) et finir par l'octave ou l'unisson
    """
    def nb_error(poss, posi,notes):
        if len(notes) != 2:
            raise error.CompositionError(f"Two notes are expected at the {poss} of the track",s.getBar(posi))

    # start
    notes = s.atFirstPos(0)
    nb_error("start",0,notes)

    if not notes[0].pitch.isPerfectlyConsonantWith(notes[1].pitch):
        raise error.CompositionError("The first two notes are not fully consonant.",s.getBar(0))

    # end
    notes = s.atFirstPos(s.lastFirstPos)
    nb_error("end",s.getBar(s.barNumber-1),notes)

    if not notes[0].pitch.isInterval(1,8,True).With(notes[1].pitch):
        raise error.CompositionError("The last interval must be an unison or an octave.",s.getBar(s.barNumber-1))

@__mix_cp_cf
def rule_5(s : stave.Stave):
    """L'unisson est défendu dans le courant du contrepoint"""

    for elt in s.barIter():

        if elt.pos == 0 or elt.pos == s.lastFirstPos:
            # first and last interval can be unisons.
            continue

        if len(elt) != 2:
            raise error.CompositionError("Two notes are expected.",elt)

        if elt[0].pitch == elt[1].pitch:
            raise error.CompositionError("Unison is forbidden insided the couterpoint",elt)

@__counterpoint_only
def rule_6(s : stave.Stave):
    """Le mouvement chromatique est défendu"""
    previous = None
    for elt in s.barIter():
        note = elt[0]
        if previous is not None and previous[0].pitch.isChromaticInflectionWith(note.pitch):
            raise error.CompositionError("Chromatic inflection is forbidden",previous,bar)
        previous = elt 

@__mix_cp_cf
def rule_7(s : stave.Stave):
    """Les intervalles formant consonance parfaites ou imparfaites avec le chant donné sont seuls employés"""
    for bar in s.barIter():
        if len(bar) != 2:
            raise error.CompositionError("Two notes expected",bar)
        ft, sd = bar[0].pitch, bar[1].pitch
        if not ft.isConsonantWith(sd):
            raise error.CompositionError("The notes must be consonant",bar)

@__mix_cp_cf
def rule_8(s : stave.Stave):
    """On ne doit pas entendre plus de trois tierces ou trois sixtes de suite"""
    _6 = _3 = 0
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

@__counterpoint_only
def rule_9(s : stave.Stave):
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

@__mix_cp_cf
def rule_10(s : stave.Stave):
    return _Rule_10(s)

def _Rule_10(s : stave.Stave):
    """Éviter les marches d'harmonie"""
    #TODO on ne gère pas le cas d'une modulation
    for start in range(s.barNumber):
        for end in range(start,s.barNumber):

            motif = []
            for i in range(start, end+1):
                for n in s.getBar(i):
                    motif.append(n)

            motif_bar_number = end - start + 1
            try:
                following = []
                for i in range(end+1, motif_bar_number + end + 1):
                    for n in s.getBar(i):
                        following.append(n)
            except IndexError:
                break
            if tools.matchSequence(motif, following, s.scale):
                if len(motif) == 1:
                    continue
                if len(motif) <= 2:
                    error.warn("Sequence should be avoided",motif, following)
                else:
                    raise error.CompositionError("Sequence should be avoided",motif, following)


@__cp_cf
def rule_11(cp : stave.Stave, cd : stave.Stave):
    """Les croisements sont tolérés, employés avec une grande réserve"""
    cp_high_part = None

    for cp_n, cd_n in zip(cp.barIter(),cd.barIter()):

        if not (len(cp_n) == len(cd_n) == 1):
            raise error.CompositionError("Two notes are expected",cp_n,cd_n)

        cdn, cpn = cd_n[0], cp_n[0]

        if cp_high_part is None:
            cp_high_part = cpn.pitch.value.semitone > cdn.pitch.value.semitone if cpn.pitch.value.semitone != cdn.pitch.value.semitone else None
        else:
            if cp_high_part is True:
                if cdn.pitch.value.semitone > cpn.pitch.value.semitone:
                    error.warn("The melodies intersect: cantus firmus is now over the counterpoint",cp_n,cd_n)
                    cp_high_part = False
            elif cp_high_part is False:
                if cpn.pitch.value.semitone > cdn.pitch.value.semitone:
                    error.warn("The melodies intersect: counterpoint is now over cantus firmus",cp_n,cd_n)
                    cp_high_part = True

            else:
                assert cp_high_part is not None

@__counterpoint_only
def rule_12(s : stave.Stave):
    """On ne doit moduler qu'aux tons relatifs"""
    sc = scale.Scale(s.keynote,s.mode)
    relative = sc.relative(scale.Mode.m_full)
    for bar in s.barIter():
        note = bar[0]
        if note.pitch not in sc:
            if note.pitch not in relative:
                raise error.CompositionError("It is forbidden to modulate outside the relative key",bar)

@__mix_cp_cf
def rule_13(s : stave.Stave):
    """Lorsque la dominante du ton se trouve à la partie inférieure - et qu'elle a été précédée de l'accord du premier degré - il faut éviter de la combiner avec une sixte car cela donnerait le sentiment d'un accord de quarte et sixte, ce qui est défendu. Si elle permet de sous-entendre un autre accord, on peut l'employer"""

    current_scale = s.scale
    previous_chord = None

    for bar in s.barIter():
        notes = [ scalenote.NoteScale(current_scale,n) for n in bar ]
        n1, n2 = notes
        # change scale if necessary 
        if notes not in current_scale:
            current_scale = current_scale.relative(scale.Mode.m_full)
        # generate chord
        first = chord.Chord(1,current_scale)
        # is it the first degree chord?
        if notes in first:
            previous_chord = notes
            continue
        if previous_chord is not None:
            # is it the dominant in the bass and an interval of sixth?
            low, high = n1,n2 if n1 < n2 else (n2, n1)
            if low.isDominant and low.note.isInterval(6).With(high):
                raise error.CompositionError("It is forbidden to use a tonic chord followed by a dominant at the bass and a sixth with the dominant",previous_chord, bar)

            # clean-up
            previous_chord = None


@__mix_cp_cf
def rule_14(s : stave.Stave):
    """Pour la fausse relation de triton, la règle est la même qu'en harmonie : la fausse relation de triton est défendue."""
    for bar in s.barIter():
        if len(bar) != 2:
            raise error.CompositionError("Two notes expected",bar)
        if abs(bar[0].pitch.semitoneWith(bar[1].pitch) == 6):
            raise error.CompositionError("Tritone is forbidden",bar)

@__counterpoint_only
def rule_15(s : stave.Stave):
    """Le contrepoint ne doit pas parcourir une étendue plus grande que la dixième et par exception la onzième."""
    res = tools.min_max(s)
    min = res.min
    max = res.max

    if max.intervalWith(min) == 11:
        error.warn("The counterpoint can exceed the 11th by tolerance only.",*s.barIter())
    if max.intervalWith(min) > 11:
        raise error.CompositionError("It is strictly forbidden to exceed the 11th.",*s.barIter())

@__counterpoint_only
def rule_16(s : stave.Stave):
    """Le mouvement conjoint est celui qui convient le mieux au style du Contrepoint rigoureux. Employer le mouvement disjoint très discrètement."""
    previous = None
    for bar in s.barIter():
        if previous is not None and bar[0].pitch.intervalWith(previous[0].pitch) > 2:
            error.warn("It is better to avoid disjunct motion",previous, bar)
        previous = bar

@__counterpoint_only
def rule_17(s : stave.Stave):
    """Les mouvements de quarte augmentée (triton), quinte dimininuée, de septième majeure et mineure sont défendus"""
    previous = None
    for bar in s.barIter():
        if previous is not None and bar[0].pitch.isQualifiedInterval(
                (5,"diminished"),
                (4,"augmented"),
                (7,"minor"),
                (7,"major")
                ).With(previous[0].pitch):
            raise error.CompositionError("Melodic motion can't be a 4th augmented, 5th diminished, 7th minor or major",previous, bar)
        previous = bar

@__mix_cp_cf
def rule_18(s: stave.Stave):
    """Comme pour l'harmonie, le mouvement contraire est préférable à l'oblique, et ce dernier au direct"""
    movs = {motion.MotionType.direct : 0,
            motion.MotionType.contrary : 0,
            motion.MotionType.oblique : 0
            }
    previous_bar = None

    for bar in s.barIter():
        notes = [*bar]
        notes.sort(key=lambda x : x.pitch.value.semitone)
        if previous_bar is not None:
            movs[motion.MotionType.motion(*previous_bar,*notes)] += 1
        previous_bar = [*notes]


    error.warn(f"Number of contrary movements: {movs[motion.MotionType.contrary]}; oblique movements: {movs[motion.MotionType.oblique]}; direct movements: {movs[motion.MotionType.direct]}. ")
    error.warn("Prefer the contrary movement to the oblique, and the oblique to the direct. ")

@__mix_cp_cf
def rule_19(s : stave.Stave):
    """Ne jamais arriver sur une quinte ou une octave par mouvement direct. A priori, deux quintes ou deux octaves sont défendues."""
    # 2 5th/8ve in a row
    previous = None
    for bar in s.barIter():
        interval = bar[0].pitch.intervalWith(bar[1].pitch)
        if previous is not None and interval in (8,5):
            if interval == previous:
                raise error.CompositionError("Two 5th or two 8ve in a row is forbidden",previous_bar, bar)
            # direct motion?
            previous_notes = [*previous_bar]
            notes = [*bar]
            previous_notes.sort(key=_semitone)
            notes.sort(key=_semitone)
            if motion.MotionType.motion(*previous_notes,*notes) == motion.MotionType.direct:
                raise error.CompositionError("It is forbidden to go to a 5th or an 8ve by direct motion",previous,bar)

        previous_bar = bar
        previous = interval

def rule_20(data, max_size = 20):
    """Prendre de préférence des chants donnés courts, en majeur et en mineur."""
    cd = next(x for x in data if x.title == "cantus firmus")

    if len(cd) > max_size:
        error.warn(f"Be careful to take shorts canti firmi. Recommanded size is {max_size}. This cantus firmus is {len(cd)}.",*s.barIter())

@__mix_cp_cf
def rule_21(s : stave.Stave, ratio = 5/20):
    """Employer de préférence les consonances imparfaites"""
    bars = []
    for bar in s.barIter():
        ft, sd = [ util.to_pitch(n) for n in bar ]
        if ft.isPerfectlyConsonantWith(sd):
            bars.append(bar)

    if len(bars) / len(s) > ratio:
        error.warn("The number of perfect consonances is possibly higher than requested",*bars)

@__cp_cf
def rule_22(cp : stave.Stave, cf : stave.Stave):
    """À l'avant dernière mesure, on emploiera la sixte majeure lorsque le chant donné sera à la basse et la tierce mineure suivie de l'octave ou de l'unisson lorsqu'il sera à la partie supérieure"""
    # is the cantus firmus above or beyond?
    cp_above = None
    for cpn, cfn in zip(cp.barIter(),cf.barIter()):
        cpn, cfn = [util.to_pitch(n[0]) for n in (cpn,cfn)]
        if cpn != cfn:
            cp_above = cpn.value.step > cfn.value.step
            break
    assert cp_above is not None
    
    # check the before last one bar
    cpn = util.to_pitch(cp.getBar(cp.barNumber-2)[0])
    cfn = util.to_pitch(cf.getBar(cf.barNumber-2)[0])
    cp = cp.copy()
    cp.extend(cf)
    before_last_bar = cp.getBar(cp.barNumber-2)

    if cp_above and not cfn.isQualifiedInterval((6,"major")):
        raise error.CompositionError("The before last interval must be a 6th major",before_last_bar)
    elif not cp_above and not cfn.isQualifiedInterval((3,"minor")):
        raise error.CompositionError("The before last interval must be a 3rd minor",before_last_bar)

@__mix_cp_cf
def rule_23(s: stave.Stave):
    """La première et la dernière mesure sont obligatoirement harmonisées par l'accord de tonique à l'état fondamental"""
    c= chord.Chord(1,s.scale)
    for bar in (s.getBar(0), s.getBar(-1)):
        if not c.isInversion([*bar],0):
            raise error.CompositionError("First and last bar must be at the root positionof the chord of the first degree",bar)

@__counterpoint_only
def rule_24(s: stave.Stave):
    """On évitera de rester dans un ambitus trop restreint (comme une quarte, par exemple), d'effectuer des retours mélodiques sur la même note, ainsi que des répétitions mélodiques rappelant les marches harmoniques"""
    # ambitus
    min = max = None
    for n in s:
        p = n.pitch
        if min is None:
            min = max = p
        elif p.value.step < min.value.step:
            min = p
        elif p.value.step > max.value.step:
            max = p

    ambitus = max.intervalWith(min)

    if ambitus <= 4:
        error.warn(f"The ambitus of your counterpoint is {max.intervalWith(min)}. Do not stay in a too tiny ambitus (like a fourth)",s)
       
    # repetition of a same note
    values = {}
    for n in s:
        p = n.pitch
        nb = values.setdefault(p,0)
        nb += 1
        values[p] = nb

    error.warn(f"Do not repeat too much the same notes.",values)

    # sequence
    _Rule_10(s)

@__counterpoint_only
def rule_25(s: stave.Stave):
    """On évitera, autant que possible, toute formule arpégée"""
    try:
        for i in range(len(s.notes)):
            l = [ s.notes[j] for j in range(i,i+4) ]
            c = chord.Chord.findChord(l,s.scale,best=True)
            if (not isinstance(c,list)) and c.isFullChord(l):
                error.warn("You should avoid every arpeggio",l)
    except IndexError:
        # end of the list
        return



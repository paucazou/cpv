#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende
"""Defines the 21 rules defined 
by Andre Geldage"""
from error import warn
import cp2_note_against_note as cp2
import dispatcher
import harmonic
import melodic
import motion
import stave
import tools
import util

@dispatcher.cp_cf
def rule_1(cp, cf):
    """Dans cette espèce, on doit combiner deux blanches sur chaque ronde du chant donné, excepté à la dernière mesure où l'on doit mettre une ronde contre une ronde"""
    if cp.barNumber != cf.barNumber:
        warn("Number of bars should be equal",cp,cf)


    rp = melodic.rythmic_pattern

    if not rp(cf,"(NSEMIBREVE )+"):
        warn("Cantus firmus must be made of wholes only",cf)

    if not rp(cp,"((RBREVE)|(NMINIM)) NMINIM (NMINIM NMINIM )+NSEMIBREVE "):
        warn("Counterpoint should be in minims, except in the last bar, where it should be a whole",cp)

def rule_2(data):
    """The rule 2 is composed of the rules 22 to 221"""
    pass

@dispatcher.cp_cf
def rule_3(cp, cf):
    """La première mesure doit contenir une demi-pause et une blanche sur le temps faible, en consonance parfaite. (On peut cependant, commencer le contrepoint en même temps que le chant donné : cette dernière manière est moins élégante.)
    """
    if not cp[0].pitch.isPerfectlyConsonantWith(cf[0].pitch):
        warn(f"First note of the counterpoint must be a perfect consonance with the first note of the cantus firmus. In {cp.title}",cp[0],cf[0])

    if cp[0].pos == 0:
        warn(f"It is better to start the counterpoint in the upbeat",cp.title,cp[0])

@dispatcher.cp_cf
def rule_4(cp,cf):
    """Le temps fort doit être en consonance. Il sera toléré, dans les cas difficiles, de placer la dissonance au temps fort, à la condition qu'elle se produise dans la forme de broderie ou de note de passage et que les deux parties procèdent par mouvement contraire et par degrés conjoints"""
    # in this function, we do not look at the first note if the first note is at the downbeat, for it is already checked by function rule_3
    for (n1, na), (n2, nb) in util.pairwise(tools.iter_melodies(cp,cf,alone=False)):
        # is it downbeat?
        if cp.isUpBeat(n2):
            continue
        n1p, nap, n2p, nbp = [util.to_pitch(x) for x in (n1,na, n2, nb)]
        #is it a consonance?
        if n2p.isConsonantWith(nbp):
            continue
        #is it a cambiata or a passing tone?
        is_pt_or_c = cp.isCambiata(n2,False) or cp.isPassingTone(n2,False)
        #is it a conjunct movement?
        is_conjunct = cp.isConjunct(n2)
        #is it a contray motion?
        first = [n1p,nap]
        second = [n2p,nbp]
        first.sort(key=lambda x : x,reverse=True)
        second.sort(key=lambda x : x,reverse=True)
        is_contrary = motion.MotionType.motion(*first,*second) == motion.MotionType.contrary

        warn(f"""The downbeat is dissonant. It must be:
        - a cambiata or passing tone: {is_pt_or_c}
        - come from a conjunct motion: {is_conjunct}
        - come from a contrary motion: {is_contrary}
        """,cp.title,n2)

@dispatcher.cp_cf
def rule_5(cp, cf):
    """Le temps faible peut être en consonance ou en dissonance, pourvu que la dissonance se produise par degrés conjoints"""
    for (n1, na), (n2, nb) in util.pairwise(tools.iter_melodies(cp,cf,alone=False)):
        if not cp.isUpBeat(n2):
            continue
        n1p, nap, n2p, nbp = [util.to_pitch(x) for x in (n1,na, n2, nb)]
        if not n2p.isConsonantWith(nbp):
            if not cp.isConjunct(n2):
                warn(f"If the upbeat is dissonant, it must come from a conjunct motion.",cp.title,n2)

@dispatcher.cp_cf
def rule_6(cp,cf):
    """La dissonance formant note de passage est préférable à celle formant broderie"""
    for (n1, na), (n2, nb) in util.pairwise(tools.iter_melodies(cp,cf,alone=False)):
        n1p, nap, n2p, nbp = [util.to_pitch(x) for x in (n1,na, n2, nb)]
        if not n2p.isConsonantWith(nbp) and cp.isCambiata(n2):
            warn(f"A dissonant passing tone is better than a dissonant cambiata",cp.title,n2)

@dispatcher.cp_cf
def rule_7(cp, cf):
    """Lorsqu'une broderie forme dissonance attractive de quarte augmentée ou de quinte diminuée, et qu'elle retourne sur la note consonante qui l'a précédée, elle est à éviter. Cette règle est applicable aussi à la dissonance de quarte et, avec plus de tolérance, à celles de seconde et de septième"""
    for (n1, na), (n2, nb) in util.pairwise(tools.iter_melodies(cp,cf,alone=False)):
        if not cp.isCambiata(n2):
            continue
        n1p, nap, n2p, nbp = [util.to_pitch(x) for x in (n1,na, n2, nb)]
        if n2p.isQualifiedInterval((5,"diminished"),(4,"augmented"),(4,"perfect")).With(nbp) and n1p.isConsonantWith(nap):
            warn(f"It is forbidden to have a cambiata having an interval of 5th diminished, 4th perfect or augmented that return to a consonant pitch", cp.title,n2)

        elif n2p.isInterval(2,7,True).With(nbp) and n1p.isConsonantWith(nap):
            warn(f"If the cambiata forms a seventh or a second with the other voice, it can return to the consonant note by tolerance only",cp.title,n2)

@dispatcher.cp_cf
def rule_8(cp, cf):
    """L'unisson est toléré au temps faible"""
    for n1, n2 in tools.iter_melodies(cp,cf,alone=False):
        if n1.pitch == n2.pitch:
            if n1 in (cp[-1],cp[0]):
                # it is the last or the first, which can be an unison
                continue
            if cp.isUpBeat(n1):
                warn(f"There is tolerance for unison if the note is upbeat. {cp.title}",n1)
            else:
                warn(f"Unison is forbidden if the note is downbeat. {cp.title}",n1)

@dispatcher.counterpoint_only
def rule_9(cp):
    """La répétition des blanches est interdite"""
    melodic.no_more_than(cp,1)

def rule_10(data):
    """On peut faire deux accords par mesure"""
    warn("It is possible to make two chords by bar")

def rule_11(data):
    """Le mouvement de sixte mineure est permis"""
    warn("6th minor movement is allowed")

@dispatcher.cp_cf
def rule_12(cp, cf):
    """Il est défendu de donner l'impression de l'accord de quarte et sixte au temps fort. On pourra le faire - avec une grande réserve - au temps faible pour conserver un mouvement mélodique élégant, ou pour sauver des quintes ou des octaves"""
    for n1, n2 in tools.iter_melodies(cp,cf,all=True):
        if n1.pitch.isInterval(6,True):
            warn("Please check that there is no impression of second inversion chord", n1, n2)

@dispatcher.cp_cf
def rule_13(cp,cf):
    """Éviter la broderie ou la note de passage qui produit l'intervalle de seconde mineure avec le chant donné"""
    for (n1, na), (n2, nb) in util.pairwise(tools.iter_melodies(cp,cf,alone=False)):
        if not (cp.isCambiata(n2) or cp.isPassingTone(n2)):
            continue
        n1p, nap, n2p, nbp = [util.to_pitch(x) for x in (n1,na, n2, nb)]
        if n2p.semitoneWith(nbp) == 1:
            warn(f"Avoid minor seconds",cp.title,n2)

@dispatcher.cp_cf
def rule_14(cp,cf):
    """Les octaves et les quintes consécutives doivent être séparées par deux blanches.
    This rule is mixed with the following one.
    """
    last_two_5th_by_2 = False
    for elt in harmonic.distance_between_intervals(cp,cf,5):
        if elt.distance < 4:
            if cp.isCambiataOrPassing(elt.second[0]) or cp.arePassingTones(elt.first[0],elt.second[0]) and not last_two_5th_by_2:
                warn("Two fifths are tolerated only separated by a minim if the second is a cambiata or a passing tones or if every fifths is a passing tone",cp.title,elt.first,elt.second)
                last_two_5th_by_2 = True
            else:
                warn("Two fifths must be separated by two minims.",cp.title,elt.first,elt.second)
                last_two_5th_by_2 = False 
        else:
            last_two_5th_by_2 = False 

    for elt in harmonic.distance_between_intervals(cp,cf,8):
        if elt.distance < 4:
            warn(f"Distance between two 8ve should be of two minims",cp.title,elt.first,elt.second)

def rule_15(data):
    """Deux quintes sont tolérées, séparées par une blanche, si la seconde quinte est formée par une note de passage ou une broderie sur un temps faible, ou si elles sont formées toutes deux par des notes de passage. Il ne doit pas y en avoir plus de deux."""
    """This rule is mixed with the previous one and does nothing"""
    pass



@dispatcher.cp_cf
def rule_16(cp, cf):
    """La quinte et l'octave directe sont défendues"""
    harmonic.forbid_direct_interval(cp,cf,5,8)

@dispatcher.cp_cf
def rule_17(cp,cf):
    """
    La fausse relation de triton reste toujours défendue. Il est d'ailleurs facile de l'éviter entièrement grâce à la faculté qu'on a dans cette espèce de faire deux accords par mesure.
    """
    harmonic.forbid_false_relation_tritone(cp,cf,allow_in_minor=True)

def rule_18(data):
    """Il est bien entendu que la fausse relation produite par la tierce et la sixte altérée du mode mineur, n'étant pas de même nature que celle dont il est question ci-haut, n'a pas les mêmes inconvénients, la même dureté"""
    """The content of this function is managed in rule_17"""
    pass

@dispatcher.cp_cf
def rule_19(cp, cf):
    """Lorsque deux dissonances se suivent, il faut que la première soit considérée comme broderie. Il est défendu d'avoir deux dissonances formées par deux notes de passage."""
    for (n1, na), (n2, nb) in util.pairwise(tools.iter_melodies(cp,cf,alone=False)):
        n1p, nap, n2p, nbp = [util.to_pitch(x) for x in (n1,na, n2, nb)]
        if not n1p.isConsonantWith(nap) and not n2p.isConsonantWith(nbp) and not cp.isCambiata(n1,upbeat=False):
            warn(f"If there is two dissonant pitches in a row, the first one must be a cambiata",cp.title,n1,na)

@dispatcher.cp_cf
def rule_20(cp, cf):
    """À l'avant-dernière mesure, on emploiera la quinte au temps fort et la sixte au temps faible lorsque le chant donné sera à la basse. On emploiera la quinte au temps fort et la sixte au temps faible si le chant donné est à la partie supérieure"""
    pattern = f".+ 5p {6 if cp[-2].pitch > cf[-2].pitch else 3}[mM] .. "
    if harmonic.interval_pattern(cp,cf,pattern) is False:
        warn("The penultiem bar must be a fifth, followed by a 6th if the cantus firmus is lower, by a third if it is higher.",cp.title,cp.getBar(-2))

@dispatcher.cp_cf
def rule_21(cp, cf):
    """La dernière mesure sera en octave ou en unisson, en rondes, dans les deux parties"""
    cp_last_bar = cp.getBar(-1)
    cf_last_bar = cf.getBar(-1)
    if len(cf_last_bar) != len(cp_last_bar) != 1:
        warn(f"The last bar must be a whole",cp_last_bar,cf_last_bar)

    if not cp_last_bar[0].pitch.isQualifiedInterval((1,"perfect"),(8,"perfect")).With(cf_last_bar[0].pitch):
        warn(f"The last bar must be an unison or an octave",cp_last_bar,cf_last_bar)


def rule_22(data):
    """rule 2 of cp2_note_against_note"""
    cp2.rule_2(data)



@dispatcher.cantus_firmus_only
def rule_23(target, source):
    """rule 3 of cp2_note_against_note"""
    melodic.transposition(target, source)

@dispatcher.cp_cf
def rule_24(cp,cf):
    """rule 4 of cp2_note_against_note"""
    if not harmonic.perfect_start(cp,cf):
        warn("First chord must be a perfect one",cp,cf)
    if not harmonic.perfect_end(cp,cf):
        warn("Last chord must be a perfect on",cp,cf)

# rule 25 is not followed. see rule 8
@dispatcher.counterpoint_only
def rule_26(cp):
    """rule 6 of cp2_note_against_note"""
    melodic.forbid_chromatism(cp)

@dispatcher.counterpoint_only
def rule_27(s : stave.Stave):
    """rule_24 of cp2_note_against_note"""
    #cp2.rule_24(s)

def rule_28(data):
    """rule_25 of cp2_note_against_note"""
    cp2.rule_25(data)

@dispatcher.cp_cf
def rule_210(cp, cf):
    """Rule 10 of cp2_note_against_note"""
    harmonic.forbid_sequence(cp,cf)

@dispatcher.cp_cf
def rule_211(cp, cf):
    """Rule 11 of cp2_note_against_note"""
    harmonic.intersection(cp,cf)

@dispatcher.counterpoint_only
def rule_212(cp):
    """Rule 12 of cp2_note_against_note"""
    melodic.relative_modulation(cp)

@dispatcher.cp_cf
def rule_214(cp,cf):
    """Rule 14 of cp2_note_against_note"""
    harmonic.forbid_false_relation_tritone(cp,cf,True)

@dispatcher.counterpoint_only
def rule_215(cp):
    """Rule 15 of cp2_note_against_note"""
    melodic.max_interval(cp, 11,[10])

@dispatcher.counterpoint_only
def rule_216(cp):
    """Rule 16 of cp2_note_against_note"""
    melodic.better_conjunct(cp)

@dispatcher.counterpoint_only
def rule_217(cp):
    """Rule 17 of cp2_note_against_note"""
    melodic.forbid_augmented_and_seventh(cp)

@dispatcher.cp_cf
def rule_218(cp, cf):
    """Rule 18 of cp2_note_against_note"""
    print(cp.title)
    print(harmonic.calculate_motion_types(cp,cf))

@dispatcher.cp_cf
def rule_219(cp, cf):
    """Rule 19 of cp2_note_against_note"""
    harmonic.forbid_consecutive_octaves(cp,cf)
    harmonic.forbid_consecutive_fifths(cp,cf)
    harmonic.forbid_direct_interval(cp,cf,5,8)

def rule_220(data):
    """Rule 20 of cp2_note_against_note"""
    cp2.rule_20(data)

@dispatcher.cp_cf
def rule_221(cp, cf):
    """Rule 21 of cp2_note_against_note"""
    for n1, na in tools.iter_melodies(cp,cf,alone=False):
        pn1, pna = [util.to_pitch(n) for n in (n1, na)]
        if not pn1.isImperfectlyConsonantWith(pna):
            warn(f"Prefer imperfect consonances",n1,na,cp.title)



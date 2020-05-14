#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende

from error import warn
import dispatcher
import melodic
import motion
import tools
import util

@dispatcher.one_voice
def rule_1(voice):
    """Tout intervalle diminué ou augmenté est interdit.
    Tout intervalle supérieur à la sixte majeure est interdit, en dehors de l'octave.
    La sixte majeure est tolérée si elle est bien prise mélodiquement."""
    melodic.allow_under_major_sixth(voice)
    for n1, n2 in util.pairwise(voice):
        if n1.pitch.isQualifiedInterval((6,"major")).With(n2.pitch):
            warn(f"Interval allowed by tolerance only: major 6th. Check the melody.",n1,n2,voice.title)


@dispatcher.one_voice
def rule_2(voice):
    """Les tritons en trois notes sont interdits si le mouvement ne change pas de sens"""
    for notes in util.nwise(voice,3):
        np1,np2,np3 = util.to_pitch(notes)
        if np1.semitoneWith(np3) == 6:
            if tools.is_same_direction(np1,np2,np3):
                warn(f"Tritone in 3 notes are forbidden, except when the middle note is lower or greater than the 2 other notes",notes,voice.title)

@dispatcher.one_voice
def rule_3(voice):
    """Les neuvièmes et septièmes en trois notes sont interdits, à moins que l’un des intervalles intermédiaires soit une octave"""
    for notes in util.nwise(voice,3):
        np1, np2, np3 = util.to_pitch(notes)
        if np1.isInterval(7,9).With(np3):
            if not np1.isQualifiedInterval(
                    (2,'minor'),
                    (2,'major'),
                    (8,'perfect')).With(np2):
                warn(f'Between 3 notes, it is not allowed to use 7th or 9nth, except where an octave leap occured between one of these 3 notes',*notes,voice.title)

@dispatcher.one_voice
def rule_4(voice):
    """Les tritons en quatre notes sont à surveiller"""
    for notes in util.nwise(voice,4):
        np1,*other,np4 = util.to_pitch(notes)
        if np1.semitoneWith(np4) == 6:
            warn(f"Tritone in 4 notes must be checked",notes,voice.title)

@dispatcher.one_voice
def rule_5(voice):
    """La sensible doit monter sur la tonique"""
    for n1, n2 in util.pairwise(voice):
        sc1 = voice.scaleAt(n1.pos)
        sc2 = voice.scaleAt(n2.pos)

        if sc1 == sc2 and sc1.isLeading(n1.pitch) and (not sc2.isTonic(n2.pitch)):
            warn(f"The leading tone should go to the tonic.",n1,n2,voice.title)


def rule_6(data):
    """Les voix ne doivent pas toutes effectuer le même mouvement"""
    for group1, group2 in util.pairwise(tools.iter_melodies(*data)):
        assert len(group1) == len(group2) and "Error : pauses not handled"
        is_same_mov =  True
        for i in range(len(group1)):
            for j in range(i+1,len(group1)):
                notes1 = sorted(util.to_pitch([group1[i],group1[j]]),key=lambda x : x.value.semitone)
                notes2 = sorted(util.to_pitch([group2[i],group2[j]]),key=lambda x : x.value.semitone)
                if motion.MotionType.motion(*notes1,*notes2) is not motion.MotionType.direct:
                    is_same_mov = False
                    break
            if is_same_mov is False:
                break

        if is_same_mov:
            warn(f"All the voices shouldn't be in the same direction.",group1,group2)

def rule_7(data):
    """Il est interdit de doubler la sensible"""
    for notes in tools.iter_melodies(*data):
        # get scale
        pos = max([n.pos for n in notes])
        sc = data[0].scaleAt(pos)

        pitches = util.to_pitch(notes)
        if len([p for p in pitches if sc.isLeading(p)]) > 1:
            warn(f"The leading tone can not be doubled",*notes)

def rule_8(data):
    """Les tierces dans le grave sont lourdes et à éviter.
    Here, we choose to warn if the third is under F3"""
    pass


                



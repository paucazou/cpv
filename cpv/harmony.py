#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende

from error import warn
import dispatcher
import melodic
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
            if (np1 < np2 < np3) or (np1 > np2 > np3):
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




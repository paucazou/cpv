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
            error.warn(f"Interval allowed by tolerance only: major 6th. Check the melody.",n1,n2,s.title)




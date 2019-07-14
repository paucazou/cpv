#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende

import chord
import dispatcher
import error
import itertools
import motion
import note
import scalenote
import shared_rules
import util

MT = motion.MotionType
NS = scalenote.NoteScale

def rule_1(data):
    """Prendre une phrase en valeurs égales non modulante
    toujours note contre note
    Only breve and semibreve are accepted."""
    scale_ = data[0].scale
    for n in itertools.chain.from_iterable(data):
        if n.duration not in (note.Duration.MINIM.value,note.Duration.SEMIBREVE.value):
            from IPython import embed;embed()
            raise error.CompositionError(f"The note should be a breve or a semibreve",n)
        if n.pitch not in scale_:
            raise error.CompositionError(f"Modulation not allowed",n)

def rule_2(data):
    """N'user que d'accords consonants à 3 sons"""
    scale_ = data[0].scale
    for x, y, z in zip(*data):
        if not chord.Chord.findChord([x,y,z],scale_):
            raise error.CompositionError(f"Only consonant chords can be used",x,y,z)

@dispatcher.two_voices
def rule_3(s1,s2):
    """Ne pas faire entendre deux Quintes ni deux Octaves de suite dans les mêmes voix, soit par mouvement direct, soit par mouvement contraire"""
    shared_rules.no_consecutive(5,s1,s2)
    shared_rules.no_consecutive(8,s1,s2)

@dispatcher.one_voice
def rule_4(s):
    """Ne pas répéter plus de deux fois la même note dans la même voix"""
    shared_rules.no_more_than(s,2)

def rule_5(data):
    """N'arriver sur une quinte ou une octave par mouvement direct entre les parties extrêmes que lorsque le soprano procède par degrés conjoints"""
    # get the staves
    soprano = util.list_finder(data,"Soprano",fun=lambda s:s.title)
    bass = util.list_finder(data,"Bass",fun=lambda s:s.title)

    # check
    previous_soprano = previous_interval = None

    for n1, n2 in zip(soprano,bass):
        p1, p2 = [util.to_pitch(n) for n in (n1, n2)]
        if previous_interval is not None and MT.motion(*previous_interval,p1,p2) == MT.direct:
            if p1.isInterval(5,8,True).With(p2) and not p1.isInterval(2,1,True).With(previous_soprano):
                raise error.CompositionError(f"It is forbidden to go to a 5th or an 8ve by direct motion with disjunct motion at soprano.", n1,n2)
        previous_soprano = p1
        previous_interval = [p1,p2]


@dispatcher.one_voice
def rule_6(s):
    """Éviter les intervalles mélodiques supérieurs à la Sixte Majeure (octave exceptée) ainsi que les intervalles augmentés ou diminués"""
    previous = None
    for n in s.notes:
        p = util.to_pitch(n)
        if previous is not None:
            interval = previous.intervalWith(p) 
            if interval > 6 and interval != 8:
                raise error.CompositionError(f"It is forbidden to use melodic interals over the 6th which is not a 8ve",previous,n)
            if p.qualifiedIntervalWith(previous).quality in ("diminished","augmented"):
                raise error.CompositionError(f"It is forbidden to use diminished or augmented intervals",previous,n)

        previous = p


def rule_7(data):
    """Résoudre la sensible sur la tonique, excepté dans l'enchaînement du 5è au 6è degré"""
    scale_ = data[0].scale
    pnotes = None
    for i, notes in enumerate(zip(*data)):
        nsnotes = [NS(scale_,n) for n in notes]
        if pnotes is not None:
            for voice, n in enumerate(pnotes):
                if n != nsnotes[voice] and n.isLeading and not nsnotes[voice].isTonic:
                    # check the previous chord
                    pchords = chord.Chord.findChord(pnotes,scale_)
                    problem = False
                    if 5 in [x.degree for x in pchords]:
                        # check current chord
                        cchords = chord.Chord.findChord(notes,scale_)
                        if 6 not in [x.degree for x in cchords]:
                            problem = True
                    else:
                        problem = True

                    if problem:
                        error.warn(f"The leading should go to the tonic, except in the 5th to 6th movement. If this is the cantus firmus, please do not take care of this warning.",notes)


        pnotes = nsnotes

def rule_8(data):
    """N'user de la quarte et sixte que pour les cadences"""
    scale_ = data[0].scale
    def check_degree(notes, degree):
        c = chord.Chord.findChord(notes,scale_)
        try:
            c = [_c for _c in c if _c.degree == degree][0]
        except IndexError:
            raise error.CompositionError(f"{degree}th degree was expected after 2nd inversion chord",notes)

        if not c.isInversion(notes,0):
            raise error.CompositionError(f"After 2nd inversion root, the {degree}th must be at root position",notes)


    for i, notes in enumerate(zip(*data)):
        c = chord.Chord.findChord(notes,scale_,best=True)
        if isinstance(c,chord.Chord) and c.isInversion(notes,2):
            if c.degree != 1:
                raise error.CompositionError(f"The 2nd inversion chord must be of the 1st degree only",notes)

            # check the Vth degree
            check_degree(list(zip(*data))[i+1],5)
            # check the 1st degree
            check_degree(list(zip(*data))[i+2],1)

@dispatcher.two_voices
def rule_9(s1, s2):
    """Ne pas employer de croisements ni d'unissons"""
    s1_high = s1.notes[0].pitch > s2.notes[0].pitch
    for n1, n2 in zip(s1.notes,s2.notes):
        p1,p2 = [util.to_pitch(n) for n in (n1,n2)]
        if p1 == p2:
            raise error.CompositionError(f"Unisons are forbidden",n1,n2)

        if (s1_high and p2 > p1) or (not s1_high and p1 > p2):
            raise error.CompositionError(f"Intersection is forbidden",n1,n2)

def rule_10(data):
    """Éviter l'accord diminué à l'état direct"""
    scale_ = data[0].scale
    previous = None
    for j,notes in enumerate(zip(*data)):
        c = chord.Chord.findChord(notes,scale_,True)
        if isinstance(c,chord.Chord) and c.isQuality("diminished"):
            for i,n in enumerate(notes):
                np = util.to_pitch(n)
                if c.findPosition(np) == 5:
                    err = error.CompositionError(f"Diminished chord must be prepared and resolved",n)
                    #check previous pos 
                    if np != previous[i]:
                        raise err
                    # check next pos
                    if (j + 1) == len(data[0]):
                        raise err
                    following_note = data[i][j+1]
                    following_pitch = util.to_pitch(following_note)
                    if np.semitone - following_pitch.semitone != 1:
                        raise err

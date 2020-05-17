#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende

from error import warn
import chord
import dispatcher
import harmonic
import melodic
import motion
import pitch
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

@dispatcher.two_voices
def rule_8(s1,s2,min=pitch.Pitch.F3):
    """Les tierces dans le grave sont lourdes et à éviter.
    Here, we choose to warn if the third is under F3"""
    for n1, n2 in tools.iter_melodies(s1,s2):
        np1,np2 = util.to_pitch((n1,n2))
        if np1.isInterval(3).With(np2) and (np1 < min and np2 < min):
            warn(f"Low thirds should be avoided",n1,n2,s1.title,s2.title)


@dispatcher.voice_and_following
def rule_9(s1,s2):
    """
    1. Le soprano et le contralto ne doivent pas être éloignés de la voix inférieure d’un intervalle supérieur à l’octave.
    2. Le ténor et la basse ne doivent pas être éloignés d’un intervalle supérieur à la douzième.
    3. Il est possible d’excéder l’intervalle maximal dans le cas d’un saut d’octave, de préférence suivi d’un mouvement mélodique inverse.
    """
    titles = (s1.title,s2.title)
    max = 12 if titles == ("Tenor","Bass") else 8

    for n1, n2 in tools.iter_melodies(s1,s2):
        np1,np2 = util.to_pitch((n1,n2))
        if np1.intervalWith(np2) > max:
            warn(f"Max interval between {s1.title} and {s2.title} is {max}, except if there's a melodic octave, or other thing of that kind followed by a melodic contrary movement. Is that the case?",n1,n2,*titles)

@dispatcher.two_voices
def rule_10(s1,s2):
    """Le mouvement contraire est préférable à l’oblique, lui-même préférable au direct."""
    titles = (s1.title,s2.title)
    movs = harmonic.calculate_motion_types(s1,s2)
    warn(f"""Between {s1.title} and {s2.title}:
    contrary motions: {movs[motion.MotionType.contrary]}
    direct motions: {movs[motion.MotionType.direct]}
    oblique motions: {movs[motion.MotionType.oblique]}
    no motion: {movs[motion.MotionType.no]}
    """
    )

def rule_11(data):
    """Les octaves et quintes consécutives sont interdites entre deux accords, à moins que ces deux intervalles ne soient séparés par l’équivalent d’une ronde (ou d’une mesure si on n'est pas en 4/4).
    """
    chords = chord.RealizedChord.chordify(data)
    distance_max = data[0].breve_value
    def func(interval):
        for c1,c2 in util.pairwise(chords):
            res = c1.hasParallelIntervalWith(c2,interval)
            for titles, results in res.items():
                for r in results:
                    if r.distance < distance_max:
                        warn(f"Parallel {interval} found between {titles[0]} and {titles[1]}.",c1,c2)

    func((8,"perfect"))
    func((5,"perfect"))

def rule_12(data):
    """La quinte juste suivie d’une quinte diminuée est tolérée si ce n’est pas entre parties extrêmes.
    """
    chords = chord.RealizedChord.chordify(data)
    extreme_titles = [data[0].title,data[-1].title]
    distance_max = data[0].breve_value
    for c1, c2 in util.pairwise(chords):
        res = c1.hasParallelIntervalWith(c2,5)
        for titles, results in res.items():
            tolerance = "tolerated" if titles != extreme_titles else "forbidden"
            for r in results:
                if r.distance < distance_max:
                    # is it a perfect 5th followed by a diminished 5th?
                    if r.first[0].pitch.isQualifiedInterval((5,'perfect')).With(r.first[1].pitch) and r.second[0].pitch.isQualifiedInterval((5,'diminished')).With(r.second[0].pitch):
                        warn(f"Perfect fifth followed by a diminished 5th is {tolerance} between {titles[0]} and {titles[1]}.", r.first,r.second)





                



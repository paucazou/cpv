#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende

from error import warn
import chord
import dispatcher
import itertools
import harmonic
import melodic
import motion
import pitch
import tessitura
import tools
import util

@dispatcher.one_voice
def rule_1(voice):
    """Tout intervalle diminué ou augmenté est interdit.
    Tout intervalle supérieur à la sixte majeure est interdit, en dehors de l'octave.
    La sixte majeure est tolérée si elle est bien prise mélodiquement.
    Ces intervalles interdits peuvent être bons ou tolérés lors d'une modulation.
    """
    melodic.allow_under_major_sixth(voice)
    for n1, n2 in util.pairwise(voice):
        if n1.pitch.isQualifiedInterval((6,"major")).With(n2.pitch):
            addendum = "Possibly good thanks to the modulation. " if melodic.modulation_at(n2,voice) else ""
            warn(f"Interval allowed by tolerance only: major 6th. {addendum}Check the melody.",n1,n2,voice.title)


@dispatcher.one_voice
def rule_2(voice):
    """Les tritons en trois notes sont interdits si le mouvement ne change pas de sens.
    Ces intervalles interdits peuvent être bons ou tolérés lors d'une modulation.
    """
    for notes in util.nwise(voice,3):
        np1,np2,np3 = util.to_pitch(notes)
        if np1.semitoneWith(np3) == 6:
            if tools.is_same_direction(np1,np2,np3):
                if melodic.modulation_at(notes[1]) or melodic.modulation_at(notes[-1]):
                    msg = "Tritone in 3 notes is possible when a modulation occurs."
                else:
                    msg = "Tritone in 3 notes are forbidden, except when the middle note is lower or greater than the 2 other notes"
                warn(msg,notes,voice.title)

@dispatcher.one_voice
def rule_3(voice):
    """Les neuvièmes et septièmes en trois notes sont interdits, à moins que l’un des intervalles intermédiaires soit une octave.
    Ces intervalles interdits peuvent être bons ou tolérés lors d'une modulation.
    """
    for notes in util.nwise(voice,3):
        np1, np2, np3 = util.to_pitch(notes)
        if np1.isInterval(7,9).With(np3):
            if not np1.isQualifiedInterval(
                    (2,'minor'),
                    (2,'major'),
                    (8,'perfect')).With(np2):
                if melodic.modulation_at(notes[1]) or melodic.modulation_at(notes[-1]):
                    msg = "7th or 9th in 3 notes are possible in a modulation"
                else:
                    msg = 'Between 3 notes, it is not allowed to use 7th or 9nth, except where an octave leap occured between one of these 3 notes'

                warn(msg,*notes,voice.title)

@dispatcher.one_voice
def rule_4(voice):
    """Les tritons en quatre notes sont à surveiller"""
    for notes in util.nwise(voice,4):
        np1,*other,np4 = util.to_pitch(notes)
        if np1.semitoneWith(np4) == 6:
            warn(f"Tritone in 4 notes must be checked.",notes,voice.title)

def rule_5(data):
    """La sensible doit monter sur la tonique.
    Si la sensible est dans l'une des répétitions d'une marche d'harmonie,
    cette règle n'est pas nécessaire."""
    st = tools.SequenceTracker(data)
    for voice in data:
        for n1, n2 in util.pairwise(voice):
            sc1 = voice.scaleAt(n1.pos)
            sc2 = voice.scaleAt(n2.pos)

            if sc1 == sc2 and sc1.isLeading(n1.pitch) and (not sc2.isTonic(n2.pitch)) and not st.isInRestatement(n1):
                warn(f"The leading tone should go to the tonic, except in a restatement of a sequence.",n1,n2,voice.title)


def rule_6(data):
    """Les voix ne doivent pas toutes effectuer le même mouvement, sauf si on enchaîne deux accords de sixtes."""
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
            # are there 2 consecutive sixth?
            pos1 = max(group1,key=lambda x:x.pos).pos
            scale1 = data[0].scaleAt(pos1)
            c1 = chord.AbstractChord.findBestChord(group1,scale1)
            pos2 = max(group2,key=lambda x:x.pos).pos
            scale2 = data[0].scaleAt(pos2)
            c2 = chord.AbstractChord.findBestChord(group2,scale2)

            if not (c1.isInversion(group1,1) and c2.isInversion(group2,1)):
                warn(f"All the voices shouldn't be in the same direction.",group1,group2)



def rule_7(data):
    """Il est interdit de doubler la sensible"""
    st = tools.SequenceTracker(data)
    for notes in tools.iter_melodies(*data):
        # get scale
        pos = max([n.pos for n in notes])
        sc = data[0].scaleAt(pos)
        leadings = [n for n in notes if sc.isLeading(n.pitch) and not st.isInRestatement(n)]
        if len(leadings) > 1:
            warn(f"The leading tone can not be doubled, except in a restatement of a sequence",*notes)

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
                        if interval == 5:
                            first_itvl = r.first[0].pitch.qualifiedIntervalWith(r.first[1].pitch)
                            second_itvl = r.second[0].pitch.qualifiedIntervalWith(r.second[1].pitch)
                            ## 2 diminished 5th
                            if first_itvl == second_itvl == (5,"diminished"):
                                continue
                            ## the second is a diminished 5th
                            if second_itvl == (5,"diminished"):
                                continue
                            ## all other possibilities: error
                        warn(f"Parallel {interval} found between {titles[0]} and {titles[1]}.",c1,r.first,c2,r.second)

    func((8,"perfect"))
    func(5)

def rule_12(data):
    """La quinte juste suivie d’une quinte diminuée est tolérée si ce n’est pas entre parties extrêmes.
    """
    chords = chord.RealizedChord.chordify(data)
    extreme_titles = (data[0].title,data[-1].title)
    distance_max = data[0].breve_value
    for c1, c2 in util.pairwise(chords):
        res = c1.hasParallelIntervalWith(c2,5)
        for titles, results in res.items():
            tolerance = "tolerated" if titles != extreme_titles else "forbidden"
            for r in results:
                if r.distance < distance_max:
                    # is it a perfect 5th followed by a diminished 5th?
                    if r.first[0].pitch.isQualifiedInterval((5,'perfect')).With(r.first[1].pitch) and r.second[0].pitch.isQualifiedInterval((5,'diminished')).With(r.second[1].pitch):
                        warn(f"Perfect fifth followed by a diminished 5th is {tolerance} between {titles[0]} and {titles[1]}.", r.first,r.second)


def rule_13(data):
    """Deux quintes diminuées peuvent être enchaînées."""
    return True

def rule_14(data):
    """Les octaves et quintes par mouvement direct ne sont autorisées que si la voix supérieure procède par mouvement conjoint.
        La quinte directe est tolérable si la voix inférieure procède par mouvement conjoint, à condition que l’une des voix soit le ténor ou le contralto et que la voix inférieure aboutisse à un des bons degrés (I – IV – V) de la gamme.
    La quinte directe est tolérable si l’une des notes de la quinte appartient à l’accord précédent, même par mouvement disjoint, à condition qu’elle ait une bonne sonorité.
    À l’intérieur d’un même accord, on tolère des quintes et des octaves directes, y compris par mouvement direct et disjoint.
    """
    chords = chord.RealizedChord.chordify(data)
    extreme_titles = data[0].title, data[-1].title
    for s1,s2 in itertools.combinations(data,2):
        for (n1,n2), (na, nb) in util.pairwise(tools.iter_melodies(s1,s2)):
            # is it a fifth or an octave?
            if not na.pitch.isQualifiedInterval((8,'perfect'),(5,'perfect'),(5,'diminished'),(5,'augmented')).With(nb.pitch):
                continue
            # is it in the same chord?
            for c in chords:
                if (n1,n2,na,nb) in c:
                    continue
            # is it a direct 5th or octave?
            if motion.MotionType.motion(n1,n2,na,nb) != motion.MotionType.direct:
                continue
            # does the upper voice proceed by conjunct movement?
            if n1.pitch.semitoneWith(na.pitch) in (1,2):
                continue
            # if it is an octave, there's no more tolerance: it's an error
            if na.pitch.isInterval(8,True).With(nb.pitch):
                warn(f"Direct octaves with no conjunct movement is forbidden.",n1,n2,na,nb,s1.title, s2.title)
                continue
            # is it a direct 5th with lower voice going to I, IV or V
            # by conjunct movement in non extreme parts?
            if extreme_titles != (s1.title, s2.title):
                # get scale of the second interval: there may be a modulation between the 2 intervals.
                pos = max(na.pos,nb.pos)
                current_scale = s2.scaleAt(pos)
                if n2.pitch.semitoneWith(nb.pitch) in (1,2) and current_scale.is1_4_5(nb.pitch) :
                    warn(f"Tolerance: direct fith with lower voice going to I, IV, V by conjunct movement between non extreme parts is tolerated. Do not hesitate to find a better disposition",n1,n2,na,nb,s1.title,s2.title)
                    continue
            # is it a direct 5th with a note of the 5th in the previous chord?
            broken=False
            for c1, c2 in util.pairwise(chords):
                if (na, nb) in c2 and (na in c1 or nb in c1):
                    warn(f"Tolerance: direct fifth is tolerated if one of the notes of the 5th can be heard in the previous chord AND if the sound is good. Please check that.",n1,n2, na,nb, s1.title,s2.title)
                    broken=True
                    break
            if broken:
                continue
            # error
            warn(f"""Direct 5th are forbidden, except:
            - when the higher voice moves by conjunct motion
            - when, except in extreme parts, the lower voice moves by conjunct motion to I, IV, V
            - when the note of the 5th can be heard in the previous chord
            - in a change of position inside a chord.
            """, n1,n2, na,nb,s1.title,s2.title)




@dispatcher.two_voices
def rule_15(s1,s2):
    """L'unisson est interdit
    Dans les accords parfaits, l'unisson peut être toléré:
        - sur les temps faibles,
        - en cas de saut d'octave
        - si la basse monte haut
        - si le soprano descend bas
        - mais l'unisson ténor-alto est très maladroit.
    """
    for n1, n2 in tools.iter_melodies(s1,s2):
        p1,p2 = [util.to_pitch(n) for n in (n1,n2)]
        if p1 == p2:
            warn(f"""Unisons are forbidden.
            There are tolerances in perfect chords progression at root position if:
            - the unison is in a downbeat
            - there is an octave leap
            - if the bass is really high, or the soprano really low
            - note that the unison alto-tenor is really clumsy.
            """,n1,n2,s1.title,s2.title)

@dispatcher.two_voices
def rule_16(s1,s2):
    """Les croisements sont interdits"""
    is_s1_higher = s1.notes[0].pitch > s2.notes[0].pitch
    for n1, n2 in tools.iter_melodies(s1,s2):
        p1,p2 = [util.to_pitch(n) for n in (n1,n2)]
        if (is_s1_higher and p2 > p1) or (not is_s1_higher and p1 > p2):
            warn(f"Intersection is forbidden",n1,n2,s1.title,s2.title)

@dispatcher.one_voice
def rule_17(v):
    """Une voix ne doit pas sortir de sa tessiture."""
    P = pitch.Pitch
    soprano = tessitura.Tessitura(P.C4,P.A5,[P.Bb5,P.B3])
    alto = tessitura.Tessitura(P.G3,P.D5,[P.Fs3,P.Ds5,P.Eb5,P.E5,P.F5])
    tenor = tessitura.Tessitura(P.D3,P.G4,[P.C3,P.Cs3,P.Db3, P.Gs4,P.Ab4,P.A4,P.Bb4])
    bass = tessitura.Tessitura(P.G2,P.D4,[P.E2,P.F2,P.Fs2,P.Gb2, P.Ds4,P.Eb4,P.E4,P.F4])

    tessituras = {'Bass':bass,'Tenor':tenor,'Alto':alto,'Soprano':soprano}
    tessituras[v.title].check(v)

def rule_18(data):
    """
    On peut doubler n’importe quelle note de l’accord.
    On peut supprimer la quinte ; dans ce cas, il vaut mieux tripler la fondamentale, mais dans certains cas, on peut aussi doubler la tierce et la fondamentale.
    La meilleure doublure est généralement la fondamentale. Doubler l’un des bons degrés est également bon.
    """
    pass

def rule_19(data):
    """On ne supprime pas la tierce"""
    for notes in tools.iter_melodies(*data,all=True):
        pos = max(notes,key=lambda x:x.pos).pos
        c = chord.AbstractChord.findBestChord(notes,data[0].scaleAt(pos))
        if not c.hasThird(notes):
            warn(f"In a chord, the third must be present: ",notes)

def rule_20(data):
    """La fausse relation de triton est proscrite."""
    st = tools.SequenceTracker(data)
    for notes1, notes2 in util.pairwise(tools.iter_melodies(*data,alone=False)):
        clef = lambda n : n.pitch
        h1 = max(notes1,key=clef)
        l1 = min(notes1,key=clef)
        h2 = max(notes2,key=clef)
        l2 = min(notes2,key=clef)
        if h1 == h2 or l1 == l2:
            continue
        if ((h1.pitch.isTritoneWith(l2.pitch) or l1.pitch.isTritoneWith(h2.pitch)) and
                (not st.isInRestatement(h1) and not st.isInRestatement(h2))):
            warn(f"False relation of tritone is forbidden between extreme parts, except inside the restatement in a sequence.",notes1,notes2)


def rule_21(data):
    """
    Dans les accords de sixte, il est interdit de doubler la basse, sauf si :
        1. la basse est l’un des bons degrés (I – IV – V) ;
        2. lors d’un changement de position ; // TODO send a warning
        3. si on arrive à la basse et à sa doublure par mouvement contraire et conjoint (fa et la vers sol, par exemple)
    """
    for group1, group2 in util.pairwise(tools.iter_melodies(*data)):
        c2 = chord.AbstractChord.findBestChordFromStave(group2,data[0])
        # is it a 6th chord?
        if not c2.isInversion(group2,1):
            continue
        # is the bass doubled?
        basses = [x for x in group2 if c2.isPosition(x,3)]
        if len(basses) <= 1:
            continue
        # is the bass I,IV or V?
        bass = sorted(group2,key=lambda n:n.pitch)[0]
        pos = max(group2,key=lambda n : n.pos).pos
        current_scale = data[0].scaleAt(pos)
        if current_scale.is1_4_5(bass.pitch):
            continue
        # is the bass in a change of position?
        c1 = chord.AbstractChord.findBestChordFromStave(group1,data[0])
        if c1 == c2:
            warn(f"It is possible, but potentially not really good to double the bass of a sixth chord when the notes change their position in the chord.",group2)
            continue
        # is the movement to the bass and its octave conjunct and contrary?
        ## is the note of the bass found more than 2 times?
        if len(basses) > 2:
            warn(f"It is not possible to double more than 2 times the bass in a 6th chord.",group2)
            continue
        indices = [group2.index(n) for n in basses]
        previous_notes = [n for i,n in enumerate(group1) if i in indices]
        if (motion.MotionType.motion(*previous_notes,*basses) == motion.MotionType.contrary ) and previous_notes[0].pitch.isConjunctWith(basses[0].pitch) and previous_notes[1].pitch.isConjunctWith(basses[1].pitch):
            warn(f"It is possible to double the bass by conjunct and contrary motion",group1,group2)
            continue

        # error
        warn(f"""It is forbidden to double the bass of a sixth chord, except when:
        - the bass is I, IV, V,
        - there is a change of position in the chord
        - there is a conjunct and contrary motion to the bass and its octave.""",
        group2)

def rule_22(data):
    """La quarte et sixte doit être préparée, c’est-à-dire que l’une des deux notes formant la quarte doit se trouver à l’accord précédent et se prolonger par syncope dans l’accord de quarte et sixte.
    La sixte et quarte sur dominante (deuxième renversement de l’accord de tonique) n’a pas besoin d’être préparée, même si c’est la dominante d’un nouveau ton.
    """
    for notes in tools.iter_melodies(*data):
        c = chord.AbstractChord.findBestChordFromStave(notes,data[0])
        # is it a 2nd inversion chord?
        if not c.isInversion(notes,2):
            continue
        # is it a chord on dominant?
        pos = max(notes,key=lambda x : x.pos).pos
        current_scale = data[0].scaleAt(pos)
        bass = [n for n in notes if c.isFifth(n)][0]
        if current_scale.isDominant(bass.pitch):
            continue
        # is one of the notes prepared?
        is_prepared = False
        for n in notes:
            if (c.isFifth(n) or c.isRoot(n) ) and n.pos < pos:
                is_prepared = True
                break
        if is_prepared:
            continue
        else:
            warn(f"In a 2nd inversion chord, one of the notes of the fourth (the root or the fifth of the chord) must be present in the previous chord at the pitch and the same voice and joined to the note in the chord by syncopation, except for a chord which bass is the dominant: in that case, it is not necessary to prepare it.",notes)


def rule_23(data):
    """
    La quarte doit être sauvée : soit la note supérieure reste en place ou descend d’un degré ; soit la basse reste en place.
    """
    for group1, group2 in util.pairwise(tools.iter_melodies(*data)):
        c = chord.AbstractChord.findBestChordFromStave(group1,data[0])
        if not c.isInversion(group1,2):
            continue
        last_pos = min(group1,key=lambda x : x.last_pos).last_pos
        is_correct = False
        for n,n2 in zip(group1,group2):
            if c.isFifth(n) and n.last_pos > last_pos:
                is_correct = True
                break
            elif c.isRoot(n):
                if (n.last_pos > last_pos):
                    is_correct = True
                    break
                elif n.pitch > n2.pitch and n.pitch.isConjunctWith(n2.pitch):
                    is_correct = True
                    break
        if is_correct:
            continue
        else:
            warn(f"In a 2nd inversion chord, the root must go to lower degree by conjunct motion, or must continue by syncopation, or the 5th must continue by syncopation",group1)

def rule_24(data):
    """
    1. L’enchaînement d’une marche à une autre n’excuse aucune faute.
    2. L’enchaînement de la dernière marche et de l’accord qui suit doit se faire sans faute.

    """
    st = tools.SequenceTracker(data)
    print(f"{len(st)} sequence{'s' if len(st) > 1 else ''} found.")
    for i, ((start,end), nb) in enumerate(st.sequences.items()):
        print(f"Sequence n° {i+1}: motif: {start}/{end}. Number of restatements: {nb}")

@dispatcher.two_voices
def rule_25(s1,s2):
    """
    1. La fausse relation chromatique est prohibée. À distance, elle peut être bonne.
    2. Tout changement chromatique s’effectue dans la même partie.
    3. Il est interdit de doubler la note qui est modifiée chromatiquement dans les deux accords.
    4. On tolère le doublement de la note caractéristique si on aboutit à la note chromatique par mouvement contraire.
    """
    warn(f"Please check by ear that there are no distant false relations")
    for (h1,l1), (h2,l2) in util.pairwise(tools.iter_melodies(s1,s2)):
        if (h1.pitch.isChromaticInflectionWith(l2.pitch,min=True) or l1.pitch.isChromaticInflectionWith(h2.pitch,min=True)):
            if (h1.pitch.isSameNote(l1.pitch) or h2.pitch.isSameNote(l2.pitch)) and motion.MotionType.motion(h1,l1,h2,l2) == motion.MotionType.contrary:
                text = "Doubling one of the notes of a chromatism when there's a contrary motion is only tolerated."
            else:
                text = "It is forbidden to do a chromatic false relation"
            warn(text,h1,l1,h2,l2,s1.title,s2.title)
            
@dispatcher.extreme_parts
def rule_26(soprano,bass): 
    """
    La quinte directe entre parties extrêmes par modulation et mouvement chromatique est prohibée.
    """
    for (h1,l1), (h2,l2) in util.pairwise(tools.iter_melodies(soprano,bass)):
        mot = motion.MotionType.motion(h1,l1,h2,l2)
        if mot == motion.MotionType.direct and (h1.pitch.isChromaticInflectionWith(h2.pitch) or l1.pitch.isChromaticInflectionWith(l2.pitch)):
            warn(f"A direct fifth by modulation and chromatic motion is forbidden",h1,h2,l1,l2,soprano.title,bass.title)


@dispatcher.one_voice
def rule_27(voice):
    """
    Si la note caractéristique est la sensible, elle devra ensuite monter sur la tonique ; si c’est la sous-dominante, elle doit descendre sur la médiante ; ou rester en place avant de suivre le mouvement obligé.
    """
    for mod in voice.modulations:
        n1 = voice.getNoteAtPos(mod.pos)
        n1_degree = mod.scale.findDegree(n1.pitch)
        if n1_degree not in (7,4):
            continue

        expected_degree = 1 if n1_degree == 7 else 3
        n2 = voice.getNoteAtPos(n1.last_pos)
        while n2 and n1.pitch == n2.pitch:
            n2 = voice.getNoteAtPos(n2.last_pos)

        if not n2 or not mod.scale.isDegree(n2.pitch,expected_degree):
            warn(f"In a modulation, the {n1_degree} must go to the {expected_degree}, or stay on place before going to the {expected_degree}. Here, the {n1_degree} goes to the {mod.scale.findDegree(n2.pitch)}.",n1,n2,voice.title)

def rule_28(data):
    """Il est bon de préparer la septième de dominante (elle doit alors être présente à l’accord précédent à la même voix et à la même octave, reliée de préférence par syncope) mais ce n’est pas obligatoire.
    """
    from IPython import embed;embed()
    chords = chord.RealizedChord.chordify(data)
    @dispatcher.one_voice
    def func(voice):
        for (n1,c1), (n2,c2) in util.pairwise(tools.iter_notes_and_chords(voice,chords)):
            if c2.abstract.isSeventh(n2) and n1.pitch != n2.pitch:
                warn(f"It is good to prepare the dominant seventh, though not mandatory",n2,voice.title)

    func(data)


    



                



#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende

import itertools
import harmonic
import motion
import note
import pitch
import scale
import scalenote
import tools
import util
# TODO add the ninth if necessary

class AbstractChord:
    """A chord"""

    def __new__(cls,degree,scale_,seventh=False):
        """Return a __minor_chord if necessary"""

        if scale_.mode is scale.Mode.m_full:
            return object.__new__(_minor__chord)

        return object.__new__(cls)
    
    def __init__(self, degree, scale, seventh=False):
        """Creates the chord of the degree required"""
        self.degree = degree
        self.scale = scale
        self.is_seventh = seventh
        self._generate_notes()

    def __contains__(self, note): # TEST
        """True if note is in chord.
        note can be a Pitch, a Note or a NoteScale 
        or a tuple. In this case, return True
        if every note in the tuple are in self
        """
        try: # iterable?
            if len(note) > 1:
                return self.__contains__(note[0]) and self.__contains__(note[1:])
            else:
                return self.__contains__(note[0])

        except (ValueError,TypeError): # not iterable
            note = util.to_pitch(note)

        return note in self.notes

    def __eq__(self,other):
        """True if other is equal to self"""
        return (self.degree == other.degree and
                self.scale == other.scale and
                self.is_seventh == other.is_seventh and
                self.notes == other.notes)

    def __repr__(self):
        return f"AbstractChord<{self.degree}|{self.scale}>"

    def _generate_notes(self):
        """Generates the notes which can figure in the chord"""
        def _generate_degrees():
            d = self.degree -1
            degrees = []
            while d < len(self.scale.notes):
                degrees += [d,d+2,d+4]
                if self.is_seventh:
                    degrees.append(d+6)
                d+=7
            return degrees

        degrees = _generate_degrees()

        self.notes = [n for i, n in enumerate(self.scale.notes) if i in degrees ]



    def isPosition(self, note, i:int): # TEST
        """True if note is in position i
        in the chord.
        i can be 1, 3, 5 or 7
        """
        assert i in (1,3,5,7)
        try:
            return i == self.findPosition(note) 
        except ValueError:
            return False

    def findPosition(self, note) -> int: # TEST
        """Find if the note is the root,
        the third, the fifth or the seventh
        raise ValueError if it can't be found"""
        note = util.to_pitch(note)
        try:
            index = self.notes.index(note)
        except ValueError:
            raise ValueError("Note not found in chord")

        j = 3 if self.is_seventh else 2
        while index > j:
            index -= (j+1)

        return {0:1, 1:3, 2:5, 3:7}[index]

    def isInversion(self, chord, i) -> bool: # TEST
        """True if chord has the inversion i"""
        try:
            return self.findInversion(chord) == i
        except ValueError:
            return False

    def _qualify(self):
        """Qualify the chord. The chord following the
        quality of the intervals:
        -5th: perfect, augmented, diminished
        -3rd: major/minor
        This information is returned as a tuple of string
        """
        #TODO doesn't work well for non triads chords
        root = self.notes[0]
        third = self.notes[1]
        fifth = self.notes[2]
        q1 = root.qualifiedIntervalWith(third).quality
        q2 = root.qualifiedIntervalWith(fifth).quality
        return q1, q2


    def isQuality(self,*args):
        """True if every *args match
        the quality of the chord
        """
        _quality = self.quality
        for a in args:
            if a not in _quality:
                return False
        return True

    quality = property(_qualify)  # TEST


    def findInversion(self,chord) -> int: # TEST
        """Find the inversion of the chord.
        0 : root position
        1 : first inversion
        2 : second inversion
        3 : third inversion
        Raise ValueError if chord is not a
        self chord
        """
        chord = [util.to_pitch(n) for n in chord]
        chord.sort(key=lambda x : x.value.step)

        # check that every note is in the chord
        for n in chord:
            self.findPosition(n)

        bass = self.findPosition(chord[0])
        return { 1:0, 3:1, 5:2, 7:3}[bass]

    @staticmethod
    def findChord(notes,scale, seventh=False,best=False): # TEST
        """Given a sequence of notes,
        find the chord and return it.
        If more than one chord can be found,
        return every chord possible.
        If best is set, return the chord
        which matches more the chord
        """
        chords = [ AbstractChord(i,scale,seventh) for i in range(1,8) ]
        notes = [ util.to_pitch(n) for n in notes ]

        returned = [ c for c in chords if notes in c ]
        if best:
            for c in chords:
                if c.isFullChord(notes):
                    return c

        return returned

    @staticmethod
    def findBestChord(notes,scale):
        """Similar to findChord(seventh=True,best=True), but the way to select
        the best chord is different.
        """
        chords = AbstractChord.findChord(notes,scale,seventh=True,best=True)
        if isinstance(chords,AbstractChord):
            return chords
        if len(chords) == 1:
            return chords[0]

        # is root absent?
        nchords = chords[:]
        chords = [ elt for elt in chords if elt.hasRoot(notes) ]
        if len(chords) == 0:
            return nchords[0]
        if len(chords) == 1:
            return chords[0]

        # which note is doubled?
        """Le but de cette section serait de regarder quelles notes sont doublées:
        si c'est la fondamentale, la tierce, la quinte, etc. Seraient privilégiés
        les accords dont les doublures sont la fondamentale ou la quinte. Cela dit,
        les résultats sont les mêmes que pour la section suivante.
        À voir en fonction des résultats in vivo"""

        # What is the best degree possible (only two different notes, or even one)
        best_degrees = (1, 5, 4, 2, 6, 7, 3)
        chords.sort(key=lambda c : best_degrees.index(c.degree))
        return chords[0]

    @classmethod
    def findBestChordFromStave(cls,notes,stave):
        """Returns the same thing as findBestChord,
        but takes a stave to find the correct scale.
        It is not mandatory that the notes are in the stave.
        notes must be an iterable of Note, not Pitch
        """
        pos = max(notes,key=lambda x:x.pos).pos
        scale = stave.scaleAt(pos)
        return cls.findBestChord(notes,scale)


    @staticmethod
    def isChord(notes,scale,seventh=False) -> bool: # TEST
        """Is the sequence of notes
        a chord?
        """
        return bool(AbstractChord.findChord(notes,scale,seventh))

    def isFullChord(self,notes) -> bool: #TEST
        """Given a sequence of notes, True if notes
        contains at least a root, a third, a fifth
        and optionally a seventh. (if is_seventh is True)
        """
        pos = [1,3,5]
        if self.is_seventh:
            pos.append(7)

        required = {n:False for n in pos}
        notes = [ util.to_pitch(n) for n in notes]
        try:
            for n in notes:
                required[self.findPosition(n)] = True
        except ValueError:
            return False

        return not (False in required.values())

    def getAbstractPitchAtPosition(i : int) -> pitch.Pitch:
        """Return the pitch at position i.
        i must be one of the degrees in the chord:
        1, 3, 5, 7, 9 (when possible)
        """
        assert i in (1,3,5,7,9)
        #TODO improve check
        # TODO doesn't work in minor
        return self.notes[i]



for i, name in zip((1,3,5,7),("Root","Third","Fifth","Seventh")): # TEST
    def __generate_func(i):
        def __function(self,note):
            return self.isPosition(note,i)
        return __function
    setattr(AbstractChord,f"is{name}",__generate_func(i))

for i, name in zip((1,3,5,7),("Root","Third","Fifth","Seventh")):
    def __generate_func(i):
        def __function(self,notes):
            for n in notes:
                if self.isPosition(n,i):
                    return True
            return False
        return __function
    setattr(AbstractChord,f"has{name}",__generate_func(i))


class _minor__chord(AbstractChord):

    def __init__(self,degree,scale_,seventh=False):

        keynote = scale_.keynote
        base = scale.Scale(keynote,scale.Mode.m)
        harmonic = scale.Scale(keynote,scale.Mode.m_harmonic)
        rising = scale.Scale(keynote,scale.Mode.m_rising)
        self._minor_chords = {
                "base"      :   AbstractChord(degree,base,seventh),
                "harmonic"  :   AbstractChord(degree,harmonic,seventh),
                "rising"    :   AbstractChord(degree,rising,seventh)
                }

        super().__init__(degree,scale_,seventh)

    def _generate_notes(self):
        self.notes = list(set([*self._minor_chords['base'].notes,
                              *self._minor_chords['harmonic'].notes,
                              *self._minor_chords['rising'].notes]))
        self.notes.sort(key=lambda x : x.value.semitone)

    def _qualify(self):
        """Return the quality of the chord.
        If the chord has two possible states,
        return the two possibilities
        """
        results = [ ]
        for _m_c in self._minor_chords.values():
            results.extend(_m_c.quality)
        return tuple(set(results))

# bools method # TEST
for method in "isPosition isInversion isFullChord".split():
    def __generate__func(method):
        def __method(self,*a,**kw):
            for c in self._minor_chords.values():
                if getattr(c,method)(*a,**kw) is True:
                    return True
            return False
        return __method
    setattr(_minor__chord,method,__generate__func(method))

# ValueError raised methods # TEST
for method in "findPosition findInversion".split():
    def __generate_func(method):
        def __method(self,*a,**kw):
            for c in self._minor_chords.values():
                try:
                    return getattr(c, method)(*a,**kw)
                except ValueError:
                    continue
        return __method
    setattr(_minor__chord,method,__generate_func(method))

# !!!! WARNING !!!!
# DEPRECATED
# for legacy purpose only
Chord = AbstractChord
# !!!! WARNING !!!!


class ActualChord:
    """An ActualChord is a chord which is realised
    in the sheet score.
    Notes are sorted by pitch. The lower is 0.
    """
    def __init__(self,abstract: AbstractChord,notes):
        """notes can be a Note, a Pitch, a NoteScale
        positions.
        If a chord changes its positions, make two different chords"""
        assert notes in abstract

        self.abstract = abstract
        self.notes = sorted(notes,key=lambda x : util.to_pitch(x).value.semitone)
        self.inversion = abstract.findInversion(notes)


    def __getitem__(self,i):
        """Return note at i position
        if it exists
        """
        return self.notes[i]

    def _highest_note(self): # TEST
        """Return highest pitched note"""
        return self.__getitem__(-1)

    def findPosition(self,i): # TEST
        """Find the position of the note i.
        """
        return self.abstract.findPosition(self.notes[i])

    def _is_highest_root(self)->bool: # TEST
        """True if highest note is the root"""
        return self.findPosition(-1) == 1

    highestNote = property(_highest_note)
    isHighestRoot = property(_is_highest_root)

class RealizedChord:
    """Chord realized in the score, but different positions are allowed
    """
    @staticmethod
    def chordify(data):
        """Takes a bunch of staves (data) and finds the chords
        inside. Return a list of RealizedChord"""
        chords = []
        for notes in tools.iter_melodies(*data):
            start = max([n.pos for n in notes])
            end = min([n.last_pos for n in notes])

            sc = data[0].scaleAt(start)
            c = AbstractChord.findBestChord(notes,sc)
            assert not isinstance(c,list)
            if chords and chords[-1].abstract == c:
                chords[-1].end = end
            else:
                chords.append(RealizedChord(c, start, end, data))
        return chords

    def __init__(self, a_chord, start,end,staves):
        self.abstract = a_chord
        self.start = start
        self.end = end
        self.staves = staves

    def __repr__(self):
        return f"RealizedChord<{self.abstract}>{self.start}:{self.end}"

    def __contains__(self,notes):
        """True if the notes
        are in the chord. 
        This function checks the position
        of the notes"""
        # TODO vérifier qu'il ne faille pas mettre supérieur(inférieur) ou égal à...
        # ça semble marcher comme ça...
        try:
            len(notes)
        except TypeError:
            notes = [notes]
        for n in notes:
            if n.last_pos < self.start or n.pos > self.end or n not in self.abstract:
                return False

        return True

    def hasParallelIntervalWith(self,following,interval):
        """
        Return parallel interval with following in every voice,
        with the distance between them.
        """
        all_staves_results = {(s1.title,s2.title) : harmonic.distance_between_intervals(s1,s2,interval)
                for s1,s2 in itertools.combinations(self.staves,2)}

        returned = {}
        for title, intervalspair in all_staves_results.items():
            intervalspair_selected = []
            for itvl in intervalspair:
                pos1 = min(itvl.first,key=lambda x : x.last_pos).last_pos
                pos2 = max(itvl.second,key=lambda x: x.pos).pos
                # are the intervals different?
                if motion.MotionType.motion(*itvl.first,*itvl.second) == motion.MotionType.no:
                    continue
                if pos1 > self.start and pos2 < following.end:
                    # check that the intervals are in two different chords
                    if itvl.first in self.abstract and itvl.second in following.abstract:
                        intervalspair_selected.append(itvl)
            returned[title] = intervalspair_selected

        return returned

    def _get_last_pos(self):
        return self.end
    last_pos = property(_get_last_pos)
    def _get_first_pos(self):
        return self.start
    pos = property(_get_first_pos)



        

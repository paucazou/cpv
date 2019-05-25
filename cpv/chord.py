#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende

import note
import scale
import scalenote
import util

class Chord:
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
        return f"Chord<{self.degree}|{self.scale}>"

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
        chords = [ Chord(i,scale,seventh) for i in range(1,8) ]
        notes = [ util.to_pitch(n) for n in notes ]

        returned = [ c for c in chords if notes in c ]
        if best:
            for c in chords:
                if c.isFullChord(notes):
                    return c

        return returned


    @staticmethod
    def isChord(notes,scale,seventh=False) -> bool: # TEST
        """Is the sequence of notes
        a chord?
        """
        return bool(Chord.findChord(notes,scale,seventh))

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



for i, name in zip((1,3,5,7),("Root","Third","Fifth","Seventh")): # TEST
    def __generate_func(i):
        def __function(self,note):
            return self.isPosition(note,i)
        return __function
    setattr(Chord,f"is{name}",__generate_func(i))


class _minor__chord(Chord):

    def __init__(self,degree,scale_,seventh=False):

        keynote = scale_.keynote
        base = scale.Scale(keynote,scale.Mode.m)
        harmonic = scale.Scale(keynote,scale.Mode.m_harmonic)
        rising = scale.Scale(keynote,scale.Mode.m_rising)
        self._minor_chords = {
                "base"      :   Chord(degree,base,seventh),
                "harmonic"  :   Chord(degree,harmonic,seventh),
                "rising"    :   Chord(degree,rising,seventh)
                }

        super().__init__(degree,scale_,seventh)

    def _generate_notes(self):
        self.notes = list(set([*self._minor_chords['base'].notes,
                              *self._minor_chords['harmonic'].notes,
                              *self._minor_chords['rising'].notes]))
        self.notes.sort(key=lambda x : x.value.semitone)

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




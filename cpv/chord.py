#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende

import note
import scale
import scalenote

class Chord:
    """A chord"""
    def __init__(self, degree, scale, seventh=False):
        """Creates the chord of the degree required"""
        self.degree = degree
        self.scale = scale
        self.isSeventh = seventh
        self.__generate_notes()

    def __contains__(self, note):
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

        except ValueError: # not iterable
            note = self.__extract_note(note)

        return note in self.notes

    def __generate_notes(self):
        """Generates the notes which can figure in the chord"""
        def _generate_degrees():
            d = self.degree -1
            degrees = []
            while d < len(self.scale.notes):
                degrees += [d,d+2,d+4]
                if self.isSeventh:
                    degrees.append(d+6)
                d+=7
            return degrees

        degrees = _generate_degrees()

        self.notes = [n for i, n in enumerate(self.scale.notes) if i in degrees ]



    def isPosition(self, note, i:int):
        """True if note is in position i
        in the chord.
        i can be 1, 3, 5 or 7
        """
        assert i in (1,3,5,7)
        try:
            return i == findPosition(note) 
        except ValueError:
            return False

    def findPosition(self, note) -> int:
        """Find if the note is the root,
        the third, the fifth or the seventh
        raise ValueError if it can't be found"""
        note = self.__extract_note(note)
        try:
            index = self.notes.index(note)
        except ValueError:
            raise ValueError("Note not found in chord")

        j = 3 if self.isSeventh else 2
        while index > j:
            index -= (j+1)

        return {0:1, 1:3, 2:5, 3:7}[index]

    def isInversion(self, chord, i) -> bool:
        """True if chord has the inversion i"""
        try:
            return self.findInversion(chord) == i
        except ValueError:
            return False

    def findInversion(self,chord) -> int:
        """Find the inversion of the chord.
        0 : root position
        1 : first inversion
        2 : second inversion
        3 : third inversion
        Raise ValueError if chord is not a
        self chord
        """
        chord = [self.__extract_note(n) for n in chord]
        chord.sort(key=lambda x : x.value.step)

        # check that every note is in the chord
        for n in chord:
            self.findPosition(n)

        bass = self.findPosition(chord[0])
        return { 1:0, 3:1, 5:2, 7:3}[bass]



    @staticmethod
    def __extract_note(n):
        """Transforms a Note or a NoteScale
        into a simple pitch"""
        if isinstance(n,note.Note):
            return n.pitch
        if isinstance(n,scalenote.NoteScale):
            return n.note.pitch
        return n

    @staticmethod
    def findChord(notes,scale, seventh=False,best=False):
        """Given a sequence of notes,
        find the chord and return it.
        If more than one chord can be found,
        return every chord possible.
        If best is set, return the chord
        which matches more the chord
        """
        chords = [ Chord(i,scale,seventh) for i in range(1,8) ]
        notes = [ Chord.__extract_note(n) for n in notes ]

        returned = [ c for c in chords if notes in c ]
        if best:
            for c in chords:
                if c.isFullChord(notes, scales,seventh):
                    return c

        return returned


    @staticmethod
    def isChord(notes,scale,seventh=False) -> bool:
        """Is the sequence of notes
        a chord?
        """
        return bool(Chord.findChord(notes,scale,seventh))

    def isFullChord(self,notes,scale,seventh=False) -> bool:
        """Given a sequence of notes, True if notes
        contains at least a root, a third, a fifth
        and optionally a seventh.
        """
        pos = [1,3,5]
        if seventh:
            pos.append(7)

        required = {n:False for n in pos}
        notes = [ Chord.__extract_note(n) for n in notes]
        try:
            for n in notes:
                required[self.findPosition(n)] = True
        except ValueError:
            return False

        return not (False in required.values())



for i, name in zip((1,3,5,7),("Root","Third","Fifth","Seventh")):
    def __function(self,note):
        return self.isPosition(note,i)
    setattr(Chord,f"is{name}",__function)


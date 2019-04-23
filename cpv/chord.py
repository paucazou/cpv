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

    def isPosition(self, note, i:int):
        """True if note is in position i
        in the chord.
        i can be 1, 3, 5 or 7
        """
        assert i in (1,3,5,7)
        note = self.__extract_note(note)

    @staticmethod
    def __extract_note(n):
        """Transforms a Note or a NoteScale
        into a simple pitch"""
        if isinstance(n,note.Note):
            return n.pitch
        if isinstance(n,scalenote.NoteScale):
            return n.note.pitch
        return n


for i, name in zip((1,3,5,7),("Root","Third","Fifth","Seventh")):
    def __function(self,note):
        return self.isPosition(note,i)
    setattr(Chord,f"is{name}",__function)


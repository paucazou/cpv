#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende

import functools
import pitch
import scale
import util

@functools.total_ordering
class NoteScale:
    """Defines a note in a scale"""
    def __init__(self, scale, note : pitch.Pitch):
        """Raises a ValueError if note
        is not in scale"""
        self.scale = scale
        self.note = note

    def moveBy(self, i : int): # TEST
        """Move the note by the number of intervals
        i. i can be negative to lower the pitch, or
        positive to find a higher note.
        A ValueError is raised if the new note can not be found
        (i.e., is too high or too low).
        """
        try:
            self.note = self.scale.notes[self.pos+i]
        except IndexError:
            raise ValueError(f"{self._note} not in {self.scale}")

    def distanceWith(self, other) ->int: # TEST
        """Find the distance between self and other
        necessary to moveBy self to other
        and return it as a positive or a negative integer.
        If the notes are the same, the interval is 0
        If other is a higher pitch, the distance is positive,
        negative if other is lower
        """
        assert other.scale == self.scale

        return other._pos - self._pos

    def __eq__(self, other): # TEST
        """True if other has the same note as other.
        Raises a ValueError if scales are different"""
        if self.scale != other.scale:
            raise ValueError("Scales are different")
        return self.note == other.note

    def __lt__(self,other): # TEST
        """True if self is lower than other"""
        assert other.scale == self.scale

        return self._pos < other._pos

    def _set_pos(self, i):
        try:
            self._pos = self.scale.notes.index(self._note)
        except IndexError:
            raise ValueError(f"{self._note} not in {self.scale}")

    def _set_note(self, note):
        self._note = util.to_pitch(note)
        self._set_pos(self.scale.notes.index(self._note))

    def _get_pos(self):
        return self._pos

    def _get_note(self):
        return self._note

    note = property(_get_note,_set_note)
    pos = property(_get_pos)

    @staticmethod
    def moveSequence(i : int, seq): # TEST
        """Apply moveBy to every NoteScale in
        seq """
        for elt in seq:
            elt.moveBy(i)

for i, name in enumerate(("Tonic","Supertonic","Mediant","Subdominant","Dominant","Submediant","Leading")): # TEST
    def __create__function(name):
        def __function(self):
            return getattr(self.scale,f"is{name}")(self.note)
        return __function
    setattr(NoteScale,f"is_{name}",__create__function(name))
    setattr(NoteScale,f"is{name}",property(getattr(NoteScale,f"is_{name}")))



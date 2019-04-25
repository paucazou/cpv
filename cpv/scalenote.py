#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende

import functools
import pitch
import scale

@functools.total_ordering
class NoteScale:
    """Defines a note in a scale"""
    def __init__(self, scale, note : pitch.Pitch):
        """Raises a ValueError if note
        is not in scale"""
        self.scale = scale
        self.note = note

    def moveBy(self, i : int):
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

    def distanceWith(self, other) ->int:
        """Find the distance between self and other
        necessary to moveBy self to other
        and return it as a positive or a negative integer.
        If the notes are the same, the interval is 0
        If other is a higher pitch, the distance is positive,
        negative if other is lower
        """
        return other._pos - self._pos

    def __eq__(self, other):
        """True if other has the same note as other.
        Raises a ValueError if scales are different"""
        if self.scale != other.scale:
            raise ValueError("Scales are different")
        return self.note == other.note

    def __lt__(self,other):
        """True if self is lower than other"""
        return self._pos < other._pos

    def _set_pos(self, i):
        try:
            self._pos = self.scale.notes.index(self._note)
        except IndexError:
            raise ValueError(f"{self._note} not in {self.scale}")

    def _set_note(self, note):
        self._note = note
        self._set_pos(self.scale.index(note))

    def _get_pos(self):
        return self._pos

    def _get_note(self):
        return self._note

    note = property(_get_note,_set_note)
    pos = property(_get_pos)

    @staticmethod
    def moveSequence(i : int, seq):
        """Apply moveBy to every NoteScale in
        seq and return a new sequence"""
        return [elt.moveBy(i) for elt in seq]

for i, name in enumerate(("Tonic","Supertonic","Mediant","Subdominant","Dominant","Submediant","Leading")):
    def __function(self):
        return getattr(self.scale,f"is{name}")(self.note)
    setattr(NoteScale,f"is_{name}",__function)
    setattr(NoteScale,f"is{name}",property(f"is_{name}"))



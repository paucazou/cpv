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
    def __new__(cls, scale_, note : pitch.Pitch):
        if scale_.mode == scale.Mode.m_full:
            return object.__new__(_minor__note_scale)
        return object.__new__(cls)

    def __init__(self, scale, note : pitch.Pitch):
        """Raises a ValueError if note
        is not in scale"""
        self.scale = scale
        self.note = note

    def __repr__(self):
        return f"NoteScale<{self.scale}>({self.note})"

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

    def _set_pos(self):
        self._pos = self.scale.positionOf(self._note)

    def _set_note(self, note):
        self._note = util.to_pitch(note)
        self._set_pos()

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

for i, name in enumerate(("Tonic","Supertonic","Mediant","Subdominant","Dominant","Submediant","Leading","Subtonic","RaisedSubmediant")): # TEST
    def __create__function(name):
        def __function(self):
            return getattr(self.scale,f"is{name}")(self.note)
        return __function
    setattr(NoteScale,f"is_{name}",__create__function(name))
    setattr(NoteScale,f"is{name}",property(getattr(NoteScale,f"is_{name}")))


class _minor__note_scale(NoteScale):
    def moveBy(self, i : int, mode=scale.Mode.m): # TEST
        """Move the not by i. If the new note is the 6th or 7th degree,
        use mode to select the note
        if the current note is in this mode
        If not, find the note following this order:
            - melodic,
            - harmonic,
            - rising
        """
        # select the correct scale
        def __selector(n):
            scale = self.scale
            for s in scale.minor_scales[mode], scale.base, scale.harmonic, scale.rising:
                if self.note in s:
                    return s
            else:
                assert False and "Note not found"
        scale_selected = __selector(self.note)

        # find note
        self.note = scale_selected.notes[self.pos+i]


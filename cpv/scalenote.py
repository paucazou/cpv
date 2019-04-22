#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende

import pitch
import scale

class NoteScale:
    """Defines a note in a scale"""
    def __init__(self, scale, note):
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

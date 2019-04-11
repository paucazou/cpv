#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende

import math
import note

class Stave:
    """Represents the stave
    """
    def __init__(self,rythm=4,breve_value=4,name=''):
        self._stave = []
        self.rythm = rythm
        self.breve_value = breve_value
        self.title = name

    @staticmethod
    def fromString(string: str):
        """Takes a string and return
        a list of stave. For syntax, see Note.fromString.
        Each note must be separated by a \\n
        The first element, separated by /, must represent the rythm
        and the breve value. They must be int.
        example: 4/4

        Add a line comment by starting the line with #:
        # everything after in this line is commented
        something # this is not a comment, but an error

        Add a title by adding * at the start of the line
        The following character is discarded
        * Title
        If a file contains at least two titles
        the function return a list of list of Stave
        """
        values = string.split('\n')
        values = [val for val in values if val and val[0] != '#']
        try:
            rythm, breve_val = values[0].split('/')
            rythm = int(rythm)
            breve_value = int(breve_val)

        except ValueError:
            raise SyntaxError(f"Rythm and breve value can't be set: {values[0]}")

        values = values[1:]
        list_of_staves = [Stave(rythm,breve_value)]
        current = list_of_staves[0]
        for val in values:
            if val[0] == '*':
                if len(current._stave) != 0:
                    list_of_staves.append(Stave(rythm,breve_value))
                    current=list_of_staves[-1]

                current.title = val[2:]
            else:
                current._stave.append(note.Note.fromString(val))

        return list_of_staves

    @staticmethod
    def fromFile(filepath):
        """Takes a file and parse it"""
        with open(filepath) as f:
            return Stave.fromString(f.read())

    def __iter__(self):
        for elt in self._stave:
            yield elt

    def atFirstPos(self,i: float):
        """Return a list of elements at position i
        This position is the start of the note
        """
        return [ elt for elt in self._stave if elt.pos == i ]

    def _lastFirstPos() -> float:
        """Return the last starting position
        of a note in the stave.
        0 means either the first note is the last one,
        or there is no note
        """
        last = 0
        for elt in self._stave:
            if last < elt.pos:
                last = elt.pos
        
        return last

    def barIter(self):
        """Yields each bar after the other"""
        for i in range(self.barNumber):
            yield self.getBar(i)

    def _get_bar_number(self) -> int:
        """Get the number of bar in
        the Stave
        """
        last_elt = max(self._stave,key=lambda x : x.pos + x.duration.value)
        return math.ceil( (last_elt.pos + last_elt.duration.value) / self.rythm)

    def getBar(self,i: int) -> list:
        """Return every element which
        is in bar i
        first one is 0
        raise IndexError if i >= barNumber
        """
        class __bar:
            def __init__(self,elts,pos,s):
                self.elts = elts
                self.pos = pos
                self.stave = s

            def __len__(self):
                return len(self.stave)

            def __getitem__(self,i):
                return self.elts[i]

        if i >= self.barNumber:
            raise IndexError(f"Bar requested does not exist: {i}. Max is {self.barNumber}")
        first_pos = i*self.rythm
        last_pos = first_pos + self.rythm - 1/50
        return __bar([ elt
                for elt in self._stave
                if first_pos <= elt.pos <= last_pos or first_pos <= elt.last_pos <= last_pos
                ],
                i,
                self)

    def extend(self,other):
        """Extend self
        with other, as in list.extend
        """
        self._stave.extend(other._stave)

    barNumber = property(_get_bar_number)
    lastFirstPos = property(_lastFirstPos)

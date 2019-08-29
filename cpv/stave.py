#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende

import math
import note
import pitch
import scale


class Stave:
    """Represents the stave
    """
    class __bar:
        def __init__(self,elts,pos,s):
            self.elts = elts
            self.pos = pos
            self.stave = s

        def __len__(self):
            return len(self.elts)

        def __getitem__(self,i):
            return self.elts[i]
        
        def __repr__(self):
            return f"Bar<{self.stave.title}:{self.pos}> {self.elts}"

    def __init__(self,rythm=4,breve_value=4,name='',keynote=pitch.Pitch.C4, mode=scale.Mode.M, nscale=None):
        """If nscale is set, keynote and mode are discarded"""
        self._stave = []
        self.rythm = rythm
        self.breve_value = breve_value
        self.title = name
        if nscale is None:
            self.keynote = keynote
            self.mode = mode
            self.scale = scale.Scale(keynote,mode)
        else:
            self.scale = nscale
            self.keynote = nscale.keynote
            self.mode = nscale.mode

    def __repr__(self):
        return f"Stave<{self.scale}>({self.title}) {self.rythm}/{self.breve_value} {self.notes}"

    @staticmethod
    def fromString(string: str):
        """Takes a string and return
        a list of stave. For syntax, see Note.fromString.
        Each note must be separated by a \\n
        The first element, separated by /, must represent the rythm
        and the breve value. They must be int.
        example: 4/4
        The second element, a line above,
        is the key tone with following syntax:
        note in upper case, accidental in lower case, followed by M or m
        examples:
            - CM
            - Ebm
            - Dm

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
        # rythm and breve value
        try:
            rythm, breve_val = values[0].split('/')
            rythm = int(rythm)
            breve_value = int(breve_val)

        except ValueError:
            raise SyntaxError(f"Rythm and breve value can't be set: {values[0]}")

        # scale 
        nscale = scale.Scale.fromString(values[1])

        values = values[2:]
        list_of_staves = [Stave(rythm,breve_value,nscale=nscale)]
        current = list_of_staves[0]
        for val in values:
            if val[0] == '*':
                if len(current._stave) != 0:
                    list_of_staves.append(Stave(rythm,breve_value,nscale=nscale))
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

    def __len__(self):
        """Return the number of notes"""
        return len(self._stave)

    def __getitem__(self,i):
        return self.notes[i]

    def __eq__(self,other):
        return self.notes == other.notes

    def atFirstPos(self,i: float):
        """Return a list of elements at position i
        This position is the start of the note
        """
        return [ elt for elt in self._stave if elt.pos == i ]

    def getNoteAtPos(self,i:float):
        """Return a note or a list of notes at pos i."""
        l = [x for x in self.notes if x.isAtPos(i)]
        return l[0] if len(l) == 1 else l


    def _lastFirstPos(self) -> float:
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

    def _last_pos(self):
        """Return the last position of a note
        in the stave"""
        return self.notes[-1].last_pos

    def barIter(self):
        """Yields each bar after the other"""
        for i in range(self.barNumber):
            yield self.getBar(i)

    def _get_bar_number(self) -> int:
        """Get the number of bar in
        the Stave
        """
        last_elt = max(self._stave,key=lambda x : x.pos + x.duration)
        return math.ceil( (last_elt.pos + last_elt.duration) / self.rythm)

    def _get_notes(self):
        self._stave.sort(key = lambda x : x.pos)
        return self._stave

    def _set_notes(self, value):
        """Set the notes of the stave. Value must be an interable"""
        self._stave.sort(key = lambda x : x.pos)
        self._stave = value


    def getBar(self,i: int) -> list:
        """Return every element which
        is in bar i
        first one is 0
        raise IndexError if i >= barNumber
        """

        if i < 0:
            i = self.barNumber + i

        if i >= self.barNumber:
            raise IndexError(f"Bar requested does not exist: {i}. Max is {self.barNumber}")
        first_pos = i*self.rythm
        last_pos = first_pos + self.rythm 
        return self.__bar([ elt
                for elt in self._stave
                if first_pos <= elt.pos < last_pos or first_pos < elt.last_pos < last_pos
                ],
                i,
                self)

    def findBarOf(self, n : note.Note): # TEST
        """Assuming that n is in the stave,
        return the bar where n can be found
        """
        for b in self.barIter():
            if n in b:
                return b
        assert False and f"{n} not in stave"


    def extend(self,other):
        """Extend self
        with other, as in list.extend
        """
        self._stave.extend(other._stave)

    def copy(self):
        """Return a shallow copy of the stave"""
        stave = Stave()
        _stave_copy = self._stave.copy()
        stave.__dict__ = self.__dict__.copy()
        stave._stave = _stave_copy
        return stave

    def isCambiata(self, n: note.Note,upbeat=True):
        """True if n is a cambiata
        Is a cambiata a note that:
            - is upbeat
            - comes from and goes to the same note
            - has a major or minor second distance with this note

        Raise ValueError if n is not in self
        """
        if n not in self:
            raise ValueError(f"{n} not in {self}")
        if upbeat and not self.isUpBeat(n):
            return False

        idx = self.notes.index(n)
        try:
            previous = self.notes[idx-1]
            next = self.notes[idx+1]
        except IndexError:
            return False
        if previous.pitch != next.pitch:
            return False
        return previous.pitch.isInterval(2).With(n.pitch)

    def isPassingTone(self, n: note.Note,upbeat=True):
        """True if n is a passing tone
        Is a passing tone a note that:
            - is upbeat and upbeat is set
            - comes from one note to another note in the same motion
            - is separated by a minor or a major second from and to these notes
        Raise ValueError if n is not in self
        """
        if n not in self:
            raise ValueError(f"{n} not in {self}")
        if upbeat and not self.isUpBeat(n):
            return False
        idx = self.notes.index(n)
        try:
            previous = self.notes[idx-1]
            next = self.notes[idx+1]
        except IndexError:
            return False
        ppitch, npitch = previous.pitch, next.pitch
        cpitch = n.pitch

        if ppitch == npitch:
            return False

        if (cpitch > ppitch and cpitch > npitch) or (cpitch < ppitch and cpitch < npitch):
            return True
        return ppitch.isInterval(2).With(cpitch) and npitch.isInterval(2).With(cpitch)

    def isUpBeat(self, n: note.Note):
        """True if n is upbeat.
        n must be in self.
        """
        assert self.breve_value == 4 and "Other breve value not set"

        if n not in self:
            raise ValueError(f"{n} not in {self}")
        return n.pos % self.rythm != 0

    def isDownBeat(self, n: note.Note):
        """Contrary of isUpBeat"""
        return not self.isUpBeat(n)

    def isConjunct(self,n : note.Note):
        """True if we go to n thanks to a conjunct movement
        False if n is the first note
        """
        assert n in self
        idx = self.notes.index(n)
        return n != self.notes[0] and self.notes[idx-1].pitch.isInterval(2).With(n.pitch)

    def isCambiataOrPassing(self, n : note.Note,upbeat=True):
        """True n is a cambiata or a passing tone"""
        return self.isCambiata(n,upbeat) or self.isPassingTone(n,upbeat)

    def arePassingTones(self, *args,**kw):
        """True if every element of args is a passing tone"""
        for elt in args:
            if self.isPassingTone(elt,**kw) is False:
                return False
        return True





    barNumber = property(_get_bar_number)
    lastFirstPos = property(_lastFirstPos)
    notes = property(fget=_get_notes,fset=_set_notes)
    lastPos = property(_last_pos)

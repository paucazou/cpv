#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende

import enum
import pitch
import util

class Mode(enum.Enum):
    """Represents the mode of a scale"""
    M           = [2,2,1,2,2,2,1]
    m           = [2,1,2,2,1,2,2]
    m_harmonic  = [2,1,2,2,1,3,1]
    m_rising    = [2,1,2,2,2,2,1]
    m_full      = 1

class Scale:
    """Represents a scale"""
    def __init__(self, keynote : pitch.Pitch, mode: Mode):
        if 'ss' in keynote.name or 'bb' in keynote.name:
            raise ValueError("Please do not use double-sharped or double-flat notes as keynotes")
        # we take the lower note possible
        keynote = pitch.Pitch[keynote.name[:-1] + '0']

        self.mode = mode
        self.notes = [keynote]
        self.keynote = keynote
        
        base = keynote.value.semitone
        absolute_degree = keynote.value.step + 1
        relative_degree = 0


        if mode == Mode.m_full:
            base = Scale(keynote,mode.m)
            harmonic = Scale(keynote,mode.m_harmonic)
            rising = Scale(keynote, mode.m_rising)
            self.notes = list(set([*base.notes,*harmonic.notes,*rising.notes]))
            self.notes.sort(key=lambda x: x.value.semitone)
            self.__minor__scales = {'base':base,
                                    'harmonic':harmonic,
                                    'rising':rising}
            return

        for note in list(pitch.Pitch):
            if note.value.semitone == base + mode.value[relative_degree] and note.value.step == absolute_degree:
                self.notes.append(note)
                base += mode.value[relative_degree]
                relative_degree = relative_degree + 1 if relative_degree < len(mode.value)-1 else 0
                absolute_degree += 1

    def __repr__(self):
        return f"Scale<{self.mode.name}>({self.keynote})"

    def __eq__(self, other):
        return self.mode == other.mode and self.notes == other.notes

    def __contains__(self, arg):
        """True if note is in notes available for
        this scale.
        If arg in an iterable, True only if every note
        is in the scale"""
        # is iterable ?
        try:
            for note in arg:
                if util.to_pitch(note) not in self.notes:
                    return False
            return True
        except TypeError:
            # it should be a simple note
            return arg in self.notes

    @staticmethod
    def fromString(s : str): # TEST
        """Takes a string with following
        format: pitch + accidental (if any) + mode
        """
        keynote_s = s[:-1]
        mode_s = s[-1]
        if mode_s not in "Mm":
            raise ValueError(f"""Impossible to parse string "{s}". Unknown mode: {mode_s}""")

        mode = Mode.M if mode_s == "M" else Mode.m_full
        keynote = pitch.Pitch[keynote_s + '0']
        return Scale(keynote,mode)

    def relative(self,minor=Mode.m):
        """Return the relative key. If self
        is major, return minor; if self is major,
        return minor. To specify which minor
        you want, enter it as an optional arg.
        """
        key = pitch.Pitch[ self.keynote.name[:-1] + '4']
        key_pos = self.notes.index(key)

        if self.mode == Mode.M:
            new_key= self.notes[key_pos-2]
            return Scale(new_key,minor)
        elif self.mode in (Mode.m, Mode.m_harmonic, Mode.m_rising, Mode.m_full):
            new_key= self.notes[key_pos+2]
            return Scale(new_key,Mode.M)

    def adjacentScales(self):
        """Return the two adjacent scales of self.
        The first one is the fourth of the tonic,
        the second one the fifth"""
        fourth = self.notes[3]
        fifth = self.notes[4]
        return Scale(fourth,self.mode), Scale(fifth,self.mode)

    def isDegree(self, note, i : int):
        """True if note is the degree i
        i can't be more than 7 and under 1
        """
        assert 0 < i < 8
        if note not in self:
            raise ValueError(f"{note} not in scale { self }")

        if self.mode == Mode.m_full:
            for scale in self.__minor__scales.values():
                try:
                    return scale.isDegree(note,i)
                except ValueError:
                    continue
            assert False

        bnote = pitch.Pitch[ note.name[:-1] + '0']
        if bnote not in self:
            bnote = pitch.Pitch[ note.name[:-1] + '1']

        return i == self.notes.index(bnote)  + 1

    def isRaisedSubmediant(self,note): # TEST
        """Is the note a sixth degree and a raised submediant?
        If the scale has not raised submediant,
        return False
        """
        if self.mode not in (Mode.m_rising,Mode.m_full):
            return False
        if self.mode == Mode.m_rising:
            return self.isDegree(note,6)
        if self.mode == Mode.m_full:
            if note in self.__minor__scales['rising']:
                return self.__minor__scales['rising'].isRaisedSubmediant(note)

    def isSubtonic(self,note): # TEST
        """Is note the seventh degree, with two semitones
        before the tonic?
        False if scale has no subtonic (major for example)
        """
        if self.mode in (Mode.M, Mode.m_harmonic,Mode.m_rising):
            return False
        if self.mode == Mode.m_full:
            if note in self.__minor__scales['base']:
                return self.__minor__scales['base'].isDegree(note,7)
            return False

        # minor natural
        return self.isDegree(note,7)


    def isLeading(self,note): # TEST
        """Is note the seventh degree, with one semitone
        between note and the tonic
        Return False if there is no leading tone in
        the scale (minor for instance)"""

        if self.mode == Mode.m:
            return False
        if self.mode == Mode.m_full:
            if note in self.__minor__scales['harmonic']:
                return self.__minor__scales['harmonic'].isLeading(note)
            return False

        # all other scales
        return self.isDegree(note,7)

for i, name in enumerate(("Tonic", "Supertonic","Mediant","Subdominant","Dominant","Submediant")):
    def create_func(i):
        def __function(self, note):
            return self.isDegree(note, i+1)
        return __function

    setattr(Scale,f'is{name}',create_func(i))


        



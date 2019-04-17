#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende

import enum
import pitch

class Mode(enum.Enum):
    """Represents the mode of a scale"""
    M           = [2,2,1,2,2,2,1]
    m           = [2,1,2,2,1,2,2]
    m_harmonic  = [2,1,2,2,1,3,1]
    m_rising    = [2,1,2,2,2,2,1]
    m_full      = 1

class Scale:
    """Represents a scale"""
    # TODO problem of the minor

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
            return

        for note in list(pitch.Pitch):
            if note.value.semitone == base + mode.value[relative_degree] and note.value.step == absolute_degree:
                self.notes.append(note)
                base += mode.value[relative_degree]
                relative_degree = relative_degree + 1 if relative_degree < len(mode.value)-1 else 0
                absolute_degree += 1

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
                if note not in self.notes:
                    return False
            return True
        except TypeError:
            # it should be a simple note
            return arg in self.notes

    def relative(self,minor=Mode.m):
        """Return the relative key. If self
        is major, return minor; if self is major,
        return minor. To specify which minor
        you want, enter it a an optional arg.
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

        



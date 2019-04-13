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

class Scale:
    """Represents a scale"""

    def __init__(self, keynote : pitch.Pitch, mode: Mode):
        if 'ss' in keynote.name or 'bb' in keynote.name:
            raise ValueError("Please do not use double-sharped or double-flat notes as keynotes")

        self.mode = mode
        self.notes = [keynote]
        
        base = keynote.value.semitone
        absolute_degree = keynote.value.step + 1
        relative_degree = 0


        for note in list(pitch.Pitch):
            if note.value.semitone == base + mode.value[relative_degree] and note.value.step == absolute_degree:
                self.notes.append(note)
                base += mode.value[relative_degree]
                relative_degree = relative_degree + 1 if relative_degree < len(mode.value)-1 else 0
                absolute_degree += 1



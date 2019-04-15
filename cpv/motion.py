#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende
"""
Contains a class to analyze motion types
"""
import enum
import pitch

P = pitch.Pitch

class MotionType(enum.Flag):
    """Enumeration of different
    motion types"""
    direct = 1
    contrary = 2
    oblique = 3

    def match(self, seq) -> bool:
        """True if seq, an iterable of four Pitch,
        has self motion"""
        assert(len(seq) == 4)
        return self.motion(seq) == self
    
    @classmethod
    def motion(cls, *seq):
        """Find the motion of seq.
        seq is a sequence of four Pitch: the first two
        is the first harmonic interval, the second is the 
        second interval.The first, the higher
        """
        assert(len(seq) == 4)
        h1, l1, h2, l2 = seq

        if h1 == h2: # oblique or direct
            return cls.direct if l1 == l2 else cls.oblique
        if l1 == l2: # oblique or direct
            return cls.direct if h1 == h2 else cls.oblique

        if (h1.value.semitone > h2.value.semitone and l1.value.semitone > l2.value.semitone) or (h1.value.semitone < h2.value.semitone and l1.value.semitone < l2.value.semitone):
            return cls.direct

        return cls.contrary

#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende
"""
Contains a class to analyze motion types
"""
import enum
import pitch
import util

P = pitch.Pitch

class MotionType(enum.Flag):
    """Enumeration of different
    motion types"""
    no = 0
    direct = 1
    contrary = 2
    oblique = 3

    def match(self, *seq) -> bool:
        """True if seq, an iterable of four Pitch,
        has self motion"""
        return self.motion(*seq) == self
    
    @classmethod
    def motion(cls, *seq): # TEST
        """Find the motion of seq.
        seq is a sequence of four Pitch: the first two
        is the first harmonic interval, the second is the 
        second interval.The first, the higher.
        It is possible to pass a sequence directly.
        """
        __sort = lambda x,y : (x, y) if x.value.step < y.value.step else (y,x)
        if len(seq) != 4:
            seq = seq[0]
        assert len(seq) == 4

        seq = [util.to_pitch(elt) for elt in seq]
        h1, l1, h2, l2 = seq
        h1,l1 = __sort(h1,l1)
        h2,l2 = __sort(h2,l2)

        if h1 == h2 and l1 == l2: # no movement
            return cls.no
        if h1 == h2 or l1 == l2: # oblique
            return cls.oblique

        if (h1.value.semitone > h2.value.semitone and l1.value.semitone > l2.value.semitone) or (h1.value.semitone < h2.value.semitone and l1.value.semitone < l2.value.semitone):
            return cls.direct

        return cls.contrary

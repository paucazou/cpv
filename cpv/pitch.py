#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende

import enum
import functools
import collections
import math

@functools.total_ordering
class pitch:
    def __init__(self,step,semitone):
        self.step = step
        self.semitone = semitone

    def __repr__(self):
        return f'({self.step}, {self.semitone})'

    def __lt__(self, other):
        return self.semitone < other.semitone


@functools.total_ordering
@enum.unique
class Pitch(enum.Enum):
    """Represents the pitch
    of a note
    Central C is C4"""

    def __lt__(self,other):
        return self.value < other.value

    def intervalWith(self, other, min=False):
        """Return the interval between self
        and other. If min is True, then it will
        return the matching interval under 9"""
        result = abs(self.value.step - other.value.step) + 1
        while result >= 9 and min:
            result -= 7
        return result

    def abstractIntervalWith(self, other):
        """Convenient method equal to
        intervalWith(other,True)
        """
        return self.intervalWith(other,True)

    def qualifiedIntervalWith(self, other):
        """Return a namedtuple containing
        the interval and the quality of this interval.
        The interval itself is not compound.
        """
        __qualified_interval = collections.namedtuple('__qualified_interval',('interval','quality'))

        interval = self.intervalWith(other,True)
        semitones = self.semitoneWith(other,True)
        quality = self.qualifyInterval(interval,semitones)

        return __qualified_interval(interval, quality)

    def semitoneWith(self, other,min=False):
        """Return the number of semitones
        between self and other
        If min is True, then it returns the
        matching semitones in the octave"""
        result = abs(self.value.semitone - other.value.semitone)
        while result >= 13 and min:
            result -= 12
        return result

    def isPerfectlyConsonantWith(self, other) -> bool:
        """True if self and other are separated
        by the following intervals (and multiple):
        1, 5, 8
        and the number of intervals are 0 or 7
        """
        return self.intervalWith(other,True) in (1, 5, 8) and self.semitoneWith(other,True) in (0, 7, 12)

    def isImperfectlyConsonantWith(self,other) -> bool:
        """True if self and other have
        an imperfect consonance
        """
        return self.isQualifiedInterval(
                (3,"minor"),
                (3,"major"),
                (6,"minor"),
                (6,"major")
                ).With(other)

    def isConsonantWith(self,other) -> bool:
        """True if other is consonant with self"""
        return self.isImperfectlyConsonantWith(other) or self.isPerfectlyConsonantWith(other)

    def isMelodicConsonantWith(self,other) -> bool: # TEST
        """True if self and other have a melodic consonance
        """
        return self.isQualifiedInterval(
                (1,"perfect"),
                (4,"perfect"),
                (5,"perfect"),
                (8,"perfect"),
                (2,"minor"),
                (2,"major"),
                (3,"minor"),
                (3,"major"),
                (6,"minor"),
                (6,"major")).With(other)

    def isInterval(self,*args):
        """This method must be used
        with the With() method of the returned
        value. This method takes the other pitch
        as argument and return a boolean
        *args can be any integer, the interval requested.
        If the last arg is a boolean, it is used to set 'min' argument
        of the intervalWith() method"""
        if len(args) == 0:
            raise ValueError("Args must be at least 1")

        if isinstance(args[-1],bool):
            min = args[-1]
            args = args[:-1]
        else:
            min = False

        class __is_interval:
            def __init__(self, p):
                self.p = p
            def With(self, other):
                return self.p.intervalWith(other,min) in args

        return __is_interval(self)

    def isQualifiedInterval(self, *args):
        """Same as isInterval, but the args
        must be a tuple: interval/quality.
        """
        class __is_qual_interval:
            @staticmethod
            def With(other):
                return self.qualifiedIntervalWith(other) in args

        return __is_qual_interval()
    
    def isTritoneWith(self, other) -> bool:
        """True if self has an interval of
        a fourth augmented"""
        return self.isQualifiedInterval((4,"augmented")).With(other)


    def isChromaticInflectionWith(self, other):
        """True if a melodic motion between self and other
        is a chromatic inflection"""
        return self.value.step == other.value.step and self.value.semitone != other.value.semitone

    @staticmethod
    def qualifyInterval(interval : int, semitones : int):
        """Return the quality of interval
        with the help of semitones
        Only major, minor, perfect, diminished and
        augmented are possible.
        Raises a ValueError if it can't find
        a quality.
        """
        perfect, minor, major, diminished, augmented = "perfect minor major diminished augmented".split()
        Perfect = {1:0, 8:12, 5:7, 4:5}
        Minor = {2:1, 3:3, 6:8, 7:10}
        Major = {2:2, 3:4, 6:9, 7:11}

        if interval in Perfect:
            if semitones == Perfect[interval]:
                return perfect
            if semitones > Perfect[interval]:
                return augmented
            elif semitones >= 0:
                return diminished
        if interval in Minor:
            if semitones == Minor[interval]:
                return minor
            if 0 < semitones < Minor[interval] :
                return diminished

        if interval in Major:
            if semitones == Major[interval]:
                return major
            if semitones > Major[interval]:
                return augmented

        raise ValueError(f"Impossible to find the quality: {interval} / {semitones}")

    @classmethod
    def lowerDegree(cls):
        """Return the lower degree.
        Note that it can be an accidental value"""
        return list(cls)[0]

    @classmethod
    def higherDegree(cls):
        """Return the higher degree.
        It can be an accidental value"""
        return list(cls)[-1]

    def findFrequency(self, A4=440):
        """Return the frequency of the pitch,
        relative to the base, which is A4
        """
        semitones = self.value.semitone - Pitch.A4.value.semitone
        return A4 * (2** (semitones/12))

    def _get_accidental(self): # TEST
        """Return the accidental of the pitch
        as a string.
        "" : natural
        "b" : flat
        "bb": double flat
        "s" : sharp
        "ss": double sharp
        """
        return self.name[1:-1]

    frequency = property(findFrequency)
    accidental = property(_get_accidental)


    

                    



    C0 = pitch(0, 0)
    Cs0 = pitch(0, 1)
    Css0 = pitch(0, 2)
    D0 = pitch(1, 2)
    Ds0 = pitch(1, 3)
    Dss0 = pitch(1, 4)
    Db0 = pitch(1, 1)
    Dbb0 = pitch(1, 0)
    E0 = pitch(2, 4)
    Es0 = pitch(2, 5)
    Ess0 = pitch(2, 6)
    Eb0 = pitch(2, 3)
    Ebb0 = pitch(2, 2)
    F0 = pitch(3, 5)
    Fs0 = pitch(3, 6)
    Fss0 = pitch(3, 7)
    Fb0 = pitch(3, 4)
    Fbb0 = pitch(3, 3)
    G0 = pitch(4, 7)
    Gs0 = pitch(4, 8)
    Gss0 = pitch(4, 9)
    Gb0 = pitch(4, 6)
    Gbb0 = pitch(4, 5)
    A0 = pitch(5, 9)
    As0 = pitch(5, 10)
    Ass0 = pitch(5, 11)
    Ab0 = pitch(5, 8)
    Abb0 = pitch(5, 7)
    B0 = pitch(6, 11)
    Bs0 = pitch(6, 12)
    Bss0 = pitch(6, 13)
    Bb0 = pitch(6, 10)
    Bbb0 = pitch(6, 9)
    C1 = pitch(7, 12)
    Cs1 = pitch(7, 13)
    Css1 = pitch(7, 14)
    Cb1 = pitch(7, 11)
    Cbb1 = pitch(7, 10)
    D1 = pitch(8, 14)
    Ds1 = pitch(8, 15)
    Dss1 = pitch(8, 16)
    Db1 = pitch(8, 13)
    Dbb1 = pitch(8, 12)
    E1 = pitch(9, 16)
    Es1 = pitch(9, 17)
    Ess1 = pitch(9, 18)
    Eb1 = pitch(9, 15)
    Ebb1 = pitch(9, 14)
    F1 = pitch(10, 17)
    Fs1 = pitch(10, 18)
    Fss1 = pitch(10, 19)
    Fb1 = pitch(10, 16)
    Fbb1 = pitch(10, 15)
    G1 = pitch(11, 19)
    Gs1 = pitch(11, 20)
    Gss1 = pitch(11, 21)
    Gb1 = pitch(11, 18)
    Gbb1 = pitch(11, 17)
    A1 = pitch(12, 21)
    As1 = pitch(12, 22)
    Ass1 = pitch(12, 23)
    Ab1 = pitch(12, 20)
    Abb1 = pitch(12, 19)
    B1 = pitch(13, 23)
    Bs1 = pitch(13, 24)
    Bss1 = pitch(13, 25)
    Bb1 = pitch(13, 22)
    Bbb1 = pitch(13, 21)
    C2 = pitch(14, 24)
    Cs2 = pitch(14, 25)
    Css2 = pitch(14, 26)
    Cb2 = pitch(14, 23)
    Cbb2 = pitch(14, 22)
    D2 = pitch(15, 26)
    Ds2 = pitch(15, 27)
    Dss2 = pitch(15, 28)
    Db2 = pitch(15, 25)
    Dbb2 = pitch(15, 24)
    E2 = pitch(16, 28)
    Es2 = pitch(16, 29)
    Ess2 = pitch(16, 30)
    Eb2 = pitch(16, 27)
    Ebb2 = pitch(16, 26)
    F2 = pitch(17, 29)
    Fs2 = pitch(17, 30)
    Fss2 = pitch(17, 31)
    Fb2 = pitch(17, 28)
    Fbb2 = pitch(17, 27)
    G2 = pitch(18, 31)
    Gs2 = pitch(18, 32)
    Gss2 = pitch(18, 33)
    Gb2 = pitch(18, 30)
    Gbb2 = pitch(18, 29)
    A2 = pitch(19, 33)
    As2 = pitch(19, 34)
    Ass2 = pitch(19, 35)
    Ab2 = pitch(19, 32)
    Abb2 = pitch(19, 31)
    B2 = pitch(20, 35)
    Bs2 = pitch(20, 36)
    Bss2 = pitch(20, 37)
    Bb2 = pitch(20, 34)
    Bbb2 = pitch(20, 33)
    C3 = pitch(21, 36)
    Cs3 = pitch(21, 37)
    Css3 = pitch(21, 38)
    Cb3 = pitch(21, 35)
    Cbb3 = pitch(21, 34)
    D3 = pitch(22, 38)
    Ds3 = pitch(22, 39)
    Dss3 = pitch(22, 40)
    Db3 = pitch(22, 37)
    Dbb3 = pitch(22, 36)
    E3 = pitch(23, 40)
    Es3 = pitch(23, 41)
    Ess3 = pitch(23, 42)
    Eb3 = pitch(23, 39)
    Ebb3 = pitch(23, 38)
    F3 = pitch(24, 41)
    Fs3 = pitch(24, 42)
    Fss3 = pitch(24, 43)
    Fb3 = pitch(24, 40)
    Fbb3 = pitch(24, 39)
    G3 = pitch(25, 43)
    Gs3 = pitch(25, 44)
    Gss3 = pitch(25, 45)
    Gb3 = pitch(25, 42)
    Gbb3 = pitch(25, 41)
    A3 = pitch(26, 45)
    As3 = pitch(26, 46)
    Ass3 = pitch(26, 47)
    Ab3 = pitch(26, 44)
    Abb3 = pitch(26, 43)
    B3 = pitch(27, 47)
    Bs3 = pitch(27, 48)
    Bss3 = pitch(27, 49)
    Bb3 = pitch(27, 46)
    Bbb3 = pitch(27, 45)
    C4 = pitch(28, 48)
    Cs4 = pitch(28, 49)
    Css4 = pitch(28, 50)
    Cb4 = pitch(28, 47)
    Cbb4 = pitch(28, 46)
    D4 = pitch(29, 50)
    Ds4 = pitch(29, 51)
    Dss4 = pitch(29, 52)
    Db4 = pitch(29, 49)
    Dbb4 = pitch(29, 48)
    E4 = pitch(30, 52)
    Es4 = pitch(30, 53)
    Ess4 = pitch(30, 54)
    Eb4 = pitch(30, 51)
    Ebb4 = pitch(30, 50)
    F4 = pitch(31, 53)
    Fs4 = pitch(31, 54)
    Fss4 = pitch(31, 55)
    Fb4 = pitch(31, 52)
    Fbb4 = pitch(31, 51)
    G4 = pitch(32, 55)
    Gs4 = pitch(32, 56)
    Gss4 = pitch(32, 57)
    Gb4 = pitch(32, 54)
    Gbb4 = pitch(32, 53)
    A4 = pitch(33, 57)
    As4 = pitch(33, 58)
    Ass4 = pitch(33, 59)
    Ab4 = pitch(33, 56)
    Abb4 = pitch(33, 55)
    B4 = pitch(34, 59)
    Bs4 = pitch(34, 60)
    Bss4 = pitch(34, 61)
    Bb4 = pitch(34, 58)
    Bbb4 = pitch(34, 57)
    C5 = pitch(35, 60)
    Cs5 = pitch(35, 61)
    Css5 = pitch(35, 62)
    Cb5 = pitch(35, 59)
    Cbb5 = pitch(35, 58)
    D5 = pitch(36, 62)
    Ds5 = pitch(36, 63)
    Dss5 = pitch(36, 64)
    Db5 = pitch(36, 61)
    Dbb5 = pitch(36, 60)
    E5 = pitch(37, 64)
    Es5 = pitch(37, 65)
    Ess5 = pitch(37, 66)
    Eb5 = pitch(37, 63)
    Ebb5 = pitch(37, 62)
    F5 = pitch(38, 65)
    Fs5 = pitch(38, 66)
    Fss5 = pitch(38, 67)
    Fb5 = pitch(38, 64)
    Fbb5 = pitch(38, 63)
    G5 = pitch(39, 67)
    Gs5 = pitch(39, 68)
    Gss5 = pitch(39, 69)
    Gb5 = pitch(39, 66)
    Gbb5 = pitch(39, 65)
    A5 = pitch(40, 69)
    As5 = pitch(40, 70)
    Ass5 = pitch(40, 71)
    Ab5 = pitch(40, 68)
    Abb5 = pitch(40, 67)
    B5 = pitch(41, 71)
    Bs5 = pitch(41, 72)
    Bss5 = pitch(41, 73)
    Bb5 = pitch(41, 70)
    Bbb5 = pitch(41, 69)
    C6 = pitch(42, 72)
    Cs6 = pitch(42, 73)
    Css6 = pitch(42, 74)
    Cb6 = pitch(42, 71)
    Cbb6 = pitch(42, 70)
    D6 = pitch(43, 74)
    Ds6 = pitch(43, 75)
    Dss6 = pitch(43, 76)
    Db6 = pitch(43, 73)
    Dbb6 = pitch(43, 72)
    E6 = pitch(44, 76)
    Es6 = pitch(44, 77)
    Ess6 = pitch(44, 78)
    Eb6 = pitch(44, 75)
    Ebb6 = pitch(44, 74)
    F6 = pitch(45, 77)
    Fs6 = pitch(45, 78)
    Fss6 = pitch(45, 79)
    Fb6 = pitch(45, 76)
    Fbb6 = pitch(45, 75)
    G6 = pitch(46, 79)
    Gs6 = pitch(46, 80)
    Gss6 = pitch(46, 81)
    Gb6 = pitch(46, 78)
    Gbb6 = pitch(46, 77)
    A6 = pitch(47, 81)
    As6 = pitch(47, 82)
    Ass6 = pitch(47, 83)
    Ab6 = pitch(47, 80)
    Abb6 = pitch(47, 79)
    B6 = pitch(48, 83)
    Bs6 = pitch(48, 84)
    Bss6 = pitch(48, 85)
    Bb6 = pitch(48, 82)
    Bbb6 = pitch(48, 81)
    C7 = pitch(49, 84)
    Cs7 = pitch(49, 85)
    Css7 = pitch(49, 86)
    Cb7 = pitch(49, 83)
    Cbb7 = pitch(49, 82)
    D7 = pitch(50, 86)
    Ds7 = pitch(50, 87)
    Dss7 = pitch(50, 88)
    Db7 = pitch(50, 85)
    Dbb7 = pitch(50, 84)
    E7 = pitch(51, 88)
    Es7 = pitch(51, 89)
    Ess7 = pitch(51, 90)
    Eb7 = pitch(51, 87)
    Ebb7 = pitch(51, 86)
    F7 = pitch(52, 89)
    Fs7 = pitch(52, 90)
    Fss7 = pitch(52, 91)
    Fb7 = pitch(52, 88)
    Fbb7 = pitch(52, 87)
    G7 = pitch(53, 91)
    Gs7 = pitch(53, 92)
    Gss7 = pitch(53, 93)
    Gb7 = pitch(53, 90)
    Gbb7 = pitch(53, 89)
    A7 = pitch(54, 93)
    As7 = pitch(54, 94)
    Ass7 = pitch(54, 95)
    Ab7 = pitch(54, 92)
    Abb7 = pitch(54, 91)
    B7 = pitch(55, 95)
    Bs7 = pitch(55, 96)
    Bss7 = pitch(55, 97)
    Bb7 = pitch(55, 94)
    Bbb7 = pitch(55, 93)





def __generatepitchs():
    """Generate enums."""

    returned = ''

    base = 'CDEFGAB'
    semitone = -1
    for i in range(8):
        for j, note in enumerate(base):

            if note in 'CF':
                semitone += 1
            else:
                semitone += 2

            step = i * 7 + j

            # natural
            returned += f"\n{note}{i} = pitch({step}, {semitone})"

            # sharps
            returned += f"\n{note}s{i} = pitch({step}, {semitone+1})"
            returned += f"\n{note}ss{i} = pitch({step}, {semitone+2})"

            if f"{note}{i}" == "C0":
                continue

            # flats
            returned += f"\n{note}b{i} = pitch({step}, {semitone-1})"
            returned += f"\n{note}bb{i} = pitch({step}, {semitone-2})"
    return returned


#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende

import enum

@enum.unique
class Pitch(enum.Enum):
    """Represents the pitch
    of a note
    Central C is C4"""
    class __pitch:
        def __init__(self,step,semitone):
            self.step = step
            self.semitone = semitone

        def __repr__(self):
            return f'({self.step}, {self.semitone})'

    def intervalWith(self, other, min=False):
        """Return the interval between self
        and other. If min is True, then it will
        return the matching interval under 8"""
        result = abs(self.value.step - other.value.step) + 1
        while result >= 8 and min:
            result -= 7
        return result

    def semitoneWith(self, other,min=False):
        """Return the number of semitones
        between self and other
        If min is True, then it returns the
        matching semitones in the octave"""
        result = abs(self.value.semitone - other.value.semitone)
        while result >= 12 and min:
            result -= 12
        return result

    def isFullyConsonantWith(self, other) -> bool:
        """True if self and other are separated
        by the following intervals (and multiple):
        1, 5, 8
        """
        return self.intervalWith(other,True) in (1, 5, 8)

    C0 = __pitch(0, 0)
    Cs0 = __pitch(0, 1)
    Css0 = __pitch(0, 2)
    D0 = __pitch(1, 2)
    Ds0 = __pitch(1, 3)
    Dss0 = __pitch(1, 4)
    Db0 = __pitch(1, 1)
    Dbb0 = __pitch(1, 0)
    E0 = __pitch(2, 4)
    Es0 = __pitch(2, 5)
    Ess0 = __pitch(2, 6)
    Eb0 = __pitch(2, 3)
    Ebb0 = __pitch(2, 2)
    F0 = __pitch(3, 5)
    Fs0 = __pitch(3, 6)
    Fss0 = __pitch(3, 7)
    Fb0 = __pitch(3, 4)
    Fbb0 = __pitch(3, 3)
    G0 = __pitch(4, 7)
    Gs0 = __pitch(4, 8)
    Gss0 = __pitch(4, 9)
    Gb0 = __pitch(4, 6)
    Gbb0 = __pitch(4, 5)
    A0 = __pitch(5, 9)
    As0 = __pitch(5, 10)
    Ass0 = __pitch(5, 11)
    Ab0 = __pitch(5, 8)
    Abb0 = __pitch(5, 7)
    B0 = __pitch(6, 11)
    Bs0 = __pitch(6, 12)
    Bss0 = __pitch(6, 13)
    Bb0 = __pitch(6, 10)
    Bbb0 = __pitch(6, 9)
    C1 = __pitch(7, 12)
    Cs1 = __pitch(7, 13)
    Css1 = __pitch(7, 14)
    Cb1 = __pitch(7, 11)
    Cbb1 = __pitch(7, 10)
    D1 = __pitch(8, 14)
    Ds1 = __pitch(8, 15)
    Dss1 = __pitch(8, 16)
    Db1 = __pitch(8, 13)
    Dbb1 = __pitch(8, 12)
    E1 = __pitch(9, 16)
    Es1 = __pitch(9, 17)
    Ess1 = __pitch(9, 18)
    Eb1 = __pitch(9, 15)
    Ebb1 = __pitch(9, 14)
    F1 = __pitch(10, 17)
    Fs1 = __pitch(10, 18)
    Fss1 = __pitch(10, 19)
    Fb1 = __pitch(10, 16)
    Fbb1 = __pitch(10, 15)
    G1 = __pitch(11, 19)
    Gs1 = __pitch(11, 20)
    Gss1 = __pitch(11, 21)
    Gb1 = __pitch(11, 18)
    Gbb1 = __pitch(11, 17)
    A1 = __pitch(12, 21)
    As1 = __pitch(12, 22)
    Ass1 = __pitch(12, 23)
    Ab1 = __pitch(12, 20)
    Abb1 = __pitch(12, 19)
    B1 = __pitch(13, 23)
    Bs1 = __pitch(13, 24)
    Bss1 = __pitch(13, 25)
    Bb1 = __pitch(13, 22)
    Bbb1 = __pitch(13, 21)
    C2 = __pitch(14, 24)
    Cs2 = __pitch(14, 25)
    Css2 = __pitch(14, 26)
    Cb2 = __pitch(14, 23)
    Cbb2 = __pitch(14, 22)
    D2 = __pitch(15, 26)
    Ds2 = __pitch(15, 27)
    Dss2 = __pitch(15, 28)
    Db2 = __pitch(15, 25)
    Dbb2 = __pitch(15, 24)
    E2 = __pitch(16, 28)
    Es2 = __pitch(16, 29)
    Ess2 = __pitch(16, 30)
    Eb2 = __pitch(16, 27)
    Ebb2 = __pitch(16, 26)
    F2 = __pitch(17, 29)
    Fs2 = __pitch(17, 30)
    Fss2 = __pitch(17, 31)
    Fb2 = __pitch(17, 28)
    Fbb2 = __pitch(17, 27)
    G2 = __pitch(18, 31)
    Gs2 = __pitch(18, 32)
    Gss2 = __pitch(18, 33)
    Gb2 = __pitch(18, 30)
    Gbb2 = __pitch(18, 29)
    A2 = __pitch(19, 33)
    As2 = __pitch(19, 34)
    Ass2 = __pitch(19, 35)
    Ab2 = __pitch(19, 32)
    Abb2 = __pitch(19, 31)
    B2 = __pitch(20, 35)
    Bs2 = __pitch(20, 36)
    Bss2 = __pitch(20, 37)
    Bb2 = __pitch(20, 34)
    Bbb2 = __pitch(20, 33)
    C3 = __pitch(21, 36)
    Cs3 = __pitch(21, 37)
    Css3 = __pitch(21, 38)
    Cb3 = __pitch(21, 35)
    Cbb3 = __pitch(21, 34)
    D3 = __pitch(22, 38)
    Ds3 = __pitch(22, 39)
    Dss3 = __pitch(22, 40)
    Db3 = __pitch(22, 37)
    Dbb3 = __pitch(22, 36)
    E3 = __pitch(23, 40)
    Es3 = __pitch(23, 41)
    Ess3 = __pitch(23, 42)
    Eb3 = __pitch(23, 39)
    Ebb3 = __pitch(23, 38)
    F3 = __pitch(24, 41)
    Fs3 = __pitch(24, 42)
    Fss3 = __pitch(24, 43)
    Fb3 = __pitch(24, 40)
    Fbb3 = __pitch(24, 39)
    G3 = __pitch(25, 43)
    Gs3 = __pitch(25, 44)
    Gss3 = __pitch(25, 45)
    Gb3 = __pitch(25, 42)
    Gbb3 = __pitch(25, 41)
    A3 = __pitch(26, 45)
    As3 = __pitch(26, 46)
    Ass3 = __pitch(26, 47)
    Ab3 = __pitch(26, 44)
    Abb3 = __pitch(26, 43)
    B3 = __pitch(27, 47)
    Bs3 = __pitch(27, 48)
    Bss3 = __pitch(27, 49)
    Bb3 = __pitch(27, 46)
    Bbb3 = __pitch(27, 45)
    C4 = __pitch(28, 48)
    Cs4 = __pitch(28, 49)
    Css4 = __pitch(28, 50)
    Cb4 = __pitch(28, 47)
    Cbb4 = __pitch(28, 46)
    D4 = __pitch(29, 50)
    Ds4 = __pitch(29, 51)
    Dss4 = __pitch(29, 52)
    Db4 = __pitch(29, 49)
    Dbb4 = __pitch(29, 48)
    E4 = __pitch(30, 52)
    Es4 = __pitch(30, 53)
    Ess4 = __pitch(30, 54)
    Eb4 = __pitch(30, 51)
    Ebb4 = __pitch(30, 50)
    F4 = __pitch(31, 53)
    Fs4 = __pitch(31, 54)
    Fss4 = __pitch(31, 55)
    Fb4 = __pitch(31, 52)
    Fbb4 = __pitch(31, 51)
    G4 = __pitch(32, 55)
    Gs4 = __pitch(32, 56)
    Gss4 = __pitch(32, 57)
    Gb4 = __pitch(32, 54)
    Gbb4 = __pitch(32, 53)
    A4 = __pitch(33, 57)
    As4 = __pitch(33, 58)
    Ass4 = __pitch(33, 59)
    Ab4 = __pitch(33, 56)
    Abb4 = __pitch(33, 55)
    B4 = __pitch(34, 59)
    Bs4 = __pitch(34, 60)
    Bss4 = __pitch(34, 61)
    Bb4 = __pitch(34, 58)
    Bbb4 = __pitch(34, 57)
    C5 = __pitch(35, 60)
    Cs5 = __pitch(35, 61)
    Css5 = __pitch(35, 62)
    Cb5 = __pitch(35, 59)
    Cbb5 = __pitch(35, 58)
    D5 = __pitch(36, 62)
    Ds5 = __pitch(36, 63)
    Dss5 = __pitch(36, 64)
    Db5 = __pitch(36, 61)
    Dbb5 = __pitch(36, 60)
    E5 = __pitch(37, 64)
    Es5 = __pitch(37, 65)
    Ess5 = __pitch(37, 66)
    Eb5 = __pitch(37, 63)
    Ebb5 = __pitch(37, 62)
    F5 = __pitch(38, 65)
    Fs5 = __pitch(38, 66)
    Fss5 = __pitch(38, 67)
    Fb5 = __pitch(38, 64)
    Fbb5 = __pitch(38, 63)
    G5 = __pitch(39, 67)
    Gs5 = __pitch(39, 68)
    Gss5 = __pitch(39, 69)
    Gb5 = __pitch(39, 66)
    Gbb5 = __pitch(39, 65)
    A5 = __pitch(40, 69)
    As5 = __pitch(40, 70)
    Ass5 = __pitch(40, 71)
    Ab5 = __pitch(40, 68)
    Abb5 = __pitch(40, 67)
    B5 = __pitch(41, 71)
    Bs5 = __pitch(41, 72)
    Bss5 = __pitch(41, 73)
    Bb5 = __pitch(41, 70)
    Bbb5 = __pitch(41, 69)
    C6 = __pitch(42, 72)
    Cs6 = __pitch(42, 73)
    Css6 = __pitch(42, 74)
    Cb6 = __pitch(42, 71)
    Cbb6 = __pitch(42, 70)
    D6 = __pitch(43, 74)
    Ds6 = __pitch(43, 75)
    Dss6 = __pitch(43, 76)
    Db6 = __pitch(43, 73)
    Dbb6 = __pitch(43, 72)
    E6 = __pitch(44, 76)
    Es6 = __pitch(44, 77)
    Ess6 = __pitch(44, 78)
    Eb6 = __pitch(44, 75)
    Ebb6 = __pitch(44, 74)
    F6 = __pitch(45, 77)
    Fs6 = __pitch(45, 78)
    Fss6 = __pitch(45, 79)
    Fb6 = __pitch(45, 76)
    Fbb6 = __pitch(45, 75)
    G6 = __pitch(46, 79)
    Gs6 = __pitch(46, 80)
    Gss6 = __pitch(46, 81)
    Gb6 = __pitch(46, 78)
    Gbb6 = __pitch(46, 77)
    A6 = __pitch(47, 81)
    As6 = __pitch(47, 82)
    Ass6 = __pitch(47, 83)
    Ab6 = __pitch(47, 80)
    Abb6 = __pitch(47, 79)
    B6 = __pitch(48, 83)
    Bs6 = __pitch(48, 84)
    Bss6 = __pitch(48, 85)
    Bb6 = __pitch(48, 82)
    Bbb6 = __pitch(48, 81)
    C7 = __pitch(49, 84)
    Cs7 = __pitch(49, 85)
    Css7 = __pitch(49, 86)
    Cb7 = __pitch(49, 83)
    Cbb7 = __pitch(49, 82)
    D7 = __pitch(50, 86)
    Ds7 = __pitch(50, 87)
    Dss7 = __pitch(50, 88)
    Db7 = __pitch(50, 85)
    Dbb7 = __pitch(50, 84)
    E7 = __pitch(51, 88)
    Es7 = __pitch(51, 89)
    Ess7 = __pitch(51, 90)
    Eb7 = __pitch(51, 87)
    Ebb7 = __pitch(51, 86)
    F7 = __pitch(52, 89)
    Fs7 = __pitch(52, 90)
    Fss7 = __pitch(52, 91)
    Fb7 = __pitch(52, 88)
    Fbb7 = __pitch(52, 87)
    G7 = __pitch(53, 91)
    Gs7 = __pitch(53, 92)
    Gss7 = __pitch(53, 93)
    Gb7 = __pitch(53, 90)
    Gbb7 = __pitch(53, 89)
    A7 = __pitch(54, 93)
    As7 = __pitch(54, 94)
    Ass7 = __pitch(54, 95)
    Ab7 = __pitch(54, 92)
    Abb7 = __pitch(54, 91)
    B7 = __pitch(55, 95)
    Bs7 = __pitch(55, 96)
    Bss7 = __pitch(55, 97)
    Bb7 = __pitch(55, 94)
    Bbb7 = __pitch(55, 93)





def __generate__pitchs():
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
            returned += f"\n{note}{i} = __pitch({step}, {semitone})"

            # sharps
            returned += f"\n{note}s{i} = __pitch({step}, {semitone+1})"
            returned += f"\n{note}ss{i} = __pitch({step}, {semitone+2})"

            if f"{note}{i}" == "C0":
                continue

            # flats
            returned += f"\n{note}b{i} = __pitch({step}, {semitone-1})"
            returned += f"\n{note}bb{i} = __pitch({step}, {semitone-2})"
    return returned


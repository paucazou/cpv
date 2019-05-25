import sys
sys.path.append('./cpv')
import chord
import pitch
import scale
P = pitch.Pitch
main_s = scale.Scale(P.C4,scale.Mode.m_full)
tonic_chord = chord._minor__chord(1,main_s,False)
subdominant_chord = chord._minor__chord(4,main_s,False)
dominant_chord = chord._minor__chord(5,main_s,False)

def test_contains():
    assert [P.A3,P.Ab3] in subdominant_chord
    assert [P.B3,P.Bb3] in dominant_chord

def test_isPosition():
    assert subdominant_chord.isPosition(P.C4,5)
    assert subdominant_chord.isPosition(P.A4,3)
    assert subdominant_chord.isPosition(P.Ab4,3)

def test_isInversion():
    assert subdominant_chord.isInversion([P.A3,P.C4,P.F4],1)
    assert subdominant_chord.isInversion([P.Ab3, P.C4, P.F4],1)

def test_isFullChord():
    assert subdominant_chord.isFullChord([P.F4,P.Ab4,P.C4])
    assert subdominant_chord.isFullChord([P.F4,P.A4,P.C4])

def test_findPosition():
    assert subdominant_chord.findPosition(P.Ab4) == 3
    assert subdominant_chord.findPosition(P.A4) == 3

def test_findInversion():
    assert subdominant_chord.findInversion([P.F4,P.Ab4,P.C5]) == 0
    assert subdominant_chord.findInversion([P.F4,P.A4,P.C5]) == 0


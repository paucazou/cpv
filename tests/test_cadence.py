import sys
sys.path.append('./cpv')
import cadence
import chord
import scale
import pitch


AbC = chord.AbstractChord
AcC = chord.ActualChord
P = pitch.Pitch
C = cadence.Cadence

main_scale = scale.Scale(P.C4,scale.Mode.M)
# 1st degree
perfect_high_root_1 = AcC(AbC(1,main_scale),[P.C4, P.E4,P.G4, P.C5])
perfect_high_third_1 = AcC(AbC(1,main_scale),[P.C4, P.G4, P.E5])
perfect_1st_inversion_1 = AcC(AbC(1,main_scale),[P.E3,P.C4, P.G4, P.C3])
# 5th degree
perfect_root_5 = AcC(AbC(5,main_scale),[P.G3, P.D4,P.G4, P.B4])
perfect_1st_inversion_5 = AcC(AbC(5,main_scale),[P.B3,P.D4,P.G4,P.D3])



def _NOtest_get_type():
    assert C.getType(perfect_root_5,perfect_high_root_1) is C.Type.PerfectAuthentic
    assert C.getType(perfect_root_5,perfect_high_third_1) is C.Type.ImperfectAuthenticRoot

    assert C.getType(perfect_root_5,perfect_1st_inversion_1) is C.Type.ImperfectAuthenticInverted 
    assert C.getType(perfect_1st_inversion_5,perfect_high_root_1) is C.Type.ImperfectAuthenticInverted

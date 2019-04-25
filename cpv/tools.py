import scalenote

NS = scalenote.NoteScale

def matchSequence(motif, part, scale) -> bool:
    """True if part matches the motif
    Each arg is an iterable of Note"""
    motif = [ NS(scale,n.pitch) for n in motif]
    part = [ NS(scale,n.pitch) for n in part]

    distance = motif[0].distanceWith(part[0])
    part = NS.moveSequence(distance, part)
    return motif == part


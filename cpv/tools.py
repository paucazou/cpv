import scalenote

NS = scalenote.NoteScale

def matchSequence(motif, part, scale) -> bool:
    """True if part matches the motif
    Each arg is an iterable of Note"""
    motif_ns = [ NS(scale,n.pitch) for n in motif]
    part_ns = [ NS(scale,n.pitch) for n in part]

    distance = motif_ns[0].distanceWith(part_ns[0])
    NS.moveSequence(distance, part_ns)
    from IPython import embed;embed()
    return motif_ns == part_ns


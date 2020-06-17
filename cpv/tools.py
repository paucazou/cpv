import itertools
import note
import queue
import rest
import scalenote
import stave
import util
from collections import namedtuple

NS = scalenote.NoteScale

def matchSequence(motif, part, scale) -> bool:
    """True if part matches the motif
    Each arg is an iterable of Note"""
    # is each note of the same length?
    if [n.duration for n in motif] != [n.duration for n in part]:
        return False
    # is each note at the same relative position?
    m_s_pos = motif[0].pos
    p_s_pos = part[0].pos
    pos_func = lambda it, pos : [n.pos - pos for n in it]
    if pos_func(motif, m_s_pos) != pos_func(part,p_s_pos):
        return False

    # is each note at the same relative pitch?

    motif_ns = [ NS(scale,n.pitch) for n in motif]
    part_ns = [ NS(scale,n.pitch) for n in part]


    distance = part_ns[0].distanceWith(motif_ns[0])
    NS.moveSequence(distance, part_ns)
    return [n.pos for n in motif_ns] == [n.pos for n in part_ns]

def min_max(s): # TEST
    """Return the highest and the lowest
    pitch of s, which must be an iterable
    as a namedtuple of pitchs
    """
    __min_max = namedtuple("MIN_MAX",("min","max"))

    min = max = None
    for n in s:
        p = util.to_pitch(n)
        if min is None:
            min = max = p
            continue
        if p.value.step > max.value.step:
            max = p
        elif p.value.step < min.value.step:
            min = p

    return __min_max(min,max)


def is_same_direction(n1,n2,n3) -> bool: # TEST
    """
    True if the melodic direction is the same
    from n1 to n3
    """
    return n1 < n2 < n3 or n1 > n2 > n3

def get_rythmic_string(s):
    """Turn s to a string
    representing the rythm
    Note the last space"""
    string = ""
    previous_pos = 0
    for n in s:
        if n.pos != previous_pos:
            string += f"R{rest.Rest(n.pos - previous_pos).name} "
        string += f"N{note.Duration(n.duration).name} "
        previous_pos = n.last_pos

    return string


class Queue:
    """A queue for tracks with notes
    of different lengths"""
    def __init__(self,*tracks):
        self.tracks = tracks
        self.pos = min(n.pos for s in tracks for n in s)
        self.last_pos = max(n.last_pos for s in tracks for n in s)

    def __call__(self,with_titles=False):
        """Return chords at each call
        until queue is empty
        if with_titles is True, return a dict with the names of the tracks as key"""
        if with_titles is True:
            returned_notes = {s.title:s.getNoteAtPos(self.pos) for s in self.tracks}
            not_empty_notes = (n for n in returned_notes.values() if n)
            self.pos = min(not_empty_notes,key=lambda n : n.last_pos).last_pos
            return returned_notes

        returned_notes = (s.getNoteAtPos(self.pos) for s in self.tracks)
        returned_notes = [n for n in returned_notes if n]
        self.pos = min(returned_notes,key=lambda n:n.last_pos).last_pos
        return returned_notes

    def _empty(self):
        """True if every queue is empty"""
        return self.pos >= self.last_pos

    empty = property(_empty)

class QueueWithChords(Queue):
    """Similar to Queue, but
    accepts iterables of chords"""
    class __mock_stave:
        def __init__(self,chords):
            self.chords = chords
        def getNoteAtPos(self,pos):
            """Actually get the chord at pos"""
            for c in self.chords:
                if c.pos <= pos < c.last_pos:
                    return c
            else:
                return None

    def __init__(self,*tracks):
        super().__init__(*tracks)
        self.tracks = [
                t if isinstance(t,stave.Stave) else self.__mock_stave(t)
                for t in tracks]




class OldQueue: # DEPRECATED
    """Simple class to manage tracks"""
    def __init__(self,*tracks):
        # creates queues
        self.tracks = [queue.Queue() for t in tracks]
        # fill the queues
        for track, queuee in zip(tracks,self.tracks):
            for elt in track:
                queuee.put(elt)

        # fill the starting block with first notes
        self.starting_block = [q.get() for q in self.tracks]
        
        self.pos = 0
        
    def __call__(self):
        """Return chords at each call
        until queue is empty"""
        print(self.pos)
        first_pos = min(self.starting_block,key=lambda x: x.pos).pos
        first_pos = first_pos if first_pos >= self.pos else self.pos
        last_pos = self._get_last_pos(first_pos)
        print(first_pos)
        print(last_pos)

        returned_notes = []
        for i, elt in enumerate(self.starting_block):
            if elt is None:
                continue
            if elt.pos <= first_pos:
                returned_notes.append(elt)
            if elt.last_pos <= first_pos:
                self.starting_block[i] = None
            elif elt.last_pos == last_pos:
                self.starting_block[i] = None

        # fill again the starting block
        print("starting_block before",self.starting_block)
        self.starting_block = [ q.get() if n is None else n
                for q, n in zip(self.tracks,self.starting_block) 
                if (not q.empty() or n is not None)]
        self.pos = last_pos
        print("starting_block after",self.starting_block)


        return returned_notes

    def _get_last_pos(self,first_pos):
        """Get the last pos of the notes that will be sent
        """
        # get least last pos from elts matching first_pos
        least_last = min([elt.last_pos for elt in self.starting_block if elt.pos == first_pos])
        # getting the second first pos
        least_second_first = min([elt.pos for elt in self.starting_block if elt.pos != first_pos],default=-1)
        print("last_pos")
        print(least_last)
        print(least_second_first)
        # return the good one
        return min(least_last,least_second_first) if least_second_first >= self.pos else least_last
    


    def _empty(self):
        """True if every queue is empty"""
        for t in self.tracks:
            if not t.empty():
                return False
        return len(self.starting_block) == 0 or all(self.starting_block) is None

    empty = property(_empty)

def iter_melodies(*tracks,**options):
    """Generator that takes at least two staves
    and yield the notes grouped by position.
    Although it yields at least one note, it can yield
    a number beyond the length of tracks.
    options can be set with a key:
        - all: if True, yields only when len(notes) == len(tracks)
        - alone: if False, forbids to yield only one note
        - queue: the class of the queue. Default is Queue
        - with_titles: yield the notes with the names of the voices. Default is False
    """
    # TODO does not work well with rests between two notes: maybe works better now.
    assert len(tracks) > 1

    queue_class = options.get("queue",Queue)
    queuer = queue_class(*tracks)
    while not queuer.empty:
        res = queuer(with_titles=options.get("with_titles",False))
        if options.get("all",False) is True and len(res) != len(tracks):
            continue
        if options.get("alone",True) is False and len(res) == 1:
            continue

        yield res
        
def pairwise_melodies(*tracks,**options):
    """Equals to:
    util.pairwise(iter_melodies(*tracks,**options)
    """
    for data in util.pairwise(iter_melodies(*tracks,**options)):
        yield data

def iter_notes_and_chords(*data,**options):
    """Same as iter_melodies, but accepts chords
    """
    if "queue" not in options:
        options["queue"] = QueueWithChords
    for elt in iter_melodies(*data,**options):
        yield elt

def pairwise_notes_and_chords(*data,**options):
    """Equals to:
    util.pairwise(iter_notes_and_chords(*data,**options)
    """
    for data in util.pairwise(iter_notes_and_chords(*data,**options)):
        yield data

def get_matching_cf(s,data):
    """For a stave s, with a title
    like 'cp1', return the matching
    cantus firmus"""
    return next((x for x in data if x.title == f'{s.title[0]}cf'),
            next((y for y in data if y.title == "cantus firmus")))
            


def get_interval_string(s1, s2):
    """Turn these two staves into a string
    representing the intervals found.
    Syntax:
        - intervals are represented by numbers under 9.
        - perfect, augmented, diminished = p, a, d
        - minor, major = m, M
        The quality is just after the number and is followed by a space.
        """
    s = ""
    for n1, n2 in iter_melodies(s1,s2,alone=False):
        inter = n1.pitch.qualifiedIntervalWith(n2.pitch)
        qual = inter.quality[0] if inter.quality != "major" else "M"
        s += f"{inter.interval}{qual} "

    return s

class SequenceTracker:
    """Given a bunch of tracks, finds all the sequences notified
    by the user."""
    __motif_pos = namedtuple("__motif_pos",("start","end"))
    __restatements_pos = namedtuple("__restatements_pos",("start","end"))

    def __init__(self,data):
        self.data = data
        # collecting motifs
        _motifs = {pos:com for s in data for pos,com in s.comments.items() if com in "seqend seqstart".split() }
        if len(_motifs) % 2 != 0:
            raise ValueError("Please check your score: there is not the same number of tags seqstart and seqend")
        _fun = lambda name : sorted([pos for pos,com in _motifs.items() if com == name])
        _start = _fun("seqstart")
        _end = _fun("seqend")
        self.motifs = [self.__motif_pos(start,end) for start,end in zip(_start,_end)]

        # finding restatements
        self.sequences = {motif:0 for motif in self.motifs}
        self.restatements = []
        for motif in self.motifs:
            length = motif.end - motif.start
            last_pos = motif.end
            while self.match(motif,last_pos,last_pos + length) is True:
                self.sequences[motif] += 1
                last_pos = last_pos + length
            self.restatements.append(self.__restatements_pos(motif.end,last_pos))


    def __len__(self):
        return len(self.sequences)

    def isInRestatement(self,note) -> bool:
        """True if note is only in a restatement,
        not in a motif or outside a sequence
        """
        for restatement in self.restatements:
            if note.pos >= restatement.start and note.last_pos <= restatement.end:
                return True

        return False

    def match(self, motif, start, end) -> bool:
        """True if part between start and end
        matches motif"""
        # TODO may be problematic with some kind of modulations, especially with enharmonic notes
        # not really tolerant: syncopation at the start/end is forbidden, for example. Try to be more tolerant.
        motif_notes = [
                [n for n in s if n.pos < motif.end and n.last_pos > motif.start]
                for s in self.data]
        part_notes = [
                [ n for n in s if n.appearsBetween(start,end)]
                for s in self.data]
        # length
        func = lambda x : [n.duration for s in x for n in s]
        if func(motif_notes) != func(part_notes):
            return False
        # relative position
        for motif, part in zip(motif_notes,part_notes):
            m_s_pos = motif[0].pos
            p_s_pos = part[0].pos
            func = lambda it, pos : [n.pos - pos for n in it]
            if func(motif,m_s_pos) != func(part,p_s_pos):
                return False

        # relative pitch
        func = lambda x : [ NS(self.data[0].scaleAt(n.pos),n.pitch) for n in x]

        for motif, part in zip(motif_notes,part_notes):
            # diatonic sequence?
            motif_ns = func(motif)
            part_ns = func(part)
            try:
                distance = part_ns[0].distanceWith(motif_ns[0])
                NS.moveSequence(distance,part_ns)
                if [n.pos for n in motif_ns] != [n.pos for n in part_ns]:
                    return False
            except AssertionError:
                # modulating sequence?
                motif_intervals = self.intervals(motif_notes)
                part_intervals = self.intervals(part_notes)
                if motif_intervals != part_intervals:
                    return False


        return True

    def intervals(self,*data):
        """Return a string of intervals
        in data, which must be of an iterable
        of more than one iterables of notes
        """
        string = ""
        for s1, s2 in itertools.combinations(data,2):
            string += get_interval_string(s1,s2)
        return string

def cut_stave(s : stave.Stave, start=0,end=None, by_measure=False):
    """Cut s from start to end. If start is not filled,
    cut from the start of the stave; if end is not filled,
    cut until the end.
    If by_measure is set, start and end points to the measure to start and end
    (end is NOT included).
    """
    # measure
    if by_measure: # TODO WARNING works only if no change of rythm
        start *= s.rythm
        end *= s.rythm
    # notes
    notes = []
    for n in s:
        # note is inside the range
        if n.pos >= start and n.last_pos <= end:
            notes.append(n)
        # note starts before the start and ends in the range
        elif start < n.last_pos <= end:
            n.duration = n.duration - (start - n.pos)
            n.pos = start
            notes.append(n)
        # note starts in the range but ends after
        elif start <= n.pos < end:
            n.duration = n.duration - (end - n.last_pos)
            notes.append(n)
        # note starts before the start and ends after the end
        elif n.pos < start and n.last_pos > end:
            n.pos = start
            n.duration = end - start
            notes.append(n)

    # comments
    comments = { k:v for k, v in s.comments.items() if start <= k < end}

    # modulations
    modulations = []
    first = None
    for m in s.modulations:
        if m.pos <= start:
            first = m
        elif start < m.pos < end:
            modulations.append(m)

    if first is None:
        first = stave.Modulation(s.keynote,s.scale,0)
    first = stave.Modulation(first.key,first.scale,start)
    modulations.insert(0,first)

    returned = stave.Stave(s.rythm,s.breve_value,s.title,modulations=modulations,comments=comments)
    returned.notes = notes
    return returned












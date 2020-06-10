#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende

import xml.etree.ElementTree as ET
import itertools
import pitch
import scale


class Importer:
    durations = {'whole':4,
                'half'  :2,
                'quarter':1,
                'eighth':'0.5',
                }

    def __init__(self,**kw):
        self.file = kw['file']
        self.result = ""
        self.ties = {}

    def run(self):
        with open(self.file,'r') as f:
            self.content = f.read()

        self.tree = ET.parse(self.file)
        self.root = self.tree.getroot()

        self.staffs = self.root.find('Score').findall('Staff')

        self.get_rhythm()
        self.get_keynote()
        self.manage_bars()

        return self.result

    def append(self,chars):
        self.result += chars + "\n"

    def get_rhythm(self):
        timesig = self.root.find('Score').find('Staff').find('Measure').find('TimeSig')
        self.numerator = timesig.find('sigN').text
        self.denominator = timesig.find('sigD').text
        self.append(f"{self.numerator}/{self.denominator}")

    def get_keynote(self):
        for s in self.root.iter("Text"):
            style = s.find('style')
            if style is not None and style.text == "Subtitle":
                str_keynote = s.find('text').text
                break
        self.append(str_keynote)
        self.main_scale = scale.Scale.fromString(str_keynote)
        self.current_scale = self.main_scale

    def manage_rest(self, r):
        # TODO half, maybe, is the half of the measure, and not 2
        # TODO is dot?
        values = {
                "quarter":1,
                "half":2,
                "measure":int(self.numerator),
                }
        duration = r.find("durationType").text
        duration = self.manage_dots(r,duration)
        self.current_pos += values[duration]

    def manage_mark(self, mark): # DEPRECATED
        pass

    def manage_stafftext(self,mark):
        txt = mark.find("text").text
        if txt[:3] == "mod":
            self.current_scale = scale.Scale.fromString(txt[3:])
        for line in txt.split("\n"):
            self.append(f"# {line}")

    def manage_dots(self,elt,duration):
        if elt.find("dots") is not None:
            val_dot = int(elt.find("dots").text)
            duration = duration + duration / (val_dot *2)
        return duration


    def manage_chord(self,c,measure):
        #duration
        duration_ = c.find("durationType").text
        sduration_ = self.durations[duration_]
        duration_ = float(sduration_)
        duration_ = self.manage_dots(c,duration_)
        sduration_ = str(duration_)
        #TODO bug change sduration
        # pitch
        pitch_ = c.find("Note").find("pitch").text
        pitch_ = int(pitch_)
        pitch_ = pitch_ - 12

        accidental = c.find("Note").find("Accidental")


        tie = c.find('Note').find('Tie')
        if tie is not None:
            self.ties[tie.get('id')] = sduration_
            sduration_ = "TIE_" + tie.get('id')

        end_spanner = c.find('Note').find('endSpanner')
        if end_spanner is not None:
            old_duration_ = self.ties.pop(end_spanner.get('id'))
            sduration_ = float(old_duration_) + float(sduration_)
            self.result = self.result.replace('TIE_' + end_spanner.get('id'),str(sduration_))
            self.current_pos += duration_
            return


        if accidental is None:
            for n in itertools.chain(self.accidentals, self.main_scale.notes):
                if n.value.semitone == pitch_:
                    self.append(f"{n.name} {sduration_} {self.current_pos}")
                    break
            else:
                from IPython import embed;embed()
                raise ValueError(f"The scale mentioned doesn't seem to match the scale used. Problem at pos {self.current_pos} in {self.current_name}. Did you really choose {self.current_scale}?");
        else:
            # foreign note
            accidentals = {"":"natural","b":"flat","s":"sharp","ss":"double sharp","bb":"double flat"}
            accidentals_ = {v:k for k,v in accidentals.items()}
            acc = accidentals_[accidental.find("subtype").text]
            for p in pitch.Pitch:
                if pitch_ == p.value.semitone and p.accidental == acc:
                    self.append(f"{p.name} {sduration_} {self.current_pos}")
                    self.accidentals.append(p)
                    break
            else:
                raise ValueError("Pitch not found")

        self.current_pos += duration_


    def manage_bars(self):
        breaks = []
        parts = self.root.find("Score").findall("Part")
        if parts:
            part_names = [elt.find("trackName").text for elt in parts]
        else:
            part_names = [None] * len(self.staffs)

        for name, staff in zip(part_names, self.staffs):
            self.current_scale = self.main_scale
            next_one=True
            for i, measure in enumerate(staff):
                if measure.tag != "Measure":
                    continue
                if next_one:
                    # title
                    if not name:
                        # DEPRECATED
                        if measure.find('StaffText') is None:
                            raise SyntaxError("A title lacks")
                        name = measure.find('StaffText').find('text').text
                    

                    self.append(f"* {name}")
                    self.current_name = name
                    next_one = False
                    # pos
                    self.current_pos = 0

                if measure.find("LayoutBreak") or i in breaks:
                    next_one = True
                    if i not in breaks:
                        breaks.append(i-1)

                # reinit of the accidentals in this measure
                self.accidentals = []

                for child in measure:
                    if child.tag == 'Rest':
                        self.manage_rest(child)

                    if child.tag == "RehearsalMark":
                        self.manage_mark(child)

                    if child.tag == "StaffText":
                        self.manage_stafftext(child)

                    if child.tag == "Chord":
                        self.manage_chord(child,measure)



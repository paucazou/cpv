#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende

import xml.etree.ElementTree as ET
import pitch
import scale


class Importer:
    durations = {'whole':4,
                'half'  :2,
                }

    def __init__(self,**kw):
        self.file = kw['file']
        self.result = ""

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
        self.rhythm = 4 ##### TEMPORARY ######
        self.append("4/4")

    def get_keynote(self):
        for s in self.root.iter("Text"):
            style = s.find('style')
            if style is not None and style.text == "Subtitle":
                str_keynote = s.find('text').text
                break
        self.append(str_keynote)
        self.main_scale = scale.Scale.fromString(str_keynote)

    def manage_rest(self, r):
        self.current_pos += self.rhythm

    def manage_chord(self,c,measure):
        #duration
        duration_ = c.find("durationType").text
        duration_ = self.durations[duration_]
        duration_ = int(duration_)
        # pitch
        pitch_ = c.find("Note").find("pitch").text
        pitch_ = int(pitch_)
        pitch_ = pitch_ - 12

        accidental = c.find("Note").find("Accidental")


        if accidental is None:
            for n in self.main_scale.notes:
                if n.value.semitone == pitch_:
                    self.append(f"{n.name} {duration_} {self.current_pos}")
                    break
            else:
                raise ValueError(f"The scale mentioned doesn't seem to match the scale used. Did you really choose {main_scale}?");
        else:
            # foreign note
            accidentals = {"":"natural","b":"flat","s":"sharp","ss":"double sharp","bb":"double flat"}
            accidentals_ = {v:k for k,v in accidentals.items()}
            acc = accidentals_[accidental.find("subtype").text]
            for p in pitch.Pitch:
                if pitch_ == p.value.semitone and p.accidental == acc:
                    self.append(f"{p.name} {duration_} {self.current_pos}")
                    break
            else:
                raise ValueError("Pitch not found")

        self.current_pos += duration_

    def manage_bars(self):
        breaks = []
        for staff in self.staffs:
            next_one=True
            for i, measure in enumerate(staff):
                if measure.tag != "Measure":
                    continue
                if next_one:
                    # title
                    if measure.find('StaffText') is None:
                        raise SyntaxError("A title lacks")

                    self.append("* " + measure.find('StaffText').find('text').text)
                    next_one = False
                    # pos
                    self.current_pos = 0

                if measure.find("LayoutBreak") or i in breaks:
                    next_one = True
                    if i not in breaks:
                        breaks.append(i-1)

                if measure.find("Rest"):
                    for r in measure.findall('Rest'):
                        self.manage_rest(r)

                if measure.find("Chord"):
                    for c in measure.findall('Chord'):
                        self.manage_chord(c,measure)



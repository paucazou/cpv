#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende

import xml.etree.ElementTree as ET
import pitch
import scale

def import_msx(file : str) -> str:
    """Import file and 
    return a string matching with readable file
    used by cpv
    """
    with open(file,'r') as f:
        content = f.read()

    class __Result:
        result = ""

    def append(elt):
        __Result.result += elt + '\n'

    tree = ET.parse(file)
    root = tree.getroot()

    staffs = root.find('Score').findall('Staff')

    # get rhythm
    # TODO
    rhythm = 4 ##### TEMPORARY ######
    # get keynote
    for s in root.iter("Text"):
        style = s.find('style')
        if style is not None and style.text == "Subtitle":
            str_keynote = s.find('text').text
            break
    append(str_keynote)
    main_scale = scale.Scale.fromString(str_keynote)
    # creating melodies
    breaks = []
    for staff in staffs:
        next_one=True
        for i, measure in enumerate(staff):
            if measure.tag != "Measure":
                continue
            if next_one:
                # title
                if measure.find('StaffText') is None:
                    raise SyntaxError("A title lacks")

                append("* " + measure.find('StaffText').find('text').text)
                next_one = False
                # pos
                current_pos = 0

            if measure.find("LayoutBreak") or i in breaks:
                next_one = True
                if i not in breaks:
                    breaks.append(i-1)

            if measure.find("Rest"):
                current_pos += rhythm

            if measure.find("Chord"):
                pitch_ = measure.find("Chord").find("Note").find("pitch").text
                pitch_ = int(pitch_)
                pitch_ = pitch_ - 12

                accidental = measure.find("Chord").find("Note").find("Accidental")


                if accidental is None:
                    for n in main_scale.notes:
                        if n.value.semitone == pitch_:
                            append(f"{n.name} {rhythm} {current_pos}")
                            break
                else:
                    # foreign note
                    accidentals = {"":"natural","b":"flat","s":"sharp","ss":"double sharp","bb":"double flat"}
                    accidentals_ = {v:k for k,v in accidentals.items()}
                    acc = accidentals_[accidental.find("subtype").text]
                    for p in pitch.Pitch:
                        if pitch_ == p.value.semitone and p.accidental == acc:
                            append(f"{p.name} {rhythm} {current_pos}")
                            break
                    else:
                        raise ValueError("Pitch not found")

                current_pos += rhythm


    return __Result.result
                



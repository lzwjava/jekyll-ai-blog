from music21 import *
import copy
import random


def __is_scale_tone(chord, note):
    scaleType = scale.DorianScale()
    if chord.quality == "major":
        scaleType = scale.MajorScale()

    scales = scaleType.derive(chord)
    allPitches = list(set([pitch for pitch in scales.getPitches()]))
    allNoteNames = [i.name for i in allPitches]

    noteName = note.name
    return noteName in allNoteNames


def __is_approach_tone(chord, note):
    for chordPitch in chord.pitches:
        stepUp = chordPitch.transpose(1)
        stepDown = chordPitch.transpose(-1)
        if (
            note.name == stepDown.name
            or note.name == stepDown.getEnharmonic().name
            or note.name == stepUp.name
            or note.name == stepUp.getEnharmonic().name
        ):
            return True
    return False


def __is_chord_tone(lastChord, note):
    return note.name in (p.name for p in lastChord.pitches)


def __generate_chord_tone(lastChord):
    lastChordNoteNames = [p.nameWithOctave for p in lastChord.pitches]
    return note.Note(random.choice(lastChordNoteNames))


def __generate_scale_tone(lastChord):
    scaleType = scale.WeightedHexatonicBlues()
    if lastChord.quality == "major":
        scaleType = scale.MajorScale()

    scales = scaleType.derive(lastChord)
    allPitches = list(set([pitch for pitch in scales.getPitches()]))
    allNoteNames = [i.name for i in allPitches]

    sNoteName = random.choice(allNoteNames)
    lastChordSort = lastChord.sortAscending()
    sNoteOctave = random.choice([i.octave for i in lastChordSort.pitches])
    sNote = note.Note(("%s%s" % (sNoteName, sNoteOctave)))
    return sNote


def __generate_approach_tone(lastChord):
    sNote = __generate_scale_tone(lastChord)
    aNote = sNote.transpose(random.choice([1, -1]))
    return aNote


def __generate_arbitrary_tone(lastChord):
    return __generate_scale_tone(lastChord)


def parse_melody(fullMeasureNotes, fullMeasureChords):
    measure = copy.deepcopy(fullMeasureNotes)
    chords = copy.deepcopy(fullMeasureChords)
    measure.removeByNotOfClass([note.Note, note.Rest])
    chords.removeByNotOfClass([chord.Chord])

    measureStartTime = measure[0].offset - (measure[0].offset % 4)
    measureStartOffset = measure[0].offset - measureStartTime

    fullGrammar = ""
    prevNote = None
    numNonRests = 0
    for ix, nr in enumerate(measure):
        try:
            lastChord = [n for n in chords if n.offset <= nr.offset][-1]
        except IndexError:
            chords[0].offset = measureStartTime
            lastChord = [n for n in chords if n.offset <= nr.offset][-1]

        elementType = " "

        if isinstance(nr, note.Rest):
            elementType = "R"

        elif nr.name in lastChord.pitchNames or isinstance(nr, chord.Chord):
            elementType = "C"

        elif __is_scale_tone(lastChord, nr):
            elementType = "S"

        elif __is_approach_tone(lastChord, nr):
            elementType = "A"

        else:
            elementType = "X"

        if ix == (len(measure) - 1):
            diff = measureStartTime + 4.0 - nr.offset
        else:
            diff = measure[ix + 1].offset - nr.offset

        noteInfo = "%s,%.3f" % (elementType, nr.quarterLength)

        intervalInfo = ""
        if isinstance(nr, note.Note):
            numNonRests += 1
            if numNonRests == 1:
                prevNote = nr
            else:
                noteDist = interval.Interval(noteStart=prevNote, noteEnd=nr)
                noteDistUpper = interval.add([noteDist, "m3"])
                noteDistLower = interval.subtract([noteDist, "m3"])
                intervalInfo = ",<%s,%s>" % (
                    noteDistUpper.directedName,
                    noteDistLower.directedName,
                )

                prevNote = nr

        grammarTerm = noteInfo + intervalInfo
        fullGrammar += grammarTerm + " "

    return fullGrammar.rstrip()


def unparse_grammar(m1_grammar, m1_chords):
    m1_elements = stream.Voice()
    currOffset = 0.0
    prevElement = None
    for ix, grammarElement in enumerate(m1_grammar.split(" ")):
        terms = grammarElement.split(",")
        currOffset += float(terms[1])

        if terms[0] == "R":
            rNote = note.Rest(quarterLength=float(terms[1]))
            m1_elements.insert(currOffset, rNote)
            continue

        try:
            lastChord = [n for n in m1_chords if n.offset <= currOffset][-1]
        except IndexError:
            m1_chords[0].offset = 0.0
            lastChord = [n for n in m1_chords if n.offset <= currOffset][-1]

        if len(terms) == 2:
            insertNote = note.Note()

            if terms[0] == "C":
                insertNote = __generate_chord_tone(lastChord)

            elif terms[0] == "S":
                insertNote = __generate_scale_tone(lastChord)

            else:
                insertNote = __generate_approach_tone(lastChord)

            insertNote.quarterLength = float(terms[1])
            if insertNote.octave < 4:
                insertNote.octave = 4
            m1_elements.insert(currOffset, insertNote)
            prevElement = insertNote

        else:
            interval1 = interval.Interval(terms[2].replace("<", ""))
            interval2 = interval.Interval(terms[3].replace(">", ""))
            if interval1.cents > interval2.cents:
                upperInterval, lowerInterval = interval1, interval2
            else:
                upperInterval, lowerInterval = interval2, interval1
            lowPitch = interval.transposePitch(prevElement.pitch, lowerInterval)
            highPitch = interval.transposePitch(prevElement.pitch, upperInterval)
            numNotes = int(highPitch.ps - lowPitch.ps + 1)

            if terms[0] == "C":
                relevantChordTones = []
                for i in range(0, numNotes):
                    currNote = note.Note(lowPitch.transpose(i).simplifyEnharmonic())
                    if __is_chord_tone(lastChord, currNote):
                        relevantChordTones.append(currNote)
                if len(relevantChordTones) > 1:
                    insertNote = random.choice(
                        [
                            i
                            for i in relevantChordTones
                            if i.nameWithOctave != prevElement.nameWithOctave
                        ]
                    )
                elif len(relevantChordTones) == 1:
                    insertNote = relevantChordTones[0]
                else:
                    insertNote = prevElement.transpose(random.choice([-2, 2]))
                if insertNote.octave < 3:
                    insertNote.octave = 3
                insertNote.quarterLength = float(terms[1])
                m1_elements.insert(currOffset, insertNote)

            elif terms[0] == "S":
                relevantScaleTones = []
                for i in range(0, numNotes):
                    currNote = note.Note(lowPitch.transpose(i).simplifyEnharmonic())
                    if __is_scale_tone(lastChord, currNote):
                        relevantScaleTones.append(currNote)
                if len(relevantScaleTones) > 1:
                    insertNote = random.choice(
                        [
                            i
                            for i in relevantScaleTones
                            if i.nameWithOctave != prevElement.nameWithOctave
                        ]
                    )
                elif len(relevantScaleTones) == 1:
                    insertNote = relevantScaleTones[0]
                else:
                    insertNote = prevElement.transpose(random.choice([-2, 2]))
                if insertNote.octave < 3:
                    insertNote.octave = 3
                insertNote.quarterLength = float(terms[1])
                m1_elements.insert(currOffset, insertNote)

            else:
                relevantApproachTones = []
                for i in range(0, numNotes):
                    currNote = note.Note(lowPitch.transpose(i).simplifyEnharmonic())
                    if __is_approach_tone(lastChord, currNote):
                        relevantApproachTones.append(currNote)
                if len(relevantApproachTones) > 1:
                    insertNote = random.choice(
                        [
                            i
                            for i in relevantApproachTones
                            if i.nameWithOctave != prevElement.nameWithOctave
                        ]
                    )
                elif len(relevantApproachTones) == 1:
                    insertNote = relevantApproachTones[0]
                else:
                    insertNote = prevElement.transpose(random.choice([-2, 2]))
                if insertNote.octave < 3:
                    insertNote.octave = 3
                insertNote.quarterLength = float(terms[1])
                m1_elements.insert(currOffset, insertNote)

            prevElement = insertNote

    return m1_elements

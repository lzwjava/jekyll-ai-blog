from __future__ import print_function

from music21 import *
from collections import OrderedDict
from itertools import groupby

from grammar import *

from grammar import parse_melody
from music_utils import *


def __parse_midi(data_fn):
    midi_data = converter.parse(data_fn)

    melody_stream = midi_data[5]
    melody1, melody2 = melody_stream.getElementsByClass(stream.Voice)
    for j in melody2:
        melody1.insert(j.offset, j)
    melody_voice = melody1

    for i in melody_voice:
        if i.quarterLength == 0.0:
            i.quarterLength = 0.25

    melody_voice.insert(0, instrument.ElectricGuitar())
    melody_voice.insert(0, key.KeySignature(sharps=1))

    partIndices = [0, 1, 6, 7]
    comp_stream = stream.Voice()
    comp_stream.append([j.flat for i, j in enumerate(midi_data) if i in partIndices])

    full_stream = stream.Voice()
    for i in range(len(comp_stream)):
        full_stream.append(comp_stream[i])
    full_stream.append(melody_voice)

    solo_stream = stream.Voice()
    for part in full_stream:
        curr_part = stream.Part()
        curr_part.append(part.getElementsByClass(instrument.Instrument))
        curr_part.append(part.getElementsByClass(tempo.MetronomeMark))
        curr_part.append(part.getElementsByClass(key.KeySignature))
        curr_part.append(part.getElementsByClass(meter.TimeSignature))
        curr_part.append(part.getElementsByOffset(476, 548, includeEndBoundary=True))
        cp = curr_part.flat
        solo_stream.insert(cp)

    melody_stream = solo_stream[-1]
    measures = OrderedDict()
    offsetTuples = [(int(n.offset / 4), n) for n in melody_stream]
    measureNum = 0
    for key_x, group in groupby(offsetTuples, lambda x: x[0]):
        measures[measureNum] = [n[1] for n in group]
        measureNum += 1

    chordStream = solo_stream[0]
    chordStream.removeByClass(note.Rest)
    chordStream.removeByClass(note.Note)
    offsetTuples_chords = [(int(n.offset / 4), n) for n in chordStream]

    chords = OrderedDict()
    measureNum = 0
    for key_x, group in groupby(offsetTuples_chords, lambda x: x[0]):
        chords[measureNum] = [n[1] for n in group]
        measureNum += 1

    del chords[len(chords) - 1]
    assert len(chords) == len(measures)

    return measures, chords


def __get_abstract_grammars(measures, chords):
    abstract_grammars = []
    for ix in range(1, len(measures)):
        m = stream.Voice()
        for i in measures[ix]:
            m.insert(i.offset, i)
        c = stream.Voice()
        for j in chords[ix]:
            c.insert(j.offset, j)
        parsed = parse_melody(m, c)
        abstract_grammars.append(parsed)

    return abstract_grammars


def get_musical_data(data_fn):
    measures, chords = __parse_midi(data_fn)
    abstract_grammars = __get_abstract_grammars(measures, chords)

    return chords, abstract_grammars


def get_corpus_data(abstract_grammars):
    corpus = [x for sublist in abstract_grammars for x in sublist.split(" ")]
    values = set(corpus)
    val_indices = dict((v, i) for i, v in enumerate(values))
    indices_val = dict((i, v) for i, v in enumerate(values))

    return corpus, values, val_indices, indices_val

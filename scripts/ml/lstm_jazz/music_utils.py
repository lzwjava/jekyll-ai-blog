from __future__ import print_function

from music21 import *
import numpy as np
from grammar import *
from preprocess import *
from qa import *


def data_processing(corpus, values_indices, m=60, Tx=30):
    Tx = Tx
    N_values = len(set(corpus))
    np.random.seed(0)
    X = np.zeros((m, Tx, N_values), dtype=np.bool)
    Y = np.zeros((m, Tx, N_values), dtype=np.bool)
    for i in range(m):
        random_idx = np.random.choice(len(corpus) - Tx)
        corp_data = corpus[random_idx : (random_idx + Tx)]
        for j in range(Tx):
            idx = values_indices[corp_data[j]]
            if j != 0:
                X[i, j, idx] = 1
                Y[i, j - 1, idx] = 1

    Y = np.swapaxes(Y, 0, 1)
    Y = Y.tolist()
    return np.asarray(X), np.asarray(Y), N_values


def next_value_processing(
    model,
    next_value,
    x,
    predict_and_sample,
    indices_values,
    abstract_grammars,
    duration,
    max_tries=1000,
    temperature=0.5,
):
    if duration < 0.00001:
        tries = 0
        while next_value.split(",")[0] == "R" or len(next_value.split(",")) != 2:
            if tries >= max_tries:
                rand = np.random.randint(0, len(abstract_grammars))
                next_value = abstract_grammars[rand].split(" ")[0]
            else:
                next_value = predict_and_sample(model, x, indices_values, temperature)

            tries += 1

    return next_value


def sequence_to_matrix(sequence, values_indices):
    sequence_len = len(sequence)
    x = np.zeros((1, sequence_len, len(values_indices)))
    for t, value in enumerate(sequence):
        if value not in values_indices:
            print(value)
        x[0, t, values_indices[value]] = 1.0
    return x

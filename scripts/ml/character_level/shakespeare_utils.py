from __future__ import print_function
from tensorflow.keras.models import load_model
import numpy as np
import sys
import io


def build_data(text, Tx=40, stride=3):
    X = []
    Y = []

    for i in range(0, len(text) - Tx, stride):
        X.append(text[i : i + Tx])
        Y.append(text[i + Tx])

    print("number of training examples:", len(X))

    return X, Y


def vectorization(X, Y, n_x, char_indices, Tx=40):
    m = len(X)
    x = np.zeros((m, Tx, n_x), dtype=np.bool)
    y = np.zeros((m, n_x), dtype=np.bool)
    for i, sentence in enumerate(X):
        for t, char in enumerate(sentence):
            x[i, t, char_indices[char]] = 1
        y[i, char_indices[Y[i]]] = 1

    return x, y


def sample(preds, temperature=1.0):
    preds = np.asarray(preds).astype("float64")
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    out = np.random.choice(range(len(chars)), p=probas.ravel())
    return out


def on_epoch_end(epoch, logs):
    None


print("Loading text data...")
text = io.open("shakespeare.txt", encoding="utf-8").read().lower()

Tx = 40
chars = sorted(list(set(text)))
char_indices = dict((c, i) for i, c in enumerate(chars))
indices_char = dict((i, c) for i, c in enumerate(chars))

print("Creating training set...")
X, Y = build_data(text, Tx, stride=3)
print("Vectorizing training set...")
x, y = vectorization(X, Y, n_x=len(chars), char_indices=char_indices)
print("Loading model...")
model = load_model("models/model_shakespeare_kiank_350_epoch.h5")


def generate_output():
    generated = ""

    usr_input = input(
        "Write the beginning of your poem, the Shakespeare machine will complete it. Your input is: "
    )

    sentence = ("{0:0>" + str(Tx) + "}").format(usr_input).lower()
    generated += usr_input

    sys.stdout.write("\n\nHere is your poem: \n\n")
    sys.stdout.write(usr_input)
    for i in range(400):
        x_pred = np.zeros((1, Tx, len(chars)))

        for t, char in enumerate(sentence):
            if char != "0":
                x_pred[0, t, char_indices[char]] = 1.0

        preds = model.predict(x_pred, verbose=0)[0]
        next_index = sample(preds, temperature=1.0)
        next_char = indices_char[next_index]

        generated += next_char
        sentence = sentence[1:] + next_char

        sys.stdout.write(next_char)
        sys.stdout.flush()

        if next_char == "\n":
            continue

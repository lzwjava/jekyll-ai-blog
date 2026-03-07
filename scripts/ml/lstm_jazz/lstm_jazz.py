import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf

from music21 import *
from grammar import *
from qa import *
from preprocess import *
from music_utils import *
from data_utils import *
from outputs import *
from test_utils import *

from tensorflow.keras.layers import (
    Dense,
    Input,
    LSTM,
    Reshape,
    RepeatVector,
)
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import to_categorical

X, Y, n_values, indices_values, chords = load_music_utils("data/original_metheny.mid")
print("number of training examples:", X.shape[0])
print("Tx (length of sequence):", X.shape[1])
print("shape of X:", X.shape)
print("Shape of Y:", Y.shape)
print("Number of chords", len(chords))

n_a = 64

n_values = 90
reshaper = Reshape((1, n_values))
LSTM_cell = LSTM(n_a, return_state=True)
densor = Dense(n_values, activation="softmax")


def djmodel(Tx, LSTM_cell, densor, reshaper):
    n_values = densor.units

    n_a = LSTM_cell.units

    X = Input(shape=(Tx, n_values))

    a0 = Input(shape=(n_a,), name="a0")
    c0 = Input(shape=(n_a,), name="c0")
    a = a0
    c = c0

    outputs = []

    for t in range(Tx):
        x = X[:, t, :]

        x = reshaper(x)

        a, _, c = LSTM_cell(inputs=[x, a, c])

        out = densor(a)

        outputs.append(out)

    model = Model(inputs=[X, a0, c0], outputs=outputs)

    return model


model = djmodel(Tx=30, LSTM_cell=LSTM_cell, densor=densor, reshaper=reshaper)

output = summary(model)
comparator(output, djmodel_out)

model.summary()

opt = Adam(lr=0.01, beta_1=0.9, beta_2=0.999, decay=0.01)

model.compile(optimizer=opt, loss="categorical_crossentropy", metrics=["accuracy"])

m = 60
a0 = np.zeros((m, n_a))
c0 = np.zeros((m, n_a))

history = model.fit([X, a0, c0], list(Y), epochs=100, verbose=0)

print(f"loss at epoch 1: {history.history['loss'][0]}")
print(f"loss at epoch 100: {history.history['loss'][99]}")
plt.plot(history.history["loss"])


def music_inference_model(LSTM_cell, densor, Ty=100):
    n_values = densor.units

    n_a = LSTM_cell.units

    x0 = Input(shape=(1, n_values))

    a0 = Input(shape=(n_a,), name="a0")
    c0 = Input(shape=(n_a,), name="c0")
    a = a0
    c = c0
    x = x0

    outputs = []

    for t in range(Ty):
        a, _, c = LSTM_cell(x, initial_state=[a, c])

        out = densor(a)

        outputs.append(out)

        x = tf.math.argmax(out, 1)
        x = tf.one_hot(x, 90)

        x = RepeatVector(1)(x)

    inference_model = Model(inputs=[x0, a0, c0], outputs=outputs)

    return inference_model


inference_model = music_inference_model(LSTM_cell, densor, Ty=50)

inference_summary = summary(inference_model)
comparator(inference_summary, music_inference_model_out)

inference_model.summary()

x_initializer = np.zeros((1, 1, n_values))
a_initializer = np.zeros((1, n_a))
c_initializer = np.zeros((1, n_a))


def predict_and_sample(
    inference_model,
    x_initializer=x_initializer,
    a_initializer=a_initializer,
    c_initializer=c_initializer,
):
    n_values = x_initializer.shape[2]

    pred = inference_model.predict([x_initializer, a_initializer, c_initializer])

    indices = np.argmax(np.array(pred), axis=-1)

    results = to_categorical(indices, num_classes=n_values)

    return results, indices


results, indices = predict_and_sample(
    inference_model, x_initializer, a_initializer, c_initializer
)

print("np.argmax(results[12]) =", np.argmax(results[12]))
print("np.argmax(results[17]) =", np.argmax(results[17]))
print("list(indices[12:18]) =", list(indices[12:18]))

out_stream = generate_music(inference_model, indices_values, chords)

mid2wav("output/my_music.midi")

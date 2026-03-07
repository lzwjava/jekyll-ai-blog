from tensorflow.keras.layers import (
    Bidirectional,
    Concatenate,
    Dot,
    Input,
    LSTM,
)
from tensorflow.keras.layers import RepeatVector, Dense, Activation
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Model
import tensorflow as tf
import numpy as np

from nmt_utils import *

m = 10000
dataset, human_vocab, machine_vocab, inv_machine_vocab = load_dataset(m)

print(dataset[:10])

Tx = 30
Ty = 10
X, Y, Xoh, Yoh = preprocess_data(dataset, human_vocab, machine_vocab, Tx, Ty)

print("X.shape:", X.shape)
print("Y.shape:", Y.shape)
print("Xoh.shape:", Xoh.shape)
print("Yoh.shape:", Yoh.shape)

index = 0
print("Source date:", dataset[index][0])
print("Target date:", dataset[index][1])
print()
print("Source after preprocessing (indices):", X[index])
print("Target after preprocessing (indices):", Y[index])
print()
print("Source after preprocessing (one-hot):", Xoh[index])
print("Target after preprocessing (one-hot):", Yoh[index])

repeator = RepeatVector(Tx)
concatenator = Concatenate(axis=-1)
densor1 = Dense(10, activation="tanh")
densor2 = Dense(1, activation="relu")
activator = Activation(softmax, name="attention_weights")
dotor = Dot(axes=1)


def one_step_attention(a, s_prev):
    s_prev = repeator(s_prev)

    concat = concatenator([a, s_prev])

    e = densor1(concat)

    energies = densor2(e)

    alphas = activator(energies)

    context = dotor([alphas, a])

    return context


def one_step_attention_test(target):
    m = 10
    Tx = 30
    n_a = 32
    n_s = 64

    a = np.random.uniform(1, 0, (m, Tx, 2 * n_a)).astype(np.float32)
    s_prev = np.random.uniform(1, 0, (m, n_s)).astype(np.float32) * 1
    context = target(a, s_prev)

    assert type(context) == tf.python.framework.ops.EagerTensor, (
        "Unexpected type. It should be a Tensor"
    )
    assert tuple(context.shape) == (m, 1, n_s), "Unexpected output shape"
    assert np.all(context.numpy() > 0), "All output values must be > 0 in this example"
    assert np.all(context.numpy() < 1), "All output values must be < 1 in this example"

    print("\033[92mAll tests passed!")


one_step_attention_test(one_step_attention)

n_a = 32
n_s = 64

post_activation_LSTM_cell = LSTM(n_s, return_state=True)
output_layer = Dense(len(machine_vocab), activation=softmax)


def modelf(Tx, Ty, n_a, n_s, human_vocab_size, machine_vocab_size):
    X = Input(shape=(Tx, human_vocab_size))
    s0 = Input(shape=(n_s,), name="s0")
    c0 = Input(shape=(n_s,), name="c0")
    s = s0
    c = c0

    outputs = []

    a = Bidirectional(LSTM(n_a, return_sequences=True))(X)

    for t in range(Ty):
        context = one_step_attention(a, s)

        s, _, c = post_activation_LSTM_cell(context, initial_state=[s, c])

        out = output_layer(s)

        outputs.append(out)

    model = Model(inputs=[X, s0, c0], outputs=outputs)

    return model


from test_utils import *


def modelf_test(target):
    Tx = 30
    n_a = 32
    n_s = 64
    len_human_vocab = 37
    len_machine_vocab = 11

    model = target(Tx, Ty, n_a, n_s, len_human_vocab, len_machine_vocab)

    print(summary(model))

    expected_summary = [
        ["InputLayer", [(None, 30, 37)], 0],
        ["InputLayer", [(None, 64)], 0],
        ["Bidirectional", (None, 30, 64), 17920],
        ["RepeatVector", (None, 30, 64), 0, 30],
        ["Concatenate", (None, 30, 128), 0],
        ["Dense", (None, 30, 10), 1290, "tanh"],
        ["Dense", (None, 30, 1), 11, "relu"],
        ["Activation", (None, 30, 1), 0],
        ["Dot", (None, 1, 64), 0],
        ["InputLayer", [(None, 64)], 0],
        [
            "LSTM",
            [(None, 64), (None, 64), (None, 64)],
            33024,
            [(None, 1, 64), (None, 64), (None, 64)],
            "tanh",
        ],
        ["Dense", (None, 11), 715, "softmax"],
    ]

    assert len(model.outputs) == 10, (
        f"Wrong output shape. Expected 10 != {len(model.outputs)}"
    )

    comparator(summary(model), expected_summary)


modelf_test(modelf)

model = modelf(Tx, Ty, n_a, n_s, len(human_vocab), len(machine_vocab))

model.summary()

opt = Adam(lr=0.005, beta_1=0.9, beta_2=0.999, decay=0.01)
model.compile(optimizer=opt, loss="categorical_crossentropy", metrics=["accuracy"])

assert opt.lr == 0.005, "Set the lr parameter to 0.005"
assert opt.beta_1 == 0.9, "Set the beta_1 parameter to 0.9"
assert opt.beta_2 == 0.999, "Set the beta_2 parameter to 0.999"
assert opt.decay == 0.01, "Set the decay parameter to 0.01"
assert model.loss == "categorical_crossentropy", (
    "Wrong loss. Use 'categorical_crossentropy'"
)
assert model.optimizer == opt, "Use the optimizer that you have instantiated"
assert model.compiled_metrics._user_metrics[0] == "accuracy", (
    "set metrics to ['accuracy']"
)

print("\033[92mAll tests passed!")

s0 = np.zeros((m, n_s))
c0 = np.zeros((m, n_s))
outputs = list(Yoh.swapaxes(0, 1))

model.fit([Xoh, s0, c0], outputs, epochs=1, batch_size=100)

model.load_weights("models/model.h5")

EXAMPLES = [
    "3 May 1979",
    "5 April 09",
    "21th of August 2016",
    "Tue 10 Jul 2007",
    "Saturday May 9 2018",
    "March 3 2001",
    "March 3rd 2001",
    "1 March 2001",
]
s00 = np.zeros((1, n_s))
c00 = np.zeros((1, n_s))
for example in EXAMPLES:
    source = string_to_int(example, Tx, human_vocab)

    source = np.array(
        list(map(lambda x: to_categorical(x, num_classes=len(human_vocab)), source))
    ).swapaxes(0, 1)
    source = np.swapaxes(source, 0, 1)
    source = np.expand_dims(source, axis=0)
    prediction = model.predict([source, s00, c00])
    prediction = np.argmax(prediction, axis=-1)
    output = [inv_machine_vocab[int(i)] for i in prediction]
    print("source:", example)
    print("output:", "".join(output), "\n")

model.summary()

attention_map = plot_attention_map(
    model, human_vocab, inv_machine_vocab, "Tuesday 09 Oct 1993", num=7, n_s=64
)

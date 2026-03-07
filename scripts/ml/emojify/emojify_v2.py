import numpy as np
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Input, Dropout, LSTM, Activation
from tensorflow.keras.layers import Embedding
from emo_utils import *
from test_utils import *

X_train, Y_train = read_csv("data/train_emoji.csv")
X_test, Y_test = read_csv("data/tesss.csv")

maxLen = len(max(X_train, key=lambda x: len(x.split())).split())

for idx in range(10):
    print(X_train[idx], label_to_emoji(Y_train[idx]))

Y_oh_train = convert_to_one_hot(Y_train, C=5)
Y_oh_test = convert_to_one_hot(Y_test, C=5)

np.random.seed(1)

for idx, val in enumerate(["I", "like", "learning"]):
    print(idx, val)

word_to_index, index_to_word, word_to_vec_map = read_glove_vecs("data/glove.6B.50d.txt")

import numpy as np


def sentences_to_indices(X, word_to_index, max_len):
    m = X.shape[0]

    X_indices = np.zeros((m, max_len))

    for i in range(m):
        sentence_words = X[i].lower().split()

        j = 0

        for w in sentence_words:
            if w in word_to_index:
                X_indices[i, j] = word_to_index[w]

                j += 1

    return X_indices


def sentences_to_indices_test(target):
    word_to_index = {}
    for idx, val in enumerate(
        ["i", "like", "learning", "deep", "machine", "love", "smile", "´0.="]
    ):
        word_to_index[val] = idx + 1

    max_len = 4
    sentences = np.array(
        [
            "I like deep learning",
            "deep ´0.= love machine",
            "machine learning smile",
            "$",
        ]
    )
    indexes = target(sentences, word_to_index, max_len)
    print(indexes)

    assert type(indexes) == np.ndarray, "Wrong type. Use np arrays in the function"
    assert indexes.shape == (sentences.shape[0], max_len), "Wrong shape of ouput matrix"
    assert np.allclose(
        indexes, [[1, 2, 4, 3], [4, 8, 6, 5], [5, 3, 7, 0], [0, 0, 0, 0]]
    ), "Wrong values. Debug with the given examples"

    print("\033[92mAll tests passed!")


sentences_to_indices_test(sentences_to_indices)

X1 = np.array(["funny lol", "lets play baseball", "food is ready for you"])
X1_indices = sentences_to_indices(X1, word_to_index, max_len=5)
print("X1 =", X1)
print("X1_indices =\n", X1_indices)


def pretrained_embedding_layer(word_to_vec_map, word_to_index):
    vocab_size = len(word_to_index) + 1
    emb_dim = word_to_vec_map[next(iter(word_to_vec_map))].shape[0]

    emb_matrix = np.zeros((vocab_size, emb_dim))

    for word, idx in word_to_index.items():
        if word in word_to_vec_map:
            emb_matrix[idx, :] = word_to_vec_map[word]

    embedding_layer = Embedding(
        input_dim=vocab_size, output_dim=emb_dim, trainable=False, input_length=None
    )

    embedding_layer.build((None,))

    embedding_layer.set_weights([emb_matrix])

    return embedding_layer


def pretrained_embedding_layer_test(target):
    word_to_vec_map = {
        "a": [3, 3],
        "synonym_of_a": [3, 3],
        "a_nw": [2, 4],
        "a_s": [3, 2],
        "a_n": [3, 4],
        "c": [-2, 1],
        "c_n": [-2, 2],
        "c_ne": [-1, 2],
        "c_e": [-1, 1],
        "c_se": [-1, 0],
        "c_s": [-2, 0],
        "c_sw": [-3, 0],
        "c_w": [-3, 1],
        "c_nw": [-3, 2],
    }

    for key in word_to_vec_map.keys():
        word_to_vec_map[key] = np.array(word_to_vec_map[key])

    word_to_index = {}
    for idx, val in enumerate(list(word_to_vec_map.keys())):
        word_to_index[val] = idx

    np.random.seed(1)
    embedding_layer = target(word_to_vec_map, word_to_index)

    assert type(embedding_layer) == Embedding, "Wrong type"
    assert embedding_layer.input_dim == len(list(word_to_vec_map.keys())) + 1, (
        "Wrong input shape"
    )
    assert embedding_layer.output_dim == len(word_to_vec_map["a"]), "Wrong output shape"
    assert np.allclose(
        embedding_layer.get_weights(),
        [
            [
                [3, 3],
                [3, 3],
                [2, 4],
                [3, 2],
                [3, 4],
                [-2, 1],
                [-2, 2],
                [-1, 2],
                [-1, 1],
                [-1, 0],
                [-2, 0],
                [-3, 0],
                [-3, 1],
                [-3, 2],
                [0, 0],
            ]
        ],
    ), "Wrong vaulues"
    print("\033[92mAll tests passed!")


pretrained_embedding_layer_test(pretrained_embedding_layer)

embedding_layer = pretrained_embedding_layer(word_to_vec_map, word_to_index)
print("weights[0][1][1] =", embedding_layer.get_weights()[0][1][1])
print("Input_dim", embedding_layer.input_dim)
print("Output_dim", embedding_layer.output_dim)


def Emojify_V2(input_shape, word_to_vec_map, word_to_index):
    sentence_indices = Input(shape=input_shape, dtype="int32")

    embedding_layer = pretrained_embedding_layer(word_to_vec_map, word_to_index)

    embeddings = embedding_layer(sentence_indices)

    X = LSTM(128, return_sequences=True)(embeddings)

    X = Dropout(0.5)(X)

    X = LSTM(128, return_sequences=False)(X)

    X = Dropout(0.5)(X)

    X = Dense(5)(X)

    X = Activation("softmax")(X)

    model = Model(inputs=sentence_indices, outputs=X)

    return model


from tensorflow.python.keras.engine.functional import Functional


def Emojify_V2_test(target):
    word_to_vec_map = {
        "a": [3, 3],
        "synonym_of_a": [3, 3],
        "a_nw": [2, 4],
        "a_s": [3, 2],
        "a_n": [3, 4],
        "c": [-2, 1],
        "c_n": [-2, 2],
        "c_ne": [-1, 2],
        "c_e": [-1, 1],
        "c_se": [-1, 0],
        "c_s": [-2, 0],
        "c_sw": [-3, 0],
        "c_w": [-3, 1],
        "c_nw": [-3, 2],
    }

    for key in word_to_vec_map.keys():
        word_to_vec_map[key] = np.array(word_to_vec_map[key])

    word_to_index = {}
    for idx, val in enumerate(list(word_to_vec_map.keys())):
        word_to_index[val] = idx

    maxLen = 4
    model = target((maxLen,), word_to_vec_map, word_to_index)

    assert type(model) == Functional, (
        'Make sure you have correctly created Model instance which converts "sentence_indices" into "X"'
    )

    expectedModel = [
        ["InputLayer", [(None, 4)], 0],
        ["Embedding", (None, 4, 2), 30],
        ["LSTM", (None, 4, 128), 67072, (None, 4, 2), "tanh", True],
        ["Dropout", (None, 4, 128), 0, 0.5],
        ["LSTM", (None, 128), 131584, (None, 4, 128), "tanh", False],
        ["Dropout", (None, 128), 0, 0.5],
        ["Dense", (None, 5), 645, "linear"],
        ["Activation", (None, 5), 0],
    ]
    comparator(summary(model), expectedModel)


Emojify_V2_test(Emojify_V2)

model = Emojify_V2((maxLen,), word_to_vec_map, word_to_index)
model.summary()

model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

X_train_indices = sentences_to_indices(X_train, word_to_index, maxLen)
Y_train_oh = convert_to_one_hot(Y_train, C=5)

model.fit(X_train_indices, Y_train_oh, epochs=50, batch_size=32, shuffle=True)

X_test_indices = sentences_to_indices(X_test, word_to_index, max_len=maxLen)
Y_test_oh = convert_to_one_hot(Y_test, C=5)
loss, acc = model.evaluate(X_test_indices, Y_test_oh)
print()
print("Test accuracy = ", acc)

C = 5
y_test_oh = np.eye(C)[Y_test.reshape(-1)]
X_test_indices = sentences_to_indices(X_test, word_to_index, maxLen)
pred = model.predict(X_test_indices)
for i in range(len(X_test)):
    x = X_test_indices
    num = np.argmax(pred[i])
    if num != Y_test[i]:
        print(
            "Expected emoji:"
            + label_to_emoji(Y_test[i])
            + " prediction: "
            + X_test[i]
            + label_to_emoji(num).strip()
        )

x_test = np.array(["I cannot play"])
X_test_indices = sentences_to_indices(x_test, word_to_index, maxLen)
print(x_test[0] + " " + label_to_emoji(np.argmax(model.predict(X_test_indices))))

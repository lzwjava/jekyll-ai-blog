import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from cnn_utils import *
from test_utils import summary, comparator

np.random.seed(1)

X_train_orig, Y_train_orig, X_test_orig, Y_test_orig, classes = load_happy_dataset()

X_train = X_train_orig / 255.0
X_test = X_test_orig / 255.0

Y_train = Y_train_orig.T
Y_test = Y_test_orig.T

print("number of training examples = " + str(X_train.shape[0]))
print("number of test examples = " + str(X_test.shape[0]))
print("X_train shape: " + str(X_train.shape))
print("Y_train shape: " + str(Y_train.shape))
print("X_test shape: " + str(X_test.shape))
print("Y_test shape: " + str(Y_test.shape))

index = 124
plt.imshow(X_train_orig[index])


def happyModel():
    model = tf.keras.Sequential(
        [
            tf.keras.layers.ZeroPadding2D(padding=3, input_shape=(64, 64, 3)),
            tf.keras.layers.Conv2D(32, (7, 7), strides=(1, 1)),
            tf.keras.layers.BatchNormalization(axis=3),
            tf.keras.layers.ReLU(),
            tf.keras.layers.MaxPooling2D(),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(1, activation="sigmoid"),
        ]
    )

    return model


happy_model = happyModel()

for layer in summary(happy_model):
    print(layer)

output = [
    ["ZeroPadding2D", (None, 70, 70, 3), 0, ((3, 3), (3, 3))],
    ["Conv2D", (None, 64, 64, 32), 4736, "valid", "linear", "GlorotUniform"],
    ["BatchNormalization", (None, 64, 64, 32), 128],
    ["ReLU", (None, 64, 64, 32), 0],
    ["MaxPooling2D", (None, 32, 32, 32), 0, (2, 2), (2, 2), "valid"],
    ["Flatten", (None, 32768), 0],
    ["Dense", (None, 1), 32769, "sigmoid"],
]

comparator(summary(happy_model), output)

happy_model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])

happy_model.summary()

happy_model.fit(X_train, Y_train, epochs=10, batch_size=16)

happy_model.evaluate(X_test, Y_test)

X_train_orig, Y_train_orig, X_test_orig, Y_test_orig, classes = load_signs_dataset()

index = 9
plt.imshow(X_train_orig[index])
print("y = " + str(np.squeeze(Y_train_orig[:, index])))

X_train = X_train_orig / 255.0
X_test = X_test_orig / 255.0
Y_train = convert_to_one_hot(Y_train_orig, 6).T
Y_test = convert_to_one_hot(Y_test_orig, 6).T
print("number of training examples = " + str(X_train.shape[0]))
print("number of test examples = " + str(X_test.shape[0]))
print("X_train shape: " + str(X_train.shape))
print("Y_train shape: " + str(Y_train.shape))
print("X_test shape: " + str(X_test.shape))
print("Y_test shape: " + str(Y_test.shape))


def convolutional_model(input_shape):
    input_img = tf.keras.Input(shape=input_shape)

    Z1 = tf.keras.layers.Conv2D(8, (4, 4), strides=(1, 1), padding="SAME")(input_img)

    A1 = tf.keras.layers.ReLU()(Z1)

    P1 = tf.keras.layers.MaxPooling2D((8, 8), strides=(8, 8), padding="SAME")(A1)

    Z2 = tf.keras.layers.Conv2D(16, (2, 2), strides=(1, 1), padding="SAME")(P1)

    A2 = tf.keras.layers.ReLU()(Z2)

    P2 = tf.keras.layers.MaxPooling2D((4, 4), strides=(4, 4), padding="SAME")(A2)

    F = tf.keras.layers.Flatten()(P2)

    outputs = tf.keras.layers.Dense(6, activation="softmax")(F)

    model = tf.keras.Model(inputs=input_img, outputs=outputs)
    return model


conv_model = convolutional_model((64, 64, 3))
conv_model.compile(
    optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"]
)
conv_model.summary()

output = [
    ["InputLayer", [(None, 64, 64, 3)], 0],
    ["Conv2D", (None, 64, 64, 8), 392, "same", "linear", "GlorotUniform"],
    ["ReLU", (None, 64, 64, 8), 0],
    ["MaxPooling2D", (None, 8, 8, 8), 0, (8, 8), (8, 8), "same"],
    ["Conv2D", (None, 8, 8, 16), 528, "same", "linear", "GlorotUniform"],
    ["ReLU", (None, 8, 8, 16), 0],
    ["MaxPooling2D", (None, 2, 2, 16), 0, (4, 4), (4, 4), "same"],
    ["Flatten", (None, 64), 0],
    ["Dense", (None, 6), 390, "softmax"],
]

comparator(summary(conv_model), output)

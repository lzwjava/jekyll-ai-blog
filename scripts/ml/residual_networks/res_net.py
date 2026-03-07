import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.layers import (
    Input,
    Add,
    Dense,
    Activation,
    ZeroPadding2D,
    Flatten,
    Conv2D,
    AveragePooling2D,
    MaxPooling2D,
)
from tensorflow.keras.models import Model
from resnets_utils import *
from tensorflow.keras.initializers import (
    random_uniform,
    glorot_uniform,
    constant,
)
from matplotlib.pyplot import imshow

from test_utils import summary, comparator

np.random.seed(1)
tf.random.set_seed(2)


def identity_block(X, f, filters, initializer=random_uniform):
    F1, F2, F3 = filters

    X_shortcut = X

    training = tf.keras.backend.learning_phase()

    X = Conv2D(
        filters=F1,
        kernel_size=1,
        strides=(1, 1),
        padding="valid",
        kernel_initializer=initializer(seed=0),
    )(X)
    X = BatchNormalization(axis=3)(X, training=training)
    X = Activation("relu")(X)

    X = Conv2D(
        filters=F2,
        kernel_size=(f, f),
        strides=(1, 1),
        padding="same",
        kernel_initializer=initializer(seed=0),
    )(X)
    X = BatchNormalization(axis=3)(X, training=training)
    X = Activation("relu")(X)

    X = Conv2D(
        filters=F3,
        kernel_size=(1, 1),
        strides=(1, 1),
        padding="valid",
        kernel_initializer=initializer(seed=0),
    )(X)
    X = BatchNormalization(axis=3)(X, training=training)

    X = Add()([X, X_shortcut])
    X = Activation("relu")(X)

    return X


tf.keras.backend.set_learning_phase(False)

np.random.seed(1)
tf.random.set_seed(2)
X1 = np.ones((1, 4, 4, 3)) * -1
X2 = np.ones((1, 4, 4, 3)) * 1
X3 = np.ones((1, 4, 4, 3)) * 3

X = np.concatenate((X1, X2, X3), axis=0).astype(np.float32)

A3 = identity_block(
    X, f=2, filters=[4, 4, 3], initializer=lambda seed=0: constant(value=1)
)
print("\033[1mWith training=False\033[0m\n")
A3np = A3.numpy()
print(np.around(A3.numpy()[:, (0, -1), :, :].mean(axis=3), 5))
resume = A3np[:, (0, -1), :, :].mean(axis=3)
print(resume[1, 1, 0])

tf.keras.backend.set_learning_phase(True)

print("\n\033[1mWith training=True\033[0m\n")
np.random.seed(1)
tf.random.set_seed(2)
A4 = identity_block(
    X, f=2, filters=[3, 3, 3], initializer=lambda seed=0: constant(value=1)
)
print(np.around(A4.numpy()[:, (0, -1), :, :].mean(axis=3), 5))


def convolutional_block(X, f, filters, s=2, initializer=glorot_uniform):
    F1, F2, F3 = filters

    X_shortcut = X

    training = tf.keras.backend.learning_phase()

    X = Conv2D(
        filters=F1,
        kernel_size=(1, 1),
        strides=(s, s),
        padding="valid",
        kernel_initializer=initializer(seed=0),
    )(X)
    X = BatchNormalization(axis=3)(X, training=training)
    X = Activation("relu")(X)

    X = Conv2D(
        filters=F2,
        kernel_size=(f, f),
        strides=(1, 1),
        padding="same",
        kernel_initializer=initializer(seed=0),
    )(X)
    X = BatchNormalization(axis=3)(X, training=training)
    X = Activation("relu")(X)

    X = Conv2D(
        filters=F3,
        kernel_size=(1, 1),
        strides=(1, 1),
        padding="valid",
        kernel_initializer=initializer(seed=0),
    )(X)
    X = BatchNormalization(axis=3)(X, training=training)

    X_shortcut = Conv2D(
        filters=F3,
        kernel_size=(1, 1),
        strides=(s, s),
        padding="valid",
        kernel_initializer=initializer(seed=0),
    )(X_shortcut)
    X_shortcut = BatchNormalization(axis=3)(X_shortcut, training=training)

    X = Add()([X, X_shortcut])
    X = Activation("relu")(X)

    return X


def ResNet50(input_shape=(64, 64, 3), classes=6, training=False):
    X_input = Input(input_shape)

    X = ZeroPadding2D((3, 3))(X_input)

    X = Conv2D(64, (7, 7), strides=(2, 2), kernel_initializer=glorot_uniform(seed=0))(X)
    X = BatchNormalization(axis=3)(X)
    X = Activation("relu")(X)
    X = MaxPooling2D((3, 3), strides=(2, 2))(X)

    X = convolutional_block(X, f=3, filters=[64, 64, 256], s=1)
    X = identity_block(X, 3, [64, 64, 256])
    X = identity_block(X, 3, [64, 64, 256])

    X = convolutional_block(X, f=3, filters=[128, 128, 512], s=2)
    X = identity_block(X, 3, [128, 128, 512])
    X = identity_block(X, 3, [128, 128, 512])
    X = identity_block(X, 3, [128, 128, 512])

    X = convolutional_block(X, f=3, filters=[256, 256, 1024], s=2)
    X = identity_block(X, 3, [256, 256, 1024])
    X = identity_block(X, 3, [256, 256, 1024])
    X = identity_block(X, 3, [256, 256, 1024])
    X = identity_block(X, 3, [256, 256, 1024])
    X = identity_block(X, 3, [256, 256, 1024])

    X = convolutional_block(X, f=3, filters=[512, 512, 2048], s=2)
    X = identity_block(X, 3, [512, 512, 2048])
    X = identity_block(X, 3, [512, 512, 2048])

    X = AveragePooling2D((2, 2))(X)

    X = Flatten()(X)
    X = Dense(classes, activation="softmax", kernel_initializer=glorot_uniform(seed=0))(
        X
    )

    model = Model(inputs=X_input, outputs=X)

    return model


tf.keras.backend.set_learning_phase(True)

model = ResNet50(input_shape=(64, 64, 3), classes=6)
print(model.summary())

from outputs import ResNet50_summary

model = ResNet50(input_shape=(64, 64, 3), classes=6)

comparator(summary(model), ResNet50_summary)

np.random.seed(1)
tf.random.set_seed(2)
opt = tf.keras.optimizers.Adam(learning_rate=0.00015)
model.compile(optimizer=opt, loss="categorical_crossentropy", metrics=["accuracy"])

X_train_orig, Y_train_orig, X_test_orig, Y_test_orig, classes = load_dataset()

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

model.fit(X_train, Y_train, epochs=10, batch_size=32)

preds = model.evaluate(X_test, Y_test)
print("Loss = " + str(preds[0]))
print("Test Accuracy = " + str(preds[1]))

preds = model.evaluate(X_test, Y_test)
print("Loss = " + str(preds[0]))
print("Test Accuracy = " + str(preds[1]))

img_path = "images/my_image.jpg"
img = image.load_img(img_path, target_size=(64, 64))
x = image.img_to_array(img)
x = np.expand_dims(x, axis=0)
x = x / 255.0
x2 = x
print("Input image shape:", x.shape)
imshow(img)
prediction = model.predict(x2)
print("Class prediction vector [p(0), p(1), p(2), p(3), p(4), p(5)] = ", prediction)
print("Class:", np.argmax(prediction))

model.summary()

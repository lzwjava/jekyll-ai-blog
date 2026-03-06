import math
import random

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class Network(object):
    def __init__(self, sizes):
        self.num_layers = len(sizes)
        self.sizes = sizes
        self.weights = [
            np.random.randn(sizes[i + 1], sizes[i]) for i in range(self.num_layers - 1)
        ]
        self.biases = [
            np.random.randn(sizes[i + 1], 1) for i in range(self.num_layers - 1)
        ]

    def SGD(
        self,
        training_data: zip,
        epochs: int,
        mini_batch_size: int,
        eta: float,
        val_data: zip,
    ):
        training_data = list(training_data)

        n = len(training_data)

        num_batches = math.ceil(n / mini_batch_size)

        if val_data:
            val_data = list(val_data)
            n_val = len(val_data)

        error_rates = [1]

        for j in range(epochs):
            mini_batches = [
                training_data[k * mini_batch_size : (k + 1) * mini_batch_size]
                for k in range(num_batches)
            ]

            for mini_batch in mini_batches:
                self.update_mini_batch(mini_batch, eta)

            if val_data:
                correct = self.evalute(val_data)
                print("Epoch {}: {}/{}".format(j, correct, n_val))
                error_rates.append(1 - correct / n_val)
            else:
                print("Epoch {} complete".format(j))

        if val_data:
            x = [i for i in range(epochs + 1)]
            plt.plot(x, error_rates)
            plt.ylim(0, 1)
            plt.show()

    def update_mini_batch(self, mini_batch, eta):
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        nabla_b = [np.zeros(b.shape) for b in self.biases]

        for x, y in mini_batch:
            delta_nabla_w, delta_nabla_b = self.backprop(x, y)
            nabla_w = [nw + dnw for nw, dnw in zip(nabla_w, delta_nabla_w)]
            nabla_b = [nb + dnb for nb, dnb in zip(nabla_b, delta_nabla_b)]

        n = len(mini_batch)

        self.weights = [w - nw / n * eta for w, nw in zip(self.weights, nabla_w)]
        self.biases = [b - nb / n * eta for b, nb in zip(self.biases, nabla_b)]

    def backprop(self, x, y) -> tuple:
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        nabla_b = [np.zeros(b.shape) for b in self.biases]

        zs = []
        activation = x
        activations = [activation]

        for w, b in zip(self.weights, self.biases):
            z = np.dot(w, activation) + b

            zs.append(z)
            activation = sigmoid(z)
            activations.append(activation)

        for l in range(1, self.num_layers):
            if l == 1:
                left = self.cost_derivative(activations[-1], y)
            else:
                left = np.dot(self.weights[-l + 1].transpose(), delta)

            delta = left * sigmoid_prime(zs[-l])

            nabla_b[-l] = delta
            nabla_w[-l] = np.dot(delta, activations[-l - 1].transpose())

        return nabla_w, nabla_b

    def cost_derivative(self, output_activations, y):
        return output_activations - y

    def evalute(self, test_data):
        test_results = [
            (np.argmax(self.feedforward(x)), np.argmax(y)) for (x, y) in test_data
        ]
        return sum(int(x == y) for (x, y) in test_results)

    def cal(self, test_data):
        return [np.argmax(self.feedforward(x)) for x in test_data]

    def feedforward(self, a):
        for w, b in zip(self.weights, self.biases):
            a = sigmoid(np.dot(w, a) + b)
        return a


def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-z))


def print_shape(array):
    arr = np.array(array)
    print(arr.shape)


def sigmoid_prime(z):
    return sigmoid(z) * (1 - sigmoid(z))


def read_training_data() -> tuple:
    df = pd.read_csv("./train.csv")
    # print(df.head())

    labels = df["label"].values
    pixels = df.drop("label", axis=1).values
    pixels = pixels / 255.0

    shuffle_list = list(zip(pixels, labels))
    random.shuffle(shuffle_list)
    pixels, labels = zip(*shuffle_list)

    n = len(labels)

    inputs = [np.reshape(x, (784, 1)) for x in pixels]
    results = [vectorized_result(y) for y in labels]

    middle = int(n * 0.98)

    training_inputs = inputs[:middle]
    training_results = results[:middle]

    val_inputs = inputs[middle:]
    val_results = results[middle:]

    training_data = zip(training_inputs, training_results)
    val_data = zip(val_inputs, val_results)
    return training_data, val_data


def read_test_input() -> list:
    df = pd.read_csv("./test.csv")
    pixels = df.values
    pixels = pixels / 255.0
    test_input = [np.reshape(x, (784, 1)) for x in pixels]
    return test_input


def vectorized_result(j):
    e = np.zeros((10, 1))
    e[j] = 1.0
    return e


def draw(some_digit):
    some_digit_image = some_digit.reshape(28, 28)

    plt.imshow(some_digit_image, cmap=matplotlib.cm.binary, interpolation="nearest")
    plt.axis("off")
    plt.show()


def submit(test_output):
    test_n = len(test_output)
    images = [i + 1 for i in range(test_n)]

    output = pd.DataFrame({"ImageId": images, "Label": test_output})
    output.to_csv("submission.csv", index=False)


def main():
    training_data, val_data = read_training_data()
    test_input = read_test_input()

    network = Network([784, 30, 10])
    network.SGD(
        training_data, epochs=100, mini_batch_size=10, eta=5e-2, val_data=val_data
    )

    test_output = network.cal(test_input)
    submit(test_output)


if __name__ == "__main__":
    main()

import random

import numpy as np
import matplotlib
import matplotlib.pyplot as plt


class Network(object):
    def __init__(self, sizes):
        self.num_layers = len(sizes)
        self.sizes = sizes

        # print(sizes)
        # print(sizes[1:])

        # print(np.random.randn(30, 1))

        self.biases = [np.random.randn(y, 1) for y in sizes[1:]]
        print("biases:", self.biases)

        self.weights = [np.random.randn(y, x) for x, y in zip(sizes[:-1], sizes[1:])]

        # print(self.weights)
        print("weights:", self.weights)
        # print('shape:')
        # print_shape(self.weights[0])

    def SGD(self, training_data, epochs, mini_batch_size, eta, test_data=None):
        training_data = list(training_data)
        n = len(training_data)

        # print(mini_batch_size)
        # print(epochs)

        if test_data:
            test_data = list(test_data)
            n_test = len(test_data)

        for j in range(epochs):
            random.shuffle(training_data)
            mini_batches = [
                training_data[k : k + mini_batch_size]
                for k in range(0, n, mini_batch_size)
            ]
            for mini_batch in mini_batches:
                self.update_mini_batch(mini_batch, eta)
            if test_data:
                print("Epoch {}: {}/{}".format(j, self.evalute(test_data), n_test))
            else:
                print("Epoch {} complete".format(j))

    def update_mini_batch(self, mini_batch, eta):
        # print(self.biases)
        # print(self.weights)
        # print(len(self.biases))
        # print(len(self.weights))
        # print_shape(self.biases[0])
        # print_shape(self.biases[1])
        # print_shape(self.weights[0])
        # print_shape(self.weights[1])

        nabla_b = [np.zeros(b.shape) for b in self.biases]

        # print_shape(nabla_b[0])
        # print_shape(nabla_b[1])

        nabla_w = [np.zeros(w.shape) for w in self.weights]

        # print_shape(nabla_w[0])
        # print_shape(nabla_w[1])

        # print(mini_batch)
        # print(mini_batch[0])
        # print_shape(mini_batch[0][0])
        # print_shape(mini_batch[0][1])

        for x, y in mini_batch:
            # print('x:', x)
            # print('y:', y)
            # print_shape(x)
            # print_shape(y)
            delta_nabla_b, delta_nabla_w = self.backprop(x, y)
            # print(delta_nabla_b)
            # print(delta_nabla_w)

            nabla_b = [nb + dnb for nb, dnb in zip(nabla_b, delta_nabla_b)]
            nabla_w = [nw + dnw for nw, dnw in zip(nabla_w, delta_nabla_w)]

        self.weights = [
            w - (eta / len(mini_batch)) * nw for w, nw in zip(self.weights, nabla_w)
        ]

        self.biases = [
            b - (eta / len(mini_batch)) * nb for b, nb in zip(self.biases, nabla_b)
        ]

    def backprop(self, x, y):
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]

        activation = x
        activations = [x]

        zs = []

        for b, w in zip(self.biases, self.weights):
            # print('w')
            # print_shape(w)
            # print('activation')
            # print_shape(activation)
            # print('b')
            # print_shape(b)

            z = np.dot(w, activation) + b
            # print('z')
            # print_shape(z)
            # quit()

            zs.append(z)
            activation = sigmoid(z)
            activations.append(activation)

        delta = self.cost_derivative(activations[-1], y) * sigmoid_prime(zs[-1])

        nabla_b[-1] = delta
        nabla_w[-1] = np.dot(delta, activations[-2].transpose())

        # print('delta')
        # print(delta)
        # print('nabla_b[-1]')
        # print(nabla_b[-1])
        # print('nabla_w[-1]')
        # print(nabla_w[-1])
        # quit()

        # print('len')
        # print(len(activations))

        for l in range(2, self.num_layers):
            z = zs[-l]
            sp = sigmoid_prime(z)
            delta = np.dot(self.weights[-l + 1].transpose(), delta) * sp
            nabla_b[-l] = delta
            nabla_w[-l] = np.dot(delta, activations[-l - 1].transpose())

        return (nabla_b, nabla_w)

    def cost_derivative(self, output_activations, y):
        return output_activations - y

    def evalute(self, test_data):
        # print('test_data', test_data[0])
        # draw(test_data[0][0])
        # print('shape of test_data[0][0]:')
        # print_shape(test_data[0][0])

        # print(type(test_data))
        # print_shape(test_data[1])

        test_results = [(np.argmax(self.feedforward(x)), y) for (x, y) in test_data]
        return sum(int(x == y) for (x, y) in test_results)

    def feedforward(self, a):
        # i = 0
        for b, w in zip(self.biases, self.weights):
            # if (i < 5):
            #     print('b:', b)
            #     print('w:', w)
            #     print('a:', a)
            #     print('dot:', np.dot(w, a))
            # i += 1
            a = sigmoid(np.dot(w, a) + b)
            # print(a)
        # quit()
        return a


def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-z))


def draw(some_digit):
    some_digit_image = some_digit.reshape(28, 28)

    plt.imshow(some_digit_image, cmap=matplotlib.cm.binary, interpolation="nearest")
    plt.axis("off")
    plt.show()


def print_shape(array):
    arr = np.array(array)
    print(arr.shape)


def sigmoid_prime(z):
    return sigmoid(z) * (1 - sigmoid(z))

import numpy as np


def print_shape(array):
    arr = np.array(array)
    print(arr.shape)


class Network(object):
    def __init__(self, sizes):
        self.num_layers = len(sizes)
        self.sizes = sizes
        self.biases = [np.random.randn(y, 1) for y in sizes[1:]]
        self.weights = [np.random.randn(y, x) for x, y in zip(sizes[:-1], sizes[1:])]

        print(self.sizes)
        print(self.sizes[1:])
        print(self.biases)

        print(type(self.biases))
        print(type(self.biases[0]))

        print(np.random.randn(10, 1))

        print(sizes[:-1])
        print(self.weights)

        for x, y in zip(sizes[:-1], sizes[1:]):
            print(x, y)

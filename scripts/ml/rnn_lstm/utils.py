import numpy as np


def sigmoid(x, derivative=False):
    x_safe = x + 1e-12
    f = 1 / (1 + np.exp(-x_safe))

    if derivative:
        return f * (1 - f)
    else:
        return f


def tanh(x, derivative=False):
    x_safe = x + 1e-12
    f = (np.exp(x_safe) - np.exp(-x_safe)) / (np.exp(x_safe) + np.exp(-x_safe))

    if derivative:
        return 1 - f**2
    else:
        return f


def softmax(x, derivative=False):
    x_safe = x + 1e-12
    f = np.exp(x_safe) / np.sum(np.exp(x_safe))

    if derivative:
        pass
    else:
        return f

test = "Hello World"

print("test: " + test)

import math
from public_tests import *


def basic_sigmoid(x):
    s = 1 / (1 + math.exp(-x))

    return s


print("basic_sigmoid(1) = " + str(basic_sigmoid(1)))

basic_sigmoid_test(basic_sigmoid)

x = [1, 2, 3]
# basic_sigmoid(x)

import numpy as np

t_x = np.array([1, 2, 3])
print(np.exp(t_x))

t_x = np.array([1, 2, 3])
print(t_x + 3)


def sigmoid(x):
    s = 1 / (1 + np.exp(-x))

    return s


t_x = np.array([1, 2, 3])
print("sigmoid(t_x) = " + str(sigmoid(t_x)))

sigmoid_test(sigmoid)


def sigmoid_derivative(x):
    s = sigmoid(x)

    ds = s * (1 - s)

    return ds


t_x = np.array([1, 2, 3])
print("sigmoid_derivative(t_x) = " + str(sigmoid_derivative(t_x)))

sigmoid_derivative_test(sigmoid_derivative)


def image2vector(image):
    l, h, d = image.shape

    v = image.reshape(l * h * d, 1)

    return v


t_image = np.array(
    [
        [[0.67826139, 0.29380381], [0.90714982, 0.52835647], [0.4215251, 0.45017551]],
        [[0.92814219, 0.96677647], [0.85304703, 0.52351845], [0.19981397, 0.27417313]],
        [[0.60659855, 0.00533165], [0.10820313, 0.49978937], [0.34144279, 0.94630077]],
    ]
)

print("image2vector(image) = " + str(image2vector(t_image)))

image2vector_test(image2vector)


def normalize_rows(x):
    x_norm = np.linalg.norm(x, axis=1, keepdims=True)
    x = x / x_norm

    return x


x = np.array([[0, 3, 4], [1, 6, 4]])
print("normalizeRows(x) = " + str(normalize_rows(x)))

normalizeRows_test(normalize_rows)


def softmax(x):
    x_exp = np.exp(x)

    x_sum = np.sum(x_exp, axis=1, keepdims=True)

    s = x_exp / x_sum

    return s


t_x = np.array([[9, 2, 5, 0, 0], [7, 5, 0, 0, 0]])
print("softmax(x) = " + str(softmax(t_x)))

softmax_test(softmax)

import time

x1 = [9, 2, 5, 0, 0, 7, 5, 0, 0, 0, 9, 2, 5, 0, 0]
x2 = [9, 2, 2, 9, 0, 9, 2, 5, 0, 0, 9, 2, 5, 0, 0]

tic = time.process_time()
dot = 0

for i in range(len(x1)):
    dot += x1[i] * x2[i]
toc = time.process_time()
print(
    "dot = "
    + str(dot)
    + "\n ----- Computation time = "
    + str(1000 * (toc - tic))
    + "ms"
)

tic = time.process_time()
outer = np.zeros((len(x1), len(x2)))

for i in range(len(x1)):
    for j in range(len(x2)):
        outer[i, j] = x1[i] * x2[j]
toc = time.process_time()
print(
    "outer = "
    + str(outer)
    + "\n ----- Computation time = "
    + str(1000 * (toc - tic))
    + "ms"
)

tic = time.process_time()
mul = np.zeros(len(x1))

for i in range(len(x1)):
    mul[i] = x1[i] * x2[i]
toc = time.process_time()
print(
    "elementwise multiplication = "
    + str(mul)
    + "\n ----- Computation time = "
    + str(1000 * (toc - tic))
    + "ms"
)

W = np.random.rand(3, len(x1))
tic = time.process_time()
gdot = np.zeros(W.shape[0])

for i in range(W.shape[0]):
    for j in range(len(x1)):
        gdot[i] += W[i, j] * x1[j]
toc = time.process_time()
print(
    "gdot = "
    + str(gdot)
    + "\n ----- Computation time = "
    + str(1000 * (toc - tic))
    + "ms"
)

x1 = [9, 2, 5, 0, 0, 7, 5, 0, 0, 0, 9, 2, 5, 0, 0]
x2 = [9, 2, 2, 9, 0, 9, 2, 5, 0, 0, 9, 2, 5, 0, 0]

tic = time.process_time()
dot = np.dot(x1, x2)
toc = time.process_time()
print(
    "dot = "
    + str(dot)
    + "\n ----- Computation time = "
    + str(1000 * (toc - tic))
    + "ms"
)

tic = time.process_time()
outer = np.outer(x1, x2)
toc = time.process_time()
print(
    "outer = "
    + str(outer)
    + "\n ----- Computation time = "
    + str(1000 * (toc - tic))
    + "ms"
)

tic = time.process_time()
mul = np.multiply(x1, x2)
toc = time.process_time()
print(
    "elementwise multiplication = "
    + str(mul)
    + "\n ----- Computation time = "
    + str(1000 * (toc - tic))
    + "ms"
)

tic = time.process_time()
dot = np.dot(W, x1)
toc = time.process_time()
print(
    "gdot = "
    + str(dot)
    + "\n ----- Computation time = "
    + str(1000 * (toc - tic))
    + "ms"
)


def L1(yhat, y):
    loss = np.sum(np.abs(y - yhat))

    return loss


yhat = np.array([0.9, 0.2, 0.1, 0.4, 0.9])
y = np.array([1, 0, 0, 1, 1])
print("L1 = " + str(L1(yhat, y)))

L1_test(L1)


def L2(yhat, y):
    loss = np.sum((y - yhat) ** 2)

    return loss


yhat = np.array([0.9, 0.2, 0.1, 0.4, 0.9])
y = np.array([1, 0, 0, 1, 1])

print("L2 = " + str(L2(yhat, y)))

L2_test(L2)

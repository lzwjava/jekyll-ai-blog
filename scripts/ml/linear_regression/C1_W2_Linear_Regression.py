import numpy as np
import matplotlib.pyplot as plt
from utils import *
import copy
import math

x_train, y_train = load_data()

print(x_train)

print(y_train)

print("Type of x_train:", type(x_train))
print("First five elements of x_train are:\n", x_train[:5])

print("Type of y_train:", type(y_train))
print("First five elements of y_train are:\n", y_train[:5])

print("The shape of x_train is:", x_train.shape)
print("The shape of y_train is: ", y_train.shape)
print("Number of training examples (m):", len(x_train))

plt.scatter(x_train, y_train, marker="x", c="r")

plt.title("Profits vs. Population per city")

plt.ylabel("Profit in $10,000")

plt.xlabel("Population of City in 10,000s")
plt.show()


def compute_cost(x, y, w, b):
    m = x.shape[0]

    total_cost = 0

    return total_cost


initial_w = 2
initial_b = 1

cost = compute_cost(x_train, y_train, initial_w, initial_b)
print(type(cost))
print(f"Cost at initial w: {cost:.3f}")

from public_tests import *

compute_cost_test(compute_cost)


def compute_gradient(x, y, w, b):
    m = x.shape[0]

    dj_dw = 0
    dj_db = 0

    return dj_dw, dj_db


initial_w = 0
initial_b = 0

tmp_dj_dw, tmp_dj_db = compute_gradient(x_train, y_train, initial_w, initial_b)
print("Gradient at initial w, b (zeros):", tmp_dj_dw, tmp_dj_db)

compute_gradient_test(compute_gradient)

test_w = 0.2
test_b = 0.2
tmp_dj_dw, tmp_dj_db = compute_gradient(x_train, y_train, test_w, test_b)

print("Gradient at test w, b:", tmp_dj_dw, tmp_dj_db)


def gradient_descent(
    x, y, w_in, b_in, cost_function, gradient_function, alpha, num_iters
):
    m = len(x)

    J_history = []
    w_history = []
    w = copy.deepcopy(w_in)
    b = b_in

    for i in range(num_iters):
        dj_dw, dj_db = gradient_function(x, y, w, b)

        w = w - alpha * dj_dw
        b = b - alpha * dj_db

        if i < 100000:
            cost = cost_function(x, y, w, b)
            J_history.append(cost)

        if i % math.ceil(num_iters / 10) == 0:
            w_history.append(w)
            print(f"Iteration {i:4}: Cost {float(J_history[-1]):8.2f}   ")

    return w, b, J_history, w_history


initial_w = 0.0
initial_b = 0.0

iterations = 1500
alpha = 0.01

w, b, _, _ = gradient_descent(
    x_train,
    y_train,
    initial_w,
    initial_b,
    compute_cost,
    compute_gradient,
    alpha,
    iterations,
)
print("w,b found by gradient descent:", w, b)

m = x_train.shape[0]
predicted = np.zeros(m)

for i in range(m):
    predicted[i] = w * x_train[i] + b

plt.plot(x_train, predicted, c="b")

plt.scatter(x_train, y_train, marker="x", c="r")

plt.title("Profits vs. Population per city")

plt.ylabel("Profit in $10,000")

plt.xlabel("Population of City in 10,000s")

predict1 = 3.5 * w + b
print("For population = 35,000, we predict a profit of $%.2f" % (predict1 * 10000))

predict2 = 7.0 * w + b
print("For population = 70,000, we predict a profit of $%.2f" % (predict2 * 10000))

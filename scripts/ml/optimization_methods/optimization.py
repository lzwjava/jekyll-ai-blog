import numpy as np
import matplotlib.pyplot as plt
import math

from opt_utils_v1a import (
    initialize_parameters,
    forward_propagation,
    backward_propagation,
)
from opt_utils_v1a import (
    compute_cost,
    predict,
    predict_dec,
    plot_decision_boundary,
    load_dataset,
)
from testCases import *
from public_tests import *

plt.rcParams["figure.figsize"] = (7.0, 4.0)
plt.rcParams["image.interpolation"] = "nearest"
plt.rcParams["image.cmap"] = "gray"


def update_parameters_with_gd(parameters, grads, learning_rate):
    L = len(parameters) // 2

    for l in range(1, L + 1):
        wl = "W" + str(l)
        bl = "b" + str(l)
        dWl = "dW" + str(l)
        dbl = "db" + str(l)
        parameters[wl] = parameters[wl] - learning_rate * grads[dWl]
        parameters[bl] = parameters[bl] - learning_rate * grads[dbl]

    return parameters


parameters, grads, learning_rate = update_parameters_with_gd_test_case()
learning_rate = 0.01
parameters = update_parameters_with_gd(parameters, grads, learning_rate)

print("W1 =\n" + str(parameters["W1"]))
print("b1 =\n" + str(parameters["b1"]))
print("W2 =\n" + str(parameters["W2"]))
print("b2 =\n" + str(parameters["b2"]))

update_parameters_with_gd_test(update_parameters_with_gd)


def random_mini_batches(X, Y, mini_batch_size=64, seed=0):
    np.random.seed(seed)
    m = X.shape[1]
    mini_batches = []

    permutation = list(np.random.permutation(m))
    shuffled_X = X[:, permutation]
    shuffled_Y = Y[:, permutation].reshape((1, m))

    inc = mini_batch_size

    num_complete_minibatches = math.floor(m / mini_batch_size)
    for k in range(0, num_complete_minibatches):
        mini_batch_X = shuffled_X[:, k * mini_batch_size : (k + 1) * mini_batch_size]
        mini_batch_Y = shuffled_Y[:, k * mini_batch_size : (k + 1) * mini_batch_size]

        mini_batch = (mini_batch_X, mini_batch_Y)
        mini_batches.append(mini_batch)

    if m % mini_batch_size != 0:
        mini_batch_X = shuffled_X[:, num_complete_minibatches * mini_batch_size :]
        mini_batch_Y = shuffled_Y[:, num_complete_minibatches * mini_batch_size :]
        mini_batch = (mini_batch_X, mini_batch_Y)
        mini_batches.append(mini_batch)

    return mini_batches


np.random.seed(1)
mini_batch_size = 64
nx = 12288
m = 148
X = np.array([x for x in range(nx * m)]).reshape((m, nx)).T
Y = np.random.randn(1, m) < 0.5

mini_batches = random_mini_batches(X, Y, mini_batch_size)
n_batches = len(mini_batches)

assert n_batches == math.ceil(m / mini_batch_size), (
    f"Wrong number of mini batches. {n_batches} != {math.ceil(m / mini_batch_size)}"
)
for k in range(n_batches - 1):
    assert mini_batches[k][0].shape == (
        nx,
        mini_batch_size,
    ), f"Wrong shape in {k} mini batch for X"
    assert mini_batches[k][1].shape == (
        1,
        mini_batch_size,
    ), f"Wrong shape in {k} mini batch for Y"
    assert np.sum(np.sum(mini_batches[k][0] - mini_batches[k][0][0], axis=0)) == (
        (nx * (nx - 1) / 2) * mini_batch_size
    ), "Wrong values. It happens if the order of X rows(features) changes"
if m % mini_batch_size > 0:
    assert mini_batches[n_batches - 1][0].shape == (
        nx,
        m % mini_batch_size,
    ), (
        f"Wrong shape in the last minibatch. {mini_batches[n_batches - 1][0].shape} != {(nx, m % mini_batch_size)}"
    )

assert np.allclose(mini_batches[0][0][0][0:3], [294912, 86016, 454656]), (
    "Wrong values. Check the indexes used to form the mini batches"
)
assert np.allclose(mini_batches[-1][0][-1][0:3], [1425407, 1769471, 897023]), (
    "Wrong values. Check the indexes used to form the mini batches"
)

print("\033[92mAll tests passed!")


def initialize_velocity(parameters):
    L = len(parameters) // 2
    v = {}

    for l in range(1, L + 1):
        wl = parameters["W" + str(l)]
        bl = parameters["b" + str(l)]
        v["dW" + str(l)] = np.zeros(wl.shape)
        v["db" + str(l)] = np.zeros(bl.shape)

    return v


parameters = initialize_velocity_test_case()

v = initialize_velocity(parameters)
print('v["dW1"] =\n' + str(v["dW1"]))
print('v["db1"] =\n' + str(v["db1"]))
print('v["dW2"] =\n' + str(v["dW2"]))
print('v["db2"] =\n' + str(v["db2"]))

initialize_velocity_test(initialize_velocity)


def update_parameters_with_momentum(parameters, grads, v, beta, learning_rate):
    L = len(parameters) // 2

    for l in range(1, L + 1):
        dWl = "dW" + str(l)
        dbl = "db" + str(l)

        gdW = grads[dWl]
        gdb = grads[dbl]

        v[dWl] = beta * v[dWl] + (1 - beta) * gdW
        v[dbl] = beta * v[dbl] + (1 - beta) * gdb

        Wl = "W" + str(l)
        bl = "b" + str(l)
        parameters[Wl] = parameters[Wl] - learning_rate * v[dWl]
        parameters[bl] = parameters[bl] - learning_rate * v[dbl]

    return parameters, v


parameters, grads, v = update_parameters_with_momentum_test_case()

parameters, v = update_parameters_with_momentum(
    parameters, grads, v, beta=0.9, learning_rate=0.01
)
print("W1 = \n" + str(parameters["W1"]))
print("b1 = \n" + str(parameters["b1"]))
print("W2 = \n" + str(parameters["W2"]))
print("b2 = \n" + str(parameters["b2"]))
print('v["dW1"] = \n' + str(v["dW1"]))
print('v["db1"] = \n' + str(v["db1"]))
print('v["dW2"] = \n' + str(v["dW2"]))
print('v["db2"] = v' + str(v["db2"]))

update_parameters_with_momentum_test(update_parameters_with_momentum)


def initialize_adam(parameters):
    L = len(parameters) // 2
    v = {}
    s = {}

    for l in range(1, L + 1):
        Wl = "W" + str(l)
        Ws = parameters[Wl].shape
        bl = "b" + str(l)
        bs = parameters[bl].shape
        v["dW" + str(l)] = np.zeros(Ws)
        v["db" + str(l)] = np.zeros(bs)
        s["dW" + str(l)] = np.zeros(Ws)
        s["db" + str(l)] = np.zeros(bs)

    return v, s


parameters = initialize_adam_test_case()

v, s = initialize_adam(parameters)
print('v["dW1"] = \n' + str(v["dW1"]))
print('v["db1"] = \n' + str(v["db1"]))
print('v["dW2"] = \n' + str(v["dW2"]))
print('v["db2"] = \n' + str(v["db2"]))
print('s["dW1"] = \n' + str(s["dW1"]))
print('s["db1"] = \n' + str(s["db1"]))
print('s["dW2"] = \n' + str(s["dW2"]))
print('s["db2"] = \n' + str(s["db2"]))

initialize_adam_test(initialize_adam)


def update_parameters_with_adam(
    parameters, grads, v, s, t, learning_rate=0.01, beta1=0.9, beta2=0.999, epsilon=1e-8
):
    L = len(parameters) // 2
    v_corrected = {}
    s_corrected = {}

    for l in range(1, L + 1):
        dWl = "dW" + str(l)
        dbl = "db" + str(l)
        gdW = grads[dWl]
        gdb = grads[dbl]
        v[dWl] = beta1 * v[dWl] + (1 - beta1) * gdW
        v[dbl] = beta1 * v[dbl] + (1 - beta1) * gdb

        v_corrected[dWl] = v[dWl] / (1 - beta1**t)
        v_corrected[dbl] = v[dbl] / (1 - beta1**t)

        s[dWl] = beta2 * s[dWl] + (1 - beta2) * (gdW**2)
        s[dbl] = beta2 * s[dbl] + (1 - beta2) * (gdb**2)

        s_corrected[dWl] = s[dWl] / (1 - beta2**t)
        s_corrected[dbl] = s[dbl] / (1 - beta2**t)

        Wl = "W" + str(l)
        bl = "b" + str(l)
        parameters[Wl] = parameters[Wl] - learning_rate * (
            v_corrected[dWl] / (np.sqrt(s_corrected[dWl]) + epsilon)
        )
        parameters[bl] = parameters[bl] - learning_rate * (
            v_corrected[dbl] / (np.sqrt(s_corrected[dbl]) + epsilon)
        )

    return parameters, v, s, v_corrected, s_corrected


parametersi, grads, vi, si, t, learning_rate, beta1, beta2, epsilon = (
    update_parameters_with_adam_test_case()
)

parameters, v, s, vc, sc = update_parameters_with_adam(
    parametersi, grads, vi, si, t, learning_rate, beta1, beta2, epsilon
)
print(f"W1 = \n{parameters['W1']}")
print(f"W2 = \n{parameters['W2']}")
print(f"b1 = \n{parameters['b1']}")
print(f"b2 = \n{parameters['b2']}")

update_parameters_with_adam_test(update_parameters_with_adam)

train_X, train_Y = load_dataset()


def model(
    X,
    Y,
    layers_dims,
    optimizer,
    learning_rate=0.0007,
    mini_batch_size=64,
    beta=0.9,
    beta1=0.9,
    beta2=0.999,
    epsilon=1e-8,
    num_epochs=5000,
    print_cost=True,
):
    L = len(layers_dims)
    costs = []
    t = 0
    seed = 10
    m = X.shape[1]

    parameters = initialize_parameters(layers_dims)

    if optimizer == "gd":
        pass
    elif optimizer == "momentum":
        v = initialize_velocity(parameters)
    elif optimizer == "adam":
        v, s = initialize_adam(parameters)

    for i in range(num_epochs):
        seed = seed + 1
        minibatches = random_mini_batches(X, Y, mini_batch_size, seed)
        cost_total = 0

        for minibatch in minibatches:
            minibatch_X, minibatch_Y = minibatch

            a3, caches = forward_propagation(minibatch_X, parameters)

            cost_total += compute_cost(a3, minibatch_Y)

            grads = backward_propagation(minibatch_X, minibatch_Y, caches)

            if optimizer == "gd":
                parameters = update_parameters_with_gd(parameters, grads, learning_rate)
            elif optimizer == "momentum":
                parameters, v = update_parameters_with_momentum(
                    parameters, grads, v, beta, learning_rate
                )
            elif optimizer == "adam":
                t = t + 1
                parameters, v, s, _, _ = update_parameters_with_adam(
                    parameters, grads, v, s, t, learning_rate, beta1, beta2, epsilon
                )
        cost_avg = cost_total / m

        if print_cost and i % 1000 == 0:
            print("Cost after epoch %i: %f" % (i, cost_avg))
        if print_cost and i % 100 == 0:
            costs.append(cost_avg)

    plt.plot(costs)
    plt.ylabel("cost")
    plt.xlabel("epochs (per 100)")
    plt.title("Learning rate = " + str(learning_rate))
    plt.show()

    return parameters


train_X, train_Y = load_dataset()


def model(
    X,
    Y,
    layers_dims,
    optimizer,
    learning_rate=0.0007,
    mini_batch_size=64,
    beta=0.9,
    beta1=0.9,
    beta2=0.999,
    epsilon=1e-8,
    num_epochs=5000,
    print_cost=True,
):
    L = len(layers_dims)
    costs = []
    t = 0
    seed = 10
    m = X.shape[1]

    parameters = initialize_parameters(layers_dims)

    if optimizer == "gd":
        pass
    elif optimizer == "momentum":
        v = initialize_velocity(parameters)
    elif optimizer == "adam":
        v, s = initialize_adam(parameters)

    for i in range(num_epochs):
        seed = seed + 1
        minibatches = random_mini_batches(X, Y, mini_batch_size, seed)
        cost_total = 0

        for minibatch in minibatches:
            minibatch_X, minibatch_Y = minibatch

            a3, caches = forward_propagation(minibatch_X, parameters)

            cost_total += compute_cost(a3, minibatch_Y)

            grads = backward_propagation(minibatch_X, minibatch_Y, caches)

            if optimizer == "gd":
                parameters = update_parameters_with_gd(parameters, grads, learning_rate)
            elif optimizer == "momentum":
                parameters, v = update_parameters_with_momentum(
                    parameters, grads, v, beta, learning_rate
                )
            elif optimizer == "adam":
                t = t + 1
                parameters, v, s, _, _ = update_parameters_with_adam(
                    parameters, grads, v, s, t, learning_rate, beta1, beta2, epsilon
                )
        cost_avg = cost_total / m

        if print_cost and i % 1000 == 0:
            print("Cost after epoch %i: %f" % (i, cost_avg))
        if print_cost and i % 100 == 0:
            costs.append(cost_avg)

    plt.plot(costs)
    plt.ylabel("cost")
    plt.xlabel("epochs (per 100)")
    plt.title("Learning rate = " + str(learning_rate))

    return parameters


layers_dims = [train_X.shape[0], 5, 2, 1]
parameters = model(train_X, train_Y, layers_dims, optimizer="gd")

predictions = predict(train_X, train_Y, parameters)

plt.title("Model with Gradient Descent optimization")
axes = plt.gca()
axes.set_xlim([-1.5, 2.5])
axes.set_ylim([-1, 1.5])

layers_dims = [train_X.shape[0], 5, 2, 1]
parameters = model(train_X, train_Y, layers_dims, beta=0.9, optimizer="momentum")

predictions = predict(train_X, train_Y, parameters)

plt.title("Model with Momentum optimization")
axes = plt.gca()
axes.set_xlim([-1.5, 2.5])
axes.set_ylim([-1, 1.5])

layers_dims = [train_X.shape[0], 5, 2, 1]
parameters = model(train_X, train_Y, layers_dims, optimizer="adam")

predictions = predict(train_X, train_Y, parameters)

plt.title("Model with Adam optimization")
axes = plt.gca()
axes.set_xlim([-1.5, 2.5])
axes.set_ylim([-1, 1.5])


def model(
    X,
    Y,
    layers_dims,
    optimizer,
    learning_rate=0.0007,
    mini_batch_size=64,
    beta=0.9,
    beta1=0.9,
    beta2=0.999,
    epsilon=1e-8,
    num_epochs=5000,
    print_cost=True,
    decay=None,
    decay_rate=1,
):
    L = len(layers_dims)
    costs = []
    t = 0
    seed = 10
    m = X.shape[1]
    lr_rates = []
    learning_rate0 = learning_rate

    parameters = initialize_parameters(layers_dims)

    if optimizer == "gd":
        pass
    elif optimizer == "momentum":
        v = initialize_velocity(parameters)
    elif optimizer == "adam":
        v, s = initialize_adam(parameters)

    for i in range(num_epochs):
        seed = seed + 1
        minibatches = random_mini_batches(X, Y, mini_batch_size, seed)
        cost_total = 0

        for minibatch in minibatches:
            minibatch_X, minibatch_Y = minibatch

            a3, caches = forward_propagation(minibatch_X, parameters)

            cost_total += compute_cost(a3, minibatch_Y)

            grads = backward_propagation(minibatch_X, minibatch_Y, caches)

            if optimizer == "gd":
                parameters = update_parameters_with_gd(parameters, grads, learning_rate)
            elif optimizer == "momentum":
                parameters, v = update_parameters_with_momentum(
                    parameters, grads, v, beta, learning_rate
                )
            elif optimizer == "adam":
                t = t + 1
                parameters, v, s, _, _ = update_parameters_with_adam(
                    parameters, grads, v, s, t, learning_rate, beta1, beta2, epsilon
                )
        cost_avg = cost_total / m
        if decay:
            learning_rate = decay(learning_rate0, i, decay_rate)

        if print_cost and i % 1000 == 0:
            print("Cost after epoch %i: %f" % (i, cost_avg))
            if decay:
                print("learning rate after epoch %i: %f" % (i, learning_rate))
        if print_cost and i % 100 == 0:
            costs.append(cost_avg)

    plt.plot(costs)
    plt.ylabel("cost")
    plt.xlabel("epochs (per 100)")
    plt.title("Learning rate = " + str(learning_rate))
    plt.show()

    return parameters


def update_lr(learning_rate0, epoch_num, decay_rate):
    learning_rate = 1 / (1 + decay_rate * epoch_num) * learning_rate0
    return learning_rate


learning_rate = 0.5
print("Original learning rate: ", learning_rate)
epoch_num = 2
decay_rate = 1
learning_rate_2 = update_lr(learning_rate, epoch_num, decay_rate)

print("Updated learning rate: ", learning_rate_2)

update_lr_test(update_lr)


def schedule_lr_decay(learning_rate0, epoch_num, decay_rate, time_interval=1000):
    learning_rate = (
        1 / (1 + decay_rate * np.floor(epoch_num / time_interval)) * learning_rate0
    )

    return learning_rate


learning_rate = 0.5
print("Original learning rate: ", learning_rate)

epoch_num_1 = 10
epoch_num_2 = 100
decay_rate = 0.3
time_interval = 100
learning_rate_1 = schedule_lr_decay(
    learning_rate, epoch_num_1, decay_rate, time_interval
)
learning_rate_2 = schedule_lr_decay(
    learning_rate, epoch_num_2, decay_rate, time_interval
)
print("Updated learning rate after {} epochs: ".format(epoch_num_1), learning_rate_1)
print("Updated learning rate after {} epochs: ".format(epoch_num_2), learning_rate_2)

schedule_lr_decay_test(schedule_lr_decay)

layers_dims = [train_X.shape[0], 5, 2, 1]
parameters = model(
    train_X,
    train_Y,
    layers_dims,
    optimizer="gd",
    learning_rate=0.1,
    num_epochs=5000,
    decay=schedule_lr_decay,
)

predictions = predict(train_X, train_Y, parameters)

plt.title("Model with Gradient Descent optimization")
axes = plt.gca()
axes.set_xlim([-1.5, 2.5])
axes.set_ylim([-1, 1.5])
plot_decision_boundary(lambda x: predict_dec(parameters, x.T), train_X, train_Y)

layers_dims = [train_X.shape[0], 5, 2, 1]
parameters = model(
    train_X,
    train_Y,
    layers_dims,
    optimizer="momentum",
    learning_rate=0.1,
    num_epochs=5000,
    decay=schedule_lr_decay,
)

predictions = predict(train_X, train_Y, parameters)

plt.title("Model with Gradient Descent with momentum optimization")
axes = plt.gca()
axes.set_xlim([-1.5, 2.5])
axes.set_ylim([-1, 1.5])
plot_decision_boundary(lambda x: predict_dec(parameters, x.T), train_X, train_Y)

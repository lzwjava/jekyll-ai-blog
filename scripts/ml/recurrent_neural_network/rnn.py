import numpy as np
from rnn_utils import *
from public_tests import *


def rnn_cell_forward(xt, a_prev, parameters):
    Wax = parameters["Wax"]
    Waa = parameters["Waa"]
    Wya = parameters["Wya"]
    ba = parameters["ba"]
    by = parameters["by"]

    a_next = np.tanh(np.dot(Waa, a_prev) + np.dot(Wax, xt) + ba)

    yt_pred = softmax(np.dot(Wya, a_next) + by)

    cache = (a_next, a_prev, xt, parameters)

    return a_next, yt_pred, cache


np.random.seed(1)
xt_tmp = np.random.randn(3, 10)
a_prev_tmp = np.random.randn(5, 10)
parameters_tmp = {}
parameters_tmp["Waa"] = np.random.randn(5, 5)
parameters_tmp["Wax"] = np.random.randn(5, 3)
parameters_tmp["Wya"] = np.random.randn(2, 5)
parameters_tmp["ba"] = np.random.randn(5, 1)
parameters_tmp["by"] = np.random.randn(2, 1)

a_next_tmp, yt_pred_tmp, cache_tmp = rnn_cell_forward(
    xt_tmp, a_prev_tmp, parameters_tmp
)
print("a_next[4] = \n", a_next_tmp[4])
print("a_next.shape = \n", a_next_tmp.shape)
print("yt_pred[1] =\n", yt_pred_tmp[1])
print("yt_pred.shape = \n", yt_pred_tmp.shape)

rnn_cell_forward_tests(rnn_cell_forward)


def rnn_forward(x, a0, parameters):
    caches = []

    n_x, m, T_x = x.shape
    n_y, n_a = parameters["Wya"].shape

    a = np.zeros((n_a, m, T_x))
    y_pred = np.zeros((n_y, m, T_x))

    a_next = a0

    for t in range(T_x):
        a_next, yt_pred, cache = rnn_cell_forward(x[:, :, t], a_next, parameters)

        a[:, :, t] = a_next

        y_pred[:, :, t] = yt_pred

        caches.append(cache)

    caches = (caches, x)

    return a, y_pred, caches


np.random.seed(1)
x_tmp = np.random.randn(3, 10, 4)
a0_tmp = np.random.randn(5, 10)
parameters_tmp = {}
parameters_tmp["Waa"] = np.random.randn(5, 5)
parameters_tmp["Wax"] = np.random.randn(5, 3)
parameters_tmp["Wya"] = np.random.randn(2, 5)
parameters_tmp["ba"] = np.random.randn(5, 1)
parameters_tmp["by"] = np.random.randn(2, 1)

a_tmp, y_pred_tmp, caches_tmp = rnn_forward(x_tmp, a0_tmp, parameters_tmp)
print("a[4][1] = \n", a_tmp[4][1])
print("a.shape = \n", a_tmp.shape)
print("y_pred[1][3] =\n", y_pred_tmp[1][3])
print("y_pred.shape = \n", y_pred_tmp.shape)
print("caches[1][1][3] =\n", caches_tmp[1][1][3])
print("len(caches) = \n", len(caches_tmp))

rnn_forward_test(rnn_forward)


def lstm_cell_forward(xt, a_prev, c_prev, parameters):
    Wf = parameters["Wf"]
    bf = parameters["bf"]
    Wi = parameters["Wi"]
    bi = parameters["bi"]
    Wc = parameters["Wc"]
    bc = parameters["bc"]
    Wo = parameters["Wo"]
    bo = parameters["bo"]
    Wy = parameters["Wy"]
    by = parameters["by"]

    n_x, m = xt.shape
    n_y, n_a = Wy.shape

    concat = np.concatenate((a_prev, xt), axis=0)

    ft = sigmoid(np.dot(Wf, concat) + bf)
    it = sigmoid(np.dot(Wi, concat) + bi)
    cct = np.tanh(np.dot(Wc, concat) + bc)
    c_next = ft * c_prev + it * cct
    ot = sigmoid(np.dot(Wo, concat) + bo)
    a_next = ot * np.tanh(c_next)

    yt_pred = softmax(np.dot(Wy, a_next) + by)

    cache = (a_next, c_next, a_prev, c_prev, ft, it, cct, ot, xt, parameters)

    return a_next, c_next, yt_pred, cache


np.random.seed(1)
xt_tmp = np.random.randn(3, 10)
a_prev_tmp = np.random.randn(5, 10)
c_prev_tmp = np.random.randn(5, 10)
parameters_tmp = {}
parameters_tmp["Wf"] = np.random.randn(5, 5 + 3)
parameters_tmp["bf"] = np.random.randn(5, 1)
parameters_tmp["Wi"] = np.random.randn(5, 5 + 3)
parameters_tmp["bi"] = np.random.randn(5, 1)
parameters_tmp["Wo"] = np.random.randn(5, 5 + 3)
parameters_tmp["bo"] = np.random.randn(5, 1)
parameters_tmp["Wc"] = np.random.randn(5, 5 + 3)
parameters_tmp["bc"] = np.random.randn(5, 1)
parameters_tmp["Wy"] = np.random.randn(2, 5)
parameters_tmp["by"] = np.random.randn(2, 1)

a_next_tmp, c_next_tmp, yt_tmp, cache_tmp = lstm_cell_forward(
    xt_tmp, a_prev_tmp, c_prev_tmp, parameters_tmp
)

print("a_next[4] = \n", a_next_tmp[4])
print("a_next.shape = ", a_next_tmp.shape)
print("c_next[2] = \n", c_next_tmp[2])
print("c_next.shape = ", c_next_tmp.shape)
print("yt[1] =", yt_tmp[1])
print("yt.shape = ", yt_tmp.shape)
print("cache[1][3] =\n", cache_tmp[1][3])
print("len(cache) = ", len(cache_tmp))

lstm_cell_forward_test(lstm_cell_forward)


def lstm_forward(x, a0, parameters):
    caches = []

    Wy = parameters["Wy"]

    n_x, m, T_x = x.shape
    n_y, n_a = Wy.shape

    a = np.zeros((n_a, m, T_x))
    c = np.zeros((n_a, m, T_x))
    y = np.zeros((n_y, m, T_x))

    a_next = a0
    c_next = np.zeros(a_next.shape)

    for t in range(T_x):
        xt = x[:, :, t]

        a_next, c_next, yt, cache = lstm_cell_forward(xt, a_next, c_next, parameters)

        a[:, :, t] = a_next

        c[:, :, t] = c_next

        y[:, :, t] = yt

        caches.append(cache)

    caches = (caches, x)

    return a, y, c, caches


np.random.seed(1)
x_tmp = np.random.randn(3, 10, 7)
a0_tmp = np.random.randn(5, 10)
parameters_tmp = {}
parameters_tmp["Wf"] = np.random.randn(5, 5 + 3)
parameters_tmp["bf"] = np.random.randn(5, 1)
parameters_tmp["Wi"] = np.random.randn(5, 5 + 3)
parameters_tmp["bi"] = np.random.randn(5, 1)
parameters_tmp["Wo"] = np.random.randn(5, 5 + 3)
parameters_tmp["bo"] = np.random.randn(5, 1)
parameters_tmp["Wc"] = np.random.randn(5, 5 + 3)
parameters_tmp["bc"] = np.random.randn(5, 1)
parameters_tmp["Wy"] = np.random.randn(2, 5)
parameters_tmp["by"] = np.random.randn(2, 1)

a_tmp, y_tmp, c_tmp, caches_tmp = lstm_forward(x_tmp, a0_tmp, parameters_tmp)
print("a[4][3][6] = ", a_tmp[4][3][6])
print("a.shape = ", a_tmp.shape)
print("y[1][4][3] =", y_tmp[1][4][3])
print("y.shape = ", y_tmp.shape)
print("caches[1][1][1] =\n", caches_tmp[1][1][1])
print("c[1][2][1]", c_tmp[1][2][1])
print("len(caches) = ", len(caches_tmp))

lstm_forward_test(lstm_forward)


def rnn_cell_backward(da_next, cache):
    a_next, a_prev, xt, parameters = cache

    Wax = parameters["Wax"]
    Waa = parameters["Waa"]
    Wya = parameters["Wya"]
    ba = parameters["ba"]
    by = parameters["by"]

    dtanh = da_next * (
        1 - np.square(np.tanh(np.dot(Wax, xt) + np.dot(Waa, a_prev) + ba))
    )

    dxt = np.dot(Wax.T, dtanh)
    dWax = np.dot(dtanh, xt.T)

    da_prev = np.dot(Waa.T, dtanh)
    dWaa = np.dot(dtanh, a_prev.T)

    dba = np.sum(dtanh, axis=1, keepdims=True)

    gradients = {"dxt": dxt, "da_prev": da_prev, "dWax": dWax, "dWaa": dWaa, "dba": dba}

    return gradients


np.random.seed(1)
xt_tmp = np.random.randn(3, 10)
a_prev_tmp = np.random.randn(5, 10)
parameters_tmp = {}
parameters_tmp["Wax"] = np.random.randn(5, 3)
parameters_tmp["Waa"] = np.random.randn(5, 5)
parameters_tmp["Wya"] = np.random.randn(2, 5)
parameters_tmp["ba"] = np.random.randn(5, 1)
parameters_tmp["by"] = np.random.randn(2, 1)

a_next_tmp, yt_tmp, cache_tmp = rnn_cell_forward(xt_tmp, a_prev_tmp, parameters_tmp)

da_next_tmp = np.random.randn(5, 10)
gradients_tmp = rnn_cell_backward(da_next_tmp, cache_tmp)
print('gradients["dxt"][1][2] =', gradients_tmp["dxt"][1][2])
print('gradients["dxt"].shape =', gradients_tmp["dxt"].shape)
print('gradients["da_prev"][2][3] =', gradients_tmp["da_prev"][2][3])
print('gradients["da_prev"].shape =', gradients_tmp["da_prev"].shape)
print('gradients["dWax"][3][1] =', gradients_tmp["dWax"][3][1])
print('gradients["dWax"].shape =', gradients_tmp["dWax"].shape)
print('gradients["dWaa"][1][2] =', gradients_tmp["dWaa"][1][2])
print('gradients["dWaa"].shape =', gradients_tmp["dWaa"].shape)
print('gradients["dba"][4] =', gradients_tmp["dba"][4])
print('gradients["dba"].shape =', gradients_tmp["dba"].shape)


def rnn_backward(da, caches):
    caches, x = caches
    a1, a0, x1, parameters = caches[0]

    n_a, m, T_x = da.shape
    n_x, m = x1.shape

    dx = np.zeros((n_x, m, T_x))
    dWax = np.zeros((n_a, n_x))
    dWaa = np.zeros((n_a, n_a))
    dba = np.zeros((n_a, 1))
    da_prevt = da[:, :, T_x - 1]

    for t in reversed(range(T_x)):
        gradients = rnn_cell_backward(da[:, :, t] + da_prevt, caches[t])

        dxt, da_prevt, dWaxt, dWaat, dbat = (
            gradients["dxt"],
            gradients["da_prev"],
            gradients["dWax"],
            gradients["dWaa"],
            gradients["dba"],
        )

        dx[:, :, t] = dxt
        dWax += dWaxt
        dWaa += dWaat
        dba += dbat

    da0 = da_prevt

    gradients = {"dx": dx, "da0": da0, "dWax": dWax, "dWaa": dWaa, "dba": dba}

    return gradients


np.random.seed(1)
x_tmp = np.random.randn(3, 10, 4)
a0_tmp = np.random.randn(5, 10)
parameters_tmp = {}
parameters_tmp["Wax"] = np.random.randn(5, 3)
parameters_tmp["Waa"] = np.random.randn(5, 5)
parameters_tmp["Wya"] = np.random.randn(2, 5)
parameters_tmp["ba"] = np.random.randn(5, 1)
parameters_tmp["by"] = np.random.randn(2, 1)

a_tmp, y_tmp, caches_tmp = rnn_forward(x_tmp, a0_tmp, parameters_tmp)
da_tmp = np.random.randn(5, 10, 4)
gradients_tmp = rnn_backward(da_tmp, caches_tmp)

print('gradients["dx"][1][2] =', gradients_tmp["dx"][1][2])
print('gradients["dx"].shape =', gradients_tmp["dx"].shape)
print('gradients["da0"][2][3] =', gradients_tmp["da0"][2][3])
print('gradients["da0"].shape =', gradients_tmp["da0"].shape)
print('gradients["dWax"][3][1] =', gradients_tmp["dWax"][3][1])
print('gradients["dWax"].shape =', gradients_tmp["dWax"].shape)
print('gradients["dWaa"][1][2] =', gradients_tmp["dWaa"][1][2])
print('gradients["dWaa"].shape =', gradients_tmp["dWaa"].shape)
print('gradients["dba"][4] =', gradients_tmp["dba"][4])
print('gradients["dba"].shape =', gradients_tmp["dba"].shape)


def lstm_cell_backward(da_next, dc_next, cache):
    a_next, c_next, a_prev, c_prev, ft, it, cct, ot, xt, parameters = cache

    n_x, m = xt.shape
    n_a, m = a_next.shape

    dot = da_next * np.tanh(c_next) * ot * (1 - ot)
    dcct = (dc_next * it + ot * (1 - np.square(np.tanh(c_next))) * it * da_next) * (
        1 - np.square(cct)
    )
    dit = (
        (dc_next * cct + ot * (1 - np.square(np.tanh(c_next))) * cct * da_next)
        * it
        * (1 - it)
    )
    dft = (
        (dc_next * c_prev + ot * (1 - np.square(np.tanh(c_next))) * c_prev * da_next)
        * ft
        * (1 - ft)
    )

    concat = np.concatenate((a_prev, xt), axis=0)

    dWf = np.dot(dft, concat.T)
    dWi = np.dot(dit, concat.T)
    dWc = np.dot(dcct, concat.T)
    dWo = np.dot(dot, concat.T)
    dbf = np.sum(dft, axis=1, keepdims=True)
    dbi = np.sum(dit, axis=1, keepdims=True)
    dbc = np.sum(dcct, axis=1, keepdims=True)
    dbo = np.sum(dot, axis=1, keepdims=True)

    da_prev = (
        np.dot(parameters["Wf"][:, :n_a].T, dft)
        + np.dot(parameters["Wi"][:, :n_a].T, dit)
        + np.dot(parameters["Wc"][:, :n_a].T, dcct)
        + np.dot(parameters["Wo"][:, :n_a].T, dot)
    )
    dc_prev = dc_next * ft + ot * (1 - np.square(np.tanh(c_next))) * ft * da_next
    dxt = (
        np.dot(parameters["Wf"][:, n_a:].T, dft)
        + np.dot(parameters["Wi"][:, n_a:].T, dit)
        + np.dot(parameters["Wc"][:, n_a:].T, dcct)
        + np.dot(parameters["Wo"][:, n_a:].T, dot)
    )

    gradients = {
        "dxt": dxt,
        "da_prev": da_prev,
        "dc_prev": dc_prev,
        "dWf": dWf,
        "dbf": dbf,
        "dWi": dWi,
        "dbi": dbi,
        "dWc": dWc,
        "dbc": dbc,
        "dWo": dWo,
        "dbo": dbo,
    }

    return gradients


np.random.seed(1)
xt_tmp = np.random.randn(3, 10)

a_prev_tmp = np.random.randn(5, 10)
c_prev_tmp = np.random.randn(5, 10)
parameters_tmp = {}
parameters_tmp["Wf"] = np.random.randn(5, 5 + 3)
parameters_tmp["bf"] = np.random.randn(5, 1)
parameters_tmp["Wi"] = np.random.randn(5, 5 + 3)
parameters_tmp["bi"] = np.random.randn(5, 1)
parameters_tmp["Wo"] = np.random.randn(5, 5 + 3)
parameters_tmp["bo"] = np.random.randn(5, 1)
parameters_tmp["Wc"] = np.random.randn(5, 5 + 3)
parameters_tmp["bc"] = np.random.randn(5, 1)
parameters_tmp["Wy"] = np.random.randn(2, 5)
parameters_tmp["by"] = np.random.randn(2, 1)

a_next_tmp, c_next_tmp, yt_tmp, cache_tmp = lstm_cell_forward(
    xt_tmp, a_prev_tmp, c_prev_tmp, parameters_tmp
)

da_next_tmp = np.random.randn(5, 10)
dc_next_tmp = np.random.randn(5, 10)
gradients_tmp = lstm_cell_backward(da_next_tmp, dc_next_tmp, cache_tmp)
print('gradients["dxt"][1][2] =', gradients_tmp["dxt"][1][2])
print('gradients["dxt"].shape =', gradients_tmp["dxt"].shape)
print('gradients["da_prev"][2][3] =', gradients_tmp["da_prev"][2][3])
print('gradients["da_prev"].shape =', gradients_tmp["da_prev"].shape)
print('gradients["dc_prev"][2][3] =', gradients_tmp["dc_prev"][2][3])
print('gradients["dc_prev"].shape =', gradients_tmp["dc_prev"].shape)
print('gradients["dWf"][3][1] =', gradients_tmp["dWf"][3][1])
print('gradients["dWf"].shape =', gradients_tmp["dWf"].shape)
print('gradients["dWi"][1][2] =', gradients_tmp["dWi"][1][2])
print('gradients["dWi"].shape =', gradients_tmp["dWi"].shape)
print('gradients["dWc"][3][1] =', gradients_tmp["dWc"][3][1])
print('gradients["dWc"].shape =', gradients_tmp["dWc"].shape)
print('gradients["dWo"][1][2] =', gradients_tmp["dWo"][1][2])
print('gradients["dWo"].shape =', gradients_tmp["dWo"].shape)
print('gradients["dbf"][4] =', gradients_tmp["dbf"][4])
print('gradients["dbf"].shape =', gradients_tmp["dbf"].shape)
print('gradients["dbi"][4] =', gradients_tmp["dbi"][4])
print('gradients["dbi"].shape =', gradients_tmp["dbi"].shape)
print('gradients["dbc"][4] =', gradients_tmp["dbc"][4])
print('gradients["dbc"].shape =', gradients_tmp["dbc"].shape)
print('gradients["dbo"][4] =', gradients_tmp["dbo"][4])
print('gradients["dbo"].shape =', gradients_tmp["dbo"].shape)


def lstm_backward(da, caches):
    caches, x = caches
    a1, c1, a0, c0, f1, i1, cc1, o1, x1, parameters = caches[0]

    n_a, m, T_x = da.shape
    n_x, m = x1.shape

    dx = np.zeros((n_x, m, T_x))
    da0 = np.zeros((n_a, m))
    da_prevt = np.zeros((n_a, m))
    dc_prevt = np.zeros((n_a, m))
    dWf = np.zeros((n_a, n_a + n_x))
    dWi = np.zeros((n_a, n_a + n_x))
    dWc = np.zeros((n_a, n_a + n_x))
    dWo = np.zeros((n_a, n_a + n_x))
    dbf = np.zeros((n_a, 1))
    dbi = np.zeros((n_a, 1))
    dbc = np.zeros((n_a, 1))
    dbo = np.zeros((n_a, 1))

    for t in reversed(range(T_x)):
        gradients = lstm_cell_backward(da[:, :, t] + da_prevt, dc_prevt, caches[t])

        da_prevt = gradients["da_prev"]
        dc_prevt = gradients["dc_prev"]
        dx[:, :, t] = gradients["dxt"]
        dWf += gradients["dWf"]
        dWi += gradients["dWi"]
        dWc += gradients["dWc"]
        dWo += gradients["dWo"]
        dbf += gradients["dbf"]
        dbi += gradients["dbi"]
        dbc += gradients["dbc"]
        dbo += gradients["dbo"]

    da0 = da_prevt

    gradients = {
        "dx": dx,
        "da0": da0,
        "dWf": dWf,
        "dbf": dbf,
        "dWi": dWi,
        "dbi": dbi,
        "dWc": dWc,
        "dbc": dbc,
        "dWo": dWo,
        "dbo": dbo,
    }

    return gradients


np.random.seed(1)
x_tmp = np.random.randn(3, 10, 7)
a0_tmp = np.random.randn(5, 10)

parameters_tmp = {}
parameters_tmp["Wf"] = np.random.randn(5, 5 + 3)
parameters_tmp["bf"] = np.random.randn(5, 1)
parameters_tmp["Wi"] = np.random.randn(5, 5 + 3)
parameters_tmp["bi"] = np.random.randn(5, 1)
parameters_tmp["Wo"] = np.random.randn(5, 5 + 3)
parameters_tmp["bo"] = np.random.randn(5, 1)
parameters_tmp["Wc"] = np.random.randn(5, 5 + 3)
parameters_tmp["bc"] = np.random.randn(5, 1)
parameters_tmp["Wy"] = np.zeros((2, 5))
parameters_tmp["by"] = np.zeros((2, 1))

a_tmp, y_tmp, c_tmp, caches_tmp = lstm_forward(x_tmp, a0_tmp, parameters_tmp)

da_tmp = np.random.randn(5, 10, 4)
gradients_tmp = lstm_backward(da_tmp, caches_tmp)

print('gradients["dx"][1][2] =', gradients_tmp["dx"][1][2])
print('gradients["dx"].shape =', gradients_tmp["dx"].shape)
print('gradients["da0"][2][3] =', gradients_tmp["da0"][2][3])
print('gradients["da0"].shape =', gradients_tmp["da0"].shape)
print('gradients["dWf"][3][1] =', gradients_tmp["dWf"][3][1])
print('gradients["dWf"].shape =', gradients_tmp["dWf"].shape)
print('gradients["dWi"][1][2] =', gradients_tmp["dWi"][1][2])
print('gradients["dWi"].shape =', gradients_tmp["dWi"].shape)
print('gradients["dWc"][3][1] =', gradients_tmp["dWc"][3][1])
print('gradients["dWc"].shape =', gradients_tmp["dWc"].shape)
print('gradients["dWo"][1][2] =', gradients_tmp["dWo"][1][2])
print('gradients["dWo"].shape =', gradients_tmp["dWo"].shape)
print('gradients["dbf"][4] =', gradients_tmp["dbf"][4])
print('gradients["dbf"].shape =', gradients_tmp["dbf"].shape)
print('gradients["dbi"][4] =', gradients_tmp["dbi"][4])
print('gradients["dbi"].shape =', gradients_tmp["dbi"].shape)
print('gradients["dbc"][4] =', gradients_tmp["dbc"][4])
print('gradients["dbc"].shape =', gradients_tmp["dbc"].shape)
print('gradients["dbo"][4] =', gradients_tmp["dbo"][4])
print('gradients["dbo"].shape =', gradients_tmp["dbo"].shape)

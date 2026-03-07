import numpy as np
import matplotlib.pyplot as plt
from public_tests import *

plt.rcParams["figure.figsize"] = (5.0, 4.0)
plt.rcParams["image.interpolation"] = "nearest"
plt.rcParams["image.cmap"] = "gray"

np.random.seed(1)


def zero_pad(X, pad):
    pad_width = ((0, 0), (pad, pad), (pad, pad), (0, 0))

    X_pad = np.pad(X, pad_width, mode="constant", constant_values=0)

    return X_pad


np.random.seed(1)
x = np.random.randn(4, 3, 3, 2)
x_pad = zero_pad(x, 3)
print("x.shape =\n", x.shape)
print("x_pad.shape =\n", x_pad.shape)
print("x[1,1] =\n", x[1, 1])
print("x_pad[1,1] =\n", x_pad[1, 1])

fig, axarr = plt.subplots(1, 2)
axarr[0].set_title("x")
axarr[0].imshow(x[0, :, :, 0])
axarr[1].set_title("x_pad")
axarr[1].imshow(x_pad[0, :, :, 0])
zero_pad_test(zero_pad)


def conv_single_step(a_slice_prev, W, b):
    s = a_slice_prev * W
    Z = np.sum(s)
    Z = Z + float(b)
    return Z


np.random.seed(1)
a_slice_prev = np.random.randn(4, 4, 3)
W = np.random.randn(4, 4, 3)
b = np.random.randn(1, 1, 1)

Z = conv_single_step(a_slice_prev, W, b)
print("Z =", Z)
conv_single_step_test(conv_single_step)

assert type(Z) == np.float64, "You must cast the output to numpy float 64"
assert np.isclose(Z, -6.999089450680221), "Wrong value"


def conv_forward(A_prev, W, b, hparameters):
    m, n_H_prev, n_W_prev, n_C_prev = A_prev.shape

    f, f, n_C_prev, n_C = W.shape

    stride = hparameters["stride"]
    pad = hparameters["pad"]

    n_H = int((n_H_prev - f + 2 * pad) / stride) + 1
    n_W = int((n_W_prev - f + 2 * pad) / stride) + 1

    Z = np.zeros((m, n_H, n_W, n_C))

    A_prev_pad = zero_pad(A_prev, pad)

    for i in range(m):
        a_prev_pad = A_prev_pad[i]
        for h in range(0, n_H * stride, stride):
            vert_start = h
            vert_end = h + f
            for w in range(0, n_W * stride, stride):
                horiz_start = w
                horiz_end = w + f

                for c in range(n_C):
                    a_slice_prev = a_prev_pad[
                        vert_start:vert_end, horiz_start:horiz_end, :
                    ]
                    weights = W[:, :, :, c]
                    biases = b[:, :, :, c]
                    Z[i, h // stride, w // stride, c] = np.sum(
                        a_slice_prev * weights
                    ) + np.squeeze(biases)
    cache = (A_prev, W, b, hparameters)

    return Z, cache


np.random.seed(1)
A_prev = np.random.randn(2, 5, 7, 4)
W = np.random.randn(3, 3, 4, 8)
b = np.random.randn(1, 1, 1, 8)
hparameters = {"pad": 1, "stride": 2}

Z, cache_conv = conv_forward(A_prev, W, b, hparameters)
z_mean = np.mean(Z)
z_0_2_1 = Z[0, 2, 1]
cache_0_1_2_3 = cache_conv[0][1][2][3]
print("Z's mean =\n", z_mean)
print("Z[0,2,1] =\n", z_0_2_1)
print("cache_conv[0][1][2][3] =\n", cache_0_1_2_3)

conv_forward_test_1(z_mean, z_0_2_1, cache_0_1_2_3)
conv_forward_test_2(conv_forward)


def pool_forward(A_prev, hparameters, mode="max"):
    m, n_H_prev, n_W_prev, n_C_prev = A_prev.shape

    f = hparameters["f"]
    stride = hparameters["stride"]

    n_H = int(1 + (n_H_prev - f) / stride)
    n_W = int(1 + (n_W_prev - f) / stride)
    n_C = n_C_prev

    A = np.zeros((m, n_H, n_W, n_C))

    for i in range(m):
        for h in range(0, n_H * stride, stride):
            vert_start = h
            vert_end = h + f
            for w in range(0, n_W * stride, stride):
                horiz_start = w
                horiz_end = w + f
                for c in range(n_C):
                    a_slice_prev = A_prev[
                        i, vert_start:vert_end, horiz_start:horiz_end, c
                    ]
                    if mode == "max":
                        A[i, h // stride, w // stride, c] = np.max(a_slice_prev)
                    elif mode == "average":
                        A[i, h // stride, w // stride, c] = np.average(a_slice_prev)

    cache = (A_prev, hparameters)

    return A, cache


print("CASE 1:\n")
np.random.seed(1)
A_prev_case_1 = np.random.randn(2, 5, 5, 3)
hparameters_case_1 = {"stride": 1, "f": 3}

A, cache = pool_forward(A_prev_case_1, hparameters_case_1, mode="max")
print("mode = max")
print("A.shape = " + str(A.shape))
print("A[1, 1] =\n", A[1, 1])
A, cache = pool_forward(A_prev_case_1, hparameters_case_1, mode="average")
print("mode = average")
print("A.shape = " + str(A.shape))
print("A[1, 1] =\n", A[1, 1])

pool_forward_test_1(pool_forward)

print("\n\033[0mCASE 2:\n")
np.random.seed(1)
A_prev_case_2 = np.random.randn(2, 5, 5, 3)
hparameters_case_2 = {"stride": 2, "f": 3}

A, cache = pool_forward(A_prev_case_2, hparameters_case_2, mode="max")
print("mode = max")
print("A.shape = " + str(A.shape))
print("A[0] =\n", A[0])
print()

A, cache = pool_forward(A_prev_case_2, hparameters_case_2, mode="average")
print("mode = average")
print("A.shape = " + str(A.shape))
print("A[1] =\n", A[1])

pool_forward_test_2(pool_forward)


def conv_backward(dZ, cache):
    A_prev, W, b, hparameters = cache

    m, n_H_prev, n_W_prev, n_C_prev = A_prev.shape

    f, f, n_C_prev, n_C = W.shape

    stride = hparameters["stride"]
    pad = hparameters["pad"]

    m, n_H, n_W, n_C = dZ.shape

    dA_prev = np.zeros((m, n_H_prev, n_W_prev, n_C_prev))
    dW = np.zeros((f, f, n_C_prev, n_C))
    db = np.zeros((1, 1, 1, n_C))

    A_prev_pad = zero_pad(A_prev, pad)
    dA_prev_pad = zero_pad(dA_prev, pad)

    for i in range(m):
        a_prev_pad = A_prev_pad[i]
        da_prev_pad = dA_prev_pad[i]

        for h in range(n_H):
            for w in range(n_W):
                for c in range(n_C):
                    vert_start = h * stride
                    vert_end = vert_start + f
                    horiz_start = w * stride
                    horiz_end = horiz_start + f

                    a_slice = a_prev_pad[vert_start:vert_end, horiz_start:horiz_end, :]

                    da_prev_pad[vert_start:vert_end, horiz_start:horiz_end, :] += (
                        W[:, :, :, c] * dZ[i, h, w, c]
                    )
                    dW[:, :, :, c] += a_slice * dZ[i, h, w, c]
                    db[:, :, :, c] += dZ[i, h, w, c]

        dA_prev[i, :, :, :] = da_prev_pad[pad:-pad, pad:-pad, :]

    return dA_prev, dW, db


np.random.seed(1)
A_prev = np.random.randn(10, 4, 4, 3)
W = np.random.randn(2, 2, 3, 8)
b = np.random.randn(1, 1, 1, 8)
hparameters = {"pad": 2, "stride": 2}
Z, cache_conv = conv_forward(A_prev, W, b, hparameters)

dA, dW, db = conv_backward(Z, cache_conv)

print("dA_mean =", np.mean(dA))
print("dW_mean =", np.mean(dW))
print("db_mean =", np.mean(db))

assert type(dA) == np.ndarray, "Output must be a np.ndarray"
assert type(dW) == np.ndarray, "Output must be a np.ndarray"
assert type(db) == np.ndarray, "Output must be a np.ndarray"
assert dA.shape == (10, 4, 4, 3), f"Wrong shape for dA  {dA.shape} != (10, 4, 4, 3)"
assert dW.shape == (2, 2, 3, 8), f"Wrong shape for dW {dW.shape} != (2, 2, 3, 8)"
assert db.shape == (1, 1, 1, 8), f"Wrong shape for db {db.shape} != (1, 1, 1, 8)"
assert np.isclose(np.mean(dA), 1.4524377), "Wrong values for dA"
assert np.isclose(np.mean(dW), 1.7269914), "Wrong values for dW"
assert np.isclose(np.mean(db), 7.8392325), "Wrong values for db"

print("\033[92m All tests passed.")


def create_mask_from_window(x):
    mask = x == np.max(x)
    return mask


np.random.seed(1)
x = np.random.randn(2, 3)
mask = create_mask_from_window(x)
print("x = ", x)
print("mask = ", mask)

x = np.array([[-1, 2, 3], [2, -3, 2], [1, 5, -2]])

y = np.array([[False, False, False], [False, False, False], [False, True, False]])
mask = create_mask_from_window(x)

assert type(mask) == np.ndarray, "Output must be a np.ndarray"
assert mask.shape == x.shape, "Input and output shapes must match"
assert np.allclose(mask, y), "Wrong output. The True value must be at position (2, 1)"

print("\033[92m All tests passed.")


def distribute_value(dz, shape):
    n_H, n_W = shape

    average = dz / (n_H * n_W)

    a = np.ones(shape) * average

    return a


a = distribute_value(2, (2, 2))
print("distributed value =", a)

assert type(a) == np.ndarray, "Output must be a np.ndarray"
assert a.shape == (2, 2), f"Wrong shape {a.shape} != (2, 2)"
assert np.sum(a) == 2, "Values must sum to 2"

a = distribute_value(100, (10, 10))
assert type(a) == np.ndarray, "Output must be a np.ndarray"
assert a.shape == (10, 10), f"Wrong shape {a.shape} != (10, 10)"
assert np.sum(a) == 100, "Values must sum to 100"

print("\033[92m All tests passed.")


def pool_backward(dA, cache, mode="max"):
    A_prev, hparameters = cache

    stride = hparameters["stride"]
    f = hparameters["f"]

    m, n_H_prev, n_W_prev, n_C_prev = A_prev.shape
    m, n_H, n_W, n_C = dA.shape

    dA_prev = np.zeros_like(A_prev)

    for i in range(m):
        a_prev = A_prev[i]

        for h in range(n_H):
            for w in range(n_W):
                for c in range(n_C):
                    vert_start = h * stride
                    vert_end = vert_start + f
                    horiz_start = w * stride
                    horiz_end = horiz_start + f

                    if mode == "max":
                        a_prev_slice = a_prev[
                            vert_start:vert_end, horiz_start:horiz_end, c
                        ]

                        mask = a_prev_slice == np.max(a_prev_slice)

                        dA_prev[i, vert_start:vert_end, horiz_start:horiz_end, c] += (
                            mask * dA[i, h, w, c]
                        )

                    elif mode == "average":
                        da = dA[i, h, w, c]

                        shape = (f, f)

                        dA_prev[i, vert_start:vert_end, horiz_start:horiz_end, c] += (
                            distribute_value(da, shape)
                        )

    return dA_prev


np.random.seed(1)
A_prev = np.random.randn(5, 5, 3, 2)
hparameters = {"stride": 1, "f": 2}
A, cache = pool_forward(A_prev, hparameters)
print(A.shape)
print(cache[0].shape)
dA = np.random.randn(5, 4, 2, 2)

dA_prev1 = pool_backward(dA, cache, mode="max")
print("mode = max")
print("mean of dA = ", np.mean(dA))
print("dA_prev1[1,1] = ", dA_prev1[1, 1])
print()
dA_prev2 = pool_backward(dA, cache, mode="average")
print("mode = average")
print("mean of dA = ", np.mean(dA))
print("dA_prev2[1,1] = ", dA_prev2[1, 1])

assert type(dA_prev1) == np.ndarray, "Wrong type"
assert dA_prev1.shape == (5, 5, 3, 2), f"Wrong shape {dA_prev1.shape} != (5, 5, 3, 2)"
assert np.allclose(dA_prev1[1, 1], [[0, 0], [5.05844394, -1.68282702], [0, 0]]), (
    "Wrong values for mode max"
)
assert np.allclose(
    dA_prev2[1, 1],
    [[0.08485462, 0.2787552], [1.26461098, -0.25749373], [1.17975636, -0.53624893]],
), "Wrong values for mode average"
print("\033[92m All tests passed.")

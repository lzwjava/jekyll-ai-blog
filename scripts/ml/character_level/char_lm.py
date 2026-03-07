from __future__ import print_function
import numpy as np
from utils import *
import pprint
import copy
from tensorflow.keras.callbacks import LambdaCallback
from shakespeare_utils import *

data = open("dinos.txt", "r").read()
data = data.lower()
chars = list(set(data))
data_size, vocab_size = len(data), len(chars)
print(
    "There are %d total characters and %d unique characters in your data."
    % (data_size, vocab_size)
)

chars = sorted(chars)
print(chars)

char_to_ix = {ch: i for i, ch in enumerate(chars)}
ix_to_char = {i: ch for i, ch in enumerate(chars)}
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(ix_to_char)


def clip(gradients, maxValue):
    gradients = copy.deepcopy(gradients)

    dWaa, dWax, dWya, db, dby = (
        gradients["dWaa"],
        gradients["dWax"],
        gradients["dWya"],
        gradients["db"],
        gradients["dby"],
    )

    for gradient in [dWax, dWaa, dWya, db, dby]:
        np.clip(gradient, -maxValue, maxValue, out=gradient)

    gradients = {"dWaa": dWaa, "dWax": dWax, "dWya": dWya, "db": db, "dby": dby}

    return gradients


def clip_test(target, mValue):
    print(f"\nGradients for mValue={mValue}")
    np.random.seed(3)
    dWax = np.random.randn(5, 3) * 10
    dWaa = np.random.randn(5, 5) * 10
    dWya = np.random.randn(2, 5) * 10
    db = np.random.randn(5, 1) * 10
    dby = np.random.randn(2, 1) * 10
    gradients = {"dWax": dWax, "dWaa": dWaa, "dWya": dWya, "db": db, "dby": dby}

    gradients2 = target(gradients, mValue)
    print('gradients["dWaa"][1][2] =', gradients2["dWaa"][1][2])
    print('gradients["dWax"][3][1] =', gradients2["dWax"][3][1])
    print('gradients["dWya"][1][2] =', gradients2["dWya"][1][2])
    print('gradients["db"][4] =', gradients2["db"][4])
    print('gradients["dby"][1] =', gradients2["dby"][1])

    for grad in gradients2.keys():
        valuei = gradients[grad]
        valuef = gradients2[grad]
        mink = np.min(valuef)
        maxk = np.max(valuef)
        assert mink >= -abs(mValue), (
            f"Problem with {grad}. Set a_min to -mValue in the np.clip call"
        )
        assert maxk <= abs(mValue), (
            f"Problem with {grad}.Set a_max to mValue in the np.clip call"
        )
        index_not_clipped = np.logical_and(valuei <= mValue, valuei >= -mValue)
        assert np.all(valuei[index_not_clipped] == valuef[index_not_clipped]), (
            f" Problem with {grad}. Some values that should not have changed, changed during the clipping process."
        )

    print("\033[92mAll tests passed!\x1b[0m")


clip_test(clip, 10)
clip_test(clip, 5)


def sample(parameters, char_to_ix, seed):
    Waa, Wax, Wya, by, b = (
        parameters["Waa"],
        parameters["Wax"],
        parameters["Wya"],
        parameters["by"],
        parameters["b"],
    )
    vocab_size = by.shape[0]
    n_a = Waa.shape[1]

    x = np.zeros((vocab_size, 1))

    a_prev = np.zeros((n_a, 1))

    indices = []

    idx = -1

    counter = 0
    newline_character = char_to_ix["\n"]

    while idx != newline_character and counter != 50:
        a = np.tanh(np.dot(Wax, x) + np.dot(Waa, a_prev) + b)
        z = np.dot(Wya, a) + by
        y = softmax(z)

        np.random.seed(counter + seed)

        idx = np.random.choice(list(range(vocab_size)), p=y.ravel())

        indices.append(idx)

        x = np.zeros((vocab_size, 1))
        x[idx] = 1

        a_prev = a

        seed += 1
        counter += 1

    if counter == 50:
        indices.append(char_to_ix["\n"])

    return indices


def sample_test(target):
    np.random.seed(24)
    _, n_a = 20, 100
    Wax, Waa, Wya = (
        np.random.randn(n_a, vocab_size),
        np.random.randn(n_a, n_a),
        np.random.randn(vocab_size, n_a),
    )
    b, by = np.random.randn(n_a, 1), np.random.randn(vocab_size, 1)
    parameters = {"Wax": Wax, "Waa": Waa, "Wya": Wya, "b": b, "by": by}

    indices = target(parameters, char_to_ix, 0)
    print("Sampling:")
    print("list of sampled indices:\n", indices)
    print("list of sampled characters:\n", [ix_to_char[i] for i in indices])

    assert len(indices) < 52, "Indices length must be smaller than 52"
    assert indices[-1] == char_to_ix["\n"], "All samples must end with \\n"
    assert min(indices) >= 0 and max(indices) < len(char_to_ix), (
        f"Sampled indexes must be between 0 and len(char_to_ix)={len(char_to_ix)}"
    )
    assert np.allclose(indices[0:6], [23, 16, 26, 26, 24, 3]), "Wrong values"

    print("\033[92mAll tests passed!")


sample_test(sample)


def optimize(X, Y, a_prev, parameters, learning_rate=0.01):
    loss, cache = rnn_forward(X, Y, a_prev, parameters)

    gradients, a = rnn_backward(X, Y, parameters, cache)

    gradients = clip(gradients, 5)

    parameters = update_parameters(parameters, gradients, learning_rate)

    return loss, gradients, a[len(X) - 1]


def optimize_test(target):
    np.random.seed(1)
    vocab_size, n_a = 27, 100
    a_prev = np.random.randn(n_a, 1)
    Wax, Waa, Wya = (
        np.random.randn(n_a, vocab_size),
        np.random.randn(n_a, n_a),
        np.random.randn(vocab_size, n_a),
    )
    b, by = np.random.randn(n_a, 1), np.random.randn(vocab_size, 1)
    parameters = {"Wax": Wax, "Waa": Waa, "Wya": Wya, "b": b, "by": by}
    X = [12, 3, 5, 11, 22, 3]
    Y = [4, 14, 11, 22, 25, 26]
    old_parameters = copy.deepcopy(parameters)
    loss, gradients, a_last = target(X, Y, a_prev, parameters, learning_rate=0.01)
    print("Loss =", loss)
    print('gradients["dWaa"][1][2] =', gradients["dWaa"][1][2])
    print('np.argmax(gradients["dWax"]) =', np.argmax(gradients["dWax"]))
    print('gradients["dWya"][1][2] =', gradients["dWya"][1][2])
    print('gradients["db"][4] =', gradients["db"][4])
    print('gradients["dby"][1] =', gradients["dby"][1])
    print("a_last[4] =", a_last[4])

    assert np.isclose(loss, 126.5039757), (
        "Problems with the call of the rnn_forward function"
    )
    for grad in gradients.values():
        assert np.min(grad) >= -5, "Problems in the clip function call"
        assert np.max(grad) <= 5, "Problems in the clip function call"
    assert np.allclose(gradients["dWaa"][1, 2], 0.1947093), (
        "Unexpected gradients. Check the rnn_backward call"
    )
    assert np.allclose(gradients["dWya"][1, 2], -0.007773876), (
        "Unexpected gradients. Check the rnn_backward call"
    )
    assert not np.allclose(parameters["Wya"], old_parameters["Wya"]), (
        "parameters were not updated"
    )

    print("\033[92mAll tests passed!")


optimize_test(optimize)


def model(
    data_x,
    ix_to_char,
    char_to_ix,
    num_iterations=35000,
    n_a=50,
    dino_names=7,
    vocab_size=27,
    verbose=False,
):
    n_x, n_y = vocab_size, vocab_size

    parameters = initialize_parameters(n_a, n_x, n_y)

    loss = get_initial_loss(vocab_size, dino_names)

    examples = [x.strip() for x in data_x]

    np.random.seed(0)
    np.random.shuffle(examples)

    a_prev = np.zeros((n_a, 1))

    last_dino_name = "abc"

    for j in range(num_iterations):
        idx = np.random.randint(0, len(examples))

        single_example = examples[idx]
        single_example_chars = list(single_example)
        single_example_ix = [char_to_ix[c] for c in single_example_chars]
        X = [None] + single_example_ix

        ix_newline = [char_to_ix["\n"]]
        Y = X[1:] + ix_newline

        curr_loss, gradients, a_prev = optimize(parameters, X, Y, a_prev)

        if verbose and j in [0, len(examples) - 1, len(examples)]:
            print(
                "j = ",
                j,
                "idx = ",
                idx,
            )
        if verbose and j in [0]:
            print("single_example =", single_example)
            print("single_example_chars", single_example_chars)
            print("single_example_ix", single_example_ix)
            print(" X = ", X, "\n", "Y =       ", Y, "\n")

        loss = smooth(loss, curr_loss)

        if j % 2000 == 0:
            print("Iteration: %d, Loss: %f" % (j, loss) + "\n")

            seed = 0
            for name in range(dino_names):
                sampled_indices = sample(parameters, char_to_ix, seed)
                last_dino_name = get_sample(sampled_indices, ix_to_char)
                print(last_dino_name.replace("\n", ""))

                seed += 1

            print("\n")

    return parameters, last_dino_name


parameters, last_name = model(
    data.split("\n"), ix_to_char, char_to_ix, 22001, verbose=True
)

assert last_name == "Trodonosaurus\n", "Wrong expected output"
print("\033[92mAll tests passed!")

print_callback = LambdaCallback(on_epoch_end=on_epoch_end)

model.fit(x, y, batch_size=128, epochs=1, callbacks=[print_callback])

generate_output()

import pickle
import gzip
import numpy as np
import matplotlib
import matplotlib.pyplot as plt


def load_data():
    f = gzip.open("mnist.pkl.gz", "rb")
    training_data, validation_data, test_data = pickle.load(f, encoding="latin1")
    f.close()
    return (training_data, validation_data, test_data)


def print_shape(array):
    arr = np.array(array)
    print(arr.shape)


def draw(some_digit):
    some_digit_image = some_digit.reshape(28, 28)

    plt.imshow(some_digit_image, cmap=matplotlib.cm.binary, interpolation="nearest")
    plt.axis("off")
    plt.show()


def load_data_wrapper():
    tr_d, va_d, te_d = load_data()

    print(tr_d)
    print(type(tr_d))

    print(type(tr_d[0]))

    print(len(tr_d[0]))

    print(len(tr_d[1]))
    print(tr_d[1][0])

    print(va_d)
    print(len(va_d[0]))

    # draw(tr_d[0][0])

    training_inputs = [np.reshape(x, (784, 1)) for x in tr_d[0]]
    training_results = [vectorized_result(y) for y in tr_d[1]]

    print_shape(training_inputs)
    print_shape(training_results)

    training_data = zip(training_inputs, training_results)

    # print_shape(training_data[0])

    validation_inputs = [np.reshape(x, (784, 1)) for x in va_d[0]]
    validation_data = zip(validation_inputs, va_d[1])

    test_inputs = [np.reshape(x, (784, 1)) for x in te_d[0]]
    test_data = zip(test_inputs, te_d[1])
    return (training_data, validation_data, test_data)


def vectorized_result(j):
    e = np.zeros((10, 1))
    e[j] = 1.0
    return e

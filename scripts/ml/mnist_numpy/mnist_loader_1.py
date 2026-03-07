import pickle
import gzip

import numpy as np


def load_data():
    f = gzip.open("mnist.pkl.gz", "rb")
    training_data, validation_data, test_data = pickle.load(f, encoding="latin1")
    f.close()
    return (training_data, validation_data, test_data)


def print_shape(array):
    arr = np.array(array)
    print(arr.shape)


def load_data_wrapper():
    tr_d, va_d, te_d = load_data()
    print_shape(tr_d[0])
    print_shape(tr_d[1])

    training_inputs = [np.reshape(x, (784, 1)) for x in tr_d[0]]
    print(len(training_inputs))

    training_results = [vectorized_result(y) for y in tr_d[1]]

    print(training_results[0])
    print_shape(training_results)
    print(tr_d[1])
    print("shape:", end="")
    print_shape(tr_d[1])
    print(tr_d[1][0])
    print("vectorized_result", vectorized_result(tr_d[1][0]))

    training_data = zip(training_inputs, training_results)
    validation_inputs = [np.reshape(x, (784, 1)) for x in va_d[0]]
    validation_data = zip(validation_inputs, va_d[1])
    test_inputs = [np.reshape(x, (784, 1)) for x in te_d[0]]
    test_data = zip(test_inputs, te_d[1])
    return (training_data, validation_data, test_data)


def vectorized_result(j):
    e = np.zeros((10, 1))
    e[j] = 1.0
    return e


td, vd, td1 = load_data_wrapper()
print(td)
print(vd)
print(td1)

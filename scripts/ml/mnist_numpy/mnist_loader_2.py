# Found that I forgot a lot in the second day, so let's do it from the beginning

import pickle
import gzip

import numpy as np

import matplotlib.pyplot as plt


def load_data():
    f = gzip.open("mnist.pkl.gz", "rb")
    training_data, validation_data, test_data = pickle.load(f, encoding="latin1")
    f.close()
    return (training_data, validation_data, test_data)


def print_shape(array):
    arr = np.array(array)
    print(arr.shape)


td, vd, td1 = load_data()
print(td)
print(vd)
print(td1)

some_digit = td[0][1]
some_digit_image = some_digit.reshape(28, 28)

# some_digit_image = some_digit

print(some_digit)
print_shape(some_digit_image)

plt.imshow(some_digit_image)
plt.show()

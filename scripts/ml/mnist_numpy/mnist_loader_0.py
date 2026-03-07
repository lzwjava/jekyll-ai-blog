import pickle
import gzip


import matplotlib
import matplotlib.pyplot as plt


def load_data():
    f = gzip.open("mnist.pkl.gz", "rb")
    training_data, validation_data, test_data = pickle.load(f, encoding="latin1")
    f.close()
    return (training_data, validation_data, test_data)


td, vd, td1 = load_data()

some_digit = td[0][1]
some_digit_image = some_digit.reshape(28, 28)

plt.imshow(some_digit_image, cmap=matplotlib.cm.binary, interpolation="nearest")
plt.axis("off")
plt.show()

print(td)
print(len(td))
print(len(td[0]))
print(len(td[0][0]))

print(vd)
print(td1)

import numpy as np
import copy
import matplotlib.pyplot as plt
from PIL import Image
from lr_utils import load_dataset
from public_tests import *

train_set_x_orig, train_set_y, test_set_x_orig, test_set_y, classes = load_dataset()

index = 25
plt.imshow(train_set_x_orig[index])
print(
    "y = "
    + str(train_set_y[:, index])
    + ", it's a '"
    + classes[np.squeeze(train_set_y[:, index])].decode("utf-8")
    + "' picture."
)

m_train = train_set_x_orig.shape[0]
m_test = test_set_x_orig.shape[0]
num_px = 64

print("Number of training examples: m_train = " + str(m_train))
print("Number of testing examples: m_test = " + str(m_test))
print("Height/Width of each image: num_px = " + str(num_px))
print("Each image is of size: (" + str(num_px) + ", " + str(num_px) + ", 3)")
print("train_set_x shape: " + str(train_set_x_orig.shape))
print("train_set_y shape: " + str(train_set_y.shape))
print("test_set_x shape: " + str(test_set_x_orig.shape))
print("test_set_y shape: " + str(test_set_y.shape))

train_set_x_flatten = train_set_x_orig.reshape(m_train, -1).T

test_set_x_flatten = test_set_x_orig.reshape(m_test, -1).T

assert np.alltrue(
    train_set_x_flatten[0:10, 1] == [196, 192, 190, 193, 186, 182, 188, 179, 174, 213]
), "Wrong solution. Use (X.shape[0], -1).T."
assert np.alltrue(
    test_set_x_flatten[0:10, 1] == [115, 110, 111, 137, 129, 129, 155, 146, 145, 159]
), "Wrong solution. Use (X.shape[0], -1).T."

print("train_set_x_flatten shape: " + str(train_set_x_flatten.shape))
print("train_set_y shape: " + str(train_set_y.shape))
print("test_set_x_flatten shape: " + str(test_set_x_flatten.shape))
print("test_set_y shape: " + str(test_set_y.shape))

train_set_x = train_set_x_flatten / 255.0
test_set_x = test_set_x_flatten / 255.0


def sigmoid(z):
    s = 1 / (1 + np.exp(-z))

    return s


print("sigmoid([0, 2]) = " + str(sigmoid(np.array([0, 2]))))

sigmoid_test(sigmoid)

x = np.array([0.5, 0, 2.0])
output = sigmoid(x)
print(output)


def initialize_with_zeros(dim):
    w = np.zeros((dim, 1))
    b = 0.0

    return w, b


dim = 2
w, b = initialize_with_zeros(dim)

assert type(b) == float
print("w = " + str(w))
print("b = " + str(b))

initialize_with_zeros_test_1(initialize_with_zeros)
initialize_with_zeros_test_2(initialize_with_zeros)


def propagate(w, b, X, Y):
    m = X.shape[1]

    A = sigmoid(np.dot(w.T, X) + b)

    cost = -1 / m * np.sum(Y * np.log(A) + (1 - Y) * np.log(1 - A))

    cost = np.squeeze(np.array(cost))

    dw = 1 / m * np.dot(X, (A - Y).T)
    db = 1 / m * np.sum(A - Y)

    grads = {"dw": dw, "db": db}

    return grads, cost


w = np.array([[1.0], [2]])
b = 1.5
X = np.array([[1.0, -2.0, -1.0], [3.0, 0.5, -3.2]])
Y = np.array([[1, 1, 0]])
grads, cost = propagate(w, b, X, Y)

assert type(grads["dw"]) == np.ndarray
assert grads["dw"].shape == (2, 1)
assert type(grads["db"]) == np.float64

print("dw = " + str(grads["dw"]))
print("db = " + str(grads["db"]))
print("cost = " + str(cost))

propagate_test(propagate)


def optimize(w, b, X, Y, num_iterations=100, learning_rate=0.009, print_cost=False):
    w = copy.deepcopy(w)
    b = copy.deepcopy(b)

    costs = []

    for i in range(num_iterations):
        grads, cost = propagate(w, b, X, Y)

        dw = grads["dw"]
        db = grads["db"]

        w = w - learning_rate * dw
        b = b - learning_rate * db

        if i % 100 == 0:
            costs.append(cost)

            if print_cost:
                print("Cost after iteration %i: %f" % (i, cost))

    params = {"w": w, "b": b}

    grads = {"dw": dw, "db": db}

    return params, grads, costs


params, grads, costs = optimize(
    w, b, X, Y, num_iterations=100, learning_rate=0.009, print_cost=False
)

print("w = " + str(params["w"]))
print("b = " + str(params["b"]))
print("dw = " + str(grads["dw"]))
print("db = " + str(grads["db"]))
print("Costs = " + str(costs))

optimize_test(optimize)


def predict(w, b, X):
    """
    Predict whether the label is 0 or 1 using learned logistic regression parameters (w, b)

    Arguments:
    w -- weights, a numpy array of size (num_px * num_px * 3, 1)
    b -- bias, a scalar
    X -- data of size (num_px * num_px * 3, number of examples)

    Returns:
    Y_prediction -- a numpy array (vector) containing all predictions (0/1) for the examples in X
    """

    m = X.shape[1]
    Y_prediction = np.zeros((1, m))
    w = w.reshape(X.shape[0], 1)

    A = sigmoid(np.dot(w.T, X) + b)

    for i in range(A.shape[1]):
        if A[0, i] > 0.5:
            Y_prediction[0, i] = 1
        else:
            Y_prediction[0, i] = 0

    return Y_prediction


w = np.array([[0.1124579], [0.23106775]])
b = -0.3
X = np.array([[1.0, -1.1, -3.2], [1.2, 2.0, 0.1]])
print("predictions = " + str(predict(w, b, X)))

predict_test(predict)


def model(
    X_train,
    Y_train,
    X_test,
    Y_test,
    num_iterations=2000,
    learning_rate=0.5,
    print_cost=False,
):
    w, b = initialize_with_zeros(X_train.shape[0])

    params, grads, costs = optimize(
        w, b, X_train, Y_train, num_iterations, learning_rate, print_cost
    )

    w = params["w"]
    b = params["b"]

    Y_prediction_test = predict(w, b, X_test)
    Y_prediction_train = predict(w, b, X_train)

    if print_cost:
        print(
            "train accuracy: {} %".format(
                100 - np.mean(np.abs(Y_prediction_train - Y_train)) * 100
            )
        )
        print(
            "test accuracy: {} %".format(
                100 - np.mean(np.abs(Y_prediction_test - Y_test)) * 100
            )
        )

    d = {
        "costs": costs,
        "Y_prediction_test": Y_prediction_test,
        "Y_prediction_train": Y_prediction_train,
        "w": w,
        "b": b,
        "learning_rate": learning_rate,
        "num_iterations": num_iterations,
    }

    return d


from public_tests import *

model_test(model)

logistic_regression_model = model(
    train_set_x,
    train_set_y,
    test_set_x,
    test_set_y,
    num_iterations=2000,
    learning_rate=0.005,
    print_cost=True,
)

index = 1
plt.imshow(test_set_x[:, index].reshape((num_px, num_px, 3)))
print(
    "y = "
    + str(test_set_y[0, index])
    + ', you predicted that it is a "'
    + classes[int(logistic_regression_model["Y_prediction_test"][0, index])].decode(
        "utf-8"
    )
    + '" picture.'
)

costs = np.squeeze(logistic_regression_model["costs"])
plt.plot(costs)
plt.ylabel("cost")
plt.xlabel("iterations (per hundreds)")
plt.title("Learning rate =" + str(logistic_regression_model["learning_rate"]))
plt.show()

learning_rates = [0.01, 0.001, 0.0001]
models = {}

for lr in learning_rates:
    print("Training a model with learning rate: " + str(lr))
    models[str(lr)] = model(
        train_set_x,
        train_set_y,
        test_set_x,
        test_set_y,
        num_iterations=1500,
        learning_rate=lr,
        print_cost=False,
    )
    print("\n" + "-------------------------------------------------------" + "\n")

for lr in learning_rates:
    plt.plot(
        np.squeeze(models[str(lr)]["costs"]),
        label=str(models[str(lr)]["learning_rate"]),
    )

plt.ylabel("cost")
plt.xlabel("iterations (hundreds)")

legend = plt.legend(loc="upper center", shadow=True)
frame = legend.get_frame()
frame.set_facecolor("0.90")
plt.show()

my_image = "my_image.jpg"

fname = "images/" + my_image
image = np.array(Image.open(fname).resize((num_px, num_px)))
plt.imshow(image)
image = image / 255.0
image = image.reshape((1, num_px * num_px * 3)).T
my_predicted_image = predict(
    logistic_regression_model["w"], logistic_regression_model["b"], image
)

print(
    "y = "
    + str(np.squeeze(my_predicted_image))
    + ', your algorithm predicts a "'
    + classes[int(np.squeeze(my_predicted_image)),].decode("utf-8")
    + '" picture.'
)

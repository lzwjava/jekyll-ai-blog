from PIL import Image

from dnn_app_utils_v3 import *
from public_tests import *

plt.rcParams["figure.figsize"] = (5.0, 4.0)
plt.rcParams["image.interpolation"] = "nearest"
plt.rcParams["image.cmap"] = "gray"

np.random.seed(1)

train_x_orig, train_y, test_x_orig, test_y, classes = load_data()

index = 10
plt.imshow(train_x_orig[index])
print(
    "y = "
    + str(train_y[0, index])
    + ". It's a "
    + classes[train_y[0, index]].decode("utf-8")
    + " picture."
)

m_train = train_x_orig.shape[0]
num_px = train_x_orig.shape[1]
m_test = test_x_orig.shape[0]

print("Number of training examples: " + str(m_train))
print("Number of testing examples: " + str(m_test))
print("Each image is of size: (" + str(num_px) + ", " + str(num_px) + ", 3)")
print("train_x_orig shape: " + str(train_x_orig.shape))
print("train_y shape: " + str(train_y.shape))
print("test_x_orig shape: " + str(test_x_orig.shape))
print("test_y shape: " + str(test_y.shape))

train_x_flatten = train_x_orig.reshape(train_x_orig.shape[0], -1).T
test_x_flatten = test_x_orig.reshape(test_x_orig.shape[0], -1).T

train_x = train_x_flatten / 255.0
test_x = test_x_flatten / 255.0

print("train_x's shape: " + str(train_x.shape))
print("test_x's shape: " + str(test_x.shape))

n_x = 12288
n_h = 7
n_y = 1
layers_dims = (n_x, n_h, n_y)
learning_rate = 0.0075


def two_layer_model(
    X, Y, layers_dims, learning_rate=0.0075, num_iterations=3000, print_cost=False
):
    np.random.seed(1)
    costs = []
    m = X.shape[1]
    n_x, n_h, n_y = layers_dims

    parameters = initialize_parameters(n_x, n_h, n_y)

    for i in range(0, num_iterations):
        A1, cache1 = linear_activation_forward(
            X, parameters["W1"], parameters["b1"], "relu"
        )
        A2, cache2 = linear_activation_forward(
            A1, parameters["W2"], parameters["b2"], "sigmoid"
        )

        cost = compute_cost(A2, Y)

        dA2 = -(np.divide(Y, A2) - np.divide(1 - Y, 1 - A2))

        dA1, dW2, db2 = linear_activation_backward(dA2, cache2, "sigmoid")
        dA0, dW1, db1 = linear_activation_backward(dA1, cache1, "relu")

        grads = {"dW1": dW1, "db1": db1, "dW2": dW2, "db2": db2}

        parameters = update_parameters(parameters, grads, learning_rate)

        W1 = parameters["W1"]
        b1 = parameters["b1"]
        W2 = parameters["W2"]
        b2 = parameters["b2"]

        if print_cost and i % 100 == 0:
            print("Cost after iteration {}: {}".format(i, np.squeeze(cost)))
        if i % 100 == 0:
            costs.append(cost)

    return parameters, costs


def plot_costs(costs, learning_rate=0.0075):
    plt.plot(np.squeeze(costs))
    plt.ylabel("cost")
    plt.xlabel("iterations (per hundreds)")
    plt.title("Learning rate =" + str(learning_rate))
    plt.show()


parameters, costs = two_layer_model(
    train_x, train_y, layers_dims=(n_x, n_h, n_y), num_iterations=2, print_cost=False
)

print("Cost after first iteration: " + str(costs[0]))

two_layer_model_test(two_layer_model)

parameters, costs = two_layer_model(
    train_x, train_y, layers_dims=(n_x, n_h, n_y), num_iterations=2500, print_cost=True
)
plot_costs(costs, learning_rate)

predictions_train = predict(train_x, train_y, parameters)

predictions_test = predict(test_x, test_y, parameters)

layers_dims = [12288, 20, 7, 5, 1]


def L_layer_model(
    X, Y, layers_dims, learning_rate=0.0075, num_iterations=3000, print_cost=False
):
    np.random.seed(1)
    costs = []

    parameters = initialize_parameters_deep(layers_dims)

    for i in range(0, num_iterations):
        AL, caches = L_model_forward(X, parameters)

        cost = compute_cost(AL, Y)

        grads = L_model_backward(AL, Y, caches)

        parameters = update_parameters(parameters, grads, learning_rate)

        if print_cost and i % 100 == 0 or i == num_iterations - 1:
            print("Cost after iteration {}: {}".format(i, np.squeeze(cost)))
        if i % 100 == 0 or i == num_iterations:
            costs.append(cost)

    return parameters, costs


parameters, costs = L_layer_model(
    train_x, train_y, layers_dims, num_iterations=1, print_cost=False
)

print("Cost after first iteration: " + str(costs[0]))

L_layer_model_test(L_layer_model)

parameters, costs = L_layer_model(
    train_x, train_y, layers_dims, num_iterations=2500, print_cost=True
)

pred_train = predict(train_x, train_y, parameters)

pred_test = predict(test_x, test_y, parameters)

print_mislabeled_images(classes, test_x, test_y, pred_test)

my_image = "my_image.jpg"
my_label_y = [1]

fname = "images/" + my_image
image = np.array(Image.open(fname).resize((num_px, num_px)))
plt.imshow(image)
image = image / 255.0
image = image.reshape((1, num_px * num_px * 3)).T

my_predicted_image = predict(image, my_label_y, parameters)

print(
    "y = "
    + str(np.squeeze(my_predicted_image))
    + ', your L-layer model predicts a "'
    + classes[int(np.squeeze(my_predicted_image)),].decode("utf-8")
    + '" picture.'
)

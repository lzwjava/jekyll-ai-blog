import numpy as np
import matplotlib.pyplot as plt
from utils import *

X_train, X_val, y_val = load_data()

print("The first 5 elements of X_train are:\n", X_train[:5])

print("The first 5 elements of X_val are\n", X_val[:5])

print("The first 5 elements of y_val are\n", y_val[:5])

print("The shape of X_train is:", X_train.shape)
print("The shape of X_val is:", X_val.shape)
print("The shape of y_val is: ", y_val.shape)

plt.scatter(X_train[:, 0], X_train[:, 1], marker="x", c="b")

plt.title("The first dataset")

plt.ylabel("Throughput (mb/s)")

plt.xlabel("Latency (ms)")

plt.axis([0, 30, 0, 30])
plt.show()


def estimate_gaussian(X):
    m, n = X.shape

    mu = 1 / m * np.sum(X, axis=0)
    var = 1 / m * np.sum((X - mu) ** 2, axis=0)

    return mu, var


mu, var = estimate_gaussian(X_train)

print("Mean of each feature:", mu)
print("Variance of each feature:", var)

from public_tests import *

estimate_gaussian_test(estimate_gaussian)

p = multivariate_gaussian(X_train, mu, var)

visualize_fit(X_train, mu, var)


def select_threshold(y_val, p_val):
    best_epsilon = 0
    best_F1 = 0
    F1 = 0

    step_size = (max(p_val) - min(p_val)) / 1000

    for epsilon in np.arange(min(p_val), max(p_val), step_size):
        predictions = p_val < epsilon

        tp = np.sum((predictions == 1) & (y_val == 1))
        fp = sum((predictions == 1) & (y_val == 0))
        fn = np.sum((predictions == 0) & (y_val == 1))

        prec = tp / (tp + fp)
        rec = tp / (tp + fn)

        F1 = 2 * prec * rec / (prec + rec)

        if F1 > best_F1:
            best_F1 = F1
            best_epsilon = epsilon

    return best_epsilon, best_F1


p_val = multivariate_gaussian(X_val, mu, var)
epsilon, F1 = select_threshold(y_val, p_val)

print("Best epsilon found using cross-validation: %e" % epsilon)
print("Best F1 on Cross Validation Set: %f" % F1)

select_threshold_test(select_threshold)

outliers = p < epsilon

visualize_fit(X_train, mu, var)

plt.plot(
    X_train[outliers, 0],
    X_train[outliers, 1],
    "ro",
    markersize=10,
    markerfacecolor="none",
    markeredgewidth=2,
)

X_train_high, X_val_high, y_val_high = load_data_multi()

print("The shape of X_train_high is:", X_train_high.shape)
print("The shape of X_val_high is:", X_val_high.shape)
print("The shape of y_val_high is: ", y_val_high.shape)

mu_high, var_high = estimate_gaussian(X_train_high)

p_high = multivariate_gaussian(X_train_high, mu_high, var_high)

p_val_high = multivariate_gaussian(X_val_high, mu_high, var_high)

epsilon_high, F1_high = select_threshold(y_val_high, p_val_high)

print("Best epsilon found using cross-validation: %e" % epsilon_high)
print("Best F1 on Cross Validation Set:  %f" % F1_high)

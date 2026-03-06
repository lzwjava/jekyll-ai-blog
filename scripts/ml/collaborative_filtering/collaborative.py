import tensorflow as tf
from tensorflow import keras

from recsys_utils import *

X, W, b, num_movies, num_features, num_users = load_precalc_params_small()
Y, R = load_ratings_small()

print("Y", Y.shape, "R", R.shape)
print("X", X.shape)
print("W", W.shape)
print("b", b.shape)
print("num_features", num_features)
print("num_movies", num_movies)
print("num_users", num_users)

tsmean = np.mean(Y[0, R[0, :].astype(bool)])
print(f"Average rating for movie 1 : {tsmean:0.3f} / 5")


def cofi_cost_func(X, W, b, Y, R, lambda_):
    nm, nu = Y.shape
    J = 0
    for j in range(nu):
        w = W[j, :]
        b_j = b[0, j]
        for i in range(nm):
            x = X[i, :]
            y = Y[i, j]
            r = R[i, j]
            J += np.square(r * (np.dot(w, x) + b_j - y))
    J += lambda_ * (np.sum(np.square(W)) + np.sum(np.square(X)))
    J = J / 2
    return J


num_users_r = 4
num_movies_r = 5
num_features_r = 3

X_r = X[:num_movies_r, :num_features_r]
W_r = W[:num_users_r, :num_features_r]
b_r = b[0, :num_users_r].reshape(1, -1)
Y_r = Y[:num_movies_r, :num_users_r]
R_r = R[:num_movies_r, :num_users_r]

J = cofi_cost_func(X_r, W_r, b_r, Y_r, R_r, 0)
print(f"Cost: {J:0.2f}")

J = cofi_cost_func(X_r, W_r, b_r, Y_r, R_r, 1.5)
print(f"Cost (with regularization): {J:0.2f}")

from public_tests import *

test_cofi_cost_func(cofi_cost_func)


def cofi_cost_func_v(X, W, b, Y, R, lambda_):
    j = (tf.linalg.matmul(X, tf.transpose(W)) + b - Y) * R
    J = 0.5 * tf.reduce_sum(j**2) + (lambda_ / 2) * (
        tf.reduce_sum(X**2) + tf.reduce_sum(W**2)
    )
    return J


J = cofi_cost_func_v(X_r, W_r, b_r, Y_r, R_r, 0)
print(f"Cost: {J:0.2f}")

J = cofi_cost_func_v(X_r, W_r, b_r, Y_r, R_r, 1.5)
print(f"Cost (with regularization): {J:0.2f}")

movieList, movieList_df = load_Movie_List_pd()

my_ratings = np.zeros(num_movies)

my_ratings[2700] = 5

my_ratings[2609] = 2

my_ratings[929] = 5
my_ratings[246] = 5
my_ratings[2716] = 3
my_ratings[1150] = 5
my_ratings[382] = 2
my_ratings[366] = 5
my_ratings[622] = 5
my_ratings[988] = 3
my_ratings[2925] = 1
my_ratings[2937] = 1
my_ratings[793] = 5
my_rated = [i for i in range(len(my_ratings)) if my_ratings[i] > 0]

print("\nNew user ratings:\n")
for i in range(len(my_ratings)):
    if my_ratings[i] > 0:
        print(f"Rated {my_ratings[i]} for  {movieList_df.loc[i, 'title']}")

Y, R = load_ratings_small()

Y = np.c_[my_ratings, Y]

R = np.c_[(my_ratings != 0).astype(int), R]

Ynorm, Ymean = normalizeRatings(Y, R)

num_movies, num_users = Y.shape
num_features = 100

tf.random.set_seed(1234)
W = tf.Variable(tf.random.normal((num_users, num_features), dtype=tf.float64), name="W")
X = tf.Variable(
    tf.random.normal((num_movies, num_features), dtype=tf.float64), name="X"
)
b = tf.Variable(tf.random.normal((1, num_users), dtype=tf.float64), name="b")

optimizer = keras.optimizers.Adam(learning_rate=1e-1)

iterations = 200
lambda_ = 1
for iter in range(iterations):
    with tf.GradientTape() as tape:
        cost_value = cofi_cost_func_v(X, W, b, Ynorm, R, lambda_)

    grads = tape.gradient(cost_value, [X, W, b])

    optimizer.apply_gradients(zip(grads, [X, W, b]))

    if iter % 20 == 0:
        print(f"Training loss at iteration {iter}: {cost_value:0.1f}")

p = np.matmul(X.numpy(), np.transpose(W.numpy())) + b.numpy()

pm = p + Ymean

my_predictions = pm[:, 0]

ix = tf.argsort(my_predictions, direction="DESCENDING")

for i in range(17):
    j = ix[i]
    if j not in my_rated:
        print(f"Predicting rating {my_predictions[j]:0.2f} for movie {movieList[j]}")

print("\n\nOriginal vs Predicted ratings:\n")
for i in range(len(my_ratings)):
    if my_ratings[i] > 0:
        print(
            f"Original {my_ratings[i]}, Predicted {my_predictions[i]:0.2f} for {movieList[i]}"
        )

filter = movieList_df["number of ratings"] > 20
movieList_df["pred"] = my_predictions
movieList_df = movieList_df.reindex(
    columns=["pred", "mean rating", "number of ratings", "title"]
)
movieList_df.loc[ix[:300]].loc[filter].sort_values("mean rating", ascending=False)

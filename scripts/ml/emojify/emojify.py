import numpy as np
from emo_utils import *
from test_utils import *

X_train, Y_train = read_csv("data/train_emoji.csv")
X_test, Y_test = read_csv("data/tesss.csv")

maxLen = len(max(X_train, key=lambda x: len(x.split())).split())

for idx in range(10):
    print(X_train[idx], label_to_emoji(Y_train[idx]))

Y_oh_train = convert_to_one_hot(Y_train, C=5)
Y_oh_test = convert_to_one_hot(Y_test, C=5)

idx = 50
print(
    f"Sentence '{X_train[idx]}' has label index {Y_train[idx]}, which is emoji {label_to_emoji(Y_train[idx])}",
)
print(f"Label index {Y_train[idx]} in one-hot encoding format is {Y_oh_train[idx]}")

word_to_index, index_to_word, word_to_vec_map = read_glove_vecs("data/glove.6B.50d.txt")

word = "cucumber"
idx = 289846
print("the index of", word, "in the vocabulary is", word_to_index[word])
print("the", str(idx) + "th word in the vocabulary is", index_to_word[idx])


def sentence_to_avg(sentence, word_to_vec_map):
    any_word = list(word_to_vec_map.keys())[0]

    words = sentence.lower().split(" ")

    avg = np.zeros(word_to_vec_map[any_word].shape)

    count = 0

    for w in words:
        if w in word_to_vec_map.keys():
            avg += word_to_vec_map[w]

            count += 1

    if count > 0:
        avg = avg / count

    return avg


avg = sentence_to_avg("Morrocan couscous is my favorite dish", word_to_vec_map)
print("avg = \n", avg)


def sentence_to_avg_test(target):
    word_to_vec_map = {
        "a": [3, 3],
        "synonym_of_a": [3, 3],
        "a_nw": [2, 4],
        "a_s": [3, 2],
        "c": [-2, 1],
        "c_n": [-2, 2],
        "c_ne": [-1, 2],
        "c_e": [-1, 1],
        "c_se": [-1, 0],
        "c_s": [-2, 0],
        "c_sw": [-3, 0],
        "c_w": [-3, 1],
        "c_nw": [-3, 2],
    }

    for key in word_to_vec_map.keys():
        word_to_vec_map[key] = np.array(word_to_vec_map[key])

    avg = target("a a_nw c_w a_s", word_to_vec_map)
    assert tuple(avg.shape) == tuple(word_to_vec_map["a"].shape), (
        "Check the shape of your avg array"
    )
    assert np.allclose(avg, [1.25, 2.5]), "Check that you are finding the 4 words"
    avg = target("love a a_nw c_w a_s", word_to_vec_map)
    assert np.allclose(avg, [1.25, 2.5]), "Divide by count, not len(words)"
    avg = target("love", word_to_vec_map)
    assert np.array_equal(avg, [0, 0]), (
        "Average of no words must give an array of zeros"
    )
    avg = target("c_se foo a a_nw c_w a_s deeplearning c_nw", word_to_vec_map)
    assert np.allclose(avg, [0.1666667, 2.0]), "Debug the last example"

    print("\033[92mAll tests passed!")


sentence_to_avg_test(sentence_to_avg)


def model(X, Y, word_to_vec_map, learning_rate=0.01, num_iterations=100):
    any_word = list(word_to_vec_map.keys())[0]

    m = Y.shape[0]
    n_y = len(np.unique(Y))
    n_h = word_to_vec_map[any_word].shape[0]

    W = np.random.randn(n_y, n_h) / np.sqrt(n_h)
    b = np.zeros((n_y,))

    Y_oh = convert_to_one_hot(Y, C=n_y)

    for t in range(num_iterations):
        cost = 0
        dW = 0
        db = 0

        for i in range(m):
            avg = sentence_to_avg(X[i], word_to_vec_map)

            z = np.dot(W, avg) + b
            a = softmax(z)

            cost += -np.sum(np.dot(Y_oh, np.log(a)))

            dz = a - Y_oh[i]
            dW += np.dot(dz.reshape(n_y, 1), avg.reshape(1, n_h))
            db += dz

            W = W - learning_rate * dW
            b = b - learning_rate * db

        assert type(cost) == np.float64, "Incorrect implementation of cost"
        assert cost.shape == (), "Incorrect implementation of cost"

        if t % 100 == 0:
            print("Epoch: " + str(t) + " --- cost = " + str(cost))
            pred = predict(X, Y, W, b, word_to_vec_map)

    return pred, W, b


def model_test(target):
    word_to_vec_map = {
        "a": [3, 3],
        "synonym_of_a": [3, 3],
        "a_nw": [2, 4],
        "a_s": [3, 2],
        "a_n": [3, 4],
        "c": [-2, 1],
        "c_n": [-2, 2],
        "c_ne": [-1, 2],
        "c_e": [-1, 1],
        "c_se": [-1, 0],
        "c_s": [-2, 0],
        "c_sw": [-3, 0],
        "c_w": [-3, 1],
        "c_nw": [-3, 2],
    }

    for key in word_to_vec_map.keys():
        word_to_vec_map[key] = np.array(word_to_vec_map[key])

    X = np.asarray(
        [
            "a a_s synonym_of_a a_n c_sw",
            "a a_s a_n c_sw",
            "a_s  a a_n",
            "synonym_of_a a a_s a_n c_sw",
            " a_s a_n",
            " a a_s a_n c ",
            " a_n  a c c c_e",
            "c c_nw c_n c c_ne",
            "c_e c c_se c_s",
            "c_nw c a_s c_e c_e",
            "c_e a_nw c_sw",
            "c_sw c c_ne c_ne",
        ]
    )

    Y = np.asarray([0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1])

    np.random.seed(10)
    pred, W, b = model(X, Y, word_to_vec_map, 0.0025, 110)

    assert W.shape == (2, 2), "W must be of shape 2 x 2"
    assert np.allclose(pred.transpose(), Y), "Model must give a perfect accuracy"
    assert np.allclose(b[0], -1 * b[1]), "b should be symmetric in this example"

    print("\033[92mAll tests passed!")


model_test(model)

np.random.seed(1)
pred, W, b = model(X_train, Y_train, word_to_vec_map)

print("Training set:")
pred_train = predict(X_train, Y_train, W, b, word_to_vec_map)
print("Test set:")
pred_test = predict(X_test, Y_test, W, b, word_to_vec_map)

X_my_sentences = np.array(
    [
        "i treasure you",
        "i love you",
        "funny lol",
        "lets play with a ball",
        "food is ready",
        "today is not good",
    ]
)
Y_my_labels = np.array([[0], [0], [2], [1], [4], [3]])

pred = predict(X_my_sentences, Y_my_labels, W, b, word_to_vec_map)
print_predictions(X_my_sentences, pred)

print(Y_test.shape)
print(
    "           "
    + label_to_emoji(0)
    + "    "
    + label_to_emoji(1)
    + "    "
    + label_to_emoji(2)
    + "    "
    + label_to_emoji(3)
    + "   "
    + label_to_emoji(4)
)
print(
    pd.crosstab(
        Y_test,
        pred_test.reshape(
            56,
        ),
        rownames=["Actual"],
        colnames=["Predicted"],
        margins=True,
    )
)
plot_confusion_matrix(Y_test, pred_test)

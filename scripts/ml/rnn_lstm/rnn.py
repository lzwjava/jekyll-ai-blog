import matplotlib.pyplot as plt

from data import *
from utils import *

np.random.seed(42)


def init_orthogonal(param):
    if param.ndim < 2:
        raise ValueError("Only parameters with 2 or more dimensions are supported.")

    rows, cols = param.shape

    new_param = np.random.randn(rows, cols)

    if rows < cols:
        new_param = new_param.T

    q, r = np.linalg.qr(new_param)

    d = np.diag(r, 0)
    ph = np.sign(d)
    q *= ph

    if rows < cols:
        q = q.T

    new_param = q

    return new_param


def init_rnn(hidden_size, vocab_size):
    U = np.zeros((hidden_size, vocab_size))

    V = np.zeros((hidden_size, hidden_size))

    W = np.zeros((vocab_size, hidden_size))

    b_hidden = np.zeros((hidden_size, 1))

    b_out = np.zeros((vocab_size, 1))

    U = init_orthogonal(U)
    V = init_orthogonal(V)
    W = init_orthogonal(W)

    return U, V, W, b_hidden, b_out


params = init_rnn(hidden_size=hidden_size, vocab_size=vocab_size)


def sigmoid(x, derivative=False):
    x_safe = x + 1e-12
    f = 1 / (1 + np.exp(-x_safe))

    if derivative:
        return f * (1 - f)
    else:
        return f


def tanh(x, derivative=False):
    x_safe = x + 1e-12
    f = (np.exp(x_safe) - np.exp(-x_safe)) / (np.exp(x_safe) + np.exp(-x_safe))

    if derivative:
        return 1 - f**2
    else:
        return f


def softmax(x, derivative=False):
    x_safe = x + 1e-12
    f = np.exp(x_safe) / np.sum(np.exp(x_safe))

    if derivative:
        pass
    else:
        return f


def forward_pass(inputs, hidden_state, params):
    U, V, W, b_hidden, b_out = params

    outputs, hidden_states = [], []

    for t in range(len(inputs)):
        hidden_state = tanh(np.dot(U, inputs[t]) + np.dot(V, hidden_state) + b_hidden)

        out = softmax(np.dot(W, hidden_state) + b_out)

        outputs.append(out)
        hidden_states.append(hidden_state.copy())

    return outputs, hidden_states


test_input_sequence, test_target_sequence = training_set[0]

test_input = one_hot_encode_sequence(test_input_sequence, vocab_size)
test_target = one_hot_encode_sequence(test_target_sequence, vocab_size)

hidden_state = np.zeros((hidden_size, 1))

outputs, hidden_states = forward_pass(test_input, hidden_state, params)

print("Input sequence:")
print(test_input_sequence)

print("\nTarget sequence:")
print(test_target_sequence)

print("\nPredicted sequence:")
print([idx_to_word[np.argmax(output)] for output in outputs])


def clip_gradient_norm(grads, max_norm=0.25):
    max_norm = float(max_norm)
    total_norm = 0

    for grad in grads:
        grad_norm = np.sum(np.power(grad, 2))
        total_norm += grad_norm

    total_norm = np.sqrt(total_norm)

    clip_coef = max_norm / (total_norm + 1e-6)

    if clip_coef < 1:
        for grad in grads:
            grad *= clip_coef

    return grads


def backward_pass(inputs, outputs, hidden_states, targets, params):
    U, V, W, b_hidden, b_out = params

    d_U, d_V, d_W = np.zeros_like(U), np.zeros_like(V), np.zeros_like(W)
    d_b_hidden, d_b_out = np.zeros_like(b_hidden), np.zeros_like(b_out)

    d_h_next = np.zeros_like(hidden_states[0])
    loss = 0

    for t in reversed(range(len(outputs))):
        loss += -np.mean(np.log(outputs[t] + 1e-12) * targets[t])

        d_o = outputs[t].copy()
        d_o[np.argmax(targets[t])] -= 1

        d_W += np.dot(d_o, hidden_states[t].T)
        d_b_out += d_o

        d_h = np.dot(W.T, d_o) + d_h_next

        d_f = tanh(hidden_states[t], derivative=True) * d_h
        d_b_hidden += d_f

        d_U += np.dot(d_f, inputs[t].T)

        d_V += np.dot(d_f, hidden_states[t - 1].T)
        d_h_next = np.dot(V.T, d_f)

    grads = d_U, d_V, d_W, d_b_hidden, d_b_out

    grads = clip_gradient_norm(grads)

    return loss, grads


loss, grads = backward_pass(test_input, outputs, hidden_states, test_target, params)

print("We get a loss of:")
print(loss)


def update_parameters(params, grads, lr=1e-3):
    for param, grad in zip(params, grads):
        param -= lr * grad

    return params


num_epochs = 1000

params = init_rnn(hidden_size=hidden_size, vocab_size=vocab_size)

hidden_state = np.zeros((hidden_size, 1))

training_loss, validation_loss = [], []

for i in range(num_epochs):
    epoch_training_loss = 0
    epoch_validation_loss = 0

    for inputs, targets in validation_set:
        inputs_one_hot = one_hot_encode_sequence(inputs, vocab_size)
        targets_one_hot = one_hot_encode_sequence(targets, vocab_size)

        hidden_state = np.zeros_like(hidden_state)

        outputs, hidden_states = forward_pass(inputs_one_hot, hidden_state, params)

        loss, _ = backward_pass(
            inputs_one_hot, outputs, hidden_states, targets_one_hot, params
        )

        epoch_validation_loss += loss

    for inputs, targets in training_set:
        inputs_one_hot = one_hot_encode_sequence(inputs, vocab_size)
        targets_one_hot = one_hot_encode_sequence(targets, vocab_size)

        hidden_state = np.zeros_like(hidden_state)

        outputs, hidden_states = forward_pass(inputs_one_hot, hidden_state, params)

        loss, grads = backward_pass(
            inputs_one_hot, outputs, hidden_states, targets_one_hot, params
        )

        if np.isnan(loss):
            raise ValueError("Gradients have vanished!")

        params = update_parameters(params, grads, lr=3e-4)

        epoch_training_loss += loss

    training_loss.append(epoch_training_loss / len(training_set))
    validation_loss.append(epoch_validation_loss / len(validation_set))

    if i % 100 == 0:
        print(
            f"Epoch {i}, training loss: {training_loss[-1]}, validation loss: {validation_loss[-1]}"
        )

inputs, targets = test_set[1]

inputs_one_hot = one_hot_encode_sequence(inputs, vocab_size)
targets_one_hot = one_hot_encode_sequence(targets, vocab_size)

hidden_state = np.zeros((hidden_size, 1))

outputs, hidden_states = forward_pass(inputs_one_hot, hidden_state, params)
output_sentence = [idx_to_word[np.argmax(output)] for output in outputs]
print("Input sentence:")
print(inputs)

print("\nTarget sequence:")
print(targets)

print("\nPredicted sequence:")
print([idx_to_word[np.argmax(output)] for output in outputs])

epoch = np.arange(len(training_loss))
plt.figure()
plt.plot(
    epoch,
    training_loss,
    "r",
    label="Training loss",
)
plt.plot(epoch, validation_loss, "b", label="Validation loss")
plt.legend()
plt.xlabel("Epoch"), plt.ylabel("NLL")
plt.show()


def freestyle(params, sentence="", num_generate=4):
    sentence = sentence.split(" ")

    sentence_one_hot = one_hot_encode_sequence(sentence, vocab_size)

    hidden_state = np.zeros((hidden_size, 1))

    outputs, hidden_states = forward_pass(sentence_one_hot, hidden_state, params)

    output_sentence = sentence

    word = idx_to_word[np.argmax(outputs[-1])]
    output_sentence.append(word)

    for i in range(num_generate):
        output = outputs[-1]
        hidden_state = hidden_states[-1]

        output = output.reshape(1, output.shape[0], output.shape[1])

        outputs, hidden_states = forward_pass(output, hidden_state, params)

        word = idx_to_word[np.argmax(outputs)]

        output_sentence.append(word)

    return output_sentence


print("Example:")
print(freestyle(params, sentence="a a a a a b"))

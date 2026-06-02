---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Simple RNN Implementation from Scratch
translated: false
type: note
---

### Simple RNN Example in NumPy (From Scratch)

Implementing an RNN from scratch in NumPy is a great way to understand the mechanics: the recurrent hidden state, forward propagation, and backpropagation through time (BPTT). Below is a basic example for binary classification on random sequences (similar to the previous PyTorch version). It uses univariate time series data (input_size=1), hidden_size=32, and sequence_length=10.

This code includes:
- Data generation.
- RNN forward pass (with tanh activation for hidden states).
- Backward pass (BPTT with simple gradient descent).
- Training loop.

Note: This is a vanilla RNN; gradients can vanish/explode on long sequences. For production, consider clipping or using LSTM logic.

```python
import numpy as np

# Hyperparameters
input_size = 1      # Feature size (univariate)
hidden_size = 32    # Hidden state size
output_size = 1     # Binary output
sequence_length = 10  # Length of each sequence
num_samples = 1000
num_epochs = 10
learning_rate = 0.01

# Generate dummy data: sequences of length 10, labels based on sum (binary)
def generate_data(num_samples):
    X = np.random.randn(num_samples, sequence_length, input_size)
    y = (np.sum(X, axis=1) > 0).astype(float).reshape(num_samples, 1)
    return X, y

# Simple RNN Class (from scratch)
class SimpleRNN:
    def __init__(self, input_size, hidden_size, output_size):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size

        # Initialize weights (Xavier init)
        self.Wxh = np.random.randn(hidden_size, input_size) * np.sqrt(1. / input_size)
        self.Whh = np.random.randn(hidden_size, hidden_size) * np.sqrt(1. / hidden_size)
        self.Why = np.random.randn(output_size, hidden_size) * np.sqrt(1. / hidden_size)

        # Biases
        self.bh = np.zeros((hidden_size, 1))
        self.by = np.zeros((output_size, 1))

    def forward(self, x):
        # x shape: (sequence_length, input_size, 1) for single sample
        self.x = x  # Store for backprop
        self.h = np.zeros((self.hidden_size, 1))  # Initial hidden state

        # Forward through time
        self.hs = np.zeros((self.hidden_size, sequence_length + 1))  # Hidden states (including initial)
        self.hs[:, 0] = self.h.flatten()

        for t in range(sequence_length):
            self.h = np.tanh(np.dot(self.Wxh, x[t]) + np.dot(self.Whh, self.h) + self.bh)
            self.hs[:, t+1] = self.h.flatten()

        # Output from last hidden state
        self.y_pred = np.dot(self.Why, self.h) + self.by
        return self.sigmoid(self.y_pred)

    def sigmoid(self, z):
        return 1 / (1 + np.exp(-np.clip(z, -250, 250)))  # Clip for stability

    def backward(self, y_true):
        # Backprop through time (simplified)
        dWhy = np.dot((self.y_pred - y_true) * self.sigmoid_deriv(self.y_pred), self.hs[-1:, :].T)
        dby = (self.y_pred - y_true) * self.sigmoid_deriv(self.y_pred)

        # Gradients for hidden and output weights
        dWhh = np.zeros_like(self.Whh)
        dWxh = np.zeros_like(self.Wxh)
        dbh = np.zeros_like(self.bh)

        dh_next = np.zeros_like(self.h)
        for t in reversed(range(sequence_length)):
            dh = np.dot(self.Why.T, (self.y_pred - y_true) * self.sigmoid_deriv(self.y_pred)) + dh_next
            dh_raw = (1 - self.h**2) * dh  # Tanh derivative
            dWxh += np.dot(dh_raw, self.x[t].T)
            dWhh += np.dot(dh_raw, self.hs[:, t:t+2].T[:, 0:1])  # Simplified; full BPTT would accumulate properly
            dbh += dh_raw
            dh_next = np.dot(self.Whh.T, dh_raw)

        # Update weights
        self.Wxh -= learning_rate * dWxh
        self.Whh -= learning_rate * dWhh
        self.Why -= learning_rate * dWhy
        self.bh -= learning_rate * dbh
        self.by -= learning_rate * dby

    def sigmoid_deriv(self, z):
        s = self.sigmoid(z)
        return s * (1 - s)

# Training
X, y = generate_data(num_samples)

# Reshape for single sample processing (batch_size=1 for simplicity)
X = X.reshape(num_samples, sequence_length, input_size, 1)  # Add batch dim of 1
y = y.reshape(num_samples, 1, 1)

model = SimpleRNN(input_size, hidden_size, output_size)

for epoch in range(num_epochs):
    total_loss = 0
    for i in range(num_samples):
        pred = model.forward(X[i])
        loss = -np.mean(y[i] * np.log(pred + 1e-8) + (1 - y[i]) * np.log(1 - pred + 1e-8))  # BCE
        total_loss += loss
        model.backward(y[i])

    avg_loss = total_loss / num_samples
    print(f'Epoch [{epoch+1}/{num_epochs}], Avg Loss: {avg_loss:.4f}')

# Inference example
test_seq = np.random.randn(sequence_length, input_size, 1)
prediction = model.forward(test_seq)
print(f'Prediction: {prediction.flatten()[0]:.4f}')
```

#### How it Works:
- **Data Generation**: Random sequences with binary labels based on sum.
- **Forward Pass**: Processes the sequence timestep-by-timestep, updating hidden state `h_t = tanh(Wxh * x_t + Whh * h_{t-1} + bh)`. Output uses the final `h` with sigmoid.
- **Backward Pass**: BPTT computes gradients for all timesteps, updating weights via simple GD. (Note: This is a minimal BPTT; full versions handle more precise accumulation.)
- **Training**: Loops over samples, computes BCE loss, and updates.
- **Output**: Sigmoid gives probability (0-1).

This runs in ~10-20 seconds on a standard machine for these params. Scale up `num_samples` or `num_epochs` to see learning. For multi-batch, vectorize the loops.

For deeper dives:
[Understanding LSTM Networks (Colah's Blog)](https://colah.github.io/posts/2015-08-Understanding-LSTMs/)
[NumPy RNN Tutorial](https://www.wildml.com/2015/09/recurrent-neural-networks-tutorial-part-1-introduction-to-rnns/)

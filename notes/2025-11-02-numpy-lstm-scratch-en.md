---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: NumPy LSTM Implementation from Scratch
translated: false
type: note
---

This is a basic implementation of a Long Short-Term Memory (LSTM) network using only NumPy, inspired by the concepts in Christopher Olah's blog post on Understanding LSTM Networks. It includes the core gates (forget, input, candidate cell, and output) and focuses on the forward pass. The class handles a single time step via `forward()` and an entire sequence via `forward_sequence()`.

Weights are randomly initialized (in practice, use better initialization like Xavier/Glorot). No backward pass or training is included here—extend with backpropagation through time (BPTT) for that.

```python
import numpy as np

class LSTM:
    def __init__(self, input_size, hidden_size):
        self.input_size = input_size
        self.hidden_size = hidden_size
        # Initialize weights and biases for forget, input, cell, and output gates
        self.Wf = np.random.randn(hidden_size, hidden_size + input_size)
        self.Wi = np.random.randn(hidden_size, hidden_size + input_size)
        self.WC = np.random.randn(hidden_size, hidden_size + input_size)
        self.Wo = np.random.randn(hidden_size, hidden_size + input_size)
        self.bf = np.zeros((hidden_size, 1))
        self.bi = np.zeros((hidden_size, 1))
        self.bC = np.zeros((hidden_size, 1))
        self.bo = np.zeros((hidden_size, 1))

    def sigmoid(self, z):
        return 1 / (1 + np.exp(-z))

    def tanh(self, z):
        return np.tanh(z)

    def forward(self, x, h_prev, C_prev):
        # x: (input_size, 1), h_prev and C_prev: (hidden_size, 1)
        # Concatenate hidden state and input
        concat = np.vstack((h_prev, x))
        # Forget gate
        f_t = self.sigmoid(np.dot(self.Wf, concat) + self.bf)
        # Input gate
        i_t = self.sigmoid(np.dot(self.Wi, concat) + self.bi)
        C_tilda = self.tanh(np.dot(self.WC, concat) + self.bC)
        # Cell state update
        C_t = f_t * C_prev + i_t * C_tilda
        # Output gate
        o_t = self.sigmoid(np.dot(self.Wo, concat) + self.bo)
        # Hidden state update
        h_t = o_t * self.tanh(C_t)
        return h_t, C_t

    def forward_sequence(self, X):
        # X: (seq_len, input_size)
        h = np.zeros((self.hidden_size, 1))
        C = np.zeros((self.hidden_size, 1))
        outputs = []
        for x in X:
            h, C = self.forward(x.reshape(-1, 1), h, C)
            outputs.append(h)
        return np.hstack(outputs).T  # Returns (seq_len, hidden_size)

# Example usage
input_size = 3
hidden_size = 5
lstm = LSTM(input_size, hidden_size)

# Single step
x_t = np.random.randn(input_size, 1)
h_prev = np.zeros((hidden_size, 1))
C_prev = np.zeros((hidden_size, 1))
h_t, C_t = lstm.forward(x_t, h_prev, C_prev)
print("Single step - Hidden state shape:", h_t.shape)

# Sequence
X = np.random.randn(4, input_size)  # seq_len=4
outputs = lstm.forward_sequence(X)
print("Sequence outputs shape:", outputs.shape)
```

### Quick Explanation
- **Initialization**: Weights connect the concatenated input (previous hidden + current input) to each gate. Biases are zero-initialized.
- **Gates**:
  - **Forget gate** (`f_t`): Decides what to forget from the previous cell state (sigmoid: 0-1).
  - **Input gate** (`i_t`) and **candidate cell** (`C_tilda`): Decide what new info to add (sigmoid + tanh).
  - **Output gate** (`o_t`): Filters the cell state to produce the hidden state (sigmoid + tanh on cell).
- **Cell state** (`C_t`): Linear flow with additive updates for long-term memory.
- **Usage**: For sequences, loop through time steps, updating hidden and cell states progressively.

This matches the LSTM architecture from Colah's blog: cell state as a "highway" controlled by gates.

[Understanding LSTMs: Implementation from Scratch](https://medium.com/@samina.amin/understanding-lstms-lstm-implementation-from-scratch-18965a150eca)

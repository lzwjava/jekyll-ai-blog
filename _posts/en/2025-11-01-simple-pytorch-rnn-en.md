---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Simple PyTorch RNN Example
translated: false
type: note
---

### Simple RNN Example in PyTorch

Recurrent Neural Networks (RNNs) are great for handling sequential data like time series or text. Here's a basic example using PyTorch to build a simple RNN for classifying sequences (e.g., binary classification on random sequences). This assumes you have PyTorch installed (`import torch` and `import torch.nn as nn`).

```python
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

# Hyperparameters
input_size = 1      # Feature size (e.g., univariate time series)
hidden_size = 32    # Hidden state size
output_size = 1     # Binary output (sigmoid for classification)
sequence_length = 10  # Length of each sequence
batch_size = 32
num_epochs = 10

# Generate dummy data: sequences of length 10, labels based on sum (binary)
def generate_data(num_samples):
    X = torch.randn(num_samples, sequence_length, input_size)
    y = (torch.sum(X, dim=1) > 0).float().unsqueeze(1)
    return X, y

# Simple RNN Model
class SimpleRNN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(SimpleRNN, self).__init__()
        self.hidden_size = hidden_size
        self.rnn = nn.RNN(input_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        # x shape: (batch, seq_len, input_size)
        h0 = torch.zeros(1, x.size(0), self.hidden_size)  # Initial hidden state
        out, _ = self.rnn(x, h0)
        # Take the last output for classification
        out = self.fc(out[:, -1, :])  # Last time step
        return self.sigmoid(out)

# Initialize model, loss, optimizer
model = SimpleRNN(input_size, hidden_size, output_size)
criterion = nn.BCELoss()
optimizer = optim.Adam(model.parameters(), lr=0.01)

# Training loop
num_samples = 1000
X, y = generate_data(num_samples)
dataset = torch.utils.data.TensorDataset(X, y)
dataloader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=True)

for epoch in range(num_epochs):
    for batch_X, batch_y in dataloader:
        optimizer.zero_grad()
        outputs = model(batch_X)
        loss = criterion(outputs, batch_y)
        loss.backward()
        optimizer.step()
    print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')

# Inference example
test_seq = torch.randn(1, sequence_length, input_size)
prediction = model(test_seq)
print(f'Prediction: {prediction.item():.4f}')
```

#### How it Works:
- **Data Generation**: Creates random sequences of length 10 with a binary label (1 if sum > 0, else 0).
- **Model**: Uses `nn.RNN` (basic RNN cell). The forward pass processes the sequence step-by-step, using the last hidden state for output.
- **Training**: Standard PyTorch loop with BCE loss for binary classification.
- **Output**: Sigmoid activation gives a probability between 0 and 1.

This is a vanilla RNN; for better performance on long sequences, consider LSTM or GRU variants (e.g., replace `nn.RNN` with `nn.LSTM`).

### LSTM Variant (Quick Extension)
For vanishing gradients, swap to LSTM:

```python
# In the model class, replace:
self.rnn = nn.LSTM(input_size, hidden_size, batch_first=True)

# And in forward:
h0 = torch.zeros(1, x.size(0), self.hidden_size)
c0 = torch.zeros(1, x.size(0), self.hidden_size)  # LSTM needs cell state
out, (hn, cn) = self.rnn(x, (h0, c0))
```

Run this in a PyTorch environment to experiment!

[PyTorch RNN Documentation](https://pytorch.org/docs/stable/generated/torch.nn.RNN.html)
[PyTorch LSTM Documentation](https://pytorch.org/docs/stable/generated/torch.nn.LSTM.html)

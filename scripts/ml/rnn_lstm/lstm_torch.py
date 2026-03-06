import matplotlib.pyplot as plt
import torch
import torch.nn as nn

from data import *
from utils import *

np.random.seed(42)


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()

        self.lstm = nn.LSTM(
            input_size=vocab_size, hidden_size=50, num_layers=1, bidirectional=False
        )

        self.l_out = nn.Linear(in_features=50, out_features=vocab_size, bias=False)

    def forward(self, x):
        x, (h, c) = self.lstm(x)

        x = x.view(-1, self.lstm.hidden_size)

        x = self.l_out(x)

        return x


num_epochs = 50

net = Net()

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(net.parameters(), lr=3e-4)

training_loss, validation_loss = [], []

for i in range(num_epochs):
    epoch_training_loss = 0
    epoch_validation_loss = 0

    net.eval()

    for inputs, targets in validation_set:
        inputs_one_hot = one_hot_encode_sequence(inputs, vocab_size)
        targets_idx = [word_to_idx[word] for word in targets]

        inputs_one_hot = torch.Tensor(inputs_one_hot)
        inputs_one_hot = inputs_one_hot.permute(0, 2, 1)

        targets_idx = torch.LongTensor(targets_idx)

        outputs = net.forward(inputs_one_hot)

        loss = criterion(outputs, targets_idx)

        epoch_validation_loss += loss.detach().numpy()

    net.train()

    for inputs, targets in training_set:
        inputs_one_hot = one_hot_encode_sequence(inputs, vocab_size)
        targets_idx = [word_to_idx[word] for word in targets]

        inputs_one_hot = torch.Tensor(inputs_one_hot)
        inputs_one_hot = inputs_one_hot.permute(0, 2, 1)

        targets_idx = torch.LongTensor(targets_idx)

        outputs = net.forward(inputs_one_hot)

        loss = criterion(outputs, targets_idx)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        epoch_training_loss += loss.detach().numpy()

    training_loss.append(epoch_training_loss / len(training_set))
    validation_loss.append(epoch_validation_loss / len(validation_set))

    if i % 5 == 0:
        print(
            f"Epoch {i}, training loss: {training_loss[-1]}, validation loss: {validation_loss[-1]}"
        )

inputs, targets = test_set[1]

inputs_one_hot = one_hot_encode_sequence(inputs, vocab_size)
targets_idx = [word_to_idx[word] for word in targets]

inputs_one_hot = torch.Tensor(inputs_one_hot)
inputs_one_hot = inputs_one_hot.permute(0, 2, 1)

targets_idx = torch.LongTensor(targets_idx)

outputs = net.forward(inputs_one_hot).data.numpy()

print("\nInput sequence:")
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

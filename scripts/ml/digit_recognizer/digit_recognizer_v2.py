import random

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
import torch.optim as optim
import torch.nn.functional as F


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, 3, 1)
        self.conv2 = nn.Conv2d(32, 64, 3, 1)
        self.fc1 = nn.Linear(9216, 128)
        self.fc2 = nn.Linear(128, 10)
        self.dropout1 = nn.Dropout(0.25)
        self.dropout2 = nn.Dropout(0.25)

    def forward(self, x):
        x = self.conv1(x)
        x = F.relu(x)
        x = self.conv2(x)
        x = F.relu(x)
        x = F.max_pool2d(x, 2)
        x = self.dropout1(x)
        x = torch.flatten(x, 1)
        x = self.fc1(x)
        x = F.relu(x)
        x = self.dropout2(x)
        x = self.fc2(x)
        output = F.log_softmax(x, dim=1)
        return output


def train(model: Net, train_loader: DataLoader, optimizer: optim.Optimizer):
    model.train()
    for batch_idx, (data, target) in enumerate(train_loader):
        data = data.to(get_device())
        target = target.to(get_device())

        optimizer.zero_grad()
        output = model(data)

        target = target.argmax(dim=1)

        loss = F.nll_loss(output, target)
        loss.backward()
        optimizer.step()


def read_training_data() -> tuple:
    df = pd.read_csv("./train.csv")
    # print(df.head())

    labels = df["label"].values
    pixels = df.drop("label", axis=1).values
    pixels = pixels / 255.0

    shuffle_list = list(zip(pixels, labels))
    random.shuffle(shuffle_list)
    pixels, labels = zip(*shuffle_list)

    n = len(labels)

    inputs = [np.reshape(x, (1, 28, 28)) for x in pixels]
    results = [vectorized_result(y) for y in labels]

    middle = int(n * 0.99)

    training_inputs = inputs[:middle]
    training_results = results[:middle]

    val_inputs = inputs[middle:]
    val_results = results[middle:]

    training_inputs = torch.Tensor(np.array(training_inputs))
    training_results = torch.Tensor(np.array(training_results))
    training_data = DataLoader(
        list(zip(training_inputs, training_results)), batch_size=10, shuffle=True
    )

    val_inputs = torch.Tensor(val_inputs)
    val_results = torch.Tensor(val_results)
    val_data = DataLoader(
        list(zip(val_inputs, val_results)), batch_size=10, shuffle=True
    )

    return training_data, val_data


def read_test_loader() -> list:
    df = pd.read_csv("./test.csv")
    pixels = df.values
    pixels = pixels / 255.0
    test_input = [np.reshape(x, (1, 28, 28)) for x in pixels]
    test_input = torch.Tensor(np.array(test_input))
    test_loader = DataLoader(test_input, batch_size=10, shuffle=False)
    return test_loader


def vectorized_result(j):
    e = np.zeros(10)
    e[j] = 1.0
    return e


def draw(some_digit):
    some_digit_image = some_digit.reshape(28, 28)

    plt.imshow(some_digit_image, cmap=matplotlib.cm.binary, interpolation="nearest")
    plt.axis("off")
    plt.show()


def get_device():
    if torch.cuda.is_available():
        return torch.device("cuda")
    else:
        return torch.device("cpu")


def validate(model, val_loader):
    model.eval()
    correct = 0
    with torch.no_grad():
        for data, target in val_loader:
            data = data.to(get_device())
            target = target.to(get_device())

            output = model(data)
            pred = output.argmax(dim=1, keepdim=True)
            target = target.argmax(dim=1, keepdim=True)
            correct += pred.eq(target).sum().item()

    print("Accuracy:{}".format(100.0 * correct / len(val_loader.dataset)))


def submit(model: Net, test_loader: DataLoader):
    model.eval()
    with torch.no_grad():
        test_n = len(test_loader.dataset)
        images = [i + 1 for i in range(test_n)]
        result = []
        for batch_idx, data in enumerate(test_loader):
            data = data.to(get_device())
            test_output = model(data)
            test_output = test_output.argmax(dim=1)
            result.extend(test_output.cpu().detach().tolist())

        output = pd.DataFrame({"ImageId": images, "Label": result})
        output.to_csv("submission.csv", index=False)


def main():
    train_loader, val_loader = read_training_data()
    test_loader = read_test_loader()

    model = Net()

    model = model.to(get_device())

    optimizer = optim.SGD(model.parameters(), lr=1e-3)

    epochs = 50

    for i in range(epochs):
        train(model, train_loader, optimizer)
        validate(model, val_loader)

    # test_output = network.cal(test_input)
    submit(model, test_loader)


if __name__ == "__main__":
    main()

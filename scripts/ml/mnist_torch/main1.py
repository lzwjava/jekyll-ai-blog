import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, 3, 1)
        self.fc_input_size = self.calculate_conv_output_size()
        print(self.fc_input_size)
        self.fc1 = nn.Linear(self.fc_input_size, 128)
        self.fc2 = nn.Linear(128, 10)
        self.dropout = nn.Dropout(0.25)

    def calculate_conv_output_size(self):
        # Create a dummy input tensor to calculate the output size of conv1
        x = torch.randn(1, 1, 28, 28)  # Assuming MNIST-like images
        x = self.conv1(x)
        return x.view(1, -1).size(1)  # Flatten the output and get the size

    def forward(self, x):
        x = self.conv1(x)
        x = F.relu(x)
        x = x.view(-1, self.fc_input_size)

        x = self.fc1(x)

        x = self.dropout(x)

        x = self.fc2(x)
        # print(x)
        # output = F.log_softmax(x, dim=1)

        return x


def train(model, train_loader, optimizer):
    model.train()
    for batch_idx, (data, target) in enumerate(train_loader):
        if batch_idx > 10000:
            break
        optimizer.zero_grad()
        output = model(data)
        loss = nn.CrossEntropyLoss()
        loss = loss(output, target)
        # print(loss)
        # print(output)
        loss.backward()
        optimizer.step()
        print("batch:{} Loss:{:.6f}".format(batch_idx, loss.item()))

        # for name, param in model.named_parameters():
        #     if param.requires_grad:
        #         print(f'Parameter name: {name}, Shape: {param.shape}')
        #         print(param)


def test(model, test_loader):
    model.eval()
    correct = 0
    with torch.no_grad():
        for data, target in test_loader:
            output = model(data)
            pred = output.argmax(dim=1, keepdim=True)
            correct += pred.eq(target.view_as(pred)).sum().item()

    print("Accuracy:{}".format(100.0 * correct / len(test_loader.dataset)))


def main():
    transform = transforms.Compose(
        [transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))]
    )
    dataset1 = datasets.MNIST("../data", train=True, download=True, transform=transform)
    # print(dataset1)
    dataset2 = datasets.MNIST("../data", train=False, transform=transform)

    train_loader = torch.utils.data.DataLoader(dataset1)
    test_loader = torch.utils.data.DataLoader(dataset2)

    model = Net()
    optimizer = optim.SGD(model.parameters(), lr=1e-3)

    train(model, train_loader, optimizer)
    test(model, test_loader)


if __name__ == "__main__":
    main()

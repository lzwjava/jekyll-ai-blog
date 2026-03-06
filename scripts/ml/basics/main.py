import torch
import torch.nn as nn

from torch import Tensor


class Net(nn.Module):
    def __init__(self):
        super().__init__()

        self.relu = nn.ReLU()

    def forward(self, x: Tensor) -> Tensor:
        y = self.relu(x)
        return y


x = torch.rand(28) - 0.5
print(x)

model = Net()

net = model(x)
print(net)

import math

import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.optim as optim


def param_str(v: torch.Tensor):
    return str(v.item())


class Polynomial(nn.Module):
    def __init__(self):
        super().__init__()
        self.a = nn.Parameter(torch.rand(1))
        self.b = nn.Parameter(torch.rand(1))
        self.c = nn.Parameter(torch.rand(1))
        self.d = nn.Parameter(torch.rand(1))

    def forward(self, x):
        return self.a + self.b * x + self.c * (x**2) + self.d * (x**3)

    def __str__(self):
        return f"y={param_str(self.a)} + {param_str(self.b)}x + {param_str(self.c)}x^2 + {param_str(self.d)}x^3"


def plot(x, y):
    print(x)
    print(y)

    x = x.numpy()
    y = y.numpy()

    plt.plot(x, y)
    # plt.show()


def main():
    model = Polynomial()
    loss_fn = nn.L1Loss()

    step = 0
    lr = 1e-3
    max_step = 10000

    optimizer = optim.SGD(model.parameters(), lr)

    x = torch.linspace(-math.pi, math.pi, 2000)
    y = torch.sin(x)

    # plot(x, y)

    while True:
        output = model(x)
        loss = loss_fn(output, y)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        step += 1

        if step % 100 == 0:
            print(f"{step} loss: {loss}")

        if step > max_step:
            break

    print(model)

    output = model(x)

    plot(x, y)
    plot(x, output.detach())
    plt.show()


if __name__ == "__main__":
    main()

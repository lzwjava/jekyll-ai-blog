import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt


class Sequence(nn.Module):
    def __init__(self):
        super(Sequence, self).__init__()
        self.lstm1 = nn.LSTMCell(1, 51)
        self.lstm2 = nn.LSTMCell(51, 51)
        self.linear = nn.Linear(51, 1)

    def forward(self, input, future=0):
        outputs = []
        i0 = input.size(0)
        h_t = torch.zeros(i0, 51, dtype=torch.double)
        c_t = torch.zeros(i0, 51, dtype=torch.double)
        h_t2 = torch.zeros(i0, 51, dtype=torch.double)
        c_t2 = torch.zeros(i0, 51, dtype=torch.double)

        for input_t in input.split(1, dim=1):
            h_t, c_t = self.lstm1(input_t, (h_t, c_t))
            h_t2, c_t2 = self.lstm2(h_t, (h_t2, c_t2))
            output = self.linear(h_t2)
            outputs += [output]

        for i in range(future):
            h_t, c_t = self.lstm1(output, (h_t, c_t))
            h_t2, c_t2 = self.lstm2(h_t, (h_t2, c_t2))
            output = self.linear(h_t2)
            outputs += [output]

        outputs = torch.cat(outputs, dim=1)
        return outputs


def main():
    steps = 1
    np.random.seed(0)
    torch.manual_seed(0)
    data = torch.load("traindata.pt")
    input = torch.from_numpy(data[3:, :-1])
    target = torch.from_numpy(data[3:, 1:])
    print(input)
    print(target)
    test_input = torch.from_numpy(data[:3, :-1])
    test_target = torch.from_numpy(data[:3, 1:])

    seq = Sequence()
    seq.double()

    loss_fn = nn.MSELoss()
    optimizer = optim.LBFGS(seq.parameters(), lr=0.8)

    for i in range(steps):
        print("STEP: ", i)

        def closure():
            optimizer.zero_grad()
            out = seq(input)
            loss = loss_fn(out, target)
            print("loss: ", loss.item())
            loss.backward()
            return loss

        optimizer.step(closure)

        with torch.no_grad():
            future = 1000
            pred = seq(test_input, future=future)
            loss = loss_fn(pred[:, :-future], test_target)
            print("test loss:", loss.item())
            y = pred.detach().numpy()

        plt.figure(figsize=(30, 10))
        plt.title("Predict")
        plt.xlabel("x", fontsize=20)
        plt.ylabel("y", fontsize=20)
        plt.xticks(fontsize=20)
        plt.yticks(fontsize=20)

        def draw(yi, color):
            i1 = input.size(1)
            plt.plot(np.arange(i1), yi[:i1], color, linewidth=2.0)
            plt.plot(np.arange(i1, i1 + future), yi[i1:], color + ":", linewidth=2.0)

        draw(y[0], "r")
        draw(y[1], "g")
        draw(y[2], "b")

        plt.savefig("predict%d.pdf" % i)
        plt.close()


if __name__ == "__main__":
    main()

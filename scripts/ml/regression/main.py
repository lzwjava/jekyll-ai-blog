from itertools import count

import torch
import torch.nn.functional as F

POLY_DEGREE = 4
W_target = torch.randn(POLY_DEGREE, 1) * 5
b_target = torch.randn(1) * 5


def poly_desc(W, b):
    result = "y = "
    for i, w in enumerate(W):
        result += "{:+.6f}x^{} ".format(w, i + 1)
    result += "{:+.6f}".format(b[0])
    return result


def make_features(x):
    x = x.unsqueeze(1)
    return torch.cat([x**i for i in range(1, POLY_DEGREE + 1)], 1)


def f(x):
    return x.mm(W_target) + b_target.item()


def get_batch(batch_size=32):
    random = torch.randn(batch_size)
    x = make_features(random)
    y = f(x)
    return x, y


def train():
    fc = torch.nn.Linear(W_target.size(0), 1)
    for batch_idx in count(1):
        batch_x, batch_y = get_batch()
        fc.zero_grad()

        fout = fc(batch_x)
        output = F.smooth_l1_loss(fout, batch_y)
        loss = output.item()

        output.backward()

        for param in fc.parameters():
            param.data.add_(-0.01 * param.grad)

        if loss < 1e-8:
            break

        if batch_idx % 1000 == 0:
            print(f"Loss: {loss} after batch {batch_idx}")

    print(f"Loss: {loss} after batch {batch_idx}")
    print("Learned function:\t" + poly_desc(fc.weight.view(-1), fc.bias))
    print("Actual function:\t" + poly_desc(W_target.view(-1), b_target))


def main():
    print(W_target)
    print(b_target)

    desc = poly_desc(W_target.view(-1), b_target)
    print(desc)

    train()


if __name__ == "__main__":
    main()

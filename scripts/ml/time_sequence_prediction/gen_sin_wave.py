import numpy as np
import torch

np.random.seed(2)

T = 20
L = 1000
N = 100

x = np.empty((N, L), "int64")

x1 = np.array(range(L))
x2 = np.random.randint(-4 * T, 4 * T, N).reshape(N, 1)

print(x1)
print(x2)

x[:] = x1 + x2

print(x)

data = np.sin(x / 1.0 / T).astype("float64")

print(data)

torch.save(data, open("traindata.pt", "wb"))

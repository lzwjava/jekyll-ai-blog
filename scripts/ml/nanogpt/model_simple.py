import torch
import torch.nn as nn
import pickle
from torch.nn import functional as F
import os

meta_path = os.path.join(os.path.dirname(__file__), "meta.pkl")
meta_vocab_size = None
if os.path.exists(meta_path):
    with open(meta_path, "rb") as f:
        meta = pickle.load(f)
    meta_vocab_size = meta["vocab_size"]
    print(f"found vocab_size = {meta_vocab_size} (inside {meta_path})")

input_path = os.path.join(os.path.dirname(__file__), "input.txt")

with open(input_path, "r", encoding="utf-8") as f:
    text = f.read()

chars = sorted(list(set(text)))
vocab_size = len(chars)

stoi = {ch: i for i, ch in enumerate(chars)}
itos = {i: ch for i, ch in enumerate(chars)}
encode = lambda s: [stoi[c] for c in s]  # encoder: take a string, output a list of ints
decode = lambda l: "".join(
    itos[i] for i in l
)  # decode: take a list of ints, output a string

data = torch.tensor(encode(text), dtype=torch.long)
# print(data.shape, data.type)
# print(data[:1000])

# Split ratio for train and val set
split_ratio: float = 0.9
# Training batch size, number of sequences in a mini batch
batch_size: int = 4
# Maximum context length
block_size: int = 8

n = int(split_ratio * len(data))
train_data = data[:n]
val_data = data[n:]

print(len(train_data), len(val_data))

torch.manual_seed(1337)


# torch.manual_seed(1338)


def get_batch(split):
    # generate a small batch of data of input x and targets y
    data = train_data if split == "train" else val_data
    ix = torch.randint(
        len(data) - block_size, (batch_size,)
    )  # because last will start from -8 and go until the end of text
    x = torch.stack([data[i : i + block_size] for i in ix])
    y = torch.stack([data[i + 1 : i + block_size + 1] for i in ix])
    return x, y


xb, yb = get_batch("train")
print("inputs:")
print(xb.shape)
print(xb)
print("targets:")
print(yb.shape)
print(yb)


class GPT(nn.Module):
    def __init__(self, vocab_size):
        super().__init__()

        self.token_embedding_table = nn.Embedding(vocab_size, vocab_size)

        print("token_embedding_table")
        print(self.token_embedding_table)

        embedding_matrix = self.token_embedding_table.weight.data
        print("embedding_matrix")
        print(embedding_matrix)
        print(embedding_matrix.size())

    def forward(self, idx, targets=None):
        # print('forward')
        # print(idx)
        # print(idx.size())
        logits = self.token_embedding_table(idx)
        # print('logits')
        # print(logits)
        # print(logits.size())
        # exit()

        if targets == None:
            loss = None
        else:
            # reshape for loss, loss needs BxCxT instead
            B, T, C = logits.shape
            logits = logits.view(B * T, C)
            targets = targets.view(B * T)
            loss = F.cross_entropy(logits, targets)

        return logits, loss

    def generate(self, idx, max_new_tokens):
        for _ in range(max_new_tokens):
            logits, loss = self(idx)
            print("logits")
            print(logits.size())
            print(logits)
            logits = logits[:, -1, :]  # becomes (B,C)
            probs = F.softmax(logits, dim=-1)  # (B, C)
            idx_next = torch.multinomial(probs, num_samples=1)  # (B, 1)
            idx = torch.cat((idx, idx_next), dim=1)  # (B, T+1)

        return idx


m = GPT(vocab_size=meta_vocab_size)

logits, loss = m(xb, yb)
# print(logits.shape)
# print(loss)

# idx = torch.zeros((1, 1), dtype=torch.long)
# print(decode(m.generate(idx, max_new_tokens=100)[0].tolist()))


batch_sieze = 32
optimizer = torch.optim.AdamW(m.parameters(), lr=1e-3)

print("begin to train...")

for steps in range(10000):
    # sample a batch of data
    xb, yb = get_batch("train")

    # print('xb')
    # print(xb)
    # print('yb')
    # print(yb)

    # evaluate the loss
    logits, loss = m(xb, yb)
    optimizer.zero_grad(set_to_none=True)
    loss.backward()
    optimizer.step()

print(loss.item())

print("training finished")

print(
    decode(
        m.generate(idx=torch.zeros((1, 1), dtype=torch.long), max_new_tokens=500)[
            0
        ].tolist()
    )
)

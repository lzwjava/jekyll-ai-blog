import os
import requests
import numpy as np
import pickle

input_file_path = os.path.join(os.path.dirname(__file__), "input.txt")

if not os.path.exists(input_file_path):
    data_url = "https://raw.githubusercontent.com/karpathy/char-rnn/master/data/tinyshakespeare/input.txt"
    with open(input_file_path, "w") as f:
        f.write(requests.get(data_url).text)

with open(input_file_path, "r") as f:
    data = f.read()

print(f"length: {len(data)}")

chars = sorted(list(set(data)))
vocab_size = len(chars)
print("all the unique characters:", "".join(chars))
print(f"vocab_size: {vocab_size}")

stoi = {ch: i for i, ch in enumerate(chars)}
itos = {i: ch for i, ch in enumerate(chars)}


def encode(s):
    return [stoi[c] for c in s]


def decode(l):
    return "".join([itos[i] for i in l])


print(encode("abc"))
print(decode([2, 3, 4]))

n = len(data)
train_data = data[: int(n * 0.9)]
val_data = data[int(n * 0.9) :]

train_ids = encode(train_data)
val_ids = encode(val_data)

# print(train_ids)
# print(val_ids)

print(f"train ids length {len(train_ids)}")
print(f"val ids length {len(val_ids)}")

train_ids = np.array(train_ids, dtype=np.uint16)
val_ids = np.array(val_ids, dtype=np.uint16)

train_ids.tofile(os.path.join(os.path.dirname(__file__), "train.bin"))
val_ids.tofile(os.path.join(os.path.dirname(__file__), "val.bin"))

meta = {"vocab_size": vocab_size, "itos": itos, "stoi": stoi}

with open(os.path.join(os.path.dirname(__file__), "meta.pkl"), "wb") as f:
    pickle.dump(meta, f)

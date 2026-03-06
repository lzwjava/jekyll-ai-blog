import torch
from torch.utils.data import Dataset
from torch.utils.data.dataloader import DataLoader


class CharDataset(Dataset):
    def __init__(self, words, chars, max_len):
        self.words = words
        self.chars = chars
        self.max_len = max_len
        self.stoi = {ch: i + 1 for i, ch in enumerate(chars)}
        # print(self.stoi)
        self.itos = {i: ch for ch, i in self.stoi.items()}
        # print(self.itos)

    def __len__(self) -> int:
        return len(self.words)

    def contains(self, word):
        return word in self.words

    def get_vocab_size(self):
        return len(self.chars) + 1

    def get_output_length(self):
        return self.max_len + 1

    def encode(self, word):
        ix = torch.tensor([self.stoi[w] for w in word], dtype=torch.long)
        return ix

    def decode(self, ix):
        word = "".join(self.itos[i] for i in ix)
        return word

    def __getitem__(self, idx):
        word = self.words[idx]
        ix = self.encode(word)
        x = torch.zeros(self.max_len + 1, dtype=torch.long)
        y = torch.zeros(self.max_len + 1, dtype=torch.long)
        x[1 : 1 + len(ix)] = ix
        y[: len(ix)] = ix
        y[len(ix) + 1 :] = -1
        return x, y


def create_datasets(input_file):
    with open(input_file, "r") as f:
        lines = f.readlines()

    lines = [l.strip() for l in lines]

    word_count = len(lines)

    test_size = int(word_count * 0.1)

    rp = torch.randperm(word_count).tolist()

    # print(rp)
    train_words = [lines[i] for i in rp[:-test_size]]

    test_words = [lines[i] for i in rp[-test_size:]]

    print(word_count)
    print(test_size)
    print(len(train_words))
    print(len(test_words))

    # print(test_words)

    chars = sorted(set("".join(lines)))

    max_len = len(max(lines, key=len))

    print(f"chars:{chars}")
    print(f"max_len={max_len}")

    train_dataset = CharDataset(train_words, chars, max_len)
    test_dataset = CharDataset(test_words, chars, max_len)

    return train_dataset, test_dataset


class InfiniteDataLoader:
    def __init__(self, dataset, **kwargs):
        train_sampler = torch.utils.data.RandomSampler(
            dataset, replacement=True, num_samples=int(1e10)
        )
        self.train_loader = DataLoader(dataset, sampler=train_sampler, **kwargs)
        self.data_iter = iter(self.train_loader)

    def next(self):
        try:
            batch = next(self.data_iter)
        except StopIteration:
            self.data_iter = iter(self.train_loader)
            batch = next(self.data_iter)

        return batch

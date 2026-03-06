import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader

import urllib.request
import collections
import os
import zipfile

import numpy as np

window_size = 3
vector_dim = 300
epochs = 1000

valid_size = 16
valid_window = 100
valid_examples = np.random.choice(valid_window, valid_size, replace=False)


def maybe_download(filename, url, expected_bytes):
    if not os.path.exists(filename):
        filename, _ = urllib.request.urlretrieve(url + filename, filename)
    statinfo = os.stat(filename)
    if statinfo.st_size == expected_bytes:
        print("Found and verified", filename)
    else:
        print(statinfo.st_size)
        raise Exception(
            "Failed to verify " + filename + ". Can you get to it with a browser?"
        )
    return filename


def read_data(filename):
    with zipfile.ZipFile(filename) as f:
        data = f.read(f.namelist()[0]).decode("utf-8").split()
    return data


def build_dataset(words, n_words):
    count = [["UNK", -1]]
    count.extend(collections.Counter(words).most_common(n_words - 1))
    dictionary = dict()
    for word, _ in count:
        dictionary[word] = len(dictionary)
    data = list()
    unk_count = 0
    for word in words:
        if word in dictionary:
            index = dictionary[word]
        else:
            index = 0
            unk_count += 1
        data.append(index)
    count[0][1] = unk_count
    reversed_dictionary = dict(zip(dictionary.values(), dictionary.keys()))
    return data, count, dictionary, reversed_dictionary


def collect_data(vocabulary_size=10000):
    url = "http://mattmahoney.net/dc/"
    filename = maybe_download("text8.zip", url, 31344016)
    vocabulary = read_data(filename)
    print(vocabulary[:7])
    data, count, dictionary, reverse_dictionary = build_dataset(
        vocabulary, vocabulary_size
    )
    del vocabulary
    return data, count, dictionary, reverse_dictionary


class Word2VecModel(nn.Module):
    def __init__(self, vocab_size, embedding_dim):
        super(Word2VecModel, self).__init__()
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim

        # Input and output embeddings
        self.in_embeddings = nn.Embedding(vocab_size, embedding_dim)
        self.out_embeddings = nn.Embedding(vocab_size, embedding_dim)

        # Initialize embeddings with small random values
        self.in_embeddings.weight.data.uniform_(
            -0.5 / embedding_dim, 0.5 / embedding_dim
        )
        self.out_embeddings.weight.data.uniform_(
            -0.5 / embedding_dim, 0.5 / embedding_dim
        )

    def forward(self, center_word, context_words):
        # Get embeddings
        center_embed = self.in_embeddings(center_word)  # [batch_size, embedding_dim]
        context_embed = self.out_embeddings(
            context_words
        )  # [batch_size, embedding_dim]

        # Compute dot product
        score = torch.sum(center_embed * context_embed, dim=1)  # [batch_size]
        return score


class SimilarityCallback:
    def __init__(self, model, reverse_dictionary, device):
        self.model = model
        self.reverse_dictionary = reverse_dictionary
        self.device = device

    def run_sim(self):
        self.model.eval()
        with torch.no_grad():
            for i in range(valid_size):
                valid_word = self.reverse_dictionary[valid_examples[i]]
                top_k = 8
                sim = self._get_sim(valid_examples[i])
                nearest = (-sim).argsort()[1 : top_k + 1]
                log_str = "Nearest to %s:" % valid_word
                for k in range(top_k):
                    close_word = self.reverse_dictionary[nearest[k]]
                    log_str = "%s %s," % (log_str, close_word)
                print(log_str)

    def _get_sim(self, valid_word_idx):
        vocab_size = len(self.reverse_dictionary)
        sim = np.zeros((vocab_size,))

        valid_word_tensor = torch.tensor([valid_word_idx], device=self.device)
        valid_embed = self.model.in_embeddings(valid_word_tensor)

        for i in range(vocab_size):
            word_tensor = torch.tensor([i], device=self.device)
            word_embed = self.model.in_embeddings(word_tensor)

            # Compute cosine similarity
            cosine_sim = F.cosine_similarity(valid_embed, word_embed, dim=1)
            sim[i] = cosine_sim.cpu().numpy()[0]

        return sim


def read_glove_vecs(glove_file):
    with open(glove_file, "r", encoding="utf-8") as f:
        words = set()
        word_to_vec_map = {}

        for line in f:
            line = line.strip().split()
            curr_word = line[0]
            words.add(curr_word)
            word_to_vec_map[curr_word] = np.array(line[1:], dtype=np.float64)

    return words, word_to_vec_map


def relu(x):
    return torch.relu(x)


def initialize_parameters(vocab_size, n_h):
    torch.manual_seed(3)
    parameters = {}

    parameters["W1"] = torch.randn(n_h, vocab_size) / np.sqrt(vocab_size)
    parameters["b1"] = torch.zeros(n_h, 1)
    parameters["W2"] = torch.randn(vocab_size, n_h) / np.sqrt(n_h)
    parameters["b2"] = torch.zeros(vocab_size, 1)

    return parameters


def softmax(x):
    return F.softmax(x, dim=-1)


class SkipGramDataset(Dataset):
    def __init__(self, data, window_size=2):
        self.data = data
        self.window_size = window_size
        self.pairs = self._generate_pairs()

    def _generate_pairs(self):
        pairs = []
        for i, center_word in enumerate(self.data):
            for j in range(
                max(0, i - self.window_size),
                min(len(self.data), i + self.window_size + 1),
            ):
                if i != j:
                    pairs.append((center_word, self.data[j]))
        return pairs

    def __len__(self):
        return len(self.pairs)

    def __getitem__(self, idx):
        center_word, context_word = self.pairs[idx]
        return torch.tensor(center_word), torch.tensor(context_word)


def train_word2vec(
    data, vocab_size, embedding_dim=300, epochs=1000, learning_rate=0.01
):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Create dataset and dataloader
    dataset = SkipGramDataset(data, window_size=window_size)
    dataloader = DataLoader(dataset, batch_size=128, shuffle=True)

    # Initialize model
    model = Word2VecModel(vocab_size, embedding_dim).to(device)
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    # Training loop
    model.train()
    for epoch in range(epochs):
        total_loss = 0
        for center_words, context_words in dataloader:
            center_words = center_words.to(device)
            context_words = context_words.to(device)

            optimizer.zero_grad()

            # Forward pass
            positive_score = model(center_words, context_words)

            # Negative sampling (simplified)
            negative_words = torch.randint(
                0, vocab_size, (center_words.size(0),), device=device
            )
            negative_score = model(center_words, negative_words)

            # Loss computation (simplified skip-gram loss)
            positive_loss = -F.logsigmoid(positive_score).mean()
            negative_loss = -F.logsigmoid(-negative_score).mean()
            loss = positive_loss + negative_loss

            # Backward pass
            loss.backward()
            optimizer.step()

            total_loss += loss.item()

        if epoch % 100 == 0:
            print(f"Epoch {epoch}, Loss: {total_loss / len(dataloader):.4f}")

    return model

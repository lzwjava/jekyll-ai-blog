from typing import Dict, List

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

torch.manual_seed(1)

lstm = nn.LSTM(3, 3)
print(lstm)

inputs = [torch.randn(1, 3) for _ in range(5)]
print(inputs)

print(torch.randn(1, 3))

hidden = (torch.randn(1, 1, 3), torch.randn(1, 1, 3))

print(f"{inputs[0]}")
print(f"{inputs[0].view(1, 1, -1)=}")

for i in inputs:
    print(f"{i.size()}")
    print(f"{i.view(1, 1, -1)=}")
    out, hidden = lstm(i.view(1, 1, -1), hidden)


def prepare_sequence(seq: List[str], to_ix: Dict[str, int]) -> torch.Tensor:
    idxs = [to_ix[w] for w in seq]
    return torch.tensor(idxs, dtype=torch.long)


training_data = [
    ("The dog ate the apple".split(), ["DET", "NN", "V", "DET", "NN"]),
    ("Everyday read that book".split(), ["NN", "V", "DET", "NN"]),
]

print(training_data)

word_to_idx = {}

for sent, tags in training_data:
    for word in sent:
        if word not in word_to_idx:
            word_to_idx[word] = len(word_to_idx)

print(word_to_idx)

tag_to_idx = {"DET": 0, "NN": 1, "V": 2}

EMBEDDING_DIM = 6
HIDDEN_DIM = 6


class LSTMTagger(nn.Module):
    def __init__(self, embedding_dim, hidden_dim, vocab_size, tagset_size):
        super().__init__()
        self.word_embeddings = nn.Embedding(vocab_size, embedding_dim)
        self.lstm = nn.LSTM(embedding_dim, hidden_dim)
        self.hidden2tag = nn.Linear(hidden_dim, tagset_size)

    def forward(self, sentence: torch.Tensor):
        # print(f'{sentence.size()=}')
        # print(f'{sentence=}')
        embeds = self.word_embeddings(sentence)
        batch = len(sentence)
        lstm_out, _ = self.lstm(embeds.view(batch, 1, -1))
        out = self.hidden2tag(lstm_out.view(batch, -1))
        tag_scores = F.log_softmax(out, dim=1)
        return tag_scores


model = LSTMTagger(EMBEDDING_DIM, HIDDEN_DIM, len(word_to_idx), len(tag_to_idx))
loss_fn = nn.NLLLoss()
optimizer = optim.SGD(model.parameters(), lr=0.1)


def evaluate():
    with torch.no_grad():
        # print(f'{training_data[0][0]=}')
        idxs = prepare_sequence(training_data[0][0], word_to_idx)
        res = model(idxs)
        print(f"{res=}")


evaluate()


def train():
    for epoch in range(300):
        for sentence, tags in training_data:
            # print(f'{sentence=}')
            # print(f'{tags=}')
            model.zero_grad()

            sentence_in = prepare_sequence(sentence, word_to_idx)
            targets = prepare_sequence(tags, tag_to_idx)

            tag_scores = model(sentence_in)
            loss = loss_fn(tag_scores, targets)
            loss.backward()
            optimizer.step()


train()

evaluate()

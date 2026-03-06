import torch
import torch.nn as nn
from torch.nn import functional as F

from config import ModelConfig


class CausalBow(nn.Module):
    def __init__(self, config: ModelConfig) -> None:
        super().__init__()

        self.block_size = config.block_size
        self.register_buffer(
            "bias",
            torch.tril(torch.ones(config.block_size, config.block_size)).view(
                1, config.block_size, config.block_size
            ),
        )

        # torch.tril(torch.ones(3, 3)).view(1, 3, 3)

    def forward(self, x):
        B, T, C = x.size()

        att = torch.zeros((B, T, T), device=x.device)
        att = att.masked_fill(self.bias[:, :T, :T] == 0, float("-inf"))
        att = F.softmax(att, dim=-1)
        y = att @ x

        return y


class BoWBlock(nn.Module):
    def __init__(self, config) -> None:
        super().__init__()

        self.cbow = CausalBow(config)

        self.mlp = nn.ModuleDict(
            dict(
                c_fc=nn.Linear(config.n_embd, config.n_embd2),
                c_proj=nn.Linear(config.n_embd2, config.n_embd),
            )
        )

        m = self.mlp

        self.mlpf = lambda x: m.c_proj(F.tanh(m.c_fc(x)))

    def forward(self, x):
        x = x + self.cbow(x)
        x = x + self.mlpf(x)
        return x


class Bow(nn.Module):
    def __init__(self, config: ModelConfig) -> None:
        super().__init__()

        self.block_size = config.block_size
        self.vocab_size = config.vocab_size

        self.wte = nn.Embedding(config.vocab_size, config.n_embd)
        self.wpe = nn.Embedding(config.block_size, config.n_embd)

        self.context_block = BoWBlock(config)

        self.lm_head = nn.Linear(config.n_embd, self.vocab_size)

    def get_block_size(self):
        return self.block_size

    def forward(self, idx, targets=None):
        device = idx.device

        b, t = idx.size()

        # print(f"{idx.size()=}")

        pos = torch.arange(0, t, dtype=torch.long, device=device).unsqueeze(0)

        tok_emb = self.wte(idx)
        pos_emb = self.wpe(pos)

        x = tok_emb + pos_emb

        x = self.context_block(x)

        logits = self.lm_head(x)

        loss = None

        if targets is not None:
            loss = F.cross_entropy(
                logits.view(-1, logits.size(-1)), targets.view(-1), ignore_index=-1
            )

        return logits, loss

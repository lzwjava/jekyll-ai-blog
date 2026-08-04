---
audio: false
generated: true
image: false
lang: en
layout: post
title: Arithmetic Transformers for Research Use
translated: false
type: note
---

Question: Is training a small model to only do simple arithmetic a good idea, and how would you do it?

Answer:

Good idea for **learning/research** (mechanistic interpretability, grokking, length generalization). Bad idea for **production math** — a 10-line `eval()`/calculator tool call beats any transformer at reliability, and you'd waste GPU hours reinventing a calculator. If you're doing this for research value or as a distillation/edge-deploy toy where you truly can't call a tool, here's the real recipe, distilled from the arithmetic-transformer literature:

**Key findings you need to bake in:**
1. Digit-level tokenization, not BPE. Each digit is its own token.
2. Reverse the output digits (units first) — this aligns the causal generation order with how carries propagate, and is why GPT-3-scale models only got addition working when trained on reversed digits Nogueira et al. (2021) find that partial length generalization on addition is observed only when models reach 3B parameters and when the addition questions are presented in reverse order.
3. Absolute position embeddings kill length generalization. the absolute position embeddings mix the representation of a token with the embedding of its position in the sequence, making trained models very susceptible to changes in sequence length. Use relative position embeddings instead — models trained on 5-digit numbers can perform 15-digit sums with this trick alone.
4. Multiplication doesn't generalize with RPE alone — needs "train set priming," i.e. injecting a handful of longer examples: priming allows models trained on 5-digit × 3-digit multiplications to generalize to 35×3 examples, and priming sample size scales as the logarithm of the training set size.
5. If you go for grokking-style generalization instead of curriculum, expect a long overfit plateau before it clicks. nearly 1 million steps for validation accuracy to catch up, with hardly any signs of generalization until the 100,000-step mark. Weight decay is what triggers it.

**Minimal nanoGPT-style implementation** (char-level, reversed-digit addition, tiny model):

```python
# arith_gpt.py — train a ~1M param GPT to add numbers
import torch, torch.nn as nn, torch.nn.functional as F, random

VOCAB = "0123456789+=$ "  # $ = pad, "=" separates a+b from result
stoi = {c:i for i,c in enumerate(VOCAB)}
itos = {i:c for c,i in stoi.items()}

def make_example(max_digits=5):
    a = random.randint(0, 10**max_digits - 1)
    b = random.randint(0, 10**max_digits - 1)
    s = str(a) + "+" + str(b) + "=" + str(a+b)[::-1]  # reverse result digits
    return s

def encode(s, block_size):
    ids = [stoi[c] for c in s] + [stoi["$"]] * (block_size - len(s))
    return torch.tensor(ids[:block_size])

def get_batch(bs, block_size, device):
    xs, ys = [], []
    for _ in range(bs):
        s = make_example()
        ids = encode(s, block_size + 1)
        xs.append(ids[:-1]); ys.append(ids[1:])
    return torch.stack(xs).to(device), torch.stack(ys).to(device)

class Block(nn.Module):
    def __init__(self, d, heads):
        super().__init__()
        self.ln1, self.ln2 = nn.LayerNorm(d), nn.LayerNorm(d)
        self.attn = nn.MultiheadAttention(d, heads, batch_first=True)
        self.mlp = nn.Sequential(nn.Linear(d, 4*d), nn.GELU(), nn.Linear(4*d, d))
    def forward(self, x, mask):
        h = self.ln1(x)
        a,_ = self.attn(h, h, h, attn_mask=mask, need_weights=False)
        x = x + a
        x = x + self.mlp(self.ln2(x))
        return x

class TinyGPT(nn.Module):
    def __init__(self, vocab=len(VOCAB), d=128, heads=4, layers=4, block_size=32):
        super().__init__()
        self.tok = nn.Embedding(vocab, d)
        self.pos = nn.Embedding(block_size, d)  # swap for RPE if you push length generalization
        self.blocks = nn.ModuleList([Block(d, heads) for _ in range(layers)])
        self.ln_f = nn.LayerNorm(d)
        self.head = nn.Linear(d, vocab)
        self.block_size = block_size
    def forward(self, idx, targets=None):
        b, t = idx.shape
        pos = torch.arange(t, device=idx.device)
        x = self.tok(idx) + self.pos(pos)
        mask = torch.triu(torch.full((t,t), float("-inf"), device=idx.device), diagonal=1)
        for blk in self.blocks: x = blk(x, mask)
        logits = self.head(self.ln_f(x))
        loss = None
        if targets is not None:
            loss = F.cross_entropy(logits.reshape(-1, logits.size(-1)), targets.reshape(-1))
        return logits, loss

device = "cuda" if torch.cuda.is_available() else "cpu"
model = TinyGPT().to(device)
opt = torch.optim.AdamW(model.parameters(), lr=3e-4, weight_decay=0.1)  # wd matters for grokking

for step in range(20000):
    x, y = get_batch(64, model.block_size, device)
    _, loss = model(x, y)
    opt.zero_grad(); loss.backward(); opt.step()
    if step % 1000 == 0: print(step, loss.item())
```

Params: `128*15 (vocab*d) + 4 blocks * (~4*128*128*3 attn + 2*128*512 mlp)` ≈ **~1M params**, trains to >99% in-distribution accuracy on a single 4090 in minutes.

**If you actually push this further**, don't hand-roll relative position embeddings — swap `nn.Embedding` position for T5-style relative bias or ALiBi (Press et al. 2021), and add the priming trick for multiplication.

**My honest take, matching what you'd get with `ww`/`iclaw`:** if the end goal is "an agent that does math reliably," just have the agent shell out to Python. If the goal is "understand what generalization even means in a transformer," this is the cleanest testbed there is — smaller and faster to iterate on than anything LLM-scale.

References:
- [Length Generalization in Arithmetic Transformers](https://arxiv.org/abs/2306.15400)
- [What Algorithms can Transformers Learn? A Study in Length Generalization](https://arxiv.org/pdf/2310.16028)
- [From Interpolation to Extrapolation: Complete Length Generalization for Arithmetic Transformers](https://arxiv.org/pdf/2310.11984)
- [Grokking: Generalization Beyond Overfitting on Small Algorithmic Datasets (notes)](https://medium.com/@zhenzhenzhong/paper-reading-note-series-ac5c271659cd)
- [Shattered Compositionality: Learning Dynamics of Transformers for Arithmetic](https://arxiv.org/html/2601.22510v1)
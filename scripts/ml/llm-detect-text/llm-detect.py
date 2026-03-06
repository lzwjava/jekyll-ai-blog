import inspect
import math
import time

import numpy as np
import pandas as pd
import torch
from contextlib import nullcontext
from torch.nn import functional as F

from torch import nn

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 1000)

dir_name = "./"
# dir_name = '/kaggle/input/llm-detect-ai-generated-text/'

train_essays = pd.read_csv(dir_name + "train_essays.csv")
test_essays = pd.read_csv(dir_name + "test_essays.csv")
train_prompts = pd.read_csv(dir_name + "train_prompts.csv")

print(train_essays.head())
print(test_essays.head())
print(train_prompts.head())

text = " ".join(train_essays.loc[train_essays["generated"] == 0, "text"])

instructions_concatenated = train_prompts["instructions"].str.cat(sep=" ")

text += " " + instructions_concatenated

chars = sorted(list(set(text)))
vocab_size = len(chars)

stoi = {ch: i for i, ch in enumerate(chars)}
itos = {i: ch for i, ch in enumerate(chars)}
encode = lambda s: [stoi[c] for c in s]
decode = lambda l: "".join(itos[i] for i in l)

data = torch.tensor(encode(text), dtype=torch.long)

split_ratio: float = 0.9

batch_size: int = 12

block_size: int = 64

n_layer = 6
n_head = 4
n_embd = 128
dropout = 0.2

bias = True

n = int(split_ratio * len(data))
train_data = data[:n]
val_data = data[n:]

print(len(train_data), len(val_data))

torch.manual_seed(1337)

device = "cuda"
dtype = (
    "bfloat16"
    if torch.cuda.is_available() and torch.cuda.is_bf16_supported()
    else "float16"
)
torch.backends.cuda.matmul.allow_tf32 = True
torch.backends.cudnn.allow_tf32 = True
device_type = "cuda" if "cuda" in device else "cpu"

ptdtype = {
    "float32": torch.float32,
    "bfloat16": torch.bfloat16,
    "float16": torch.float16,
}[dtype]
ctx = (
    nullcontext()
    if device_type == "cpu"
    else torch.amp.autocast(device_type=device_type, dtype=ptdtype)
)


def get_batch(split):
    data = train_data if split == "train" else val_data
    ix = torch.randint(len(data) - block_size, (batch_size,))
    x = torch.stack([data[i : i + block_size] for i in ix])
    y = torch.stack([data[i + 1 : i + block_size + 1] for i in ix])
    if device_type == "cuda":
        x, y = x.to(device, non_blocking=True), y.to(device, non_blocking=True)
    else:
        x, y = x.to(device), y.to(device)
    return x, y


xb, yb = get_batch("train")
print("inputs:")
print(xb.shape)
print(xb)
print("targets:")
print(yb.shape)
print(yb)


class LayerNorm(nn.Module):
    def __init__(self, ndim, bias):
        super().__init__()
        self.weight = nn.Parameter(torch.ones(ndim))
        self.bias = nn.Parameter(torch.zeros(ndim)) if bias else None

    def forward(self, input):
        return F.layer_norm(input, self.weight.shape, self.weight, self.bias, 1e-5)


class CausalSelfAttention(nn.Module):
    def __init__(self):
        super().__init__()
        self.c_attn = nn.Linear(n_embd, 3 * n_embd, bias=bias)
        self.c_proj = nn.Linear(n_embd, n_embd, bias=bias)
        self.attn_dropout = nn.Dropout(dropout)
        self.resid_dropout = nn.Dropout(dropout)
        self.n_head = n_head
        self.n_embd = n_embd
        self.dropout = dropout
        self.register_buffer(
            "bias",
            torch.tril(torch.ones(block_size, block_size)).view(
                1, 1, block_size, block_size
            ),
        )

    def forward(self, x):
        B, T, C = x.size()

        q, k, v = self.c_attn(x).split(self.n_embd, dim=2)
        k = k.view(B, T, self.n_head, C // self.n_head).transpose(1, 2)
        q = q.view(B, T, self.n_head, C // self.n_head).transpose(1, 2)
        v = v.view(B, T, self.n_head, C // self.n_head).transpose(1, 2)

        att = (q @ k.transpose(-2, -1)) * (1.0 / math.sqrt(k.size(-1)))
        att = att.masked_fill(self.bias[:, :, :T, :T] == 0, float("-inf"))
        att = F.softmax(att, dim=-1)
        att = self.attn_dropout(att)
        y = att @ v

        y = y.transpose(1, 2).contiguous().view(B, T, C)

        y = self.resid_dropout(self.c_proj(y))
        return y


class MLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.c_fc = nn.Linear(n_embd, 4 * n_embd, bias=bias)
        self.gelu = nn.GELU()
        self.c_proj = nn.Linear(4 * n_embd, n_embd, bias=bias)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        x = self.c_fc(x)
        x = self.gelu(x)
        x = self.c_proj(x)
        x = self.dropout(x)

        return x


class Block(nn.Module):
    def __init__(
        self,
    ):
        super().__init__()
        self.ln_1 = LayerNorm(n_embd, bias=bias)
        self.attn = CausalSelfAttention()
        self.ln_2 = LayerNorm(n_embd, bias=bias)
        self.mlp = MLP()

    def forward(self, x):
        x = x + self.attn(self.ln_1(x))
        x = x + self.mlp(self.ln_2(x))
        return x


class GPT(nn.Module):
    def __init__(self):
        super().__init__()

        self.transformer = nn.ModuleDict(
            dict(
                wte=nn.Embedding(vocab_size, n_embd),
                wpe=nn.Embedding(block_size, n_embd),
                drop=nn.Dropout(dropout),
                h=nn.ModuleList([Block() for _ in range(n_layer)]),
                ln_f=LayerNorm(n_embd, bias=bias),
            )
        )

        self.lm_head = nn.Linear(n_embd, vocab_size)

        self.transformer.wte.weight = self.lm_head.weight

        for pn, p in self.named_parameters():
            if pn.endswith("c_proj.weight"):
                torch.nn.init.normal_(p, mean=0.0, std=0.02 / math.sqrt(2 * n_layer))

        print("number of parameters: %.2fM" % (self.get_num_params() / 1e6,))

    def get_num_params(self, non_embedding=True):
        n_params = sum(p.numel() for p in self.parameters())
        if non_embedding:
            n_params -= self.transformer.wpe.weight.numel()
        return n_params

    def forward(self, idx, targets=None):
        device = idx.device
        b, t = idx.size()
        assert t <= block_size, (
            f"Cannot forward sequence of length {t}, block size is only {block_size}"
        )

        pos = torch.arange(0, t, dtype=torch.long, device=device)

        tok_emb = self.transformer.wte(idx)
        pos_emb = self.transformer.wpe(pos)

        x = self.transformer.drop(tok_emb + pos_emb)
        for block in self.transformer.h:
            x = block(x)
        x = self.transformer.ln_f(x)

        if targets is not None:
            logits = self.lm_head(x)
            loss = F.cross_entropy(
                logits.view(-1, logits.size(-1)), targets.view(-1), ignore_index=-1
            )
        else:
            logits = self.lm_head(x[:, [-1], :])
            loss = None

        return logits, loss

    def configure_optimizers(self, weight_decay, learning_rate, betas, device_type):
        param_dict = {pn: p for pn, p in self.named_parameters()}

        param_dict = {pn: p for pn, p in param_dict.items() if p.requires_grad}

        decay_params = [p for n, p in param_dict.items() if p.dim() >= 2]
        nodecay_params = [p for n, p in param_dict.items() if p.dim() < 2]
        optim_groups = [
            {"params": decay_params, "weight_decay": weight_decay},
            {"params": nodecay_params, "weight_decay": 0.0},
        ]
        num_decay_params = sum(p.numel() for p in decay_params)
        num_nodecay_params = sum(p.numel() for p in nodecay_params)
        print(
            f"num decayed parameter tensors: {len(decay_params)}, with {num_decay_params:,} parameters"
        )
        print(
            f"num non-decayed parameter tensors: {len(nodecay_params)}, with {num_nodecay_params:,} parameters"
        )

        fused_available = "fused" in inspect.signature(torch.optim.AdamW).parameters
        use_fused = fused_available and device_type == "cuda"
        extra_args = dict(fused=True) if use_fused else dict()
        optimizer = torch.optim.AdamW(
            optim_groups, lr=learning_rate, betas=betas, **extra_args
        )
        print(f"using fused AdamW: {use_fused}")

        return optimizer

    @torch.no_grad()
    def generate(self, idx, max_new_tokens, temperature=1.0, top_k=None):
        for _ in range(max_new_tokens):
            idx_cond = idx if idx.size(1) <= block_size else idx[:, -block_size:]

            logits, _ = self(idx_cond)

            logits = logits[:, -1, :] / temperature

            if top_k is not None:
                v, _ = torch.topk(logits, min(top_k, logits.size(-1)))
                logits[logits < v[:, [-1]]] = -float("Inf")

            probs = F.softmax(logits, dim=-1)

            idx_next = torch.multinomial(probs, num_samples=1)

            idx = torch.cat((idx, idx_next), dim=1)

        return idx

    @torch.no_grad()
    def is_generated(self, prompt, text):
        text_len = len(text)
        prob_sum = 0
        for i in range(text_len):
            part_text = text[:i]
            prompt_with_text = prompt + part_text
            idx = torch.tensor(encode(prompt_with_text), dtype=torch.long).view(1, -1)

            idx = idx.to(device)

            idx_cond = idx if idx.size(1) <= block_size else idx[:, -block_size:]

            logits, _ = self(idx_cond)

            logits = logits[:, -1, :]

            probs = F.softmax(logits, dim=-1)

            tv = encode(text[i])

            prob = probs[0][tv[0]]

            prob_sum += prob

        average = prob_sum / text_len

        return average > 0.5


model = GPT()

batch_sieze = 32
optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3)

print("begin to train...")

t0 = time.time()

iter_num = 0

gradient_accumulation_steps = 5 * 8

scaler = torch.cuda.amp.GradScaler(enabled=(np.dtype == "float16"))

learning_rate = 6e-4

weight_decay = 1e-1

beta1 = 0.9

beta2 = 0.95

model.to(device)

optimizer = model.configure_optimizers(
    weight_decay, learning_rate, (beta1, beta2), device
)

grad_clip = 1.0

max_iters = 1

eval_iters = 2


@torch.no_grad()
def estimate_loss():
    out = {}
    model.eval()
    for split in ["train", "val"]:
        losses = torch.zeros(eval_iters)
        for k in range(eval_iters):
            X, Y = get_batch(split)
            with ctx:
                logits, loss = model(X, Y)
            losses[k] = loss.item()
        out[split] = losses.mean()
    model.train()
    return out


eval_interval = 1

master_process = True

X, Y = get_batch("train")

while True:
    print(f"iter num: {iter_num}")

    lr = learning_rate

    if iter_num % eval_interval == 0 and master_process:
        losses = estimate_loss()
        print(losses)

    for micro_step in range(gradient_accumulation_steps):
        with ctx:
            logits, loss = model(X, Y)
            loss = loss / gradient_accumulation_steps
        X, Y = get_batch("train")
        scaler.scale(loss).backward()

    if grad_clip != 0.0:
        scaler.unscale_(optimizer)
        torch.nn.utils.clip_grad_norm_(model.parameters(), grad_clip)

    scaler.step(optimizer)
    scaler.update()

    optimizer.zero_grad(set_to_none=True)

    iter_num += 1

    if iter_num > max_iters:
        break

print("training finished")

# idx = torch.zeros((1, 1), dtype=torch.long)
# idx = idx.to(device)
#
# print(decode(model.generate(idx=idx, max_new_tokens=100)[0].tolist()))

# print(model.is_generated('abc', 'abc'))

for index, row in train_essays.iterrows():
    t_id = row["id"]

    instructions = ""

    for index2, row2 in train_prompts.iterrows():
        if row2["prompt_id"] == row["prompt_id"]:
            instructions = row2["instructions"]
            break

    model.is_generated(instructions, row["text"])


def submit():
    ids = []
    generated = []

    for index, row in test_essays.iterrows():
        t_id = test_essays["id"]

        instructions = ""

        for index2, row2 in train_prompts.iterrows():
            if row2["prompt_id"] == row["prompt_id"]:
                instructions = row2["instructions"]
                break

        model.is_generated(instructions, test_essays["text"])

        ids.append(t_id)

    output = pd.DataFrame({"id": ids, "generated": generated})
    output.to_csv("submission.csv", index=False)

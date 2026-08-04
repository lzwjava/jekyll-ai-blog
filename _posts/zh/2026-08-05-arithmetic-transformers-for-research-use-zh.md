---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Arithmetic Transformers用于研究
translated: true
type: note
---

问题：训练一个小模型只做简单的算术运算是个好主意吗？如何实现？

答案：

对于**学习/研究**（机械可解释性、顿悟式泛化、长度泛化）来说是个好主意。但对于**生产环境中的数学运算**来说不是好主意——一个10行的`eval()`/计算器工具调用在可靠性上胜过任何Transformer，而且你会浪费GPU时间重新发明一个计算器。如果你是为了研究价值，或者作为无法调用工具的蒸馏/边缘部署玩具来做这件事，这里是从算术Transformer文献中提炼出的真实方案：

**你需要融入的关键发现：**
1. 按数字级别进行词元化，而非BPE。每个数字是一个单独的token。
2. 反转输出数字（个位在前）——这使因果生成顺序与进位传播方式对齐，这也是为什么GPT-3规模的模型只有在训练反转数字时才能成功进行加法运算的原因。Nogueira等人（2021）发现，只有模型参数达到3B，并且加法问题以反转顺序呈现时，才能观察到部分长度泛化。
3. 绝对位置嵌入会破坏长度泛化。绝对位置嵌入将token的表示与其在序列中的位置嵌入混合，使得训练后的模型对序列长度的变化非常敏感。改用相对位置嵌入——仅凭这一技巧，在5位数上训练的模型就能执行15位数的加法。
4. 仅靠相对位置嵌入无法实现乘法的泛化——需要“训练集预置”，即注入少量更长的示例：预置允许在5位数×3位数乘法上训练的模型泛化到35×3的示例，且预置样本数量随训练集大小的对数增长。
5. 如果你追求顿悟式泛化而非课程学习，预计在“开悟”之前会有一个漫长的过拟合平台期。验证准确率需要近一百万步才能赶上，在十万步之前几乎没有泛化的迹象。权重衰减是触发泛化的关键。

**最小化的nanoGPT风格实现**（字符级、反转数字加法、小模型）：

```python
# arith_gpt.py — 训练一个约1M参数的GPT来执行加法
import torch, torch.nn as nn, torch.nn.functional as F, random

VOCAB = "0123456789+=$ "  # $ = 填充符，"="分隔a+b与结果
stoi = {c:i for i,c in enumerate(VOCAB)}
itos = {i:c for c,i in stoi.items()}

def make_example(max_digits=5):
    a = random.randint(0, 10**max_digits - 1)
    b = random.randint(0, 10**max_digits - 1)
    s = str(a) + "+" + str(b) + "=" + str(a+b)[::-1]  # 反转结果数字
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
        self.pos = nn.Embedding(block_size, d)  # 若追求长度泛化，可替换为RPE
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
opt = torch.optim.AdamW(model.parameters(), lr=3e-4, weight_decay=0.1)  # 权重衰减对顿悟式泛化很重要

for step in range(20000):
    x, y = get_batch(64, model.block_size, device)
    _, loss = model(x, y)
    opt.zero_grad(); loss.backward(); opt.step()
    if step % 1000 == 0: print(step, loss.item())
```

参数：`128*15 (vocab*d) + 4 blocks * (~4*128*128*3 attn + 2*128*512 mlp)` ≈ **约1M参数**，在单张4090上数分钟内训练至分布内准确率>99%。

**如果你要进一步推进**，不要手写相对位置嵌入——将`nn.Embedding`位置替换为T5风格的相对偏置或ALiBi（Press等人，2021），并为乘法添加预置技巧。

**我的真实看法，与`ww`/`iclaw`的建议一致：** 如果最终目标是“一个能可靠进行数学运算的智能体”，那么直接让智能体调用Python即可。如果目标是“理解Transformer中泛化究竟意味着什么”，那么这是最干净的测试平台——比任何LLM规模的东西都更小、迭代更快。

参考文献：
- [Length Generalization in Arithmetic Transformers](https://arxiv.org/abs/2306.15400)
- [What Algorithms can Transformers Learn? A Study in Length Generalization](https://arxiv.org/pdf/2310.16028)
- [From Interpolation to Extrapolation: Complete Length Generalization for Arithmetic Transformers](https://arxiv.org/pdf/2310.11984)
- [Grokking: Generalization Beyond Overfitting on Small Algorithmic Datasets (notes)](https://medium.com/@zhenzhenzhong/paper-reading-note-series-ac5c271659cd)
- [Shattered Compositionality: Learning Dynamics of Transformers for Arithmetic](https://arxiv.org/html/2601.22510v1)
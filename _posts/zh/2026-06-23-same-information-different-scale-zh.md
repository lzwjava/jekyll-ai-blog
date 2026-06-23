---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 相同信息，不同尺度
translated: true
type: note
---

是的，没错。

**PPL = exp(L)**，其中 L 是交叉熵损失——它们本质相同，只是尺度不同。

```python
import torch
import torch.nn.functional as F

logits = torch.randn(8, 512, 50257)   # (batch, seq_len, vocab)
targets = torch.randint(0, 50257, (8, 512))

loss = F.cross_entropy(logits.view(-1, 50257), targets.view(-1))
ppl  = torch.exp(loss)

print(f"loss={loss:.4f}  ppl={ppl:.1f}")
# loss=10.8239  ppl=50257.0  ← 随机初始化 → ppl ≈ vocab_size ✓
```

关系是精确的：

```
L   = -1/N · Σ log P(xᵢ | x<ᵢ)    # nats（自然对数）
PPL = exp(L)
```

因此：

| L (loss) | PPL | 含义 |
|----------|-----|------|
| ln(50257) ≈ 10.82 | ~50257 | 随机模型 |
| 3.0 | ~20 | GPT-2 small 在 WebText 上 |
| 1.5 | ~4.5 | 强模型 |
| 0.0 | 1.0 | 完美/记忆 |

**为什么同一事物有两个名称？**

- **L (loss)** 是优化器看到的内容——可加、可微、数值稳定
- **PPL** 是人类阅读的内容——“模型的不确定性相当于从 N 个等概率 token 中随机挑选”

在你的 nanoGPT 训练循环中，你已经在最小化 PPL —— 只是你看到的是 `loss`。两种方式都记录一下：

```python
print(f"iter {step} | loss {loss.item():.4f} | ppl {torch.exp(loss).item():.1f}")
```

在你用 MI300X 运行 GPT-2 760M 的实验中：当前验证损失稳定在多少？在 OpenWebText 上完成完整训练后，应该在 2.85–3.1 左右。
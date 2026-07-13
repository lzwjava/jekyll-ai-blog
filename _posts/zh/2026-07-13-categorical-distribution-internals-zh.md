---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 分类分布内部机制
translated: true
type: note
---

问题：`torch.distributions.Categorical(logits=logits)` 内部做了什么？

回答：它从非归一化的对数概率构建了一个关于 `K` 个类别的分类（离散）分布，并为你提供 `.sample()`、`.log_prob()`、`.entropy()`、`.probs`，无需你手动进行 softmax 加采样计算。

**底层实现：**

```python
import torch

logits = torch.tensor([2.0, 1.0, 0.1])  # 非归一化，任意实数
dist = torch.distributions.Categorical(logits=logits)

# 1. probs 通过 softmax 惰性计算，数值稳定
#    dist.probs = softmax(logits, dim=-1)
print(dist.probs)  # tensor([0.6590, 0.2424, 0.0986])

# 2. 采样使用 Gumbel-max 技巧（并非字面上的 cumsum+search，但等价）
action = dist.sample()  # tensor(0)，索引到 K 个类别之一

# 3. log_prob 就是 log_softmax 在采样类别上的取值
#    避免了先计算 softmax 再取对数（log-sum-exp 稳定性）
logp = dist.log_prob(action)  # = log_softmax(logits)[action]

# 4. entropy = -sum(p * log p)，直接从 log_softmax 计算
ent = dist.entropy()
```

源代码（简化自 `torch/distributions/categorical.py`）：

```python
class Categorical(Distribution):
    def __init__(self, probs=None, logits=None):
        if logits is not None:
            self.logits = logits - logits.logsumexp(dim=-1, keepdim=True)  # 归一化为对数概率
            self._param = self.logits
        # probs 按需推导：self.probs = self.logits.exp()

    def sample(self, sample_shape=torch.Size()):
        probs_2d = self.probs.reshape(-1, self._num_events)
        samples_2d = torch.multinomial(probs_2d, sample_shape.numel(), True).T
        return samples_2d.reshape(...)

    def log_prob(self, value):
        value = value.long().unsqueeze(-1)
        value, log_pmf = torch.broadcast_tensors(value, self.logits)
        value = value[..., :1]
        return log_pmf.gather(-1, value).squeeze(-1)
```

**为什么使用 `logits=` 而不是 `probs=`：**

- 无需手动 softmax → 避免分母过小导致 `nan` 的风险
- `log_prob` 内部使用 `log_softmax`（通过 `logsumexp` 减法），这是标准的稳定技巧：`log_softmax(x) = x - logsumexp(x)` 而非 `log(softmax(x))`
- 这正是你直接将模型原始输出（最后一层，softmax 之前）用于强化学习策略梯度或 LLM 标记采样时所需要的——你跳过了多余的 softmax→log 往返

**典型用例（策略梯度 / RL，结合你的 agent 工作你会熟悉）：**

```python
logits = policy_net(state)          # 原始输出，形状 [batch, num_actions]
dist = torch.distributions.Categorical(logits=logits)
action = dist.sample()              # 采样一个动作
log_prob = dist.log_prob(action)    # 用于 REINFORCE 损失：-log_prob * reward
```

LLM 采样代码在概念底层使用的也是同一对象类型——来自最终线性层的 `logits`，经过温度缩放，然后分类采样用于下一个 token 生成。

参考文献：

- [torch.distributions.Categorical 文档](https://docs.pytorch.org/docs/stable/distributions.html#categorical)
- [categorical.py 源码](https://github.com/pytorch/pytorch/blob/main/torch/distributions/categorical.py)

---
audio: false
generated: true
image: false
lang: zh
layout: post
title: RL策略：智能体决策函数
translated: true
type: note
---

**问题：** 在强化学习中，“策略”（policy）是什么？

**答案：**

策略 **π** 本质上是一个将状态映射到动作的函数：

```
π(a | s) → 在状态 s 下采取动作 a 的概率
```

就是这样。它是智能体的**决策函数**——即被学习的主体。

## 两种类型

**随机策略** —— 输出动作的概率分布：
```python
probs = softmax(neural_net(state))  # [0.1, 0.7, 0.2]
action = sample(probs)              # → 动作 1
```

**确定性策略** —— 直接输出单个动作：
```python
action = neural_net(state)          # → 0.73 (连续控制)
```

## 用 LLM 的视角理解

LLM **就是**策略：

```
π_θ(token | context) = softmax(W · transformer(context))
```

- **state** = 当前的上下文窗口（已有提示 + 已生成的 token）
- **action** = 下一个要生成的 token
- **θ** = 模型权重

当你进行 RLHF/GRPO 时，实际上是在优化 θ，使得策略能生成更高奖励的 token 序列。“策略更新” = 对权重做梯度步长。

## 完整的强化学习循环

```
状态 s
    ↓
策略 π(a|s)       ← 这就是你在学习的东西
    ↓
动作 a
    ↓
环境
    ↓
下一个状态 s', 奖励 r
    ↓
使用 (s, a, r, s') 改进 π
    ↓
重复
```

## 具体的最小示例

```python
import torch
import torch.nn as nn

class Policy(nn.Module):
    def __init__(self, state_dim, action_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(state_dim, 64),
            nn.ReLU(),
            nn.Linear(64, action_dim)
        )
    
    def forward(self, state):
        logits = self.net(state)
        return torch.distributions.Categorical(logits=logits)

policy = Policy(state_dim=4, action_dim=2)  # 例如 CartPole

state = torch.tensor([0.1, -0.2, 0.05, 0.3])
dist = policy(state)
action = dist.sample()           # 随机动作
log_prob = dist.log_prob(action) # 策略梯度所需
```

`log_prob` 是关键量 —— REINFORCE 梯度为：

```
∇θ J = E[ ∇θ log π_θ(a|s) · R ]
```

你通过微调策略，使高奖励的动作更可能被选到。

## 一句话总结

**策略 = 大脑。状态输入，动作输出。强化学习 = 通过试错找到最佳大脑。**
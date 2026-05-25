---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 同策略强化学习详解
translated: true
type: note
---

**问题：**在强化学习中，“on-policy”是什么意思？具体来说，是指立即从当前策略收集数据，而不是从存储的/离线数据中收集吗？

**回答：**

是的，完全正确。以下是精确的定义：

**On-policy** 意味着你训练所用的数据是由*你当前正在更新的同一个策略*生成的。每一个梯度步都会消耗当前 π_θ 生成的新轨迹，然后这些样本在更新后被**丢弃**。

**Off-policy** 意味着你可以使用*任意*策略生成的数据进行训练——包括你自己的旧版本，或一个完全不同的行为策略。这就是经验回放缓冲区（DQN、SAC）所实现的功能。

## 为什么它在机制上很重要

核心的强化学习目标是：

```
J(θ) = E_{τ ~ π_θ} [R(τ)]
```

期望值是在 **π_θ** 下的。当你用样本估计这个梯度时，这些样本必须来自 π_θ 才能使估计无偏。如果你重复使用来自 π_{θ_old} 的旧样本，就引入了分布不匹配——除非你用**重要性采样**进行修正，否则梯度估计是错误的：

```
∇J(θ) ≈ E_{τ ~ π_old} [ (π_θ(a|s) / π_old(a|s)) · ∇log π_θ · R ]
```

PPO 正是这样做的——它在技术上是 **带有小额 off-policy 容忍窗口的 on-policy**，通过截断重要性采样比率来避免偏离太远：

```python
ratio = (new_log_probs - old_log_probs).exp()
clipped = torch.clamp(ratio, 1 - eps, 1 + eps)
loss = -torch.min(ratio * advantage, clipped * advantage).mean()
```

## 在 LLM RLHF 上下文（GRPO/PPO）中

在 GRPO（DeepSeek-R1 所用的方法）中，你：

1. 采样一批提示（prompts）
2. 从 **当前 π_θ** 生成 G 个补全——这就是 on-policy rollout
3. 使用奖励模型给它们打分
4. 计算优势，更新 θ
5. **丢弃这些补全**——下一步需要从更新后的 θ 生成新的补全

这很昂贵，但为了正确性必不可少。这就是为什么 RLHF 训练很慢——你在训练循环内部进行生成（自回归、序列化）。

**REINFORCE / 原始策略梯度** = 严格 on-policy，每批 rollout 做一次更新  
**PPO** = on-policy，带有小额重用窗口（同一批数据上做几个 epoch，并截断）  
**DPO** = 技术上 off-policy（在预先收集的偏好对上训练，没有实时 rollout）  
**GRPO** = 类似 PPO 的 on-policy，但没有单独的评论家网络

所以是的——on-policy 意味着“每次更新前，我必须从当前的自己生成全新数据。”一旦你将数据存入经验回放缓冲区并在之后采样，你就变成了 off-policy。
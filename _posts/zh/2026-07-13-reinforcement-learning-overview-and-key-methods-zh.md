---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 强化学习概述与关键方法
translated: true
type: note
---

问题：什么是强化学习？

回答：

强化学习是通过与环境进行试错交互来学习策略 π(a|s)，从而最大化期望累计奖励——没有标记的 (x,y) 对，只有一个可能稀疏且延迟的奖励信号。

**核心形式化（MDP）：**
- 状态 `s`，动作 `a`，奖励 `r(s,a)`，转移 `P(s'|s,a)`
- 策略 `π(a|s)`——你正在学习的内容
- 回报：`G_t = Σ γ^k r_{t+k}`（折扣后的未来奖励）
- 目标：`max_π E[G_0]`

**价值函数：**
```
V(s)   = E_π[G_t | s_t = s]           # 这个状态有多好
Q(s,a) = E_π[G_t | s_t=s, a_t=a]      # 在这里采取这个动作有多好
```

**Bellman 方程**（一切构建其上的递归恒等式）：
```
Q(s,a) = r(s,a) + γ Σ_s' P(s'|s,a) max_a' Q(s',a')
```

**两大流派：**
1. **基于价值**（Q-learning, DQN）——学习 Q，贪婪地选择动作：`a = argmax_a Q(s,a)`
2. **策略梯度**（REINFORCE, PPO）——直接参数化 π_θ 并沿着梯度攀升：

```
∇_θ J(θ) = E_π[ ∇_θ log π_θ(a|s) · Q(s,a) ]
```

最简 REINFORCE，除 torch 外无需其他库：

```python
import torch, torch.nn as nn

policy = nn.Sequential(nn.Linear(obs_dim, 64), nn.Tanh(), nn.Linear(64, act_dim))
opt = torch.optim.Adam(policy.parameters(), lr=3e-4)

def rollout(env):
    logps, rewards = [], []
    s = env.reset()
    done = False
    while not done:
        logits = policy(torch.tensor(s, dtype=torch.float32))
        dist = torch.distributions.Categorical(logits=logits)
        a = dist.sample()
        logps.append(dist.log_prob(a))
        s, r, done, _ = env.step(a.item())
        rewards.append(r)
    return logps, rewards

def returns(rewards, gamma=0.99):
    G, out = 0, []
    for r in reversed(rewards):
        G = r + gamma * G
        out.insert(0, G)
    return torch.tensor(out)

logps, rewards = rollout(env)
G = returns(rewards)
G = (G - G.mean()) / (G.std() + 1e-8)   # 基线/方差缩减
loss = -torch.stack(logps) @ G
opt.zero_grad(); loss.backward(); opt.step()
```

**PPO**（实际大规模使用的算法，包括 RLHF）通过裁剪策略比率更新来防止破坏性的步长：
```
r_t(θ) = π_θ(a|s) / π_θ_old(a|s)
L = E[ min(r_t · A_t, clip(r_t, 1-ε, 1+ε) · A_t) ]
```
其中 `A_t = Q(s,a) - V(s)` 是优势函数（实践中使用 GAE）。

**为什么训练模型的人需要关心**：RLHF/RLVR 正是这个循环——奖励模型或验证器给出 `r`，策略是你的 LLM，PPO/GRPO 更新权重。GRPO（DeepSeek）完全丢弃了价值网络，并使用从采样完成中得到的组相对优势——更便宜，这也是梁文锋团队在 R1 中使用的方法。

参考文献：
- [Sutton & Barto — Reinforcement Learning: An Introduction](http://incompleteideas.net/book/the-book.html)
- [Schulman et al. — Proximal Policy Optimization](https://arxiv.org/abs/1707.06347)
- [DeepSeekMath — GRPO](https://arxiv.org/abs/2402.03300)
- [Karpathy — Deep RL pong from pixels](http://karpathy.github.io/2016/05/31/rl/)
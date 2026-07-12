---
audio: false
generated: true
image: false
lang: en
layout: post
title: Reinforcement Learning Overview and Key Methods
translated: false
type: note
---

Question: What is reinforcement learning?

Answer:

RL is learning a policy π(a|s) that maximizes expected cumulative reward through trial-and-error interaction with an environment — no labeled (x,y) pairs, just a reward signal that may be sparse and delayed.

**Core formalism (MDP):**
- State `s`, action `a`, reward `r(s,a)`, transition `P(s'|s,a)`
- Policy `π(a|s)` — what you're learning
- Return: `G_t = Σ γ^k r_{t+k}` (discounted future reward)
- Goal: `max_π E[G_0]`

**Value functions:**
```
V(s)   = E_π[G_t | s_t = s]           # how good is this state
Q(s,a) = E_π[G_t | s_t=s, a_t=a]      # how good is this action here
```

**Bellman equation** (the recursive identity everything is built on):
```
Q(s,a) = r(s,a) + γ Σ_s' P(s'|s,a) max_a' Q(s',a')
```

**Two families:**
1. **Value-based** (Q-learning, DQN) — learn Q, act greedily: `a = argmax_a Q(s,a)`
2. **Policy-gradient** (REINFORCE, PPO) — directly parameterize π_θ and climb the gradient:

```
∇_θ J(θ) = E_π[ ∇_θ log π_θ(a|s) · Q(s,a) ]
```

Minimal REINFORCE, no libraries beyond torch:

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
G = (G - G.mean()) / (G.std() + 1e-8)   # baseline/variance reduction
loss = -torch.stack(logps) @ G
opt.zero_grad(); loss.backward(); opt.step()
```

**PPO** (what actually gets used at scale, incl. RLHF) clips the policy-ratio update to avoid destructive step sizes:
```
r_t(θ) = π_θ(a|s) / π_θ_old(a|s)
L = E[ min(r_t · A_t, clip(r_t, 1-ε, 1+ε) · A_t) ]
```
where `A_t = Q(s,a) - V(s)` is the advantage (GAE in practice).

**Why you care as someone training models**: RLHF/RLVR is exactly this loop — reward model or verifier gives `r`, policy is your LLM, PPO/GRPO updates weights. GRPO (DeepSeek) drops the value network entirely and uses group-relative advantage from sampled completions — cheaper, and what Liang Wenfeng's team used for R1.

References:
- [Sutton & Barto — Reinforcement Learning: An Introduction](http://incompleteideas.net/book/the-book.html)
- [Schulman et al. — Proximal Policy Optimization](https://arxiv.org/abs/1707.06347)
- [DeepSeekMath — GRPO](https://arxiv.org/abs/2402.03300)
- [Karpathy — Deep RL pong from pixels](http://karpathy.github.io/2016/05/31/rl/)

---
audio: false
generated: true
image: false
lang: en
layout: post
title: "RL Policy: Agent Decision-Making Function"
translated: false
type: note
---

**Question:** What is a "policy" in reinforcement learning?

**Answer:**

A policy **π** is simply a function that maps states to actions:

```
π(a | s) → probability of taking action a in state s
```

That's it. It's the agent's **decision-making function** — the thing being learned.

## Two flavors

**Stochastic policy** — outputs a probability distribution over actions:
```python
probs = softmax(neural_net(state))  # [0.1, 0.7, 0.2]
action = sample(probs)              # → action 1
```

**Deterministic policy** — outputs a single action directly:
```python
action = neural_net(state)          # → 0.73 (continuous control)
```

## In LLM terms

The LLM **is** the policy:

```
π_θ(token | context) = softmax(W · transformer(context))
```

- **state** = the current context window (prompt + tokens so far)
- **action** = next token to generate
- **θ** = the model weights

When you do RLHF/GRPO, you're literally optimizing θ so the policy generates higher-reward token sequences. The "policy update" = gradient step on the weights.

## The full RL loop

```
state s
    ↓
policy π(a|s)       ← this is what you're learning
    ↓
action a
    ↓
environment
    ↓
next state s', reward r
    ↓
use (s, a, r, s') to improve π
    ↓
repeat
```

## Concrete minimal example

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

policy = Policy(state_dim=4, action_dim=2)  # e.g. CartPole

state = torch.tensor([0.1, -0.2, 0.05, 0.3])
dist = policy(state)
action = dist.sample()           # stochastic action
log_prob = dist.log_prob(action) # needed for policy gradient
```

`log_prob` is the key quantity — the REINFORCE gradient is:

```
∇θ J = E[ ∇θ log π_θ(a|s) · R ]
```

You nudge the policy to make high-reward actions more probable.

## One-line summary

**Policy = the brain. State goes in, action comes out. RL = finding the best brain via trial and error.**
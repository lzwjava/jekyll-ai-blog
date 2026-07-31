---
audio: false
generated: true
image: false
lang: en
layout: post
title: Two Different Things Share the Name
translated: false
type: note
---

Question: What's the current state of policy distillation — classic RL sense and the on-policy LLM sense?

Answer:

Two different things share the name. Worth separating cleanly since you're training models yourself.

**1. Classic Policy Distillation (Rusu et al., DeepMind 2015)**

Train one small network to match the *action distribution* of a big DQN teacher (or multiple game-specific teachers → one generalist). Loss is just KL between teacher's softmax(Q/τ) and student's softmax(Q/τ), not matching Q-values directly — cross-entropy on the policy is empirically better than regression on Q. This is basically Hinton distillation applied to Atari policies. Not what's driving 2026 discourse — that's the LLM variant below.

**2. On-Policy Distillation (OPD) — this is what's actually hot right now**

The core problem with plain SFT distillation: student trains on teacher's tokens, but at inference the student has to condition on *its own* generated prefix. Once it drifts off-distribution (compounding error / exposure bias), the teacher's supervision at those states was never seen during training. Classic DAgger problem.

OPD fix: sample rollouts from the **student**, then score those same tokens under the **teacher**, minimize reverse KL:

$$
D_{KL}(\pi_\theta \| \pi_T) = -\mathbb{E}_{o \sim \pi_\theta}\left[\log \frac{\pi_T(o|q)}{\pi_\theta(o|q)}\right]
$$

this is equivalent to maximizing the expectation of the log-likelihood ratio between teacher and student. Since it's reverse KL (mode-seeking, mass-covering avoided), gradient only needs teacher logprobs on student's own samples — no teacher rollout generation needed, no reward model, no PPO machinery. Minimal viable loop:

```python
# per step, given prompt batch
student_out = student.generate(prompts, sample=True)          # on-policy: student's own tokens
with torch.no_grad():
    teacher_logp = teacher.log_prob(student_out)               # teacher scores student's tokens
student_logp = student.log_prob(student_out)

# reverse KL per-token, teacher's log-ratio IS the implicit reward
per_token_reward = teacher_logp - student_logp
loss = -(per_token_reward.detach() * student_logp).mean()      # REINFORCE-style, or just do dense CE against teacher softmax if you have full logits access
loss.backward()
```

If you have full teacher logits (same tokenizer, white-box), you skip REINFORCE entirely and do dense token-level KL — the GKD (Agarwal et al. 2024) recipe, way lower variance, this is what most 2026 papers build on.

Why it's eating budget from RL: on-policy distillation has rapidly emerged as a core technique for LLM post-training, with Qwen3, MiMo, and GLM-5 all adopting OPD in their post-training pipelines and reporting substantial gains over conventional SFT and outcome-reward RL. Thinking Machines Lab replicated the Qwen3 OPD recipe at a fraction of the RL compute cost — this is the "on-policy distillation" essay/post that's been circulating. And theoretically: OPD has been formalized as a special case of dense KL-constrained RL, where the teacher's per-token log-ratio is an implicit reward, and scaling that reward beyond its standard weight can push the student past the teacher's own performance. That last part is the counterintuitive bit — over-weighting the teacher signal isn't just "clone the teacher," it can produce a student that beats it, because the reward-tilting acts like RL with a free, dense, per-token reward instead of one scalar per episode.

Practical framing for your setup (GPT-2 760M-scale training runs): OPD gives you RL-shaped, dense credit assignment without a reward model or PPO's variance/instability — cheaper to implement, cheaper to run, same conceptual family. DeepSeek-V4 went furthest, replacing its mixed RL stage entirely with multi-teacher OPD for model consolidation. If you're doing student distillation off any of the big open teachers into your own small model, this is strictly better than plain SFT-on-teacher-completions, and it's a small code diff from what you already have (sample from your model, backprop through KL against a frozen teacher forward pass).

References:

- [Rethinking On-Policy Distillation of LLMs: Phenomenology, Mechanism, Recipe](https://arxiv.org/html/2604.13016v1)
- [A Survey of On-Policy Distillation for LLMs](https://arxiv.org/html/2604.00626v3)
- [Scaling Reasoning Efficiently via Relaxed On-Policy Distillation](https://arxiv.org/pdf/2603.11137)
- [Awesome-LLM-On-Policy-Distillation (paper list)](https://github.com/nick7nlp/Awesome-LLM-On-Policy-Distillation)
- [GKD: Generalized Knowledge Distillation (Agarwal et al. 2024)](https://arxiv.org/abs/2306.13649)

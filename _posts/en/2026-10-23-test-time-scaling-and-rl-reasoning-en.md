---
audio: false
generated: true
image: false
lang: en
layout: post
title: test-time scaling and RL reasoning
translated: false
type: note
---

**Question:** Explain the paradigm shift toward test-time compute scaling + RL refinement, and how models like o3, DeepSeek-R1, and Gemini 2.0 Flash Thinking use RL to teach reasoning.

---

**Answer:**

## The Old Paradigm vs. The New Paradigm

### Old Paradigm — "Train Bigger, Infer Fast"
```
Training (expensive) → Fixed model weights → Single-pass answer (cheap)
```
- Scale up parameters, data, and training compute
- At inference: one forward pass → one answer
- RL was used **only for alignment** (RLHF): making the model polite, safe, and helpful

### New Paradigm — "Train to Think, Spend Compute at Inference"
```
Training (RL teaches reasoning) → Model that can THINK → Extended reasoning at inference → Better answer
```
- RL is used to teach the model **how to reason**, not just how to behave
- At inference: the model spends variable compute "thinking" before answering
- More thinking time → better answers on hard problems

---

## 1. What is Test-Time Compute Scaling?

The core insight:

> **You don't always need a bigger model — you need a model that thinks longer.**

Instead of making the model larger (training-time scaling), you allow the model to **generate a long internal reasoning trace** before producing the final answer.

```
[User Question]
      ↓
  [Think... think... think... verify... backtrack... try again...]
      ↓
  [Final Answer]
```

This is powerful because:
- Hard problems (math, code, logic) **need exploration**, not just pattern matching
- Errors can be **caught and corrected mid-thought**
- The model can **generate and verify multiple solution paths**

---

## 2. How RL Teaches Reasoning (The Mechanism)

Traditional RLHF trains on **human preference**:
> "Which answer do humans like better?" → Reward signal → Update model

RL-for-reasoning trains on **outcome correctness with verifiable rewards**:

```
Model generates a chain-of-thought reasoning trace
        ↓
Final answer is checked against ground truth
        ↓
Reward = +1 if correct, -1 if wrong (or partial for partial credit)
        ↓
RL updates the model to produce reasoning traces that lead to correct answers
```

This is called **RLVR (RL with Verifiable Rewards)** — and it works because math/code has **objective, checkable answers**. No human labeler needed.

### Key Components:

| Component | Role |
|-----------|------|
| **Process Reward Model (PRM)** | Scores each *step* in reasoning, not just the final answer |
| **Outcome Reward Model (ORM)** | Scores only the final answer (simpler but noisier) |
| **MCTS / Beam Search at inference** | Explores multiple reasoning paths, picks the best |
| **Self-consistency / Majority voting** | Sample N solutions, pick the most common answer |

---

## 3. How Each Model Implements This

### 🔵 OpenAI o1 / o3
- Trains a model to produce a **hidden chain-of-thought** (not shown to users in o1, partially in o3)
- Uses RL with **search** during training to find reasoning traces that lead to correct answers
- At inference: model "thinks" for variable time (seconds to minutes)
- **o3** scales this dramatically — on ARC-AGI benchmark, more compute time = dramatically better scores
- The reasoning trace is like the model's **scratchpad** — it can write equations, check steps, abandon wrong paths

```
o3 performance on ARC-AGI:
Low compute  → ~75%
High compute → ~87%
         ↑
   Same model, more thinking time
```

### 🟠 DeepSeek-R1
- Uses **GRPO (Group Relative Policy Optimization)** — a variant of PPO that's more efficient
- Key innovation: trained **without a pre-built reward model** — just verifiable math/code answers
- The model **spontaneously developed** behaviors like:
  - Self-reflection ("Wait, let me reconsider...")
  - Backtracking ("That approach is wrong, trying differently...")
  - Verification ("Let me check: 3 × 7 = 21 ✓")
- These "aha moment" behaviors **emerged from RL**, not from supervised training
- Open-source, competitive with o1 at a fraction of the cost

### 🟢 Gemini 2.0 Flash Thinking
- Google's implementation of extended chain-of-thought with RL training
- Shows the reasoning trace to users (transparent thinking)
- Optimized for **speed** (Flash = faster than Pro/Ultra) while still reasoning deeply
- Uses RL to learn when to think more vs. less (adaptive compute)

---

## 4. Why This is a Paradigm Shift

### Before: Scaling Law was about Training
```
More parameters + More data + More training FLOPs = Better model
```
(Chinchilla scaling laws, GPT-3 → GPT-4)

### Now: Scaling has TWO dimensions
```
Axis 1: Training compute (bigger model, more data)
Axis 2: Inference compute (more thinking time per question)
```

This is huge because:
- **Inference compute is flexible** — you can spend more on hard problems, less on easy ones
- **RL unlocks a new capability ceiling** — a smaller model that reasons well can beat a larger model that doesn't
- **It changes the economics**: instead of training a 10× bigger model, you run the same model for 10× longer on hard questions

---

## 5. Visual Summary

```
TRAINING TIME:
┌──────────────────────────────────────────────────┐
│  RL generates thousands of reasoning traces      │
│  Verifiable reward (correct/wrong) guides model  │
│  Model learns: good reasoning → correct answers  │
└──────────────────────────────────────────────────┘
                        ↓
                  Model Weights
                        ↓
INFERENCE TIME:
┌─────────────────────────────────────────────────────────────────┐
│ Question → [Explore path A... dead end]                         │
│           → [Explore path B... looks promising...]              │
│           → [Verify step 3... error found, fix it...]           │
│           → [Path B leads to solution ✓]                        │
│           → Final Answer                                         │
└─────────────────────────────────────────────────────────────────┘
   ^                                                    ^
   More time here                            Better answer here
```

---

## 6. What This Means Going Forward

- **RL is no longer optional** for frontier models — it's how you build reasoning
- **Math and code** were the entry point (verifiable rewards), but the technique is expanding to **science, medicine, law**
- The race is now about: who can train the best *reasoner*, not just the biggest model
- Smaller models with strong RL reasoning (DeepSeek-R1 7B) can compete with much larger non-reasoning models

---

**References:**
- [DeepSeek-R1 Paper: Incentivizing Reasoning via RL](https://arxiv.org/abs/2501.12948)
- [OpenAI o3 and Test-Time Compute Scaling (OpenAI Blog)](https://openai.com/index/openai-o3-mini/)
- [Scaling LLM Test-Time Compute Verbosely (Google DeepMind, 2024)](https://arxiv.org/abs/2408.03314)
- [Let's Verify Step by Step — Process Reward Models (Lightman et al.)](https://arxiv.org/abs/2305.20050)
- [GRPO: Group Relative Policy Optimization (DeepSeek)](https://arxiv.org/abs/2402.03300)

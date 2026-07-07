---
audio: false
generated: true
image: false
lang: en
layout: post
title: SFT Inference Results Analysis
translated: false
type: note
---

Here's the full analysis.

---

## d12 SFT Inference Results — 7 Prompts

### What works

| Prompt | Result | Verdict |
|--------|--------|---------|
| **Capital of France** | "Paris" | Correct — simple factual recall |
| **Palindrome function** | Correct Python code with explanation + examples | Good — SFT code data working |
| **Chat format** | All responses wrapped in `<|assistant_start|>`/`<|assistant_end|>` | SFT successfully taught dialogue structure |

### What fails

| Prompt | Result | Failure mode |
|--------|--------|-------------|
| **2+2** | Talked about Gauss, "pairing effect", never said 4 | Arithmetic — complete hallucination |
| **1,1,2,3,5,8 (Fibonacci)** | Rambled about "stars and bars", Euclid, bar heights | Pattern recognition — didn't identify sequence |
| **Gradient descent** | "descending a surface by moving air" | Factual — completely off |
| **SQL: employees hired 2023** | `WHERE name = 'John Doe'` | Semantic — ignored date filter |
| **Poem about ML** | Repeats "machine learning instrument" 15+ times | Repetition loop |
| **Train average speed** | 120+80=200 miles, 3h → 200/3=66.7, but computed 120/3=60 then 60/120=0.933 | Arithmetic error mid-reasoning |
| **Three types of ML** | Listed Linear Regression, Decision Trees, Random Forest instead of Supervised/Unsupervised/RL | Factual — wrong categories |
| **Neural network definition** | "a type of ML that uses neural networks" | Circular definition |

### Root cause analysis

**The checkpoint at 0.4053 val_bpb is well-trained for its size**, but ~140M parameters is fundamentally too small for reliable knowledge or reasoning — this is a Chinchilla scaling issue. The model has ~589M tokens of SFT data over 12 layers/768-embd, which is a data:param ratio of ~4:1 — below Chinchilla's recommended ~20:1 for optimal compute.

Specific failure patterns:

1. **Arithmetic** — small models can't innately do math. The forward pass treats `2+2` as token prediction in a distribution it hasn't seen enough. A 140M param model has essentially no working memory for multi-step computation.

2. **Repetition loops** — common in autoregressive models at this scale. The softmax head has limited capacity; once it enters a probability sink ("machine learning instrument"), there's no mechanism to break out. A repetition penalty during inference (`--repetition-penalty 1.1`) would help.

3. **Factual recall** — factual knowledge in LLMs scales roughly with parameter count. The model can only store facts that appear very frequently in the training data ("Paris is capital of France"). Everything else is memorization noise.

4. **Code works better** — code has high statistical regularity. `def is_palindrome(s):` → `return s == s[::-1]` is a high-probability continuation. The model learned the pattern without needing to "understand" what a palindrome is.

### If you want to improve inference quality, options:

- **Repetition penalty**: `engine.generate(... repetition_penalty=1.1)` would fix the poem loops
- **Scale up**: d24 or d32 with n_embd=1024+ would give the model capacity for reasoning
- **Tool-use**: at this scale, give the model a calculator tool for arithmetic rather than expecting raw computation
- **CoT fine-tuning**: train on chain-of-thought traces to externalize multi-step reasoning into tokens
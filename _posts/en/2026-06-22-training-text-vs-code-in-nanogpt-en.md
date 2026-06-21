---
audio: false
generated: true
image: false
lang: en
layout: post
title: Training Text vs Code in nanoGPT
translated: false
type: note
---

**Question:** What are the differences between training on text (like FineWeb/OpenWebText) and code (like GitHub Code) in nanoGPT?

**Answer:**

Given your pipeline — GPT-2 124M on 14B tokens of GitHub Code — here's a precise breakdown of what's actually different, from the forward pass all the way to what the model learns.

---

## 1. Tokenization Behavior

**Text:** Natural language has high token diversity, lots of common words map to single tokens, average ~4 chars/token.

**Code:** BPE (tiktoken gpt2) handles code poorly relative to code-specific tokenizers. Identifiers, indentation, and symbols fragment badly:

```python
# "    return loss.item()" tokenizes roughly as:
# ['    ', 'return', ' loss', '.', 'item', '()']
# indentation spaces = multiple tokens wasted on whitespace
```

**Impact on your pipeline:** You're using `uint16` for token IDs (max 65535), which fits GPT-2's 50,257 vocab. Fine. But code has a long tail of rare tokens (hex literals, obscure symbols) → your val loss starts high (~5.87 at iter 14k) vs typical text which starts ~4.5-5.0.

GPT-2 BPE was trained on WebText (internet text), not code. A code-native tokenizer (like StarCoder's) would get ~30% fewer tokens for the same bytes — meaning your 27 GB → ~14B tokens ratio is slightly wasteful. Code-specialized tokenizers pack more semantic content per token.

---

## 2. Loss Landscape & What the Model Actually Learns

### Text training
- Models common word co-occurrences, syntactic patterns, factual associations
- Loss converges to ~3.0-3.5 (bits-per-character ~1.1) for GPT-2 scale
- Attention heads specialize in: subject-verb agreement, coreference, positional syntax

### Code training
- **Structure is stricter** — code has hard syntactic rules (balanced parens, correct indentation, valid identifiers). The model must learn these or it fails catastrophically (syntactically invalid output = useless).
- **Long-range dependencies matter more** — a function defined at line 10 is called at line 200. Text can be locally coherent; code must be globally consistent.
- **Loss floor is higher** — even perfect code prediction is harder because identifier names are essentially arbitrary. `get_user_by_id` vs `fetch_user_from_db` are semantically equivalent but tokenize differently. The model can't "know" which convention a codebase uses without full context.

Expected val loss trajectory for your run:
```
iter 0:      ~10.5  (random)
iter 14k:    5.87   (you're here — learning basic syntax)
iter 50k:    ~4.5   (learning language-level patterns)
iter 150k:   ~3.8   (learning idioms, APIs)
iter 427k:   ~3.2-3.5  (GPT-2 scale ceiling on code)
```

---

## 3. Context Window & Repetition Patterns

**Text (FineWeb/OpenWebText):**
```python
block_size = 1024  # usually enough for a paragraph or two
# documents are often <1024 tokens, packed with EOT separator
```

**Code:**
- Files are often >1024 tokens (a single Python file can be 5k+ tokens)
- Your config uses `block_size = 1024` — meaning most code files get **truncated mid-function**
- This is a known limitation: model never sees complete function bodies for longer files
- The model learns local syntax well but struggles with file-level structure

**Improvement for your next run:**
```python
# train_github_code_124m.py
block_size = 2048  # doubles memory usage, but worth it for code
# Or filter dataset to only files < 1024 tokens
```

---

## 4. Data Heterogeneity

**Text:** Relatively homogeneous — English prose, similar structure across docs.

**Code:** Wildly heterogeneous — your GitHub Code dataset has 30+ programming languages, wildly different styles, docstrings, comments, auto-generated files, build scripts, JSON configs, etc.

```python
# In your tokenization pipeline, you're mixing ALL of this:
# Python, Java, JavaScript, C, Go, Rust, Shell...
# No language filtering happening
```

This means your model is learning a "polyglot code" distribution. It'll be mediocre at all languages vs. excellent at one. If you want strong Python completion, filter:

```python
# tokenize_github_code.py — add language filter
if row['language'] != 'Python':
    continue
```

The `codeparrot/github-code` dataset has a `language` column — use it.

---

## 5. Evaluation Metrics

**Text training:** Val loss is a good proxy. You can also eyeball generated samples — are they grammatical? coherent?

**Code training:** Val loss is a **weak proxy**. Code can be syntactically valid but semantically wrong. Real evaluation:

```python
# After training, test with HumanEval-style prompts:
prompt = "def fibonacci(n):\n    "
# Does the completion produce correct code?
# Val loss 3.3 doesn't tell you this — you need execution-based eval
```

For your 124M run, don't expect HumanEval scores — GPT-2 scale is too small for complex reasoning. But you can test:
- Does it produce syntactically valid Python?
- Does it complete simple patterns (list comprehensions, for loops)?
- Does it generalize across languages?

---

## 6. Practical Difference in Your Config

```python
# train_github_code_124m.py — key differences vs. text config

# Same architecture — nanoGPT doesn't change
n_layer = 12; n_head = 12; n_embd = 768  # GPT-2 124M

# What you might want to tune for code vs text:
learning_rate = 6e-4   # same as GPT-2 — fine
min_lr = 6e-5          # cosine decay floor
warmup_iters = 2000    # standard

# Code benefit: longer warmup sometimes helps
# because loss surface is rougher (heterogeneous data)
warmup_iters = 4000  # try this on next run

# Gradient clipping — same
grad_clip = 1.0

# Weight decay — some evidence code benefits from slightly higher
weight_decay = 0.1  # standard; try 0.15 for code
```

---

## TL;DR

| Dimension | Text (FineWeb) | Code (GitHub) |
|-----------|---------------|---------------|
| Tokenizer fit | Good (BPE on text) | Suboptimal (code-native better) |
| Val loss floor | ~3.0-3.3 | ~3.2-3.5 |
| Key skill learned | Syntax, facts, coherence | Structure, conventions, APIs |
| Long-range deps | Moderate | High (functions, classes) |
| Eval metric | Loss + sample quality | Loss + execution tests |
| Data heterogeneity | Low | High (30+ languages) |
| Block size sensitivity | Low | High (files truncated at 1024) |

Your val loss of 5.87 at 3.3% through training is normal — roughly tracking what CodeParrot/similar runs showed at early iterations. You're on track.

---
audio: false
generated: true
image: false
lang: en
layout: post
title: Why LLMs Fail at Random Hashes
translated: false
type: note
---

**Question:** Why are LLMs not good at working with random strings like Git commit hashes? Specifically, if I give it 10–20 Git commit log entries and ask it to generate `git cherry-pick` commands, then run them, Git reports a fatal error because the commit hashes don't actually exist in the repo.

**Answer:**

This is a very well-known and fundamental limitation of LLMs. There are several layered reasons why this happens.

---

## 1. Root Cause: Tokenization — LLMs Don't See Characters, They See Chunks

The deepest reason is **tokenization**. LLMs can't spell words or do simple string processing tasks like reversing a string, and the root of this is tokenization. Tokens are the fundamental unit of large language models — everything is processed in units of tokens, and tokenization translates strings into sequences of tokens. Many things that look like neural network problems actually trace back to tokenization.

A Git commit hash looks like this: `a3f9c2d1b8e047...`

Tokenization typically splits strings into word-level or subword-level tokens instead of individual characters. This means LLMs lack character-level understanding. So when an LLM "sees" a commit hash, it doesn't process it character-by-character like a human would carefully copy it. Instead, it processes arbitrary **chunks** of the hash as combined tokens, losing the precise positional awareness needed to reproduce it exactly.

Research reveals two key problems: (1) tokenization fails to split strings into individual characters, resulting in a lack of character-level understanding; and (2) token embeddings lack character-level information such as token length, further highlighting LLMs' limited character-level comprehension of strings.

---

## 2. LLMs Are Probabilistic Pattern Generators, Not Copy Machines

Even when you paste the commit hashes directly into the prompt, an LLM does not treat them as sacred literals. It is generating the **most statistically likely next token** at each step.

For any string from the vocabulary, the LLM may halt at any position. Without knowing where it must begin or will halt, there is a non-zero probability of generating anything — which is why LLMs have generated what seems to be random content.

So when the model outputs what looks like `a3f9c2d1b8e047`, it may actually be generating `a3f9c2d1b8e048` or some other close-but-wrong variant, because those character positions are encoded as chunks, not atoms.

---

## 3. Hallucination Is a Mathematical Inevitability for Rare/Unique Values

OpenAI's research shows that hallucinations are not just bad training data or sloppy fine-tuning, but a mathematical consequence of how pretraining with cross-entropy works. Generative models can be reduced to a binary "is this valid" classifier, which means a non-zero error rate is inevitable — especially on rare or singleton facts.

A Git commit hash is the ultimate singleton — it's a 40-character SHA-1 string that appears in no training data, has no semantic meaning, and carries zero statistical signal. The model has never seen *your* repo's hashes before. Companies with private code bases are especially vulnerable because popular LLMs trained on public data have not seen their code. As one researcher puts it: "The chance to get hallucinations is much, much bigger because the models don't know the facts about their code base."

---

## 4. The Model Feels Compelled to Complete the Task

The goal of generative AI tools is to finish the task assigned to them — to provide a complete response to a prompt. Models sometimes make things up to achieve this.

When you ask the LLM to generate `git cherry-pick` commands for 20 commits, it will not say "I can't be sure of these hashes." It will confidently fill in what looks like a valid hash. Training objectives and common leaderboards reward confident guessing over calibrated uncertainty, so models learn to bluff.

---

## 5. Why Cherry-Pick Hashes Fail Specifically

When you run the generated cherry-pick commands:

- The hash the LLM output is **visually close** to your real hash but has 1–4 characters subtly wrong
- Git does an exact SHA-1 lookup — there is zero tolerance for any deviation
- Git reports `fatal: bad object` or `fatal: reference is not a tree`

This is the worst-case scenario for LLMs: a task requiring **exact character-level fidelity** on **unique, unseen, semantically opaque strings**.

---

## How to Fix This in Practice

Instead of asking an LLM to reproduce commit hashes from memory or context, use proper tooling:

**Option 1 — Use Git directly to get the list, then cherry-pick:**
```bash
# Get hashes from git log and build cherry-pick command yourself
git log --oneline origin/feature-branch | head -20 | awk '{print $1}' | xargs git cherry-pick
```

**Option 2 — If using an LLM, give it the hashes and ask it only for the command structure:**
Provide the hashes yourself and ask the LLM only to wrap them in `git cherry-pick` syntax — don't trust it to reproduce exact hashes from prose descriptions.

**Option 3 — Use `git cherry-pick` with a range:**
```bash
git cherry-pick <oldest-hash>^..<newest-hash>
```

**Option 4 — Always verify LLM-generated hashes:**
```bash
git cat-file -t <hash>   # Should return "commit" if real
```

---

## Summary Table

| Property | Natural Language | Git Commit Hash |
|---|---|---|
| Appears in training data | Massively | Never (private repo) |
| Has semantic meaning | Yes | No |
| Tokenizes cleanly | Yes | No — chunked arbitrarily |
| Tolerates small errors | Yes | Zero tolerance |
| LLM reliability | Good | Very poor |

The bottom line: never trust an LLM to reproduce exact opaque identifiers like commit hashes, UUIDs, API keys, or any high-entropy random string. Always feed it the exact values and have it use them as pass-through — not regenerate them.

**References:**

- [StringLLM: Understanding the String Processing Capability of LLMs (ICLR 2025)](https://arxiv.org/html/2410.01208)
- [LLMs Will Always Hallucinate — arxiv](https://arxiv.org/html/2409.05746v1)
- [Why LLMs Hallucinate — Lakera](https://www.lakera.ai/blog/guide-to-hallucinations-in-large-language-models)
- [LLM Tokenization Explained — fast.ai](https://www.fast.ai/posts/2025-10-16-karpathy-tokenizers)
- [Nonsense and Malicious Packages: LLM Hallucinations in Code — ACM](https://cacm.acm.org/news/nonsense-and-malicious-packages-llm-hallucinations-in-code-generation/)

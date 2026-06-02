---
audio: false
generated: true
image: false
lang: en
layout: post
title: LLM Tokens Simply Explained
translated: false
type: note
---

Great question — tokens in LLM APIs can be a bit confusing at first. Let me break it down clearly.

---

## What Tokens Are

* A **token** is the smallest unit of text that the model processes.
* It’s **not exactly a word**. Tokens are usually pieces of words, full words, punctuation marks, or even spaces depending on the language and the tokenizer.
* LLMs (like OpenAI GPT models) split text into tokens using a predefined **tokenizer**.

For example:

* `"cat"` → 1 token
* `"cats"` → might be split as `"cat"` + `"s"` → 2 tokens
* `"You're handsome."` → splits into something like `"You"`, `"'re"`, `" handsome"`, `"."` → **4 tokens**

So tokens are **subword units**, optimized so the model can handle many languages and rare words efficiently.

---

## Why Tokens Matter in APIs

1. **Billing** – Most LLM APIs charge by tokens (input + output).
2. **Limits** – Models have max token limits (e.g., GPT-4 Turbo 128k means up to 128,000 tokens total for input + output).
3. **Efficiency** – You want to minimize tokens when sending prompts to reduce cost and stay under limits.

---

## Handling Tokens in Practice

* **Estimate tokens**: A rough rule is \~4 characters per token in English. So a 1,000-word English essay (≈5,000 characters) is \~1,200–1,300 tokens.
* **Check tokens precisely**: Most SDKs (like `tiktoken` in Python for OpenAI) let you count tokens before sending.
* **Optimize prompts**:

  * Remove unnecessary whitespace/words.
  * Use concise instructions.
  * Summarize context instead of dumping raw text.

---

## Example

```python
import tiktoken

enc = tiktoken.get_encoding("cl100k_base")
text = "You're handsome."
tokens = enc.encode(text)
print(tokens)        # list of token IDs
print(len(tokens))   # number of tokens
```

This would output something like `[9125, 3938, 13]` → 3 tokens (depending on the exact tokenizer version).

---

✅ So: **tokens ≠ words**. They’re the building blocks the LLM sees. `"You're handsome."` is about 3–4 tokens, not 2 words.

---

Do you want me to show you **how to count tokens with your own text (e.g. transcripts, essays, code)** so you can see cost/limits before calling the API?

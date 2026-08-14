---
audio: false
generated: true
image: false
lang: en
layout: post
title: Best English Alternatives to Scientific Spaces
translated: false
type: note
---

Question: **What are good English-language alternatives to 苏剑林’s “科学空间” (`spaces.ac.cn`)?**

Answer: Yes. But there is **no exact 1:1 equivalent**. What makes Scientific Spaces unusually good is the combination of:

* mathematical derivation
* implementation-level understanding
* “why does this work?” rather than just “what is this?”
* Transformer/LLM architecture
* following research evolution over years
* occasionally proposing or analyzing new ideas himself

For your level, I’d rank the English ecosystem like this:

### 1. Sebastian Raschka — probably the closest overall

Sebastian Raschka

[Sebastian Raschka’s blog](https://sebastianraschka.com/?utm_source=chatgpt.com)

This is probably **the closest English equivalent for you**.

He writes from a practitioner/researcher perspective and frequently goes from equations → PyTorch → actual model behavior.

Especially good:

* LLM architecture
* attention
* scaling
* training
* PyTorch implementations
* reading papers by reconstructing them

His current article index explicitly covers **LLM architectures, reasoning models, PyTorch, and from-scratch implementations**. ([Sebastian Raschka, PhD][1])

His LLM reading list also explicitly recommends Jay Alammar and Lilian Weng as complementary technical resources. ([Sebastian Raschka, PhD][2])

---

### 2. Lilian Weng — strongest for mathematical/conceptual depth

Lilian Weng

[Lilian Weng’s blog](https://lilianweng.github.io/?utm_source=chatgpt.com)

This is less "I invented/analyzed this architecture" than 苏剑林, but excellent for **building the conceptual/mathematical map** of modern ML.

Good topics include:

* attention
* diffusion
* RL
* RLHF
* agents
* generative models
* LLM reasoning

I'd use Lilian Weng when you want:

> "Give me the mathematical landscape around this technique."

---

### 3. Jay Alammar — best visual intuition

Jay Alammar

[The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/?utm_source=chatgpt.com)

Very different style from Scientific Spaces, but extremely useful.

His famous **Illustrated Transformer** gives a visual forward-pass understanding of:

```text
tokens
  ↓
embeddings
  ↓
Q K V
  ↓
attention
  ↓
FFN
  ↓
residual
  ↓
next layer
```

For learning an architecture before diving into its equations, this is hard to beat.

---

### 4. Aman Arora — implementation-first deep learning

[Aman Arora’s blog](https://amaarora.github.io/?utm_source=chatgpt.com)

This is closer to:

> "Let's actually implement the paper and understand every tensor."

Good if you want to go from:

```text
paper
  ↓
equations
  ↓
PyTorch
  ↓
tensor shapes
  ↓
experiment
```

rather than just reading conceptual explanations.

---

### 5. Jay Shah / Raschka-style "from scratch" material

Another particularly useful category is **from-scratch LLM implementation blogs**.

For example, Raschka's *Build a Large Language Model (From Scratch)* ecosystem is excellent because it forces you to understand the actual computation rather than treating Transformers as black boxes.

[Build a Large Language Model (From Scratch)](https://sebastianraschka.com/books/ml-python/?utm_source=chatgpt.com)

For someone doing your kind of work, I would value this style more than generic "AI tutorials."

---

### 6. The official research engineers are sometimes better than blogs

For **modern architecture**, I would also read the original authors/repos directly.

For example, Scientific Spaces' Transformer series goes all the way into things like:

```text
MHA
 ↓
MQA / GQA
 ↓
RoPE
 ↓
long-context methods
 ↓
MLA
 ↓
low-rank KV representation
```

苏剑林's MLA analysis is particularly interesting because he doesn't stop at describing MLA; he tries to explain *why* MLA works theoretically. ([Spaces][3])

For English, I would therefore pair blogs with:

```text
DeepSeek papers
Qwen technical reports
Meta Llama papers
Google research
Anthropic research
OpenAI research
```

rather than looking for one blog to replace Scientific Spaces.

---

## My personal ranking for **your** use case

Given that you're currently digging into things like **MLA, QK projections, RoPE, Transformer evolution, and model implementations**, I'd use this stack:

| Resource                    | Best for                            | Scientific Spaces similarity |
| --------------------------- | ----------------------------------- | ---------------------------: |
| **Sebastian Raschka**       | LLM + implementation + architecture |                        ★★★★★ |
| **Lilian Weng**             | Mathematical/conceptual synthesis   |                        ★★★★☆ |
| **Aman Arora**              | Code / implementation               |                        ★★★★☆ |
| **Jay Alammar**             | Visual intuition                    |                        ★★★☆☆ |
| **Original papers + repos** | Frontier architecture               |                        ★★★★★ |
| **Hugging Face blog**       | Practical ecosystem                 |                        ★★★☆☆ |

The important point is that **Scientific Spaces is unusually research-oriented for a personal blog**. For example, 苏剑林's Transformer series doesn't merely explain RoPE; it analyzes why sinusoidal position encoding behaves the way it does and then develops RoFormer/RoPE. ([Spaces][4])

So if you're looking for an English resource with the same spirit, I would start with:

**Raschka → Lilian Weng → original papers → implement yourself.**

And for your particular current topic, I'd actually recommend **Raschka + DeepSeek papers/repos** over trying to find one perfect English equivalent.

References:

* [Scientific Spaces / 苏剑林](https://spaces.ac.cn/?utm_source=chatgpt.com)
* [Sebastian Raschka](https://sebastianraschka.com/?utm_source=chatgpt.com)
* [Lilian Weng](https://lilianweng.github.io/?utm_source=chatgpt.com)
* [Jay Alammar](https://jalammar.github.io/?utm_source=chatgpt.com)
* [Aman Arora](https://amaarora.github.io/?utm_source=chatgpt.com)

[1]: https://sebastianraschka.com/best-articles/?utm_source=chatgpt.com "Best Articles by Topic | Sebastian Raschka, PhD"
[2]: https://sebastianraschka.com/blog/2023/llm-reading-list.html?utm_source=chatgpt.com "Large Language Models Reading List | Sebastian Raschka, PhD"
[3]: https://www.spaces.ac.cn/author/1/8/?utm_source=chatgpt.com "苏剑林 发布的文章 - 科学空间|Scientific Spaces"
[4]: https://www.spaces.ac.cn/author/1/37/?utm_source=chatgpt.com "苏剑林 发布的文章 - 科学空间|Scientific Spaces"

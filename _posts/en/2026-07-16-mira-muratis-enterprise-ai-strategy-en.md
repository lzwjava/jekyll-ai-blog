---
audio: false
generated: true
image: false
lang: en
layout: post
title: Mira Murati’s Enterprise AI Strategy
translated: false
type: note
---

Question: Is Mira Murati’s Thinking Machines bet on open/customizable foundation models + enterprise fine-tuning likely wrong because enterprise data is too small, and the real competition is pushing intelligence/agents like GLM or Anthropic?

Answer:

Your intuition is pointing at a real tension in the AI market, but the conclusion is slightly too strong.

The key distinction:

**"Enterprise fine-tuning" ≠ "training intelligence from enterprise data."**

There are at least four different layers:

```
Internet-scale pretraining
        |
        v
Base model intelligence
        |
        v
Post-training / alignment / reasoning
        |
        v
Enterprise adaptation
        |
        +--> RAG
        +--> tool use
        +--> workflows
        +--> fine-tuning
        +--> agents
```

The mistake is assuming enterprise fine-tuning is trying to create a smarter model.

Usually it is not.

---

## 1. You are right: enterprise data is tiny compared with internet data

For general intelligence:

```
Internet corpus:
    trillions of tokens

Single enterprise:
    millions ~ billions of tokens
```

Even a huge company like Microsoft has:

* internal documents
* emails
* code
* tickets
* meeting transcripts

but compared with:

* Common Crawl
* GitHub
* books
* papers
* Wikipedia
* web forums

it is small.

So:

```
enterprise data -> smarter GPT
```

is probably false.

A bank's documents will not create a better Claude.

---

## 2. But enterprises don't buy "smarter GPT"

They buy:

```
GPT-5 + company knowledge + company actions
```

Example:

A bank does not need:

> "a model that knows banking better"

It needs:

```
Customer request
        |
        v
Agent
        |
        +--> search internal policy
        |
        +--> query transaction system
        |
        +--> call compliance API
        |
        +--> generate response
```

The value is not the weights.

The value is the **integration layer**.

---

## 3. Fine-tuning is becoming less important

I agree with you here.

The 2023 idea:

> "Every company will fine-tune its own Llama"

was probably exaggerated.

Why?

Because models improve quickly.

Example:

Company trains:

```
Llama-3.1 fine-tuned Jan 2025
```

Six months later:

```
Claude/GPT/Qwen new model
```

beats it.

The company now has:

* old model
* expensive maintenance
* unclear benefit

So many enterprises move toward:

```
strong foundation model
+
RAG
+
tools
+
agent framework
```

---

## 4. The real battlefield is agent capability

This is where your point is strongest.

The frontier is:

```
Can the model reliably complete long tasks?
```

Not:

```
Can it memorize more enterprise PDFs?
```

The competition:

### Anthropic

Focus:

```
Claude
+
computer use
+
tool use
+
coding agents
```

### OpenAI

Focus:

```
reasoning models
+
agent infrastructure
+
operator-like systems
```

### GLM / Chinese labs

Focus:

```
open models
+
efficient reasoning
+
agent ecosystems
```

The winner probably needs:

```
better base intelligence
        +
better reasoning
        +
better planning
        +
better tool execution
        +
lower inference cost
```

---

## 5. Then why is Thinking Machines interesting?

The bet is not necessarily:

> "enterprise data makes models smarter"

The bet may be:

> "companies want control over AI systems"

For example:

Open/custom models allow:

```
Company
 |
 +-- choose model
 |
 +-- inspect behavior
 |
 +-- customize safety
 |
 +-- deploy private
 |
 +-- integrate agents
```

This matters for:

* banks
* governments
* healthcare
* defense
* large enterprises

They often cannot send everything to OpenAI/Anthropic.

---

## 6. The future probably looks like Linux + cloud

A possible analogy:

1990s:

```
Every company does not build its own OS.
```

But:

```
Linux kernel
+
company customization
+
enterprise software
```

became huge.

AI may become:

```
foundation model
+
company agent layer
+
private data/tools
```

The model itself becomes commodity.

The agent system becomes differentiation.

---

## My prediction

The market splits:

### Frontier labs win:

```
training intelligence
reasoning
multimodal capability
agent algorithms
```

(OpenAI, Anthropic, Google DeepMind, xAI, DeepSeek, etc.)

### Enterprise AI companies win:

```
deployment
integration
workflow automation
security
evaluation
```

Thinking Machines is betting on the second layer.

The risky part is if they are too focused on:

```
fine-tune your own model
```

The stronger thesis is:

```
customizable agent systems built on frontier/open models
```

because, as you said, the scarce resource is not enterprise text.

The scarce resource is **making models reliably do useful work.**

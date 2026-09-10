---
audio: false
generated: true
image: false
lang: en
layout: post
title: Originality Shifts from Code to Ideas
translated: false
type: note
---

Question: Is this a reasonable take on the current “AI coding” / open-source culture?

Answer: **Yes, I think the core point is right.**

If everyone can ask an LLM to generate a competent implementation, then **“I wrote this code” becomes a much weaker signal of originality**. The code itself is increasingly becoming a commodity.

The scarce part moves upward:

```text
以前:
idea → design → code → product

现在:
idea → experiment → product
              ↑
          AI writes code
```

So this distinction matters:

* **Copy code** → reproduce someone else's implementation.
* **AI-generated code** → reproduce an implementation through natural-language instructions.
* **AI-native engineering** → discover a problem, invent an approach, run experiments, iterate, and use AI as the implementation engine.
* **Original project/research** → create something that didn't exist before and demonstrate that it works.

That's why your line:

> **“需要有新想法、新实践、原创想法、原创项目”**

is probably the more important direction.

And the slightly provocative:

> **“还不如说只开源提示词得了”**

actually points at something real. If the *only* novel thing in a project is “here is the prompt I used to make GPT generate this code,” then publishing thousands of lines of generated code may have very little informational value. The interesting artifact might instead be:

```text
problem
  ↓
hypothesis
  ↓
prompt / agent strategy
  ↓
experiments
  ↓
failures
  ↓
implementation
  ↓
benchmark
  ↓
result
```

**But I wouldn't go as far as saying AI-written code has “no meaning.”** The implementation still matters when it embodies difficult engineering: performance, reliability, systems integration, novel algorithms, production constraints, etc.

The stronger statement is:

> **AI makes code cheaper. Therefore, originality increasingly lies in what you choose to build, how you build it, and what you discover—not merely in the code you type.**

That is a much more interesting “new furnace.”